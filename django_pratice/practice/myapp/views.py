from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import random
# Create your views here.
topics=[{'id':1,'title':'routing','body':'Routing is..'}
 ,{'id':2,'title':'routing2','body':'view is..'}]

def htmlTemplate(article_tag):
    global topics
    ol=''
    for i in topics:
        ol+=f'<li><a href="/read/{i["id"]}">{i["title"]}</a></li>'
    return f'''
    <html>
    <body>
        <h1>Django</h1>
        <ol>
            {ol}
        </ol>
        {article_tag}
        <ul>
            <li><a href="/create/">create</a></li>
        </ul>
    </body>
    </html>
'''
def index(request):
    article= '''
    <h2>hellow</h2>
    Welcome
    '''
    return HttpResponse(htmlTemplate(article))

@csrf_exempt
def create(request):
    article='''
        <form action="/create/" method="post">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p> 
            <p><input type="submit"></p>
        </form>
    '''#여러줄의 텍스트를 입력하기 위함

    return HttpResponse(htmlTemplate(article))
def read(request,id):
    global topics
    article=''
    for i in topics:
        if i["id"]==int(id):
            article=f'<h2>{i["title"]}</h2>{i["body"]}'
    return HttpResponse(htmlTemplate(article))