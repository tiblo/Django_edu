# File 처리
영화 정보 관리 사이트 프로젝트로 파일 관련 처리를 진행한다.
> 프로젝트 이름 - movieinfo<br>
앱 이름 - movies<br>
DB - Movie

포스터 이미지의 저장 및 수정, 삭제, 다운로드를 처리.

## File Upload
ImageField를 사용하기 위해서는 파이썬 이미지 처리 라이브러리인 pillow가 필요하다.
```
pip install pillow
```
FileField를 사용할 경우 pillow를 설치할 필요 없음

### ImageField와 FileField의 차이
ImageField
> ImageField는 이미지 파일을 저장하기 위한 특수한 필드.<br>
파일을 업로드할 때, 이미지인지를 확인하고, 필요에 따라 썸네일 생성과 같은 추가적인 작업을 수행할 수 있다.(이미지 크기 조정이나 필터링 등)

FileField
> FileField는 모든 종류의 파일을 저장하기 위한 범용 필드.<br>
이미지 뿐만 아니라 문서, 비디오, 오디오 등 모든 종류의 파일을 다룰 수 있다.<br>
이미지인지 여부를 검증하지 않기 때문에 이미지 파일 이외의 파일을 업로드할 수 있다.

파일 정보 저장을 위해 models.py에 FileField 또는 ImageField를 설정(파일명과 경로를 저장)
```python
class Movie(models.Model):
    ...
    mposter = models.FileField('',upload_to='images/',blank=True)
```
또는
```python
class Movie(models.Model):
    ...
    mposter = models.ImageField('',upload_to='images/',blank=True)
```
FileField 또는 ImageField에는 upload_to로 파일을 저장할 경로를 지정한다.<br>
저장을 위한 기본 경로의 설정은 settings.py에서 처리한다.<br>
```python
...
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

urls.py에 settings.py에서 설정한 경로 정보를 가져오기 위해 다음을 추가한다.
```python
...
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

> 파일의 저장 경로는 'movieinfo/media/images/'가 된다.(프로젝트폴더/media/images)
```
project_name/
├── manage.py
├── media
│   └── images
├── project_name/
└── app_name/    
```

form.py의 ModelForm에 각 입력 필드의 속성을 설정
```python
class MovieForm(ModelForm):
    class Meta:
        ...
        widgets = {
            ...
            'mposter': FileInput(attrs = {
                ...
            }),
        }
```

views.py
```python
def write(request):
    if request.method == 'POST':
        movieForm = MovieForm(request.POST)
        if movieForm.is_valid():
            movie = movieForm.save(commit=False)
            movie.mposter = request.FILES.get('mposter', None)
            movie.save()
            return redirect('index')
    else:
        ...
```
request에서 multipart로 전송되는 파일 정보를 꺼내 movie 객체의 해당 필드에 넣은 다음 DB에 저장한다.

HTML의 form 태그에는 반드시 enctype을 'multipart/form-data'로 설정해야 한다.
```html
    <form method="post" enctype="multipart/form-data">
    ...
```

## File Download
파일의 위치 정보와 물리적인 파일 로딩을 위해 다음과 같이 views.py에 import를 추가한다.
```python
from django.conf import settings     # 파일이 저장된 위치 정보를 setting.py에서 가져오기 위해 추가
import os                            # 물리적인 파일접근을 위해 추가
```
다운로드 함수는 다음과 같다.
```python
def download(request):
    poster = request.GET['poster']
    path = os.path.join(settings.MEDIA_ROOT, poster)
    file_name = os.path.basename(path)
    # 한글 파일명 처리를 위한 방법
    file_name = file_name.encode('utf-8').decode('latin-1')
    if os.path.exists(path):
        with open(path, 'rb') as binary_file:
            response = HttpResponse(binary_file.read(), content_type="application/octet-stream; charset=utf-8")
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
            return response
    else:
        return HttpResponse("<script>alert('파일 없음!');history.back()</script>")
```
settings.py에 설정된 media 폴더의 위치와 DB에 저장된 file의 경로 및 파일명을 path로 설정한다.<br>
os.path.basename() 메소드로 파일명과 확장자를 구할 수 있다.<br>
with ... as는 파일 처리 후 자동으로 파일 객체를 해제해 주기 때문에 유용하다.<br>

HttpResponse를 사용하여 파일을 전송할 때 Content-Disposition 헤더를 사용하여 파일명을 지정한다.<br>
저장 위치로부터 해당 파일을 읽어와서 HttpResponse 객체에 담아서 사용자 컴퓨터로 전송한다.<br>
Content-Disposition 헤더에 파일명을 설정하는데, 이때 한글 파일명은 UTF-8로 인코딩하고, 그 결과를 Latin-1로 디코딩한다.<br>
Latin-1으로 디코딩하는 이유는 HTTP 헤더의 Content-Disposition 필드에는 ASCII 문자 집합만 사용 가능하기 때문에 UTF-8로 인코딩된 문자열을 직접 사용할 수 없기 때문이다.<br>

