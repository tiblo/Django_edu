# ModelForm을 활용한 CRUD
ModelForm은 Form 클래스를 상속받은 클래스로 model에서 정의한 내용을 기반으로 template의 form을 작성할 수 있다.

## Form vs ModelForm
* Form은 직접 입력을 위한 필드를 정의해야 하는데, 이 코드는 model.py에서 정의한 모델 필드와 거의 동일하기 때문에 중복된 작업이 된다.
* ModelForm은 모델과 입력을 위한 필드를 지정하면 자동으로 template의 form에 필요한 필드를 자동으로 생성한다.

## ModelForm의 장점
* 폼을 위한 HTML을 작성할 필요가 없다.
* 데이터의 유효성 검사를 자동으로 수행한다.
* 잘못된 데이터 입력 시 에러 메시지를 출력해준다.
* 재사용이 가능하다.

> 프로젝트 이름 - myproject<br>
앱 이름 - myapp<br>
테이블 모델 - DataTbl<br>
컬럼 - str_data, int_data, reg_data, upd_data

## Forms.py
app 폴더(myapp)에 form.py를 생성하여 다음과 같이 라이브러리를 import한다.
```python
from django.forms import *
from .models import DataTbl
```

ModelForm을 상속받은 클래스를 작성한다.
```python
class DataForm(ModelForm):
    class Meta:
        model = DataTbl
        fields = '__all__'
        exclude = ('reg_data', 'upd_data',)
        widgets = {
            'str_data': TextInput(attrs = {
                'placeholder': '문자열',
            }),
            'int_data': NumberInput(attrs = {
                'placeholder': '숫자',
            }),
        }
```

### Meta class
Model의 정보를 작성하는 내부 클래스.<br>
ModelForm에서 사용하는 model을 지정하고 필드의 포함 및 제외 등을 정의. 

#### model
models.py에 작성한 model을 지정

#### fields
form으로 생성할 필드를 지정.
* \_\_all\_\_ : model의 모든 필드를 지정하는 값.
* 모든 필드를 지정하지 않는 경우 튜플로 생성할 필드를 지정
    * fields = ('field1', 'field2')

#### exclude
제외할 필드를 지정. 튜플로 작성.

#### widgets
HTMl input 태그에 적용될 attributes를 지정하기 위해 사용. dictionary로 작성.
```python
widgets = {
    'field1': TextInput(attrs = {
        'class': 'some_class',
        'id': 'some_id',
        ...
    }),
    'field2': ...
}
```

## 데이터 입력 처리
### 입력 페이지 작성
writeForm.html에 \<input\> 대신 form.py에서 작성한 field를 사용한다.
```html
{% extends "master.html" %}
{% load static %}
{% block section %}
<h2>데이터 입력</h2>
<hr>
<div>
    <form method="post" class="i-form">
        {% csrf_token %}
        <div>
            <label>문자열</label>
            {{ form.str_data }}
        </div>
        <div>
            <label>숫자</label>
            {{ form.int_data }}
        </div>
        <input type="submit" value="Send">
    </form>
</div>
{% endblock %}
```

### view 처리
form.py에 작성한 ModelForm class를 import
```python
from .form import DataForm
```

HTML 전송 method에 따라 '입력 페이지로의 이동'인지 '데이터의 저장'인지를 구별하여 하나의 메소드로 처리
* request.method == 'GET' : 입력 페이지로의 이동
* request.method == 'POST' : 입력 데이터 DB insert

```python
from django.shortcuts import render, redirect
...

def write(request):
    if request.method == 'GET':
        title = "처음으로"
        data_form = DataForm()
        template = loader.get_template('writeForm.html')
        context = {
            'title': title,
            'form': data_form,
        }
        return HttpResponse(template.render(context, request))
    else:
        data_form = DataForm(request.POST)
        if data_form.is_valid():
            data = data_form.save(commit=False)
            data.save()
            return redirect('index')
```

#### is_valid()
ModelForm에 정의되어 있는 유효성 검사 메소드.<br>
각 필드에 맞지 않는 데이터 입력 시 저장하지 못하게 막는다.

#### save()
Form에 바인딩된 데이터로 DB 객체를 만들어 저장하는 메소드.<br>
기존 model의 instance가 있다면(수정하는 경우라면) DB Update를 수행하고, 없다면 DB Insert를 수행.<br>
Transaction을 위해 인자로 commit을 False로 설정하고 이후 save()를 재실행하는 방식으로 활용할 것.<br>
(파일 업로드 처리와 같은 경우 파일명 등의 추가 정보를 ModelForm에 넣은 다음 insert하기 위한 방식이기도 함.)

