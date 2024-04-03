# *args와 **kwargs
파이썬에서 '*'는 여러개의 인수를 받을 때 사용하는 표시이며, '**'는 키워드 인수를 받을 때 사용하는 표시
## *args
* args는 arguments의 줄임말로 함수에서 다수의 인자를 받을 때 사용.
* args는 튜플(tuple, 수정 불가 배열) 형태임.
```
def some_function(*args):
    for arg in args:
        # 반복 코드

some_function(1)
some_function(1, 2)
...
```
  
## **kwargs
* kwargs는 keyword arguments의 줄임말.
* kwargs는 딕셔너리(dictionary, key=value) 형태임.
```
def some_function(**kwargs):
    for key, value in kwargs.item():
        # 반복 코드

some_function(key='value')
...
```

#### Mixin
객체 지향 프로그램에서 많이 쓰이는 개념으로 간단하게 말하여 필요한 메소드들을 포함하고 있는 클래스를 이용하여 상속없이 다른 클래스에 기능을 더해주는 방식. 서로 다른 컴포넌트에서 유사한 기능을 공유하고자 할 때 사용하며, Vue나 React에서 널리 사용됨.
> 예를 들어, 여러 테이블을 생성하기 위해 model을 따로따로 작성하게 되는데 공통된 컬럼이 있다면(생성 시간 저장, 수정 시간 저장 등) 이러한 컬럼들을 분류하여 Mixin 클래스로 작성하고, 각 model 클래스는 필요한 컬럼이 작성된 Mixin 클래스를 상속받아서 작성한다.

Mixin 예제(by ChatGpt)
```python
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def display_info(self):
        print(f"Brand: {self.brand}, Model: {self.model}")


class EngineMixin:
    def start_engine(self):
        print("Engine started.")


class ElectricMixin:
    def charge_battery(self):
        print("Battery charging...")


class Car(Vehicle, EngineMixin):
    def __init__(self, brand, model):
        super().__init__(brand, model)


class ElectricCar(Vehicle, EngineMixin, ElectricMixin):
    def __init__(self, brand, model):
        super().__init__(brand, model)


car1 = Car("Toyota", "Corolla")
car1.display_info()
car1.start_engine()

print()

car2 = ElectricCar("Tesla", "Model S")
car2.display_info()
car2.start_engine()
car2.charge_battery()

print()
```

실행 결과
```
Brand: Toyota, Model: Corolla
Engine started.

Brand: Tesla, Model: Model S
Engine started.
Battery charging...
```


# VSCode 설정
## Compact Folders
기본값으로 Explorer에서 폴더를 간략히 한줄로 표시하고 있음

이 부분을 해제하는 방법
* Setting > Features > Explorer
    * Compact Folders의 체크를 해제

## Django-HTML과 HTML 자동완성
setting.json에 다음과 같이 추가(Auto Close Tag 설정과 함께 추가)
```
{
    ...,
    "emmet.includeLanguages": {
        "django-html": "html"
    }
}
```

# Django 프로젝트 백업 및 복구
장고 프로젝트를 복사하여 다른 개발환경으로 이동하는 경우

프로젝트 폴더만 압축 -> 새 환경(컴퓨터)의 작업 폴더에서 압축해제 -> 가상환경 설치 -> 개발용 라이브러리 설치(django 등) -> 실행

DB 내용과 동적 업로드 파일(media) 등을 초기화 할 경우 해당 파일을 제거하고 압축


## 가상환경 실행 시 보안오류 처리
* Windows Powershell을 관리자 권한으로 실행하여 다음 명령을 실행한다.
```
set-ExecutionPolicy RemoteSigned
```
중간에 y 입력할 것.
