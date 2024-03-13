# Django Model
Database 테이블을 정의하기 위한 추상화된 클래스

Database를 처리하는 부분으로 myapp 폴더의 models.py 파일에 테이블을 위한 클래스를 작성하면 지정한 DB에 테이블을 작성.

> 프로젝트 이름 - myproject<br>
앱 이름 - myapp

## myapp의 models.py
> 설계한 테이블을 클래스로 작성

문법
```python
from django.db import models
from django.urls import reverse

class Data_tbl(models.Model):
    # Fields
    col_name = models.Field(option)
    ...

    # Meta
    class Meta:
        verbose_name = '테이블 별칭'
        verbose_name_plural = '테이블 별칭 복수형'
        ordering = ['col_name',]

    # Methods
    def get_absolute_url(self):
        return reverse('myapp:myapp_datail', kwargs={'id':self.id})

    def __str__(self):
        return self.col_name

    ...
```

## Model class
테이블의 컬럼을 구성하는 field, 모델에 대한 메타데이터 정의를 위한 meta, 다양한 메소드를 정의

### Fields
테이블 컬럼의 정보를 정의하기 위한 클래스 변수이며, Form 작성 시 input 태그와 연계되는 부분.

#### Field Type
주요 필드 타입 클래스
|Field Type|설명|
|---|---|
|CharField|제한된 문자열 필드 타입.<br>최대 길이를 max_length 옵션에 지정해야 한다.|
|TextField|대용량 문자열을 갖는 필드|
|IntegerField|32 비트 정수형 필드|
|BooleanField|true/false 필드|
|DateTimeField|날짜와 시간을 갖는 필드|
|DecimalField|소숫점을 갖는 decimal 필드|
|BinaryField|바이너리 데이타를 저장하는 필드|
|FileField|파일 업로드 필드|
|ImageField|FileField의 파생클래스로서 이미지 파일인지 체크한다.|
|UUIDField|GUID (UUID)를 저장하는 필드|

* CharField의 파생클래스로서, 이메일 주소를 체크를 하는 EmailField, IP 주소를 체크를 하는 GenericIPAddressField, 콤마로 정수를 분리한 CommaSeparatedIntegerField, 특정 폴더의 파일 패스를 표현하는 FilePathField, URL을 표현하는 URLField 등이 있다.
* 정수 사이즈에 따라 BigIntegerField, SmallIntegerField 을 사용할 수도 있다.
* Null 을 허용하기 위해서는 NullBooleanField를 사용한다.
* 날짜만 가질 경우는 DateField, 시간만 가질 경우는 TimeField를 사용한다.

#### Field Option
필드 타입에 따른 여러 선택사항을 지정
|Field Option|설명|
|---|---|
|null (Field.null)|null=True 이면, Empty 값을 DB에 NULL로 저장한다. DB에서 Null이 허용된다.<br>예: models.IntegerField(null=True)|
|blank (Field.blank)|blank=False 이면, 필드가 Required 필드이다. blank=True 이면, Optional 필드이다.<br>예: models.DateTimeField(blank=True)|
|primary_key (Field.primary_key)|해당 필드가 Primary Key임을 표시한다.<br>예: models.CharField(max_length=10, primary_key=True)|
|unique (Field.unique)|해당 필드가 테이블에서 Unique함을 표시한다. 해당 컬럼에 대해 Unique Index를 생성한다.<br>예: models.IntegerField(unique=True)|
|default (Field.default)|필드의 디폴트값을 지정한다.<br>예: models.CharField(max_length=2, default="WA")|
|db_column (Field.db_column)|컬럼명은 디폴트로 필드명을 사용하는데, 만약 다르게 쓸 경우 지정한다.|
|auto_now (Field.auto_now)| True로 설정하면 model이 저장(수정)될 때마다 현재 날짜로 갱신한다.<br>예: models.DateTimeField(auto_now=True)|
|auto_now_add (Field.auto_now_add)| True로 설정하면 model이 처음 저장될 때 현재 날짜를 저장한다.<br>예: models.DateTimeField(auto_now_add=True)|

