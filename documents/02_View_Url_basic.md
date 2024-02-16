# view와 url
> 프로젝트 이름 - myproject<br>
앱 이름 - myapp
* views.py - 요청 url에 따라 해당 제공될 기능을 위한 서비스 로직을 작성
* urls.py - url을 등록하여 views에 작성된 서비스 로직용 함수(또는 클래스)와 해당 url을 매핑
    * URLconf(URL Configuration) - Django에서 URL과 일치하는 뷰를 찾기 위한 패턴들의 집합
    * 사용자의 request를 url로 분류하여 해당 view에 전달

## myapp의 views.py
> 사용자의 브라우저 화면에 출력할 내용을 처리하기 위한 뷰를 FBV 또는 CBV 방식으로 작성<br>

함수 작성 형태 - index 페이지
```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world.")
```
문법
```python
def page_name(request):
    # 기능 처리 코드
    return HttpResponse(data, content_type)
```
### HttpResponse()
> 사용자의 request(HttpRequest API로 생성된 객체)에 대한 처리 결과를 사용자 측에 전달(응답)하기 위한 API
* Django는 Request에 따라 메타데이터를 포함하는 HttpRequset객체를 생성한다.
* urls.py에서 정의한 특정 View 클래스/함수에 첫 번째 인자로 해당 HttpRequest객체를 전달.
* 해당 View는 결과값을 HttpResponse나 JsonResponse 객체에 담아 전달.
#### data
> 브라우저에 출력될 내용으로 직접 문자열로 html 태그를 작성하거나 처리된 내용을 담은 template을 지정
#### content-type
> 전송되는 데이터의 MIME type을 지정<br>
주로 파일 다운로드 시 활용하며 html 전송시는 거의 생략함

## url path 등록
> myproject/myproject/urls.py의 urlpatterns에 앱의 url path를 등록
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('myapp/', include('myapp.urls')),
    path('admin/', admin.site.urls), # 원래 있는 내용(admin 사이트 url)
]
```
기본적으로 view의 url들은 config용 (하위)myproject폴더의 urls.py에 등록하는데 include를 써서 고정적인 url을 쉽게 관리하거나, 앱별로 url을 관리 할 수 있다.

myapp에 'urls.py' 파일을 생성 후 다음을 작성
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),    
]
```
> urlpatterns의 형식은 다음과 같다.
```python
urlpatterns = [
    path("some_url1", views.page_name, name="page_name"),
    path("some_url2", views.page_name, name="page_name"),
    ...
]
```

### path()
path() 함수에는 2개의 필수 인수인 route 와 view, 2개의 선택 가능한 인수로 kwargs 와 name 까지 모두 4개의 인수가 전달된다.

```python
path(route, view, kwargs=None, name=None)
```

#### route
route는 URL 패턴을 가진 문자열. 
> 요청이 처리될 때, Django는 urlpatterns의 첫 번째 패턴부터 시작하여, 일치하는 패턴을 찾을 때 까지 요청된 URL을 각 패턴과 리스트의 순서대로 비교.<br>
이 때, GET 이나 POST의 매개 변수들, 혹은 도메인 이름은 비교 대상에서 제외.<br>
예를 들어, https://www.example.com/myapp/ 이 요청된 경우, URLconf는 오직 myapp/ 부분만 작성.

#### view
views.py에 작성된 view 함수(또는 클래스)를 지정.
> Django에서 일치하는 패턴을 찾으면, HttpRequest 객체를 첫번째 인수로 하고, url에 포함된 전송 데이터(파라미터)를 추출하여 키워드 인수로 대상 view에 전달.

#### kwargs
임의의 키워드 인수들은 대상 view에 딕셔너리로 전달.

#### name
URL에 이름을 지으면, 템플릿을 포함한 Django 어디에서나 명확하게 참조할 수 있다.<br>
이 기능을 이용하여, 단 하나의 파일만 수정해도 project 내의 모든 URL패턴을 바꿀 수 있도록 도와준다.
```html
<a href="some_url">이동</a>
```
이 경우 path 메소드의 'route'를 사용하여 페이지를 이동한다.
```python
path('some_url', views.some, name='some'),
```
url 태그를 사용하게 되면 name의 값을 사용한다.
```html
<a href="{% url 'some' %}">이동</a>
```
즉, 페이지의 url이 바뀌더라도 url 태그를 사용한 코드를 수저하지 않고 그대로 사용할 수 있다.(url 태그를 사용하는 이유이기도 함)<br>
또한 redirect() 메소드에서도 name 값을 활용한다.

## 앱 시작 url에 Root 경로 사용
http://127.0.0.1:8000 으로 접속하면 'Page not found' 페이지가 출력된다.

현재 앱에 접속하기 위한 주소는 http://127.0.0.1:8000/myapp 이 되어 있기 때문이다.

Root 경로(http://127.0.0.1:8000) 를 앱의 시작 경로로 사용하기 위해서는 myproject/myproject/urls.py의 urlpatterns에 앱의 url path를 다음과 같이 수정한다.
> path()의 route를 빈문자열로 작성
```python
urlpatterns = [
    path('', include('myapp.urls')),
    path('admin/', admin.site.urls),
]
```


