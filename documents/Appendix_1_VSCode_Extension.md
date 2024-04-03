# 기본 확장팩
## Pyton

![image](https://github.com/tiblo/Django_edu/assets/34559256/b3bc83d5-9587-4769-ae9b-ec598bcb6079)

## Django

![image](https://github.com/tiblo/Django_edu/assets/34559256/35f52596-e398-43d8-ba82-f289bb6ce1a7)

## Auto Close Tag
Django template 작성 시 유용한 확장팩

기본적으로 Django HTML에서는 일반 HTML에서의 단축키나 자동완성이 처리되지 않음

설정에서 emmet 검색 후 '항목 추가'로 다음과 같이 설정하면 Django HTML에서 HTML 자동완성 기능을 사용할 수 있음

![image](https://github.com/tiblo/Django_edu/assets/34559256/6f61912a-def3-468c-b666-ed7ddbf45275)

하지만 불편함.

![image](https://github.com/tiblo/Django_edu/assets/34559256/fafe6d22-e38f-48c0-bf76-92cf26213fc2)

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
