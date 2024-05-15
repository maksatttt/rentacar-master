import sys

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMultiAlternatives
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.utils import timezone
from rest_framework.authtoken.models import Token

from .forms import RegisterForm
from .models import Cars, Orders


# Create your views here.

@login_required(login_url='/login')
def index(request):
    """ Главная страница """
    car_list = Cars.objects.all().order_by('born_year')
    rented = Orders.objects.filter(active=True)
    rent_cars = []
    for y in rented:
        rent_cars.append(y.rented_car_id)
    for x in car_list:
        if x.id in rent_cars:
            x.rent = True
        else:
            x.rent = False
    lists = {'Car_list': car_list}
    return render(request, 'index.html', lists)


@login_required(login_url='/login')
def add_car(request):
    """ Добавление новых машин """
    if 'add_car' in request.POST:
        name_car = request.POST.get('name_car')
        year_born = request.POST.get('year_born')
        foto_car = request.FILES.get('foto')
        fs = FileSystemStorage()
        fs.save('foto/' + str(foto_car.name), foto_car)
        p1 = Cars(name_car_en=str(name_car), born_year=int(year_born), foto='foto/' + str(foto_car.name))
        p1.save()
        return HttpResponseRedirect('/')
    lists = {"form": ''}
    return render(request, 'add_car.html', lists)


@login_required(login_url='/login')
def rent_car(request, article):
    try:
        article = int(article)
    except ValueError:
        print(sys.exc_info())
        raise Http404()
    car_items = Cars.objects.get(id=article)
    lists = {'Car_item': car_items}
    u_sername = None
    if request.user.is_authenticated:
        u_sername = request.user
    if 'add_rent' in request.POST:
        p1 = Orders(date_begin=timezone.now(), renter_id=u_sername.id, rented_car_id=article)
        p1.save()
        # Отправка письма после сохранения
        plaintext = get_template('order_mail.txt')
        htmly = get_template('order_mail.html')
        d = {'list_cart': car_items}
        subject = 'Аренда автомобиля #' + str(car_items.name_car_en)
        from_email = 'rent@brainsite.ru'
        to2 = 'rent@brainsite.ru'
        to = u_sername.email
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        for adress in [to, to2]:
            msg = EmailMultiAlternatives(subject, text_content, from_email, [adress, ])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        return render(request, 'index.html', lists)
    return render(request, 'add_rent.html', lists)


@login_required(login_url='/login')
def my_account(request):
    """ Мой кабинет """
    u_sername = None
    tokens = None
    if request.user.is_authenticated:
        u_sername = request.user
    try:
        tokens = Token.objects.get(user=u_sername.id)
    except:
        tokens = Token.objects.create(user=u_sername)
    if 'ch-pass' in request.POST:
        # Смена пароля
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Ваш пароль изменён')
            return redirect('my_account')
        else:
            messages.error(request, 'Ошибки в пароле')
    if 'save' in request.POST:
        # Сохранение другой информации
        form = RegisterForm(request.POST)
        print(form)
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        u_sername.last_name = last_name
        u_sername.first_name = first_name
        u_sername.save()
    form = PasswordChangeForm(request.user)
    print(form)
    lists = {'formm': tokens, 'rorm': form}
    return render(request, 'my_account.html', lists)


def login(request):
    if 'login' in request.POST:
        # c.update(csrf(request))
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Правильный пароль и пользователь "активен"
            auth.login(request, user)
            # Перенаправление на "правильную" страницу
            return HttpResponseRedirect("/")
        else:
            # Отображение страницы с ошибкой
            return HttpResponseRedirect("/account/invalid/")
    if 'register' in request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            auth_login(request, user)
            return redirect('/')
    return render(request, 'login.html', {'formm': ''})
