# Django Paginator
Paginator는 Django Framework에서 제공하는 페이징 처리용 class다.

영화 정보 관리 사이트 프로젝트로 페이징 관련 처리를 진행한다.
> 프로젝트 이름 - movieinfo<br>
앱 이름 - movies<br>
DB - Movie

## View에서의 페이지 처리
먼저 views.py에 Paginator를 import 한다.
```python
...
from django.core.paginator import Paginator
```

첫 화면인 목록 페이지의 index 함수를 다음과 같이 작성한다.
```python
def index(request):
    page = request.GET.get('page', 1)
    movie_list = Movie.objects.all().order_by('-mcode').values()
    paginator = Paginator(movie_list, 5)
    movies = paginator.get_page(page)
    template = loader.get_template('index.html')
    context = {
        'movies': movies,
    }
    return HttpResponse(template.render(context, request))
```

- ``page = request.GET.get('page', 1)`` : request의 parameter로 넘어오는 page 번호를 받아서 처리한다.
    - 만약, page가 넘어오지 않을 경우(처음 방문했을 경우)에는 1페이지가 되도록 default 값을 1로 설정한다.
- ``movie_list = Movie.objects.all().order_by('-mcode').values()`` : movie 테이블의 모든 데이터를 mcode 역순으로 정렬하여 가져온다.
- ``paginator = Paginator(movie_list, 5)`` : Paginator에 가져온 데이터를 넣고, 페이지 당 출력 제한은 5로 설정한다.
- ``movies = paginator.get_page(page)`` : page 번호에 해당하는 페이지를 Paginator에서 꺼내온다.

## Template에서의 페이지 처리
Paginator는 template에서 페이지 처리를 위한 다음과 같은 데이터를 제공한다.
- page.number : 현재 출력되는 페이지의 번호
- page.has_previous : 현재 출력되는 페이지의 이전 페이지 유무(True/False)
- page.has_next : 현재 출력되는 페이지의 다음 페이지 유무(True/False)
- page.previous_page_number : 현재 출력되는 페이지의 이전 페이지 번호
- page.next_page_number : 현재 출력되는 페이지의 다음 페이지 번호
- page.paginator.num_pages : 전체 페이지 개수

활용 예는 다음과 같다.
```html
<div class="paging-area">
    <div class="paging">
        {% if movies.has_previous %}
        <a class='pno' href='?page={{movies.previous_page_number}}'>◀</a>
        {% endif %}
        {% if movies.has_next %}
        <a class='pno' href='?page={{movies.next_page_number}}'>▶</a>
        {% endif %}
        <b class='pno'>{{movies.number}} / {{movies.paginator.num_pages}}</b>
    </div>
</div>
```
