from django.contrib import admin
from .models import DataTbl

# Register your models here.
@admin.register(DataTbl) # 데코레이터 사용한 등록 형식
class DataTblAdmin(admin.ModelAdmin):
    list_display = ('id', 'str_data', 'int_data', 
                    'reg_data')
# 일반 등록 형식
# admin.site.register(DataTbl, DataTblAdmin)