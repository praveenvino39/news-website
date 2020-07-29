from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .models import SavedNew
from django.http import HttpResponse
# Create your views here.

def homepage(request):
    weatherdata = requests.get('http://api.openweathermap.org/data/2.5/weather?q=chennai&appid=98025f7a1edae67852b8b2a15b858486')
    weatherdata = json.loads(weatherdata.text)
    weatherdata = weatherdata['main']
    response = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=4c0a0778eb4b4e1aa06fa178a050c62f')
    response = json.loads(response.text)
    response = response['articles']
    high = int(weatherdata['temp_min'])
    low = int(weatherdata['temp_max'])
    high = high-273
    low = low-273
    articles = []
    id = 0
    for article in response:
        article.update({'id': id})
        articles.append(article)
        id = id + 1
    return render(request, 'homepage/homepage.html', {'content': response, 'high': high, 'low': low, 'meta_title': 'Snack Time News - Homepage', 'search_term':'homepage'})

def detail(request, news_id, search_term):
    weatherdata = requests.get('http://api.openweathermap.org/data/2.5/weather?q=chennai&appid=98025f7a1edae67852b8b2a15b858486')
    weatherdata = json.loads(weatherdata.text)
    weatherdata = weatherdata['main']
    response = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=4c0a0778eb4b4e1aa06fa178a050c62f')
    response = json.loads(response.text)
    response = response['articles']
    high = int(weatherdata['temp_min'])
    low = int(weatherdata['temp_max'])
    high = high - 273
    low = low - 273
    articles = []
    id = 0
    for article in response:
        article.update({'id': id})
        articles.append(article)
        id = id + 1
    selected_news = None
    for article in articles:
        if article['id'] == news_id:
            selected_news = article
    return render(request, 'homepage/detail.html', {'selected_news': selected_news, 'meta_title': selected_news['title'],'id': news_id,'high':high, 'low': low,'search_term':'default'})