#### ModelForm(arg1, arg2)
ModelForm class를 상속받아 작성한 클래스의 instance 생성 시 arg1은 HTML에서 넘어온 데이터이다.<br>
DB insert 시에는 arg1만 작성한다.<br>
DB update 시에는 arg1은 HTML에서 넘어온 데이터, arg2는 QuerySet의 instance가 된다.
이 때 save()를 실행하면 arg1의 데이터로 DB를 update 한다.
arg1에 instance를 작성하는 경우 QuerySet의 instance(데이터)로 template에 출력할 필드에 데이터를 지정하는 것이다.(수정 처리 부분에서 확인할 것)

### url 처리
myapp/urls.py
```python
urlpatterns = [
    ...
    path('write', views.write, name='write'),
    ...
]
```

## 데이터 수정 처리
입력 처리와 마찬가지로 HTML 전송 method에 따라 '입력 페이지로의 이동'인지 '데이터의 저장'인지를 구별하여 하나의 메소드로 처리
* request.method == 'GET' : 수정 페이지로의 이동
* request.method == 'POST' : 수정 데이터 DB update


template(index.html)
```html
<a href="{% url 'update' id=item.id %}">{{item.str_data}}</a>
```

view method(views.py)
```python
from django.shortcuts import render, redirect, get_object_or_404

def update(request, id):
    data = get_object_or_404(DataTbl, id=id)
    if request.method == 'GET':
        title = "처음으로"
        data_form = DataForm(instance=data)
        template = loader.get_template('updateForm.html')
        context = {
            'title': title,
            'form': data_form,
        }
        return HttpResponse(template.render(context, request))        
    else:
        data_form = DataForm(request.POST, instance=data)
        if data_form.is_valid():
            data = data_form.save(commit=False)
            data.save()
            return redirect('index')
```

urlpatterns(urls.py)
```python
urlpatterns = [
    ...
    path('update/<int:id>', views.update, name='update'),
]
```

> updateForm.html은 writeForm.html과 동일하다.

### parameter의 처리
Client에서 Server로 데이터를 전송할 때 사용하는 방식(상세 페이지 이동 등에서 활용)
* Query Parameter
```html
/data?id=1
```
* Path Variable
```html
/data/1
```

#### Query Parameter 활용
Query Parameter를 사용하는 경우 template에는 다음과 같이 작성한다.
```html
<a href="data?id={{item.id}}">데이터 전송</a>
```

url의 urlpatterns에는 다음과 같이 작성한다.
```python
urlpatterns = [
    ...
    path('data', views.data, name='data'),
    ...
]
```

view의 메소드에서는 다음과 같이 작성한다.
```python
def data(request):
    id = request.GET['id']
    ...
```

#### Path Variable 활용
Path Variable을 사용하는 경우 template에는 다음과 같이 작성한다.
```html
<a href="{% url 'data' id=item.id %}">데이터 전송</a>
```

url의 urlpatterns에는 다음과 같이 작성한다.
```python
urlpatterns = [
    ...
    path('data/<int:id>', views.data, name='data'),
    ...
]
```

view의 메소드에서는 다음과 같이 작성한다.
```python
def data(request, id):
    ...
```

updateForm.html은 다음과 같다.
```html
{% extends "master.html" %}
{% load static %}
{% block section %}
<h2>데이터 수정</h2>
<hr>
<div>
    <form method="post" class="i-form">
        {% csrf_token %}
        {% comment %} 
        {{form}}
        {% endcomment %}
        <div>
            <label>문자열</label>
            {{ form.str_data }}
        </div>
        <div>
            <label>숫자</label>
            {{ form.int_data }}
        </div>
        <input type="submit" value="Send">
    </form>
</div>
{% endblock %}
```

### get_object_or_404()
QuerySet의 get()는 검색한 데이터가 없을 경우 DoesNotExist 메시지를 반환한다. 이 결과를 처리할 때 Http404 예외를 발생시켜 사용자에게 해당 결과가 없음을 보여주어야 한다.<br>
즉, get_object_or_404()는 get()과 404 처리를 합친 것이다.

## 데이터의 삭제 처리
template(index.html)
```html
<a href="{% url 'delete' id=item.id %}">[삭제]</a>
```

view method(views.py)
```python
def delete(request, id):
    data = get_object_or_404(DataTbl, id=id)
    data.delete()
    return redirect('index')
```

urlpatterns(urls.py)
```python
urlpatterns = [
    ...
    path('delete/<int:id>', views.delete, name='delete'),
]
```

### delete()
QuerySet에서 해당 데이터를 삭제하고 이를 DB에 반영.
