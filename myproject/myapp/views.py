from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import DataTbl
from .form import DataForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import datetime

# Create your views here.
# def index(request):
#     context = '''<h1>Hello, world.</h1>
#             <p><a href="testing">[이동]</a></p>'''
#     return HttpResponse(context)

def index(request):
    dList = DataTbl.objects.all().order_by('-id').values()
    template = loader.get_template('index.html')
    context = {
        'dList': dList,
    }
    return HttpResponse(template.render(context, request))

def testing(request):
    template = loader.get_template('template.html')
    test_list = ('아메리카노','카페라떼','카페모카','카푸치노','녹차')
    context = {
        'title': '테스트용 페이지',
        'data': '출력할 내용',
        'date_data': datetime.datetime.now(),
        'count': 1,
        'tlist': test_list,
    }
    return HttpResponse(template.render(context, request))

def somepage(request):
    template = loader.get_template('somepage.html')
    context = {
        'title': ' - Myapp',
        'site_title': '어떤 페이지',
        'data': 'master.html을 활용한 template 확장',
    }
    return HttpResponse(template.render(context, request))

def write(request):
    if request.method == 'POST':
        data_form = DataForm(request.POST)
        if data_form.is_valid():
            data = data_form.save(commit=False)
            data.save()
            messages.success(request, '작성 성공')
            return redirect('index')
    else:
        data_form = DataForm()
        template = loader.get_template('writeForm.html')
        context = {
            'form': data_form,
        }
    return HttpResponse(template.render(context, request))
    
def update(request, id):
    data = get_object_or_404(DataTbl, id=id)
    if request.method == 'POST':
        data_form = DataForm(request.POST, instance=data)
        if data_form.is_valid():
            data = data_form.save(commit=False)
            data.save()
            messages.success(request, '수정 성공')
            return redirect('index')
    else:
        data_form = DataForm(instance=data)
        template = loader.get_template('updateForm.html')
        context = {
            'form': data_form,
        }
    return HttpResponse(template.render(context, request))

def delete(request, id):
    data = get_object_or_404(DataTbl, id=id)
    data.delete()
    messages.success(request, '삭제 성공')
    return redirect('index')
    
def page_not_found(request, exception):
    context = {
        'title': ' - 페이지 없음'
    }
    response = render(request, 'error/404.html', context)
    response.status_code= 404
    return response
