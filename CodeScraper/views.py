from django.shortcuts import render, redirect
#from .forms import PostForm
import requests
import urllib.request as req
from bs4 import BeautifulSoup
from requests import get

# Create your views here.

code_list = []

def index(request):
  code_list = []
  return render(request, 'index.html')

def process(request):
  base_url = "https://search.naver.com/search.naver?where=webkr&sm=mtv_jum&ie-utf8&query="
  q_id=request.POST['oj_url'].split('/')[-1]
  lang=request.POST['lang']
  search_url = base_url + "백준+" + q_id +"번+"+lang

  result = requests.get(search_url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'})
  result.encoding = "utf-8"
  soup = BeautifulSoup(result.content.decode("utf-8"), "html.parser")
  target_url_list = []
  target_url_a = soup.find("div", {"class":"sp_website section"}).find("ul").find_all("a", {"class":"title_link"})
  for target in target_url_a :
    target_url_list.append(target.get("href"))
  codes_list = []
  for url in target_url_list:
    result = requests.get(url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'})
    result.encoding = "utf-8"
    soup = BeautifulSoup(result.content.decode("utf-8"), "html.parser")
    print("Scraping site url : "+url)
    if soup.find("div", {"class":"colorscripter-code"}):
      print("got colorscripter")
      codes_list.append(soup.find_all("div", {"class":"colorscripter-code"}))
    elif soup.find("div", {"class":"se_code"}):
      print("got __se_code_view")
      codes_list.append(soup.find_all("div", {"class":"se_code"}))
    elif soup.find("table", {"class":"highlight"}):
      print("got highlightjs")
      codes_list.append(soup.find_all("table", {"class":"highlight"}))
#왠진 모르겠지만 se_code랑 highlightjs가 포함된 html들은 제대로 긁혀 오지가 않네요..
    elif soup.find("code"):
      print("got code")
      codes_list.append(soup.find_all("code"))
    else:
      continue
  for codes in codes_list:
    code_list.append(str(codes)[1:-1])
    print(type(str(codes)))
  return redirect('result', lang=lang, q_id=q_id)
  #return redirect(f'result/{lang}/{q_id}')

def result(request, lang, q_id):
  return render(request, 'result.html', {'q_id':q_id, 'lang':lang, 'code_list':code_list})
