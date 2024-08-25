# Django 개발환경 설정
설치할 것들
1. vscode
2. python
> vscode이 콘솔에서 python을 입력.<br>
> Microsoft Store를 통해 설치하면 vscode에서 바로 사용 가능

3. vscode 확장(Extension) 
* Python Extension
* Django Extension

---
# Django 프로젝트 생성 단계
## 1. Django 가상환경 생성
가상환경(Virtual Environments)이란 독립적인 파이썬의 실행 환경을 의미.

Django를 비롯하여 다양한 파이썬 프로젝트들에서 사용할 여러 패키지를 따로 관리하기 위해 분야별로 가상환경을 만들어서 따로 관리함.(프로젝트별로 다른 패키지를 사용할 수 있기 때문에..)

* 터미널 명령어

```
py -m venv '가상환경이름'
```

'가상환경이름'으로 폴더가 생성됨

## 2. 프로젝트 생성
가상환경을 실행한 상태에서 Django를 설치하고 그 후에 프로젝트를 생성.
### 1) 가상환경 실행
```
'가상환경이름'/Scripts/activate
```
### 2) Django 설치
```
pip install django
```
가상환경에 django가 설치됨

* 설치 확인
```
pip freeze
```
또는 '가상환경이름' 폴더의 Lib 폴더 확인
> django, Django-x.x.x.dist-info 폴더가 생성되었는지 확인
### 3) 프로젝트 생성
#### (1) 프로젝트 생성
```
django-admin startproject project_name
```
> 프로젝트를 생성하면 'project_name' 폴더가 생성되고 그 하위에 'project_name' 폴더와 동일한 이름의 폴더가 하나 더 생성되어 설정관련 파이썬 파일들이 생성된다.

### 4) 앱 생성 및 등록
하나의 프로젝트에는 하나 이상의 앱이 작성될 수 있음.

앱(app, application)이란 웹을 구성하는 한 부분이라고 생각할 수 있음. 

즉, 한 쇼핑몰 사이트(프로젝트)를 사용자 부분, 판매자 부분, 관리자 부분으로 구분하여 개발할 경우, 각 부분들을 개별 앱으로 작성한다.

#### (1) 앱 생성
> myproject로 경로 이동 후
```
cd myproject
py manage.py startapp app_name
```

#### (2) setting.py에 언어와 시간을 한국값으로 변경(project_name/project_name/setting.py)
```
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
```

#### (3) 앱 생성 후 프로젝트 구조
```
project_name/
├── manage.py
├── project_name/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── app_name/
    ├── migrations/
    │   └── __init__.py
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    └── views.py
```

### 5) 앱 실행
```
py manage.py runserver
```
> 실행 url : 127.0.0.1:8000<br>
> 실행 중지 : ctrl + c
#### Port 번호 변경
> Django는 기본 포트번호가 8000으로 지정되어 있음.<br>
변경을 위해 따로 설정하는 파일은 없으며 실행 시 port 번호를 지정
```
py manage.py runserver 80
```

### 6) 가상환경 중지
```
deactivate
```
---
## 참고> 가상환경 중지 후 프로젝트를 재시작할 경우
> 경로를 잘 확인할 것.(프로젝트 폴더로 이동했을 경우 activate 안됨)<br>
> 그 경우 ../'가상환경이름'/Scripts/activate 으로 가상환경을 실행할 것

## VSCode Debugging 설정
> '실행 및 디버그' 메뉴에서 'launch.json 파일 만들기' 수행<br>
> '디버거 선택' -> 'python' 선택 -> 'django' 선택<br>
> 작업 폴더에 '.vscode' 폴더와 'launch.json' 파일 생성
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/[프로젝트폴더]/manage.py",
            "args": [
                "runserver",
                "--insecure"
            ],
            "django": true,
            "justMyCode": true,
            "preLaunchTask": "activateVirturalEnv",
        }
    ]
}
```

위와 같이 작성하고 실행하면 오류가 발생한다. 'preLaunchTask' 관려 설정이 없기 때문인데, 다음과 같은 순서로 tasks.json 파일을 생성한다.
* 오류창에서 'Configure Task'버튼 클릭
* 'Create task.json file from template' 선택
* 'Others Example to run an arbitrary external command' 선택

생성된 tasks.json 파일에 다음과 같이 작성한다.
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "activateVirturalEnv",
            "type": "shell",
            "command": "${workspaceFolder}/[가상환경폴더]/Scripts/activate",
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            }
        }
    ]
}
```


