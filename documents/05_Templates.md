# Django Templates
내장된 template tag를 사용하여 파이썬코드를 html 코드로 변환하여 동적인 웹 페이지를 작성.
> 프로젝트 이름 - myproject<br>
앱 이름 - myapp

## Template 문법
myapp 폴더 하위에 templates 폴더를 작성하고 html문서를 생성하여 django template 문법에 따라 작성.

### Template 주석
* 한줄 주석 - {# #}
```html
{# 여기에 한줄로 주석을 작성 #}
```
* 여러줄 주석 - {% comment %} {% endcomment %}
```html
{% comment %}
여러줄의 주석을 작성하는 경우
...
{% endcomment %}
```

### Template variable
{{ 식별자 }} : view에서 template으로 전달된 값을 출력하는 형식

'식별자'는 view에서 값을 저장한 객체의 key임.({key : value})

myapp/urls.py
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('testing', views.testing, name='testing'),
]
```

views.py
```python
from django.http import HttpResponse
from django.template import loader
import datetime

def testing(request):
    template = loader.get_template('template.html')
    context = {
        'data': '출력할 내용',
        'date_data': datetime.datetime.now(),
    }
    return HttpResponse(template.render(context, request))
```
template.html
```html
<p>{{data}}</p>
```

### Template Filter
변수의 표시에 변화를 줄 때 사용

변수 뒤에 '|'(pipe) 문자와 함께 사용

> 형식 : {{ value|filter }}

```python
{{ date_data|date:'Y-m-d'}}
```
> 결과 : 2024-04-06

#### 주요 필터
주요 필터 관련 문서 : https://docs.djangoproject.com/ko/4.2/ref/templates/builtins/#std-templatefilter-add


### Template tag
변수 생성, 제어문 활용(if, for 등)을 위한 태그

실행할 태그를 {% %}로 묶어서 작성하며, 시작 태그와 종료 태그로 구성된다.

#### 변수 생성 태그 : {% with %}
Template tag를 사용하여 직접 변수를 생성하여 활용할 수 있음(띄어쓰기 주의)
* 시작 태그 - {% with name="값" %}
* 종료 태그 - {% endwith %}<br>
```html
{% with name='user' %}
<h2>{{name}}님 안녕하세요.</h2>
{% endwith %}
```

#### 조건 분기 태그 : {% if %}
변수의 값을 평가하여 true인 경우 코드 블록을 실행
* 시작 태그 : {% if condition %}
* 종료 태그 : {% endif %}

추가 조건을 처리하는 {% elif %}, false에 해당하는 {% else %}를 함께 사용(조건 작성 시 연사자 앞뒤로 띄어쓰기 주의.)
```html
{% if testing == 1 %}
  <h1>Hello</h1>
{% elif testing == 2 %}
  <h1>Welcome</h1>
{% else %}
  <h1>Goodbye</h1>
{% endif %} 
```
활용 연산자
> 비교 연산자 : ==, !=, >, >=, <, <=<br>
논리 연산자 : and, or<br>
객체 내 항목의 존재 여부 : in/not in<br>
두 객체의 동일 여부 : is/is not

#### 반복 태그 : {% for %}
배열, 목록 또는 딕셔너리의 항목을 순서대로 반복하여 출력(또는 활용)할 때 사용
* 시작 태그 : {% for %}
* 종료 태그 : {% endfor %}

목록 데이터가 빈 상태의 처리를 위한 {% empty %}를 함께 사용
```html
<ul>
  {% for item in object %}
    <li>{{ itme.name }}</li>
  {% empty %}
    <li>No item</li>
  {% endfor %}
</ul> 
```
역순으로 반복할 경우 reversed를 붙인다.
```html
{% for item in object reversed %}
```

forloop 객체를 활용하여 반복 횟수 등의 목록 index나 count와 같은 상태(status) 값을 활용할 수 있다.
|variable|설명|
|---|---|
|forloop.counter0|0부터 시작하는 반복 횟수 출력|
|forloop.counter|1부터 시작하는 반복 횟수 출력|
|forloop.revcounter0|0부터 시작하는 반복 횟수를 역순으로 출력|
|forloop.revcounter|1부터 시작하는 반복 횟수를 역순으로 출력|
|forloop.first|첫번째 반복이면 True|
|forloop.last|마지막 반복이면 True|
|forloop.parentloop|중첩된 반복일 경우 외부 반복 객체를 참조<br>예: forloop.parentloop.counter|

#### CSRF(Cross Site Request Forgery) : {% csrf_token %}
> CSRF : 웹사이트 취약점 공격의 하나로, 사용자가 자신의 의지와는 무관하게 공격자가 의도한 행위(수정, 삭제, 등록 등)로 특정 웹사이트에 요청하게 하는 공격

CSRF 공격을 방어하기 위한 태그로 주로 ```<form>```에서 ModelForm을 사용하기 전에 작성.
```html
<form method="post">
    {% csrf_token %}
    <div>
        <label>문자열</label>
        {{ form.some_input1 }}
    </div>
    <div>
        <label>숫자</label>
        {{ form.some_input2 }}
    </div>
    <input type="submit" value="Send">
