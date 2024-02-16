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
