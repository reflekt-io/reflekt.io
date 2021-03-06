import json
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Curhatan
from .forms import CurhatForm
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

# imported login required
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def index(request):
    Curhat = Curhatan.objects.all().values() 
    response = {'Curhat': Curhat}
    return render(request, 'pojok_curhat_index.html', response)

@login_required(login_url='/login/')
def add_curhat(request):
  
    # create object of form
    form = CurhatForm(request.POST or None)
      
    # check if form data is valid
    if (form.is_valid() and request.method == 'POST'):
        # save the form data to model
        form.save()
        # when saved go back to lab-3
        return HttpResponseRedirect('/')
    
    else:
        form = CurhatForm()

    return render(request, 'pojok_curhat_form.html', {'form': form})

@login_required(login_url='/login/')
def curhat_list(request):
    Curhat = Curhatan.objects.all().values()
    response = {'Curhat': Curhat}
    return render(request, 'pojok_curhat_cards.html', response)


def navbar(request):
    return render(request, 'pojok_curhat_navbar.html')

@login_required(login_url='/login/')
def json_pojok_curhat(request):
    data = serializers.serialize('json', Curhatan.objects.all())
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
def add_pojok_curhat_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        fromCurhat = data["fromCurhat"]

        title = data["title"]

        message = data["message"]

        curhat_form = Curhatan(fromCurhat=fromCurhat, title = title, message = message)
        curhat_form.save()
        return JsonResponse({"status": "success"}, status = 200)
    else:
        return JsonResponse({"status": "error"}, status = 401)
