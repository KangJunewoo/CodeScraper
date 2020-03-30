from flask import Flask, render_template, request, redirect, send_file
import requests, ssl, urllib, traceback
from bs4 import BeautifulSoup

app = Flask('CodeScraper')

code_db={}
code_list=[]

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
  global code_list, code_db
  code_list=[]

  base_url='https://www.google.co.kr/search'
  q_id=request.form['oj_url'].split('/')[-1]
  lang=request.form['lang']
  searching=f'백준 {q_id} {lang}'
  
  #해당 문제번호+언어가 db에 존재하면, 그대로 load.
  if q_id+lang in code_db:
    print('Already in DB😙')
    code_list=code_db[q_id+lang]
    return render_template('result.html', q_id=q_id, lang=lang, code_list=code_list)
  
  #db에 존재하지 않을 경우, scrapping 시작.
  values={
    'q':searching,
    'oq':searching,
    'aqs':'chrome..69i57.35694j0j7',
    'sourceid':'chrome',
    'ie':'UTF-8',
  }
  hdr={'User-Agent':'Mozilla/5.0'}
  querystring=urllib.parse.urlencode(values)
  req=urllib.request.Request(base_url+'?'+querystring, headers=hdr)
  context=ssl._create_unverified_context()
  
  #구글검색을 돌려 되면 res 생성, 안되면 오류 출력
  try:
    res=urllib.request.urlopen(req, context=context)
  except:
    traceback.print_exc()
    
  #bs4로 res에서 url 10개를 추출해 target_url_list에 저장.
  #(구글 검색시 나오는 사이트 10개의 url이 담김)
  soup=BeautifulSoup(res.read(), 'html.parser')
  targets = soup.find_all('a')[17:27]
  target_url_list=[]
  for target in targets:
    target_url_list.append('https://www.google.com'+target.get("href"))
  
  #각 url마다 아래 세 가지 경우에 따라 처리해줍니다.
  for url in target_url_list:
    result = requests.get(url, headers=hdr)
    result.encoding = "utf-8"
    soup = BeautifulSoup(result.content.decode("utf-8"), "html.parser")
    print("◈ Scraping site url : "+url)
    # 1) colorscripter가 달린 코드가 있다면 제일 좋은 경우죠, 바로 code_list에 append!
    if soup.find("div", {"class":"colorscripter-code"}):
      print("♪ got colorscripter")
      for code in soup.find_all("div", {"class":"colorscripter-code"}):
        code_list.append(str(code))
    # 2) 그냥 code가 달려있어도, 처리 한 번 해주고 code_list에 append!
    elif soup.find("code"):
      print("♪ got code")
      for code in soup.find_all("code"):
        strCode = str(code).strip()
        
        #strCode -> newCode 변환 : 공백을 없애줍니다!
        newCode = strCode[:strCode.find(">")+1] + "\n" + strCode[strCode.find(">")+1:]
        code_list.append(newCode)
    # 3) code가 없다면.. skip..
    else:
      continue
  
  #db에 저장 후 render.
  code_db[q_id+lang]=code_list
  return render_template('result.html', q_id=q_id, lang=lang, code_list=code_list)

if __name__ == "__main__":
  app.run(debug = True)