import uuid
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from rest_framework.exceptions import ValidationError

from apps.files.storages import PrivateStorage


if settings.USE_AWS_S3:
    TEMP_BUCKET = f'{settings.AWS_STORAGE_BUCKET_NAME}-temp'
    CASE_BUCKET = f'{settings.AWS_STORAGE_BUCKET_NAME}-case'
    TEMP_STORAGE = PrivateStorage(bucket=TEMP_BUCKET)
    CASE_STORAGE = PrivateStorage(bucket=CASE_BUCKET)
else:
    TEMP_STORAGE = FileSystemStorage(location=f'{settings.MEDIA_ROOT}/tempfile', base_url=f'{settings.MEDIA_URL}tempfile/')
    CASE_STORAGE = FileSystemStorage(location=f'{settings.MEDIA_ROOT}/casefile', base_url=f'{settings.MEDIA_URL}casefile/')


class TempFile(models.Model):
    """
    暫存檔案
    * case: 案件編號，因案件未成立，先以字串紀錄
    * file: 案件檔案，storage指定到 TEMP
    * file_name: 案件檔案名稱，不可編輯，save()時自動產生
    * upload_time: 檔案上傳時間
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    case_uuid = models.UUIDField(verbose_name=_('UUID'))
    file = models.FileField(storage=TEMP_STORAGE, verbose_name=_('Temp file'))
    file_name = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name=_('File Name'))
    size = models.PositiveIntegerField(editable=False, verbose_name=_('Size'))
    upload_time = models.DateTimeField(auto_now=True, verbose_name=_('Upload Time'))

    def __str__(self):
        return f'{self.case_uuid} - {self.file_name}'

    @property
    def url(self):
        return self.file.url

    def check_duplicate(self):
        """
        以案件編號及檔案名稱去query檢查資料是否重複
        """
        if TempFile.objects.filter(case_uuid=self.case_uuid, file_name=self.file_name):
            return True
        else:
            return False

    def check_size(self):
        """
        檢查已上傳案件的總大小與目前上傳的檔案相加是否超過限制
        """
        objs = TempFile.objects.filter(case_uuid=self.case_uuid)
        size = [i.size for i in objs]

        if self.size + sum(size) > 41943040:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        """
        TempFile save()時觸發
        給予file_name欄位檔案名稱
        檢查上傳的檔案是否重複
        檢查上傳的檔案大小是否超過上限
        將案件編號及檔案名稱組成路徑+檔案名稱
        最後再執行原本save()的code
        """
        self.file_name = self.file.name
        self.size = self.file.size
        if self.check_duplicate():
            raise ValidationError(_('Duplicate file'))
        if self.check_size():
            raise ValidationError(_('File over limit size'))
        self.file.name = f'{self.case_uuid}/{self.file_name}'
        super(TempFile, self).save(*args, **kwargs)


class CaseFile(models.Model):
    """
    案件檔案
    * case: 案件編號，案件成立時會根據TempFile紀錄的案件編號，關聯到正確的案件
    * file: 案件檔案，storage指定到 CASE
    * file_name: 案件檔案名稱，不可編輯，save()時自動產生
    * upload_time: 檔案上傳時間
    """
    case = models.ForeignKey('cases.Case', on_delete=models.CASCADE, related_name='casefiles', verbose_name=_('Case File'))
    file = models.FileField(storage=CASE_STORAGE, verbose_name=_('Case File'))
    file_name = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name=_('File Name'))
    upload_time = models.DateTimeField(auto_now=True, verbose_name=_('Upload Time'))

    def __str__(self):
        return f'{self.case} - {self.file_name}'

    @property
    def url(self):
        return self.file.url

    def save(self, *args, **kwargs):
        """
        CaseFile save()時觸發
        給予file_name欄位檔案名稱
        """
        start = self.file.name.find(f'{self.case.uuid}')
        if start > -1:
            self.file.name = self.file.name[start:]
        self.file_name = self.file.name.replace(f'{self.case.uuid}/', '')
        self.file.name = f'{self.case.uuid}/{self.file_name}'
        super(CaseFile, self).save(*args, **kwargs)


@receiver(pre_delete, sender=TempFile)
def temp_file_delete_handler(sender, instance, **kwargs):
    """
    TempFile delete()時觸發
    將storage的檔案刪除
    """
    instance.file.storage.delete(name=instance.file.name)


@receiver(pre_delete, sender=CaseFile)
def case_file_delete_handler(sender, instance, **kwargs):
    """
    CaseFile delete()時觸發
    將storage的檔案刪除
    """
    instance.file.storage.delete(name=instance.file.name)
