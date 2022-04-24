from binascii import rledecode_hqx
from curses.panel import top_panel
import imp
from re import I
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages

from matplotlib.style import context
from pkg_resources import register_finder
from .forms import OfferForm, UserForm

from django.contrib.auth.decorators import login_required
from django.db.models import Q 

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm

from .models import Message, Offer, Topic

from django.contrib.auth.models import User
#offers=[
 #  {'id':2, 'name': 'Trending offers'},
   # {'id':3, 'name': 'Amazing deals'},
#]
def loginPage(request):
    page= 'login'

    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username= request.POST.get('username').lower()
        password= request.POST.get('password')

        try:
            user= User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user= authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username Or Password does not exist')


    context={'page':page}
    return render(request, 'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form= UserCreationForm()

    if request.method=='POST':
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registeration')



    return render(request, 'base/login_register.html',{'form':form})

def home(request):
    q= request.GET.get('q') if request.GET.get('q')!=None else ''
    offers= Offer.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )
    
    topics= Topic.objects.all()[0:5]
    offer_count = offers.count()
    offer_messages= Message.objects.filter(Q(offer__topic__name__icontains=q))

    context={'offers': offers, 'topics':topics, 'offer_count':offer_count, 'offer_messages': offer_messages}
    return render(request, 'base/home.html',context)

def offer(request,pk):
          offer= Offer.objects.get(id=pk)
          offer_messages = offer.message_set.all()
          participants = offer.participants.all()

          
          
          if request.method == 'POST':
              message= Message.objects.create(
                  user= request.user,
                  offer= offer,
                  body= request.POST.get('body')
              )
              offer.participants.add(request.user)
              return redirect('offer', pk= offer.id )
          
          context={'offer':offer, 'offer_messages': offer_messages, 
                    'participants':participants}
          return render(request, 'base/offer.html',context)

def userProfile(request, pk):
    user= User.objects.get(id=pk)
    offers=user.offer_set.all()
    offer_messages= user.message_set.all()
    topics= Topic.objects.all()

    context= {'user': user,'offers': offers, 
    'offer_messages':offer_messages,'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='/login')
def createOffer(request):
    form= OfferForm()
    topics= Topic.objects.all()
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created= Topic.objects.get_or_create(name=topic_name)
        Offer.objects.create(
            host= request.user,
            topic= topic,
            name= request.POST.get('name'),
            description= request.POST.get('name'),
        )
        return redirect('home')
    context={'form':form,'topics':topics}
    return render(request, 'base/offer_form.html',context)

@login_required(login_url='/login')
def updateOffer(request,pk):
    offer= Offer.objects.get(id=pk)
    form= OfferForm(instance=offer)
    topics= Topic.objects.all()
    if request.user != offer.host:
        return HttpResponse('Your are not allowed here')
    
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created= Topic.objects.get_or_create(name=topic_name)
        form= OfferForm(request.POST, instance=offer)
        offer.name= request.POST.get('name')
        offer.topic= topic
        offer.description= request.POST.get('description')
        offer.save()
        return redirect('home')
    context={'form': form,'topics':topics, 'offer':offer}
    return render(request ,'base/offer_form.html', context)

@login_required(login_url='/login')
def deleteOffer(request, pk):
    offer= Offer.objects.get(id=pk)

    if request.user != offer.host:
        return HttpResponse('Your are not allowed here')
   

    if request.method=='POST':
        offer.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':offer})


def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here')

    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})



@login_required(login_url='/login')
def updateUser(request):
    user= request.user
    form= UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context={'form':form}
    return render(request, 'base/update-user.html', context)

def topicsPage(request):
    q= request.GET.get('q') if request.GET.get('q')!=None else ''
 
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html',{'topics':topics})
def activityPage(request):
    offer_messages= Message.objects.all()
    return render(request, 'base/activity.html',{'offer_messages':offer_messages})