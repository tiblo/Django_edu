# Messages Framework
Django의 messages framework은 사용자에게 메시지를 표시하는 유용한 도구이다. 성공 메시지, 경고 메시지, 오류 메시지 등을 쉽게 생성하고 표시할 수 있다.

Message Framework 다음과 같은 특징을 갖는다.
* 1회성 메시지를 담는 용도로 사용한다.
* HttpRequest 인스턴스를 통해 메시지를 담을 수 있다.
* 메시지는 1회 노출되고 사라진다.

## Message level
다양한 메시지 레벨: Django의 messages framework은 다양한 메시지 레벨을 제공합니다. 주요 메시지 레벨에는 다음이 포함됩니다.

* DEBUG: 개발 목적으로 사용되며 주로 디버그 정보를 제공합니다.
* INFO: 일반적인 정보를 제공합니다.
* SUCCESS: 작업이 성공적으로 완료되었음을 나타냅니다.
* WARNING: 사용자에게 경고를 제공합니다.
* ERROR: 오류 메시지를 제공합니다.

## 간단한 예제(by ChatGPT)
views.py
```python
from django.shortcuts import redirect

def my_view(request):
    # 성공 메시지 추가
    messages.success(request, '작업이 성공적으로 완료되었습니다.')
    # 경고 메시지 추가
    messages.warning(request, '주의: 이 작업은 되돌릴 수 없습니다.')

    return redirect('my_redirect_url')
```
html
```html
{% if messages %}
    <ul class="messages">
        {% for message in messages %}
            <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
        {% endfor %}
    </ul>
{% endif %}
```
message.tags를 class로 활용하여 style을 줄 수 있다(bootstrap에서도 활용할 수 있음)
