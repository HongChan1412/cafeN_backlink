from cafe_crawl import getcafe 
import wp_post
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError

def job(cafe):
  try:
    for i in cafe:
      print(i, "게시글 크롤링 시작")
      posts = getcafe().get_post(i)
      print(i, "게시글 크롤링 완료")
      if posts:
        print(i, "새 게시글 존재")
        for j in posts:
          if wp_post.wpcafePost(j, i):
            print(j['title'],"성공")
          else:
            print(j['title'],"실패")
        print(i, "새 게시글 업로드 완료")
      else:
        print(i, "새 게시글 없음")
      if i == "akqjatk22":
        print(i, "카페답변 크롤링 시작")
        kins = getcafe().get_kin(i)  
        print(i, "카페답변 크롤링 완료")
        if kins:
          print(i, "새 카페답변 존재")
          for j in kins:
            if wp_post.wpkinPost(j):
              print(j['title'],"성공")
            else:
              print(j['title'],"실패")
          print(i, "새 카페답변 업로드 완료")
        else:
          print(i, "새 카페답변 없음")
    return 
  except  Exception as e:
    print(e)
    return 
  
def main():
  try:
    print("""
  ___              _  _     _____  _               _        
  |_  |            (_)| |   /  ___|| |             | |       
    | | _   _  ___  _ | | __\ `--. | |_  _   _   __| | _   _ 
    | || | | |/ __|| || |/ / `--. \| __|| | | | / _` || | | |
/\__/ /| |_| |\__ \| ||   < /\__/ /| |_ | |_| || (_| || |_| |
\____/  \__,_||___/|_||_|\_\\____/  \__| \__,_| \__,_| \__, |
                                                        __/ |
                                                      |___/       
""")
    # cafe = input("카페이름을 입력해주세요 ex) atmproject, akqjatk22 : ")
    sched = BackgroundScheduler(timezone='Asia/Seoul')
    sched.start()
    try:
      sched.add_job(job, 'interval', minutes=5, id="cafeBacklink", args=[["atmproject","akqjatk22"]], misfire_grace_time=600)
    except:
      try:
        print("기존 Job 제거 후 새로 추가") 
        sched.remove_all_jobs()
        sched.add_job(job, 'interval', minutes=5, id="cafeBacklink", args=[["atmproject","akqjatk22"]], misfire_grace_time=600)
      except JobLookupError as e:
        print("Scheduler 오류 발생", e)
        return
    while True:
      try:
        print("Running main process............","| [time] ", str(time.localtime().tm_hour)+":"+str(time.localtime().tm_min)+":"+str(time.localtime().tm_sec))
        time.sleep(600)  
      except KeyboardInterrupt:
        import sys
        print("Ctrl + C 중지, Job 제거 후 프로그램 종료")
        sched.remove_all_jobs()
        sys.exit()
  except KeyboardInterrupt:
    print("Ctrl + C 중지")
    
if __name__ == "__main__":
  main()