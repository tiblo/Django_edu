from django.db import models

# Create your models here.
class DataTbl(models.Model):
    str_data = models.CharField(max_length=50)
    int_data = models.IntegerField()
    reg_data = models.DateTimeField(auto_now_add=True)
    upd_data = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'data_tbl'
        verbose_name = '입력데이터'
        verbose_name_plural = '입력데이터들'