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

```page = request.GET.get('page', 1)``` - request의 parameter로 넘어오는 page 번호를 받아서 처리한다.

만약, page가 넘어오지 않을 경우(처음 방문했을 경우)에는 1페이지가 되도록 default 값을 1로 설정한다.
