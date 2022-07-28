from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Invention, UserInvention


# Create your views here.

def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def inventions(request):
    inventions = Invention.objects.all()
    if request.user.is_authenticated:

        try:
            items = UserInvention.objects.filter(user = request.user)
        except:
            pass
        else:
            item_ids = []

            for i in items:
                item_ids.append(i.product_id)

            return render(request, 'inventions.html', {'inventions':inventions, "items":item_ids})

    return render(request, 'inventions.html', {'inventions':inventions})


def verify(request, id):
    if request.user.is_authenticated:
        user = request.user
        try:
            item = Invention.objects.get(id = id)
        except:
            #404
            return redirect('/')

        else:
            try:
                check = user.userinvention_set.get(product_id = id)

            except:
                #user does not own the item, hence we get an error
                UserInvention.objects.create(product_id = id, user = user)
                # print(user.userinvention_set.count())

                return render(request,'success.html', {"item":item})

            else:
                #user already owns item
                return redirect('/')
    else:
        return redirect('/accounts/login')

def remove(request, id):
    if request.user.is_authenticated:
        user = request.user
        try:
            item = Invention.objects.get(id = id)
        except:
            #404
            return redirect('/')

        else:
            try:
                check = user.userinvention_set.get(product_id = id)
                print(check)
            except:
                #user does not own the item, hence we get an error
                return redirect('/')

            else:
                #user already owns item
                check.delete()
                return redirect('account')
    else:
        return redirect('/accounts/login')


def account(request):
    if request.user.is_authenticated:
        inventions = Invention.objects.all()
        username = request.user.username
        purchases = request.user.userinvention_set.all()
        none = False
        user_purchases = []

        for i in purchases:
            item = Invention.objects.get(id = i.product_id)
            user_purchases.append(item)

        if user_purchases == []:
            none = True

        return render(request, 'account.html', {"username":username, "purchases": user_purchases, "none": none})

    else:
        #CUSTOM ERROR PAGE
        return redirect('/accounts/login')

def login(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid credentials.", extra_tags="login")
            return redirect('/accounts/login')

    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def change_pass(request):
    if request.method == "POST":
        p1 = request.POST['password1']
        p2 = request.POST['password2']

        user= request.user

        n_user = auth.authenticate(username=request.user.username, password=p1)

        if n_user is not None:
            user.set_password(p2)
            user.save()

            auth.login(request, user)
            return redirect('/account')

        else:
            messages.info(request, "Invalid 'Old Password'.", extra_tags="change_pass")
            return redirect('/account/change-password')
    else:
        return render(request, 'pass.html')


def edit(request):
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            n_user = User.objects.get(username = username)
            if n_user.id == request.user.id:
                pass

            else:
                messages.info(request, "Username already exists, pick a new one.", extra_tags = "username")
                return redirect("/account/edit")

        elif User.objects.filter(email = email).exists():
            n_user = User.objects.get(email= email)
            if n_user.id == request.user.id:
                pass

            else:
                messages.success(request, "This email already exists, try another one.", extra_tags = "email")
                return redirect("/account/edit")

        else:
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()
            return redirect('/account')

    else:
        return render(request, 'edit.html')

def register(request):
    if request.method == "POST":

        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']


        if password == password2:

            if User.objects.filter(username=username).exists():

                messages.info(request, "Username already exists, pick a new one.", extra_tags = "username")
                return redirect("/accounts/register")

            elif User.objects.filter(email = email).exists():

                messages.success(request, "This email already exists, try another one.", extra_tags = "email")
                return redirect("/accounts/register")

            else:
                user = User.objects.create_user(email=email, username= username, password= password, last_name= last_name, first_name=first_name)
                user.save()
                auth.login(request, user)
                return redirect('/')

        else:
            messages.warning(request, "These passwords do not match", extra_tags = "password")
            return redirect("/accounts/register")

    else:
        return render(request, 'register.html')
