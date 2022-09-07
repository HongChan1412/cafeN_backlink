from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods import posts

def wpcafePost(post_info, cafe):
  try:
    client = Client('https://moneyseo.cafe24.com/xmlrpc.php', 'admin', 'dnfl12qw!@')
    
    postTitle = post_info['title']
    content = ""
    content += f"<a href='https://cafe.naver.com/{cafe}/{post_info['num']}' target='_blank' rel='noopener'>{postTitle} 게시글 바로가기</a>"
    content += f"<iframe title='Naver cafe post' src = 'https://cafe.naver.com/{cafe}/{post_info['num']}' width='1200' height='2000' frameborder='1' allowfullscreen='allowfullscreen'></iframe>"
    post = WordPressPost()
    post.title = postTitle ## 제목
    post.content = content ## 컨텐츠 내용
    post.terms_names = {
        'post_tag': ['주식스터디', '금융정보', ' 증권정보', '주식추천', '급등주', '주식', '증권', '테마주', '주식종목', '종목추천', '카카오주식', '삼성전자주식', '추천종목', '종목추천', '주식무료사이트', '대박주', '주식투자방법', '주식고수', '주식단타', '주식하는법', '주식사는법', '주식공부', '저평가우량주', '주식빅데이터', '주식정보'], ##게시글 태그
        'category': ['post'] ## 카테고리
    }
    post.comment_status = 'open'
    post.post_status = 'publish' ##임시저장은 draft

    client.call(posts.NewPost(post))
    
    return True
  except Exception as e:
    print(e)
    return False
  
def wpkinPost(post_info):
  try:
    client = Client('https://moneyseo.cafe24.com/xmlrpc.php', 'admin', 'dnfl12qw!@')
    
    postTitle = post_info['title']
    postUrl = post_info['url'].replace("http","https")
    content = ""
    content += f"<a href='{postUrl}' target='_blank' rel='noopener'>{postTitle} 답변 바로가기</a>"
    content += f"<iframe title='Naver kin post' src = '{postUrl}' width='1200' height='2000' frameborder='1' allowfullscreen='allowfullscreen'></iframe>"
    post = WordPressPost()
    post.title = postTitle ## 제목
    post.content = content ## 컨텐츠 내용
    post.terms_names = {
        'post_tag': ['주식스터디', '금융정보', ' 증권정보', '주식추천', '급등주', '주식', '증권', '테마주', '주식종목', '종목추천', '카카오주식', '삼성전자주식', '추천종목', '종목추천', '주식무료사이트', '대박주', '주식투자방법', '주식고수', '주식단타', '주식하는법', '주식사는법', '주식공부', '저평가우량주', '주식빅데이터', '주식정보'], ##게시글 태그
        'category': ['kin'] ## 카테고리
    }
    post.comment_status = 'open'
    post.post_status = 'publish' ##임시저장은 draft

    client.call(posts.NewPost(post))
    
    return True
  except Exception as e:
    print(e)
    return False