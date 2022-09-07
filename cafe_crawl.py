from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import os
os.environ['WDM_LOG_LEVEL'] = '0'

chrome_options = webdriver.ChromeOptions()
pc_header = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36', #chrome 88
]
chrome_options.add_argument('blink-settings=imagesEnabled=false') #이미지 로딩 X
chrome_options.add_argument('headless') #창 띄우지않음
chrome_options.add_argument("disable-gpu")
chrome_options.add_argument("lang=ko_KR")
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument(f"user-agent={pc_header}")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-setuid-sandbodx")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-browser-side-navigation")
prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}  
chrome_options.add_experimental_option('prefs', prefs)

class MyChrome(webdriver.Chrome):
  def quit(self):
    webdriver.Chrome.quit(self)
    self.session_id = None
    
class getcafe():
  def __init__(self) -> None:  
    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    self.driver.implicitly_wait(30) 

  def get_post(self, cafe):
    with open(f"last_post({cafe}).txt", encoding="UTF8") as f:
      last_post = f.read()
    
    if cafe == "atmproject":
      self.driver.get("https://cafe.naver.com/atmproject?iframe_url=/ArticleList.nhn%3Fsearch.clubid=29470508%26search.boardtype=L")
    else:
      self.driver.get("https://cafe.naver.com/akqjatk22?iframe_url=/ArticleList.nhn%3Fsearch.clubid=19903517%26search.boardtype=L")

    time.sleep(3)
    self.driver.switch_to.frame("cafe_main")
    pageString = self.driver.page_source  
    bsObj = BeautifulSoup(pageString, 'html.parser') 
    posts = []
    
    for i in reversed(bsObj.find_all("a",{"class":"article"})):
      if "specialmenutype" in i['href'] or last_post >= i['href'][:i['href'].rfind("&")][i['href'][:i['href'].rfind("&")].rfind("=")+1:] :
        continue
      posts.append({'title':i.text.strip(),'num':i['href'][:i['href'].rfind("&")][i['href'][:i['href'].rfind("&")].rfind("=")+1:]})
      now_post = i['href'][:i['href'].rfind("&")][i['href'][:i['href'].rfind("&")].rfind("=")+1:]
    
    self.driver.quit()
    
    if posts:
      with open(f"last_post({cafe}).txt","w",encoding="UTF8") as f:
        f.writelines(now_post)

    return posts

  def get_kin(self, cafe):
    with open(f"last_kins({cafe}).txt", encoding="UTF8") as f:
      file = f.read()
      last_kins = file.splitlines()
      
    # self.driver.get("https://cafe.naver.com/atmproject?iframe_url=/KinActivityAnsweredQuestionList.nhn%3Fsearch.clubid=29470508") #주식스터디카페 카페답변
    self.driver.get("https://cafe.naver.com/akqjatk22?iframe_url=/KinActivityAnsweredQuestionList.nhn%3Fsearch.clubid=19903517") #재테크카페 카페답변
      
    self.driver.switch_to.frame("cafe_main")
    pageString = self.driver.page_source  
    bsObj = BeautifulSoup(pageString, 'html.parser') 
    kins = []
    now_kins = []
    
    for i in reversed(bsObj.find_all("a",{"class":"article"})):
      if i['href'] not in last_kins:
        kins.append({'title':i.text.strip(),'url':i['href']})
      now_kins.append(i['href'])
    
    self.driver.quit()
      
    if kins:
      with open(f"last_kins({cafe}).txt","w",encoding="UTF8") as f:
        for i in now_kins:
          f.writelines(i+"\n")
        
    return kins