# Django Authentication
Django Framework에서 제공하는 Authentication을 활용하여 간단히 회원가입, 로그인/로그아웃을 처리할 수 있다.
> 프로젝트 이름 - myproject<br>
앱 이름 - myapp<br>

## 회원 가입 - UserCreationForm
Django에서 제공하는 폼 클래스 중 하나로, 사용자를 생성하기 위한 폼으로 주로 회원가입과 같은 곳에서 사용된다. 

이 폼을 사용하면 사용자 이름과 비밀번호를 입력하고, 해당 정보를 사용하여 새로운 사용자를 생성할 수 있다.

일반적으로 UserCreationForm은 Django의 내장 인증 시스템과 함께 사용된다. Django의 내장 인증 시스템은 사용자 인증을 처리하는 데 사용되며, 사용자의 로그인, 로그아웃, 회원가입 등을 처리할 때 편리하게 사용할 수 있다.

UserCreationForm은 Django의 django.contrib.auth.forms 모듈에 포함되어 있다.

UserCreationForm은 기본적으로 'auth_user'라는 테이블과 연동하여 사용자를 저장하는데, 이 테이블은 django framework에서 제공하는 테이블이다.

superuser(root 또는 admin) 계정도 이 테이블에 저장되며, admin 페이지에서 관리할 수 있다.

원하는 형태로 회원 가입 페이지를 작성할 경우 다음과 같이 작업한다.

### Form 작성
form.py에 먼저 UserCreationForm과 auth model의 User를 import한다.
```python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
```

그리고 UserCreationForm을 상속받은 form 클래스를 작성한다.
```python
...
class UserForm(UserCreationForm):
    username = CharField(label='사용자 ID')
    email = EmailField(label="이메일")
    first_name = CharField(label='사용자 이름')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name')
```
 * username, password 1, password 2는 기본값으로 처리된다.
 * 추가적으로 email, first_name을 받기 위한 문장을 작성한다.
   * username은 id를 의미하며, 사용자 이름은 first_name과 last_name으로 되어 있다.
   * 이를 위해 username의 label을 지정해 준다.
  
### Template 작성
templates 폴더에 'join.html'을 생성하고 다음과 같이 작성한다.
```html
{% extends "master.html" %}
{% load static %}
{% block section %}
<h2>회원가입</h2>
<div>
    <form method="post" action="{% url 'join' %}">
        {% csrf_token %}
        {% include "form_errors.html" %}
        <div class="j-form">
            <div>
                <label for="username">사용자 ID</label>
                <input type="text" name="username" id="username"
                       value="{{ form.username.value|default_if_none:'' }}">
            </div>
            <div>
                <label for="password1">비밀번호</label>
                <input type="password" name="password1" id="password1"
                       value="{{ form.password1.value|default_if_none:'' }}">
            </div>
            <div>
                <label for="password2">비밀번호 확인</label>
                <input type="password" name="password2" id="password2"
                       value="{{ form.password2.value|default_if_none:'' }}">
            </div>
            <div>
                <label for="email">이메일</label>
                <input type="text" name="email" id="email"
                       value="{{ form.email.value|default_if_none:'' }}">
            </div>
            <div>
                <label for="first_name">사용자 이름</label>
                <input type="text" name="first_name" id="first_name"
                       value="{{ form.first_name.value|default_if_none:'' }}">
            </div>
            <input type="submit" value="JOIN">
        </div>
    </form>
</div>
{% endblock %}
```
각 입력 필드의 name 속성값은 'auth_user' 테이블의 컬럼과 동일한 이름(model의 필드명)으로 작성한다.

'form_error.html'은 각 입력 필드의 유효성을 검사 후 에러 발생에 대한 메시지를 출력하기 위한 template이다.

UserCreationForm은 각 필드에 대한 유효성 검사 코드가 내장되어 있으며, 그 결과를 template에 전송한다.

'form_error.html'은 다음과 같이 작성할 수 있다.
```html
{% if form.errors %}
<div class="form_error">
    {% for field in form %}
        {% for error in field.errors %}  <!-- field error -->
            <div class="field_error">
                <span>- {{ field.label }} : {{ error }}</span>                
            </div>
        {% endfor %}
    {% endfor %}
    {% for error in form.non_field_errors %}   <!-- none field error -->
        <div class="non_field_errors">
            <span>{{ error }}</span>
        </div>
    {% endfor %}
</div>
{% endif %}
```
발생하는 오류의 종류는 2가지 이다.
* field error : 각 필드의 유효성 검사 결과에 해당하는 오류.
* none field error : 필드의 유효성 검사와 상관없는 오류(예를 들어, 로그인 시 id나 비밀번호가 잘못된 경우 등)

회원 가입 페이지로 이동하기 위해 다음과 같이 링크를 작성한다.
```html
<a href="{% url "join" %}">[회원가입]</a>
```

### view 작성
views.py에는 write나 update와 마찬가지로 GET과 POST에 따라 구분하여, 가입 페이지를 출력하거나 가입 처리를 수행하도록 코드를 작성한다.

form.py에서 작성한 가입용 class와 authentication 관련 모듈을 import 한다.
```python
from .form import UserForm
from django.contrib.auth import authenticate, login, logout
```

회원 가입 관련 처리를 위한 코드를 작성한다.
```python
def join(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '가입 성공')
            return redirect('index')
    else: # Get 요청일 떄
        form = UserForm()        
    return render(request, 'join.html', {"form": form})
```

### url 작성
urls.py에 가입 페이지로 이동하기 위한 urlpattern을 작성한다.

```python
urlpatterns = [
    ...
    path('join', views.join, name='join'),
]
```

## 로그인
로그인은 view를 따로 만들지 않고 django framework에서 제공하는 login용 모듈을 사용한다.