urls.py는 다음과 같다.
```python
urlpatterns = [
    ...
    path('download', views.download, name='download'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

detail.html의 이미지에 다운로드의 링크를 건다.
```html
    <a href="/download?poster={{movie.mposter}}">
        <img class="poster" src="/media/{{movie.mposter}}">
    </a>
```

## File Update
본 예제에서와 같이 하나의 파일만 저장하는 프로그램일 경우 기존 파일을 삭제하고 새 파일을 저장하는 과정이 필요하다.<br>
DB에 데이터를 저장하기 전 또는 후에 이런 과정을 진행하게 되는데 이때 Django의 Signal을 활용한다.
> Django의 Signal은 애플리케이션에서 발생하는 특정 이벤트를 감지하고 처리하기 위한 메커니즘이다. 이벤트가 발생하면 Signal을 트리거하고, 이에 연결된 리스너 함수들이 실행된다. Signal은 애플리케이션 내에서 여러 가지 작업을 자동화하거나 이벤트에 대한 처리를 추가하기 위해 사용된다.

이 예제어서 파일 수정을 위해 model 객체의 signal을 활용한다. model 객체의 Signal은 다음과 같다.
|Signal|설명|
|---|---|
|pre_save|model 객체가 저장되기 전에 발생하는 signal. 객체가 저장되기 전에 어떤 처리를 수행하려는 경우에 사용.|
|post_save|model 객체가 저장된 후에 발생하는 signal. 객체가 저장된 후에 추가적인 작업을 수행하려는 경우에 사용.|
|pre_delete|model 객체가 삭제되기 전에 발생하는 signal. 객체가 삭제되기 전에 어떤 처리를 수행하려는 경우에 사용.|
|post_delete|model 객체가 삭제된 후에 발생하는 signal. 객체가 삭제된 후에 추가적인 작업을 수행하려는 경우에 사용.|

Signal과 연결된 리스너 함수를 만들 때, receiver 데코레이터를 사용한다.<br>
파일의 수정은 models.py에서 처리한다. 먼저 receiver와 물리적인 처리를 위한 os를 import한다.
```python
from django.dispatch import receiver
import os
```
파일 수정을 객체 저장 전에 먼저 수행하기 위해 pre_save를 활용한다. 해당 코드는 다음과 같다.
```python
@receiver(models.signals.pre_save, sender=Movie)
def update_file_delete(sender, instance, **kwargs):
    if not instance.mcode:
        return False
    try:
        old_obj = sender.objects.get(mcode=instance.mcode)
    except sender.DoesNotExist:
        return False

    for field in instance._meta.fields:
        field_type = field.get_internal_type()
        if field_type == 'FileField' or field_type == 'ImageField':
            ori_file = getattr(old_obj, field.name)
            new_file = getattr(instance, field.name)
            if ori_file and ori_file != new_file and os.path.isfile(ori_file.path):
                os.remove(ori_file.path)
```
views.py에서의 처리는 다음과 같다.
```python
def update(request, mcode):
    movie = get_object_or_404(Movie, mcode=mcode)
    if request.method == 'POST':
        movie_form = MovieForm(request.POST, instance=movie)
        if movie_form.is_valid():
            movie = movie_form.save(commit=False)
            poster = request.FILES.get('mposter', None)
            if poster != None:
                movie.mposter = poster
            movie.save()
            return redirect('/detail/' + str(mcode))
    else:
        movie_form = MovieForm(instance=movie)
        template = loader.get_template('updateForm.html')
        context = {
            'form': movie_form,
            'poster': movie.mposter,
        }
        return HttpResponse(template.render(context, request))
```

urls.py는 다음과 같다.
```python
urlpatterns = [
    ...
    path('update/<int:mcode>', views.update, name='update'),
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## File Delete
파일의 삭제는 데이터의 삭제 후에 진행하도록 post_delete를 활용한다. 해당 코드는 다음과 같다.(models.py)
```python
@receiver(models.signals.post_delete, sender=Movie)
def file_delete(sender, instance, **kwargs):
    for field in instance._meta.fields:
        field_type = field.get_internal_type()
        if field_type == 'FileField' or field_type == 'ImageField':
            ori_file = getattr(instance, field.name)
            if ori_file and os.path.isfile(ori_file.path):
                os.remove(ori_file.path)
```
views.py에서의 처리는 다음과 같다.
```python
def delete(request, mcode):
    movie = get_object_or_404(Movie, mcode=mcode)
    movie.delete()
    return redirect('index')
```

urls.py는 다음과 같다.
```python
urlpatterns = [
    ...
    path('delete/<int:mcode>', views.delete, name='delete'),
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

detail.html에서의 처리는 다음과 같다.(jQuery 사용함)
```javascript
    $(function (){
        ...
        //게시글 삭제
        $("#delbtn").click(function () {
            let conf = confirm("삭제할까요?");
            if (conf) {
                location.href = "/delete/{{movie.mcode}}";
            }
        });
    });
```


> 완성된 코드는 project 폴더에 있습니다.
