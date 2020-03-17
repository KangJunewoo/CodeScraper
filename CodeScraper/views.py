from django.shortcuts import render, redirect
#from .forms import PostForm

# Create your views here.

def index(request):
  return render(request, 'index.html')


def process(request):
  q_id=request.POST['oj_url'].split('/')[-1]
  lang=request.POST['lang']
  return redirect('result', lang=lang, q_id=q_id)
  #return redirect(f'result/{lang}/{q_id}')


def result(request, lang, q_id):
  return render(request, 'result.html', {'q_id':q_id, 'lang':lang})