django.contrib.auth 패키지는 로그인용 view를 제공한다.

### Template 작성
templates 폴더에 'login.html'을 생성하고 다음과 같이 작성한다.
```html
{% extends "master.html" %}
{% load static %}
{% block section %}
<h2>로그인</h2>
<div>
    <form method="post" action="{% url "login" %}">
        {% csrf_token %}
        {% include "form_errors.html" %}
        <div class="i-form">
            <div>
                <label for="username">사용자ID</label>
                <input type="text" name="username" id="username" value="{{ form.username.value|default_if_none:'' }}">
            </div>
            <div>
                <label for="password">비밀번호</label>
                <input type="password" name="password" id="password" value="{{ form.password.value|default_if_none:'' }}">
            </div>
            <input type="submit" value="login">
        </div>        
    </form>
</div>
{% endblock %}
```

각 입력 필드의 name 속성값은 'auth_user' 테이블의 컬럼과 동일한 이름(model의 필드명)으로 작성한다.

로그인 페이지로 이동을 위해 다음과 같이 링크를 작성한다.
```html
<a href="{% url "login" %}">[로그인]</a>
```

### url 작성
urls.py에 먼저 django.contrib.auth 패키지의 views 모듈을 import한다.
```python
from django.contrib.auth import views as auth_views
```
myapp에 작성한 views.py와의 구분을 위해 'auth_views'로 지정한다.

로그인 페이지로 이동하기 위한 urlpattern을 작성한다.
```phthon
urlpatterns = [
    ...
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),    
]
```

LoginView는 로그인 화면에 해당하는 view class로 as_view()로 template을 지정할 수 있으며, 로그인과 관련된 기능을 제공한다.

### 로그인 성공 시 리다이렉트 설정
myproject/myproject 폴더의 settings.py에 다음과 같이 설정한다.
```python
...
# Login 성공시 URL 경로
LOGIN_REDIRECT_URL = "/"
```

## 로그아웃
역시 django.contrib.auth 패키지에서 로그아웃용 view를 제공한다.

### 로그아웃 링크 처리
Django framework 5부터 GET으로 전송되는 logout은 처리하지 않는다.

따라서, form을 작성하여 POST로 처리해야 한다.
```html
<form action="{% url "logout" %}" method="post">
    {% csrf_token %}
    <label for="logout">[로그아웃]</label>
    <input type="submit" id="logout" style="display: none;">
</form>
```

### url 작성
로그아웃을 처리하기 위한 urlpattern을 작성한다.
```phthon
urlpatterns = [
    ...
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),    
]
```

### 로그아웃 성공 시 리다이렉트 설정
myproject/myproject 폴더의 settings.py에 다음과 같이 설정한다.
```python
...
# Logout 성공시 URL 경로
LOGOUT_REDIRECT_URL = "/"
```

### 로그아웃 성공 시 메시지 전송
로그아웃 후 첫페이지로 이동 시 메시지를 전송하여 출력할 경우 위의 django.contrib.auth 패키지에서 로그아웃용 view를 사용할 수 없다.

이 작업을 위해 views.py에 로그아웃을 처리하는 메소드를 작성한다.
```python
def logout_view(request):
    if request.method == 'GET': # 또는 'POST'
        logout(request)
        messages.success(request, '로그아웃 성공')
        return redirect('index')
```

urls.py는 다음과 같이 수정한다.
```phthon
urlpatterns = [
    ...
    path('logout/', views.logout_view, name='logout'),
]
```

settings.py에 작성한 logout 시 리다이렉트 설정은 지운다.

링크 작성 시 form을 사용하면 로그아웃은 버튼 형태가 된다.

로그인이나 회원가입과 같이 ```<a>``` 태그를 사용하고자 할 경우는 다음과 같이 작성한다.
```html
<a href="{% url "logout" %}">[로그아웃]</a>
```

```<form>```을 사용하여 작성한 경우는 views의 메소드에서 'POST'로 작성하면 되고, ```<a>```를 사용한 경우는 'GET'으로 작성한다.

## 로그인/로그아웃에 따른 template 변화
### is_anonymous
로그아웃의 상태를 저장하는 것으로, 로그아웃일 때 True를 반환한다.

views.py에서 사용할 때는 다음과 같이 사용할 수 있다.
```python
if request.user.is_anonymous:
    # 로그아웃이면 처리할 작업
else:
    # 로그인이면 처리할 작업
```

Template에서는 다음과 같이 사용할 수 있다.
```html
{% if user.is_anonymous %}
    <p>로그아웃 되었습니다.</p>
{% endif %}
```

### is_authenticated
is_anonymous의 반대로, 로그인일 때 True를 반환한다.

views.py에서 사용할 때는 다음과 같이 사용할 수 있다.
```python
if request.user.is_authenticated:
    # 로그인이면 처리할 작업
else:
    # 로그아웃이면 처리할 작업
```

Template에서는 다음과 같이 사용할 수 있다.
```html
{% if user.is_authenticated %}
    <p>로그인 되었습니다.</p>
{% endif %}
```

### is_authenticated 적용한 프로젝트 예
header 부분에 로그인, 로그아웃, 회원가입 메뉴를 추가하는 예는 다음과 같다.
```html
{% if user.is_authenticated %}
    {% comment %} 
    <form action="{% url "logout" %}" method="post">
        {% csrf_token %}
        <label for="logout">[로그아웃]</label>
        <input type="submit" id="logout" style="display: none;">
    </form> 
    {% endcomment %}
    <span>{{user.username}}님</span> <a href="logout">[로그아웃]</a>
{% else %}
    <a href="login">[로그인]</a>
    <a href="join">[회원가입]</a>
{% endif %}
```


