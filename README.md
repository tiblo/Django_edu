# Django

Django는...
> 프랑스의 유명한 작곡가 Django Reinhardt의 이름을 따서 명명된, 모델-뷰-컨트롤러(MVC)의 아키텍처 패턴을 따르는 Python 기반 웹 프레임워크.<br>
  쉽고 빠르게 웹사이트를 개발할 수 있도록 돕는 구성요소로 이루어져 있으며 강력한 라이브러리들을 그대로 사용할 수 있다는 큰 장점을 가지고 있다.

## Django 사용의 장점
* Django는 확장성이 뛰어난 것으로 알려져 있다. 특히 코드 재사용성 기능을 통해 개발자는 웹사이트에서 증가하는 트래픽에 쉽게 적응할 수 있다.
* Django를 기반으로 하는 웹사이트는 최적화가 쉽고 SEO 친화적. IP 주소가 아닌 URL을 통해 서버에서 Django 기반 애플리케이션의 유지가 가능.
* 코드 없음 지향: 코드 없는 프레임워크가 아니지만 개발자가 코드를 사용하지 않고 활용할 수 있는 패키지가 있다.
* 다용성: 언급한 바와 같이 Django는 특히 데이터베이스 기반 웹사이트에 적합하며, 모든 유형의 웹 사이트를 만드는 데 사용할 수 있다.

# Django Cycle
> WSGI(Web Server Gateway Interface)는 웹 서버 소프트웨어와 파이썬으로 작성된 웹 응용 프로그램 간의 표준 인터페이스.<br>
  Django 프레임워크는 웹 서버를 통해 넘어오는 client의 request를 WSGI Server(Middleware)로 처리.<br>
  ASGI(Asynchronous Server Gateway Interface)는 비동기 웹 서버, 프레임워크 및 애플리케이션 간의 표준 인터페이스를 제공하기 위한 WSGI의 정신적 후속 버전.

![rLfSC](https://github.com/tiblo/Django/assets/34559256/686e9222-c642-483a-9732-4462ec481082)

# MTV 패턴
MTV(Model, Template, View) 패턴은 웹 개발에서 활용하는 MVC 패턴에 대응되는 Django의 디자인 패턴이다.

![image](https://github.com/tiblo/Django/assets/34559256/66ec095b-1773-4ffb-9e52-0f771eb1071e)

## Model
> DB를 처리하는 부분.<br>
  클래스로 정의하며, 하나의 클래스가 하나의 DB table에 대응된다.<br>
  ORM(Object Relational Mapping)을 지원하여 파이썬 코드로 DB의 CRUD를 처리한다.<br>
  SQL 쿼리 및 파일 저장에 대한 처리도 가능하다.
## Template
> 브라우저에 출력될 화면을 처리하는 부분.<br>
  View에서 처리된 로직의 결과인 context와 html 코드를 렌더링하여 Client에 전달된다.<br>
  Django의 자체적인 Template 문법을 활용하여 html 내에서 context로 전달된 데이터를 출력할 수 있다.
## View
> URL Mapping 및 서비스 로직을 처리하는 부분.<br>
  FBV(Function-Based View)와 CBV(Class-Based View)의 두가지 방식을 활용할 수 있다.<br>
### FBV
> 함수 기반 뷰 작성 방식으로 심플하고 가독성이 좋음

```
def some_url(request):
  if request.method == 'POST':
    # post 전송에 대한 처리 코드
  else:
    # get 전송에 대한 처리 코드
```

코드를 확장하거나 재사용하기 어려우며, 조건문으로 http method를 구분해야 한다.
### CBV
> Class 기반 뷰 작성 방식으로 상속과 믹스인(Mixin) 기능을 이용할 수 있으며, 코드를 재사용하고 뷰를 체계적으로 구성할 수 있음.

```
class SomeUrlClass(View):
  def post(self, request):
    # post 전송에 대한 처리 코드
  def get(self, request):
    # get 전송에 대한 처리 코드
```

http method에 대한 처리를 조건문 대신 메소드 명으로 처리하여 코드 구조가 깔금하고 객체지향 기법을 활용할 수 있지만, FBV에 비하여 코드가 복잡하고 가독성이 떨어짐
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
```
실행 결과
```
Brand: Toyota, Model: Corolla
Engine started.

Brand: Tesla, Model: Model S
Engine started.
Battery charging...
```


## 가상환경 실행 시 보안오류 처리
* Windows Powershell을 관리자 권한으로 실행하여 다음 명령을 실행한다.
```
set-ExecutionPolicy RemoteSigned
```
중간에 y 입력할 것.