</form>
```
>동작 과정
* 사용자가 해당 페이지에 접속하면 Django에서 자동으로 csrf_token을 클라이언트로 보내어 cookie에 저장
* 사용자가 form을 모두 입력한 후 전송
* form과 cookie의 csrf_token을 함께 POST로 전송
* 전송된 token의 유효성을 검증
* 유효한 요청이면 요청을 처리
* token이 유효하지 않거나(없거나 값이 잘못된 경우) 검증 오류 시에는 403 Forbidden Response 반환


## 실습용 코드
### myapp/views.py
```python
...
def testing(request):
    template = loader.get_template('template.html')
    test_list = ('아메리카노','카페라떼','카페모카','카푸치노','녹차')
    context = {
        'title': '테스트용 페이지',
        'data': '출력할 내용',
        'count': 1,
        'tlist': test_list,
    }
    return HttpResponse(template.render(context, request))
...
```

### myapp/urls.py
```python
urlpatterns = [
    ...
    path('testing', views.testing, name='testing'),
    ...
]
```

### template.html
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
</head>
<body>
    <h1>{{title}}</h1>
    <p>{{data}}</p>
    <hr>
    {% with name="user" %}
    <h2>{{name}}님 안녕하세요.</h2>
    {% endwith %}
    {% if count == 0 %}
        <p>첫 방문입니다.</p>
    {% elif count == 1 %}
        <p>다시 오셨군요.</p>
    {% endif %}
    <hr>
    <h2>메뉴</h2>
    <ul>
    {% for item in tlist reversed %}
        <li>{{forloop.revcounter0}} : {{item}}</li>
    {% empty %}
        <li>메뉴 없음</li>
    {% endfor %}
    </ul>
    <hr>
    <p><a href="somepage">[이동]</a></p>
</body>
</html>
```

## Template 확장 - Master Template(또는 Base Template)
header 영역, navigation 영역, footer영역 등 모든 페이지(template)에서 동일한(공통적인) 부분을 하나의 template에 모아 놓는 방식

![image](https://github.com/tiblo/Django/assets/34559256/ef9d5d8b-cde2-4511-8415-9499159a67ee)

그림과 같은 구조의 페이지를 작성할 경우, master.html은 다음과 같이 작성한다.
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>페이지 제목</title>
</head>
<body>
    {% include "header.html" %}
    {% block section %}{% endblock %}
    {% include "footer.html" %}
</body>
</html>
```
### 공통된 영역의 파일 포함 - {% include "some.html" %}
별도로 작성한 html 파일을 특정 페이지에 포함시킬 때 사용하는 template 태그<br>
위의 예에서 header와 footer를 따로 파일로 작성하여 모든 페이지에 포함시키는 형식으로 활용할 수 있다.<br>
master.html은 모든 페이지의 공통된 부분을 처리하는 페이지이므로 결과적으로 모든 페이지에 동일한 header와 footer가 포함된다.
> 별도의 html 파일에는 &lt;html&gt;, &lt;head&gt; 태그 등은 작성하지 않고 &lt;body&gt;에 들어갈 요소관련 태그만 작성

### 개별적인 페이지 영역 처리 - {% block xxx %} ... {% endblock %}
개별적인 화면을 위한 영역은 block 태그를 사용한다. 이 영역은 개별적인 내용이 나오는 html 페이지를 각각 작성하여 포함시키도록 한다.

예를 들어, index.html 페이지는 master 페이지를 확장(extends)시켜서 head 부분을 처리하고 section 부분만 작성하는 방식으로 완성한다.
```html
{% extends 'master.html' %}
{% block section %}
    index.html에서 보여질 요소...
{% endblock %}
```

# Static resource 처리
Static resource(정적 자원)는 배경 이미지, 스타일 시트, Javascript 등을 나타낸다.

## static 폴더 설정
project_name/project_name/setting.py에 이미 설정되어 있다. 다음을 추가한다.
```python
...
STATIC_URL = 'static/'
...
```

프로젝트 폴더 하위에 static 폴더를 작성하여 해당 파일을 저장

```
project_name/
├── manage.py
├── project_name/
└── app_name/
    └── static/
        ├── css/
        ├── images/
        └── js/
```

* 각 자원들은 폴더로 구분하여 처리하는 것이 좋다.
    * 이미지 파일 - images
    * 스타일 시트 - css
    * Javascript - js

## Static url 
myproject/myproject 폴더의 urls.py에 static url을 작성한다.
```python
from django.urls import re_path as url
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    ...    
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
```

## Template 안에서 static 불러오기 - {% load static %}
html 파일에서 정적 자원을 활용하기 위해서 사용하는 태그.<br>
반드시 자원 활용 전에 먼저 작성되어야 한다.
```html
{% load static %}
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django Home</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
...
```
## static 활용 태그 - {% static '경로/파일' %}
static 파일을 활용하는 요소에서 사용하는 태그.(위의 예와 같이 사용)
```html
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
```

## 실습용 코드
### myapp/views.py
```python
...
def somepage(request):
    template = loader.get_template('somepage.html')
    context = {
        'site_title': ' - Myapp',
        'title': '어떤 페이지',
        'data': 'master.html을 활용한 template 확장',
    }
    return HttpResponse(template.render(context, request))
```

### myapp/urls.py
```python
...
urlpatterns = [
    ...
    path('somepage', views.somepage, name='somepage'),
]
```

### static/mystyle.css
```css
* {
    background-color: beige;
}
```

### templates/header.html
```html
<h1><a href="/">Django 사이트{{title}}</a></h1>
<hr>
```

### templates/master.html
```html
{% load static %}
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <link rel="stylesheet" href="{% static "css/mystyle.css" %}">
</head>
<body>
    {% include "header.html" %}
    {% block section %}{% endblock %}
</body>
</html>
```

### templates/somepage.html
```html
{% extends "master.html" %}
{% block section %}
<h1>{{site_title}}</h1>
<p>{{data}}</p>
{% endblock %}
```


