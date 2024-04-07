# urls.py
```python
urlpatterns = [
    ...
    # 삭제 url 작성
    path('delete/<int:mcode>', views.delete, name='delete'),
    ...
]
```

# views.py
```python
def delete(request, mcode):
    movie = get_object_or_404(Movie, mcode=mcode)
    movie.delete()
    return redirect('index')
```

