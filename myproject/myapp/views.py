from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template import loader
from .models import DataTbl
from .form import DataForm

# Create your views here.
# 1차 메소드
# def first(request):
#     return HttpResponse("Hello, world.")

def index(request):
    title = "Django 사이트"
    dList = DataTbl.objects.all().order_by('-id').values()
    template = loader.get_template('index.html')
    context = {
        'title': title,
        'dList': dList,
    }
    return HttpResponse(template.render(context, request))

def write(request):
    if request.method == 'POST':
        data_form = DataForm(request.POST)
        if data_form.is_valid():
            data = data_form.save(commit=False)
            data.save()
            return redirect('index')
    else:
        title = "처음으로"
        data_form = DataForm()
        template = loader.get_template('writeForm.html')
        context = {
            'title': title,
            'form': data_form,
        }
        return HttpResponse(template.render(context, request))

# def update(request): # query parameter
def update(request, id):    # path parameter
    # id = request.GET['id'] # query parameter
    data = get_object_or_404(DataTbl, id=id)
    if request.method == 'POST':
        data_form = DataForm(request.POST, instance=data)
        if data_form.is_valid():
            data = data_form.save(commit=False)
            data.save()
            return redirect('index')
    else:
        title = "처음으로"
        data_form = DataForm(instance=data)
        template = loader.get_template('updateForm.html')
        context = {
            'title': title,
            'form': data_form,
        }
    return HttpResponse(template.render(context, request))

def delete(request, id):
    data = get_object_or_404(DataTbl, id=id)
    data.delete()
    return redirect('index')