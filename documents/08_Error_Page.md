# Custom Error Page

404, 500 등의 에러 페이지를 원하는 디자인으로 구성할 수 있다.
> 프로젝트 이름 - myproject<br>
앱 이름 - myapp<br>

## Setting.py
프로젝트를 생성하면 Debug 모드는 기본적으로 True로 설정된다. 이 경우 Django의 기본 에러페이지를 사용하기 때문에 False로 변경한다.
```python
...
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
...
```

그 다음 문장인 ALLOWED_HOSTS는 서버 접근이 허용된 도메인 네임 또는 IP를 작성한다. 개발 중이기 때문에 'localhost'와 '127.0.0.1'을 함께 추가한다.
```python
...
ALLOWED_HOSTS = ['localhost','127.0.0.1']
...
```

DEBUG를 False로 설정하고 ALLOWED_HOSTS 작성하지 않을 경우 서버는 실행되지 않는다.

## Error Page
'templates' 폴더 밑에 error 폴더를 생성하여 404.html(또는 다른 이름의) 페이지를 작성한다. 
> 기본 설정으로 error 폴더를 생성하지 않고 templates 폴더에 작성하는 것도 가능하며, 각 에러 페이지의 이름은 stauts 코드와 같은 이름을 사용할 수도 있다.
 - 404 오류 -> 404.html<br>
 - 500 오류 -> 500.html 등

```html
{% extends "master.html" %}
{% load static %}
{% block section %}
<h2>페이지 없음</h2>
{% endblock %}
```

## urls.py
myproject/myproject 폴더의 urls.py에 Error Handler를 추가한다.
```python
from django.conf.urls import handler404, handler500

...
handler404 = 'myapp.views.page_not_found'
handler500 = 'myapp.views.server_error'
...
```

## views.py
위의 url에 작성한 핸들러와 연계되는 메소드를 작성한다.

```python
def page_not_found(request, exception):
    context = {
            'title': "처음으로",
        }
    response = render(request, "error/404.html", context)
    response.status_code=404
    return response

def server_error(request, exception):
    context = {
            'title': "처음으로",
        }
    response = render(request, "error/500.html", context)
    response.status_code=500
    return response
```
context에 에러 페이지로 전송할 내용을 작성한다.


