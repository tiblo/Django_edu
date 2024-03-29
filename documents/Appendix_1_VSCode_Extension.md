# 기본 확장팩
## Pyton

![image](https://github.com/tiblo/Django/assets/34559256/3ff530f0-b9fb-46f7-bb7a-2c3bbd54a772)

## Django

![image](https://github.com/tiblo/Django/assets/34559256/80a82821-ef5b-44b9-b23a-907ac2e1c3ed)

## Auto Close Tag
Django template 작성 시 유용한 확장팩

기본적으로 Django HTML에서는 일반 HTML에서의 단축키나 자동완성이 처리되지 않음

설정에서 emmet 검색 후 '항목 추가'로 다음과 같이 설정하면 Django HTML에서 HTML 자동완성 기능을 사용할 수 있음

![image](https://github.com/tiblo/Django/assets/34559256/49f8f076-e24f-4f5f-89d9-4451cc3fb049)

하지만 불편함.

![image](https://github.com/tiblo/Django/assets/34559256/62987317-bb8d-4375-8223-ca09e5689b48)

VSCode의 setting.json에 다음을 추가
```
{
    ...,
    "auto-close-tag.activationOnLanguage": ["*"]
}
```
> setting.json 여는 방법 : 파일 > 기본설정 > 설정<br>
-> 설정 검색에 'setting'을 입력<br>
아무 항목에서 'setting.json에서 편집'을 선택
