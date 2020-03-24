from django.shortcuts import render, redirect
import requests, ssl, urllib, traceback
from bs4 import BeautifulSoup
from requests import get

# Create your views here.

code_list = []

def index(request):
  code_list.clear()
  print("list cleared")
  print(code_list)
  return render(request, 'index.html')

def process(request):
  base_url = "https://www.google.co.kr/search"
  q_id=request.POST['oj_url'].split('/')[-1]
  lang=request.POST['lang']
  searching = f"백준 {q_id} {lang}"
  
  i=0

  while (len(code_list) <= 4) and (i<20) :
    values={
      'q':searching,
      'oq':searching,
      'aqs':'chrome..69i57.35694j0j7',
      'sourceid':'chrome',
      'ie':'UTF-8',
      'start': i
    }
    hdr={'User-Agent':'Mozilla/5.0'}

    querystring=urllib.parse.urlencode(values)
    req=urllib.request.Request(base_url+'?'+querystring, headers=hdr)
    context=ssl._create_unverified_context()
    try:
      res=urllib.request.urlopen(req, context=context)
    except:
      traceback.print_exc()
      break

    i += 10
    soup=BeautifulSoup(res.read(), 'html.parser')
  #print(soup.prettify('utf-8'))
    targets = soup.find_all('a')[17:27]

    target_url_list=[]
    for target in targets:
      target_url_list.append('https://www.google.com'+target.get("href"))
    #print(target_url_list)
    #return redirect('result', lang=lang, q_id=q_id)
    
    for url in target_url_list:
      result = requests.get(url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'})
      result.encoding = "utf-8"
      soup = BeautifulSoup(result.content.decode("utf-8"), "html.parser")
      print("Scraping site url : "+url)
      if soup.find("div", {"class":"colorscripter-code"}):
        print("♪ got colorscripter")
        for code in soup.find_all("div", {"class":"colorscripter-code"}):
          code_list.append(str(code))
      elif soup.find("code"):
        print("♪ got code")
        for code in soup.find_all("code"):
          code_list.append(str(code).strip())
      else:
        continue
  #code_list = list(set(code_list))
  return redirect('result', lang=lang, q_id=q_id)
  #return redirect(f'result/{lang}/{q_id}')

def result(request, lang, q_id):
  return render(request, 'result.html', {'q_id':q_id, 'lang':lang, 'code_list':code_list})
