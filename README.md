# 장고 시작~

Django는...
> 프랑스의 유명한 작곡가 Django Reinhardt의 이름을 따서 명명된, 모델-뷰-컨트롤러(MVC)의 아키텍처 패턴을 따르는 Python 기반 웹 프레임워크.<br>
  쉽고 빠르게 웹사이트를 개발할 수 있도록 돕는 구성요소로 이루어져 있으며 강력한 라이브러리들을 그대로 사용할 수 있다는 큰 장점을 가지고 있다.

## Django 사용의 장점
* Django는 확장성이 뛰어난 것으로 알려져 있다. 특히 코드 재사용성 기능을 통해 개발자는 웹사이트에서 증가하는 트래픽에 쉽게 적응할 수 있다.
* Django를 기반으로 하는 웹사이트는 최적화가 쉽고 SEO 친화적. IP 주소가 아닌 URL을 통해 서버에서 Django 기반 애플리케이션의 유지가 가능.
* 코드 없음 지향: 코드 없는 프레임워크가 아니지만 개발자가 코드를 사용하지 않고 활용할 수 있는 패키지가 있다.
* 다용성: 언급한 바와 같이 Django는 특히 데이터베이스 기반 웹사이트에 적합하며, 모든 유형의 웹 사이트를 만드는 데 사용할 수 있다.

## 가상환경 실행 시 보안오류 처리
* Windows Powershell을 관리자 권한으로 실행하여 다음 명령을 실행한다.
```
set-ExecutionPolicy RemoteSigned
```
중간에 y 입력할 것.

# Django Cycle
> WSGI(Web Server Gateway Interface)는 웹 서버 소프트웨어와 파이썬으로 작성된 웹 응용 프로그램 간의 표준 인터페이스.<br>
  Django 프레임워크는 웹 서버를 통해 넘어오는 client의 request를 WSGI Server(Middleware)로 처리.<br>
  ASGI(Asynchronous Server Gateway Interface)는 비동기 웹 서버, 프레임워크 및 애플리케이션 간의 표준 인터페이스를 제공하기 위한 WSGI의 정신적 후속 버전.

![rLfSC](https://github.com/tiblo/Django/assets/34559256/686e9222-c642-483a-9732-4462ec481082)
