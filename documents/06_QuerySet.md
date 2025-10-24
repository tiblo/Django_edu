# QuerySet
Django ORM(Object Relational Mapping)에서 제공하는 데이터 타입으로 DB에서 가져온 객체 목록.

DB 테이블의 데이터를 불러오기 위한 작업은 view와 template에서 수행한다.
> 프로젝트 이름 - myproject<br>
앱 이름 - myapp<br>
테이블 모델 - DataTbl<br>
컬럼 : str_data, int_data, reg_data, upd_data

## objects
QuerySet을 만들어 주는 manager.<br>
manager는 models.py에서 정의한 클래스를 django에서 활용하기 위한 queryset 형태로 만들어 주는 역할을 담당.

## 여러개의 결과 검색
### all()
```python
DataTbl.objects.all()
```
QuerySet의 전체(테이블의 전체) 데이터를 불러온다. 다음의 SQL query문과 같다.
```sql
SELECT * FROM DataTbl
```

### filter()
```python
DataTbl.objects.filter(str_data='문자열')
```
id가 1인 데이터를 불러온다. 다음의 SQL query문과 같다.
```sql
SELECT * FROM DataTbl
WHERE str_data = '문자열'
```

### exclude()
```python
DataTbl.objects.exclude(id=2)
```
id가 2인 데이터를 제외한 나머지 데이터를 불러온다. 다음의 SQL query문과 같다.
```sql
SELECT * FROM DataTbl
WHERE id != 2
```

### Chaining
```python
DataTbl.objects.filter(str_data='문자열').exclude(id=2)
```
filter와 exclude를 연속적으로 사용할 수 있다. id가 2인 데이터를 제외한 str_data가 '문자열'인 데이터를 불러온다.<br>다음의 SQL query문과 같다.
```sql
SELECT * FROM DataTbl
WHERE str_data = '문자열' AND id != 2
```

### Lookup Filter
filter(), exclude() 메소드에서 사용할 수 있는, 필드(컬럼)별 구체적인 값에 대한 비교를 가능하게 하는 Django의 내장 모듈.<br>
연속된 두개의 ```_```(underscore)로 시작.

#### __contains, __icontains
특정 문자가 포함된 데이터를 검색할 때 사용. __contains는 대소문자를 구분하며, __icontains는 대소문자를 구분하지 않는다.
```python
DataTbl.objects.filter(str_data__contains='abc')
```

#### __startwith, __endwith
특정 문자로 시작(startwith)하거나 끝(endwith)나는 데이터를 검색할 때 사용.
```python
DataTbl.objects.filter(str_data__startwith='ab')
```

#### __gt, __lt
지정한 값보다 크(gt)거나 작은(lt) 데이터를 검색할 때 사용.
```python
DataTbl.objects.filter(id__gt=2)
```

#### __isnull
True로 지정 시 해당 컬럼이 null인 데이터만, False로 지정 시 해당 컬럼이 null이 아닌 데이터만 검색.
```python
DataTbl.objects.filter(str_data__isnull=True)
```

#### __year, __month, __day, __date
date 타입의 필드에서 특정 년(__year), 월(__month), 일(__day) 혹은 특정 날짜(__date : YY-MM-DD 형식)의 데이터를 검색.

### AND/OR
두개 이상의 조건을 AND 또는 OR을 이용하여 결합할 수 있다.
* AND 조건 : 두 개 이상의 쿼리 셋을 '&' 로 연결
* OR 조건 : 두 개 이상의 퀴리 셋을 '|'로 연결
```python
DataTbl.objects.filter(str_data__isnull=True) & DataTbl.objects.filter(str_data__icontains='abc')
```

## 하나의 결과 검색
### get()
```python
DataTbl.objects.get(id=1)
```
id가 1인 데이터 하나를 불러온다.<br>다음의 SQL query문과 같다.
```sql
SELECT * FROM DataTbl
WHERE id = 1
```

#### filter와의 차이
filter는 데이터가 없을 경우 빈(empty) queryset을 불러오지만, get의 경우 DoesNotExist 메시지를 출력.<br>
get은 데이터가 여러개일 경우 MultipleObjectsReturned라는 메시지를 출력.<br>
또 get은 chaining을 할 수 없다.

## 기타 메소드
### count()
QuerySet에 포함된 데이터의 개수를 구하는 데 사용.
```python
DataTbl.objects.count()
```

### exists()
filter, exclude와 chining하여 사용. 해당 데이터가 있으면 True, 없으면 False를 리턴.
```python
DataTbl.objects.filter(str_data__icontains='abc').exists()
```

### values(), values_list()
QuerySet의 내용을 dictionary 형태로 변환하여 반환. (template에 전달하기 위해 변환이 필요)<br>
인자가 없을 경우 모든 컬럼의 데이터를 반환하지만, 특정 컬럼을 넣으면 해당 컬럼의 데이터만 반환.<br>
values_list는 내용을 list 형태로 변환하여 반환.

### order_by()
인자에 작성한 컬럼명을 기준으로 정렬한 데이터를 반환.<br>
기본은 오름차순 정렬이며, 컬럼명 앞에 '-'(minus)를 붙이면 내림차순으로 정렬.


# 간이 프로젝트용 view와 template 처리
## views.py
먼저 model의 테이블 객체를 import.
```python
from .models import DataTbl
```

목록 출력을 위한 view 메소드에 QuerySet으로부터 전체 데이터를 가져온다.
```python
def index(request):
    title = "Django 사이트"
    dList = DataTbl.objects.all().order_by('-id').values()
    template = loader.get_template('index.html')
    context = {
        'title': title,
        'dList': dList,
    }
    return HttpResponse(template.render(context, request))
```

## index.html
```html
{% extends "master.html" %}
{% load static %}
{% block section %}
<a href="/write">[데이터입력]</a>
<hr>
<h2>데이터 목록</h2>
<table border="1" class="dtable">
    <thead>
    <tr>
        <th width="50">번호</th>
        <th width="300">문자열</th>
        <th width="100">숫자</th>
        <th width="300">작성일시</th>
        <th width="300">수정일시</th>
        <th width="80">삭제</th>
    </tr>
    </thead>
    <tbody>
        {% for item in dList %}
        <tr>
            <td>{{item.id}}</td>
            <td><a href="">{{item.str_data}}</a></td>
            <td>{{item.int_data}}</td>
            {# filter 활용 예 : 날짜를 출력하는 형식 지정. #}
            <td>{{item.reg_data|date:'Y년 n월 j일'}}</td>
            <td>{{item.upd_data}}</td>
            <td><a href="">[삭제]</a></td>
        </tr>
        {% empty %}
        <tr><td colspan="6">데이터가 없습니다.</td></tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```
