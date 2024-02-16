from django.forms import *
from .models import DataTbl

class DataForm(ModelForm):
    class Meta:
        model = DataTbl
        fields = '__all__'
        exclude = ('reg_data', 'upd_data',)
        widgets = {
            'str_data': TextInput(attrs={
                'placeholder': '문자열',
            }),
            'int_data': NumberInput(attrs={
                'placeholder': '숫자',
            }),
        }