def signup_user(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 == password2:
                try:
                    new_user = User.objects.create_user(username=username, password=password1)
                    new_user.save()
                    messages.success(request, 'Your Account created successfully, Now you can Login')
                    return redirect('homepage')
                except IntegrityError:
                    messages.error(request, 'Username already taken, Try different!')
                    return redirect('signup')
            else:
                messages.error(request, 'Password not match, please try again.', extra_tags='danger')
                return redirect('signup')
        return render(request, 'homepage/signup.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Hello, Now you\'ve logged in.', extra_tags='success')
                return redirect('homepage')
            else:
                messages.error(request, 'User not found!', extra_tags='danger')
                return redirect('login')
        return render(request, 'homepage/login.html', {'meta_title': 'Snack Time News - Login'})

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
    else:
        return redirect('homepage')
@login_required()
def saved_news(request, news_id,search_term):
    response = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=4c0a0778eb4b4e1aa06fa178a050c62f')
    response = json.loads(response.text)
    response = response['articles']
    articles = []
    id = 0
    for article in response:
        article.update({'id': id})
        articles.append(article)
        id = id + 1
    selected_news = None
    for article in articles:
        if article['id'] == news_id:
            selected_news = article
    users=request.user.username
    print(type(selected_news['content']))
    if selected_news['content'] is None:
        new_save = SavedNew(user=users, title=selected_news['title'], description=selected_news['description'],
                            urlToImage=selected_news['urlToImage'],
                            url=selected_news['url'], date=selected_news['publishedAt'],
                            source=selected_news['source']['name'])
        new_save.save()
        messages.success(request, 'News added to saved!', extra_tags='success')
        return redirect('homepage')
    else:
        new_save = SavedNew(user=users, title=selected_news['title'],content=selected_news['content'], description = selected_news['description'], urlToImage=selected_news['urlToImage'], url=selected_news['url'], date=selected_news['publishedAt'], source=selected_news['source']['name'])
        new_save.save()
        messages.success(request, 'News added to saved!', extra_tags='success')
        return redirect('homepage')
@login_required()
def saved_list(request):
    contents = SavedNew.objects.filter(user=request.user.username)
    return render(request, 'homepage/saved_list.html',{'content': contents,'meta_title': 'Snack Time News - Your Picks'})

@login_required()
def saved_detail(request, id):
    selected_news = get_object_or_404(SavedNew, pk=id)
    if selected_news.user == request.user.username:
        return render(request, 'homepage/saved_detail.html',{'selected_news': selected_news,'meta_title': selected_news.title})
    else:
        return redirect('homepage')

def delete(request, id):
    news = get_object_or_404(SavedNew, pk=id)
    news.delete()
    return redirect('saved_list')

def search(request):
    weatherdata = requests.get('http://api.openweathermap.org/data/2.5/weather?q=chennai&appid=98025f7a1edae67852b8b2a15b858486')
    weatherdata = json.loads(weatherdata.text)
    weatherdata = weatherdata['main']
    search_term = request.POST['search']
    url = 'https://newsapi.org/v2/everything?q={}&apiKey=4c0a0778eb4b4e1aa06fa178a050c62f'.format(search_term)
    response = requests.get(url)
    response = json.loads(response.text)
    response = response['articles']
    high = int(weatherdata['temp_min'])
    low = int(weatherdata['temp_max'])
    high = high - 273
    low = low - 273
    articles = []
    id = 0
    for article in response:
        article.update({'id': id})
        articles.append(article)
        id = id + 1
    return render(request, 'homepage/search.html',
                  {'content': response, 'high': high, 'low': low,'search_term': request.POST["search"],'search_term': search_term, 'meta_title': 'Snack Time News - {}'.format(search_term)})

def search_detail(request, news_id,search_term):
    print(search_term)
    weatherdata = requests.get('http://api.openweathermap.org/data/2.5/weather?q=chennai&appid=98025f7a1edae67852b8b2a15b858486')
    weatherdata = json.loads(weatherdata.text)
    weatherdata = weatherdata['main']
    url = 'https://newsapi.org/v2/everything?q={}&apiKey=4c0a0778eb4b4e1aa06fa178a050c62f'.format(search_term)
    response = requests.get(url)
    response = json.loads(response.text)
    response = response['articles']
    high = int(weatherdata['temp_min'])
    low = int(weatherdata['temp_max'])
    high = high - 273
    low = low - 273
    articles = []
    id = 0
    for article in response:
        article.update({'id': id})
        articles.append(article)
        id = id + 1
    selected_news = None
    for article in articles:
        if article['id'] == news_id:
            selected_news = article
    return render(request, 'homepage/detail.html', {'selected_news': selected_news, 'meta_title': selected_news['title'],'id': news_id,'high':high, 'low': low,'search_term':search_term})

@login_required()
def saved_news_search(request, news_id, search_term):
    url= 'https://newsapi.org/v2/everything?q={}&apiKey=4c0a0778eb4b4e1aa06fa178a050c62f'.format(search_term)
    response = requests.get(url)
    response = json.loads(response.text)
    response = response['articles']
    articles = []
    id = 0
    for article in response:
        article.update({'id': id})
        articles.append(article)
        id = id + 1
    selected_news = None
    for article in articles:
        if article['id'] == news_id:
            selected_news = article
    users=request.user.username
    print(type(selected_news['content']))
    if selected_news['content'] is None:
        new_save = SavedNew(user=users, title=selected_news['title'], description=selected_news['description'],
                            urlToImage=selected_news['urlToImage'],
                            url=selected_news['url'], date=selected_news['publishedAt'],
                            source=selected_news['source']['name'])
        new_save.save()
        messages.success(request, 'News added to saved!', extra_tags='success')
        return redirect('homepage')
    else:
        new_save = SavedNew(user=users, title=selected_news['title'],content=selected_news['content'], description = selected_news['description'], urlToImage=selected_news['urlToImage'], url=selected_news['url'], date=selected_news['publishedAt'], source=selected_news['source']['name'])
        new_save.save()
        messages.success(request, 'News added to saved!', extra_tags='success')
        return redirect('homepage')