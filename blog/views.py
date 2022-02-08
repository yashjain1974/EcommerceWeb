from django.shortcuts import render
from django.http import HttpResponse
from.models import Blogpost
# Create your views here.

def index(request):
    allposts=Blogpost.objects.all()


    return render(request,'blog/index.html',{'myposts':allposts})

    # return HttpResponse("Hello Here is Blog website")
def blogpost(request,id):
    post=Blogpost.objects.filter(post_id=id)[0]
    print(post)
    return render(request,'blog/blogpost.html',{'post':post})

    # return HttpResponse("Hello Here is Blog website")

