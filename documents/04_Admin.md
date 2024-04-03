# Admin 페이지
Django Admin은 모델의 CRUD 작업을 위한 사용자 인터페이스이다.

admin 페이지의 url
```
http://127.0.0.1:8000/admin
```
![image](https://github.com/tiblo/Django_edu/assets/34559256/b98361bb-fce5-4643-bebd-c4d7775aae0a)

(하위)myproject 폴더의 urls.py에 admin 페이지에 대한 경로가 등록되어 있음.
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('members.urls')),
    path('admin/', admin.site.urls), # admin 페이지의 url
]
```
admin 페이지로 들어가려면 사용자를 생성해야 하며, 생성한 사용자로 로그인이 필요하다.

## 사용자 생성
먼저 가동중인 서버를 중지한 다음 작업한다.

> 사용자 생성 명령
```
py manage.py createsuperuser
```

사용자 생성에 필요한 정보
* Username - 사용자 계정 이름
* Email address - 이메일 주소(가짜 이메일 주소 사용 가능)
* Password
```
> py manage.py createsuperuser
사용자 이름 (leave blank to use 'user'): admin
이메일 주소: admin@example.com
Password:
Password (again):
비밀번호가 너무 일상적인 단어입니다.
비밀번호가 전부 숫자로 되어 있습니다.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

## Model 보이기
처음 로그인한 화면은 다음과 같다.

![image](https://github.com/tiblo/Django/assets/34559256/b162c7b7-316d-4d10-a002-65087d54eac1)

myapp/admin.py에 관리해야할 Model을 포함시켜야 한다.
```python
from django.contrib import admin
from .models import DataTbl

# Register your models here.
admin.site.register(DataTbl)
```

models.py에서 작성한 클래스를 등록하는 메소드 register()
```python
# 개별적인 클래스를 가져올 때
from .models import 클래스이름
# 모든 클래스를 가져올 때
from .models import *

admin.site.register(클래스이름)
```

![image](https://github.com/tiblo/Django/assets/34559256/210e8d44-92af-4f5d-98b1-b633a8cc092a)

이 화면에서 해당 테이블에 데이터를 추가하거나 수정/삭제할 수 있다.

## 정보 입력
![image](https://github.com/tiblo/Django/assets/34559256/315c9616-a3c8-41c9-907e-18079b8a0812)

화면에서 정보를 입력하고 '저장'하면 다음과 같이 테이블이 저장되고 확인할 수 있다.

![image](https://github.com/tiblo/Django/assets/34559256/d9324586-22fe-44de-a4cd-d4fb2935c470)


## Admin 페이지 수정
### Admin 페이지 제목 수정
하위 myproject 폴더의 urls.py에서 admin 페이지의 제목을 수정할 수 있다.
```python
admin.site.site_header = 'My Project Admin'
```
![image](https://github.com/tiblo/Django/assets/34559256/5b88c957-4b4e-46cb-84bb-bcf6620f40fd)

페이지 제목이 'Django 관리'에서 'My Project Admin'으로 변경된다.


### 브라우저 탭에 출력되는 title 수정
마찬가지 urls.py에서 수정한다.
```python
admin.site.site_title = 'My Admin'
```
![image](https://github.com/tiblo/Django/assets/34559256/72178bec-b911-4169-8bb5-28ae618c34fc)

탭의 제목이 '사이트 관리 | Django 사이트 관리'에서 '사이트 관리 | My Admin'으로 변경된다.


### 목록 제목 수정
마찬가지 urls.py에서 수정한다.
```python
admin.site.index_title = 'Project Apps'
```
![image](https://github.com/tiblo/Django/assets/34559256/a95a68cd-f606-4883-a044-fe049b927272)

목록 제목이 '사이트 관리'에서 'Project Apps'로 변경된다.(탭 제목도 함께 변경된다.)

### 테이블 목록 출력 항목 설정
admin.py에서 해당 모델에 대한 클래스를 작성
```python
# Register your models here.
class DataTblAdmin(admin.ModelAdmin):
    list_display = ('id', 'str_data', 'int_data', 'reg_data')

admin.site.register(DataTbl, DataTblAdmin)
```
![image](https://github.com/tiblo/Django/assets/34559256/a0fbb256-194e-41a4-b0da-9e9be05a2d4e)

> 입력 양식 등 다양한 admin 사이트의 수정이 가능함

데코레이터를 사용한 등록 형식
```python
@admin.register(DataTbl)
class DataTblAdmin(admin.ModelAdmin):
    list_display = ('id', 'str_data', 'int_data', 'reg_data')
```

## 최종 코드
> myproject의 urls.py
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('myapp.urls')),
    path('admin/', admin.site.urls),
]

admin.site.site_header = 'My Project Admin'
admin.site.site_title = 'My Admin'
admin.site.index_title = 'Project Apps'
```
