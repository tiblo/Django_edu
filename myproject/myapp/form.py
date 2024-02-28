from django.forms import *
from .models import DataTbl
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DataForm(ModelForm):
    class Meta:
        model = DataTbl
        fields = '__all__'
        exclude = ('reg_data','upd_data')
        widgets = {
            'str_data': TextInput(attrs = {
                'placeholder': '문자열',
            }),
            'int_data': NumberInput(attrs = {
                'placeholder': '숫자',
            }),
        }

class UserForm(UserCreationForm):
    # username, password 1, password 2는 기본값으로 처리됨.
    # 추가적으로 email, first_name을 받기 위해, 수동으로 잡아줘야함.
    # username은 id를 의미하며, 사용자 이름은 first_name과 last_name으로 되어 있음.
    username = CharField(label='사용자 ID')
    email = EmailField(label="이메일")
    first_name = CharField(label='사용자 이름')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name')