#### verbose_name
> 외래키(관계) 관련 필드를 제외한, 각 필드 타입은 선택적으로 첫 번째 인자의 위치에 작성하거나 verbose_name='문자열'로 작성.<br>
외래키 관련 필드는 첫 번째 인자로 관계된 테이블의 클래스가 위치함
```python
col_name = model.CharField(verbose_name='컬럼명', max_length=200)
# 또는
col_name = model.CharField('컬럼명', max_length=200) # 첫 위치인 경우 verbose_name은 생략 가능
# 또는
col_name = model.CharField(max_length=200, verbose_name='컬럼명')
```
> verbose_name은 admin 페이지나 Form(또는 ModelForm)을 활용한 입력 양식에서 출력할 컬럼의 별칭.<br>
생략할 경우 필드의 이름(col_name)이 자동으로 사용된다.

#### id field
기본적으로 Django는 각 모델에 자동으로 id 필드를 추가해준다.
* id 필드는 기본키(primary key) 컬럼으로 작성됨
* id 필드는 자동증가(Auto Increment) 컬럼으로 작성됨
* 다른 필드에 primary_key 옵션이 명시된 경우 자동으로 생성되지 않음

### Meta
Model 클래스의 내부 클래스로 모델의 취급 방법을 변경할 수 있음.
* db_table : 테이블의 이름을 지정
* verbose_name : admin 사이트에서 출력하는 테이블의 별칭을 지정
* verbose_name_plural : admin 사이트에서 출력하는 테이블 별칭의 복수형(한글 별칭에 대해서는 적용 안됨)
* ordering : 테이블의 정렬 기준 컬럼과 방향을 지정
    * 작성한 필드명으로 정렬을 수행하며, 필드명 앞에 '-'를 붙이면 내림차순으로 정렬한다.

### Methods
Django의 Model 클래스에 정의된 기본 메소드(save, delete 등)를 재정의하거나 admin 페이지에서의 인스턴스 출력을 위한 메소드를 작성

#### \_\_str\_\_() 메소드
admin 페이지에서 저장된 데이터 인스턴스의 출력 내용을 지정한다.

> \_\_str\_\_() 메소드를 작성하지 않은 경우 'Model_class_name object (index)'로 출력<br>
\_\_str\_\_()' 메소드에서 특정 필드를 지정하면 해당 컬럼에 저장된 Data 값이 출력됨

admin 페이지에서의 처리에만 해당되므로 반드시 작성할 필요는 없음.

### get_absolute_url() 메소드
템플릿이나 redirect() 에서 해당 모델의 인스턴스를 사용할 때 이 메소드를 작성하면, 코드를 간략화할 수 있으며 모델 접근에 대한 url 변경 시 일일이 변경해야하는 번거로움을 피할 수 있음
> models.py
```python
from django.urls import reverse

class DataModel(models.Model):
  #...
  def get_absolute_url(self):
    return reverse('myapp:data_detail', kwargs={'id': self.id})
```
> data_list.html
```html
<!-- 사용 전 -->
<a href="{% url 'myapp:data_detail' data.id %}">{{data.title}}</a>

<!-- 사용 후 -->
<a href="{{data.get_absolute_url}}">{{data.title}}</a>
```
사용 전 상황에서 하드코딩되어 있는 detail url을 변경하게 되면 모든 url 부분('myapp:data_detail')을 수정해야하지만, get_absolute_url()을 사용할 경우 model(views.py 포함)에서 변경하면 모든 html에서 변경 사항이 적용됨.

### 사용자 정의 메소드
row-level(행) 단위의 인스턴스 처리를 위한 메소드를 정의하여 활용할 수 있음.

예를 들어, 테이블의 두 컬럼을 조합하여 하나의 결과로 화면에 출력하는 경우
```python
from django.db import models

class Data_tbl(models.Model):
    col_name = models.CharField(max_length=20)
    ...

    @property
    def id_col(self):
        return '%d : %s' % (self.id, self.col_name)

# 사용 시
data = Data_tbl.object.get(id=1)
data.id_col
# 출력 -> 1 : some_data
```
#### @property 데코레이터(Decorator)
메소드를 필드인 것처럼 취급할 수 있게 해주는 데코레이터로 사용 시 메소드 명만 작성.
> 파이썬의 Decorator는 함수를 Wrapping하는 기법<br>
기존에 작성된 함수에 기능을 추가하고 싶을 때, 함수 수정 없이 처리가 가능<br>
반복되는 코드를 간소화 시켜 가독성을 높여주는 장점을 갖는다.
```python
def greet(func):
    def todo():
        print('Hi~~')
        func()
        print('Bye~~')
    return todo

@greet
def talk():
    print('Something subject')

# 사용 시
talk()

# 출력
Hi~~
Something subject
Bye~~
```

## Database 생성
models.py 작성 후 db 및 테이블을 생성하기 위한 작업

먼저, 서버가 가동 중이라면 서버는 중지시키고 작업한다.

작업 순서
> makemigrations -> migrate
```
> py manage.py makemigrations myapp
> py manage.py migrate
```

테이블을 수정할 경우도 위와 같은 과정을 다시 수행한다.(서버 중지 -> makemigrations -> migrate -> 서버 실행)

### Migrations
새로 models.py에 작성하거나 변경한 내용을(예를 들면 field를 추가하거나, model을 삭제하는 것 등) 데이터베이스 스키마에 적용.
* Migrations는 내 모델에 적용된 변화를 모아서 각 migrations files에 적용시켜주는 것
* python 문법으로 쓰인 models.py를 SQL문으로 바꾸고 database에 적용시킬 준비를 하는 작업
* setting.py의 INSTALLED_APP에 생성한 App이 등록되어 있지 않으면 실행되지 않음
    * makemigrations 하기 전에 등록할 것!

### Migrate
데이터베이스에 변화된 내용을 실제 테이블에 적용해주는 것. 
* 각 앱의 migrations file은 해당 앱 폴더의 migrations 폴더 안에 존재하고, 승인 처리되어 코드로서 분배된다.
> migrate 명령은 INSTALLED_APPS의 설정을 탐색하여, myproject/settings.py의 데이터베이스 설정과 app과 함께 제공되는 database migrations에 따라, 필요한 데이터베이스 테이블을 생성.<br>
또한 template 파일을 사용할 경우, 파일 인식을 위해서도 앱을 등록해야 한다.
#### setting.py에 앱이름 등록
> myproject/myproject 폴더에 setting.py를 연다.<br>
  INSTALLED_APPS 항목의 마지막에 '앱이름'을 추가한다.
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '앱이름', #<-- 추가`
]
```

## 간이 프로젝트용 DB 스키마
테이블 명 - data_tbl
컬럼
* id - 기본키, 자동증가 정수
* str_data - 문자열 저장 컬럼. 50자.
* int_data - 숫자 저장 컬럼
* reg_data - 생성 일시 저장 컬럼
* upd_data - 수정 일시 저장 컬럼

```python
from django.db import models

# Create your models here.
class DataTbl(models.Model):
    str_data = models.CharField(max_length=50)
    int_data = models.IntegerField()
    reg_data = models.DateTimeField(auto_now_add=True)
    upd_data = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'data_tbl' # 테이블 이름
        verbose_name = '입력테이터'
        verbose_name_plural = '입력데이터들'
```

# Database 초기화
- 먼저 mirgrations 폴더의 파일 중 __init__.py를 제외한 나머지 파일을 모두 삭제한다.
- 다음 db.sqlite3 파일을 삭제한다.
- migration을 재수행한다.

