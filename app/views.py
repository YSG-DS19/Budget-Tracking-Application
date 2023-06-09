from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth  import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *

@login_required(login_url='login')
def IncomePage(request):
    profile = Profile.objects.filter(user= request.user).first()
    expenses = Expense.objects.filter(user = request.user)
    if request.method == 'POST':
        if profile in Profile.objects.filter(user=request.user):
            pass
        else:
            income =request.POST.get('income')
            balance  = request.POST.get('balance')
            profile = Profile(user=request.user,income=income,balance=balance)
            profile.save()
            messages.success(request,'Income added Successfully!')
            return redirect("home")
    context = {'profile': profile,'expenses':expenses}
    return render(request,"income.html",context)




@login_required(login_url='login')
def HomePage(request):
    profile = Profile.objects.filter(user= request.user).first()
    expenses = Expense.objects.filter(user = request.user)
    if request.method == 'POST':
        text = request.POST.get('text')
        amount = request.POST.get('amount')
        amount_type = request.POST.get('amount_type')
        expense = Expense(name=text,amount=amount,expense_type=amount_type,user=request.user) 
        expense = Expense(user=request.user,name=text,amount=amount,)
        expense.save()

        if amount_type=='Positive':
            profile.balance+= float(amount)
            profile.income+=float(amount)
        else:
            profile.expenses += float(amount)
            profile.balance -= float(amount)

        profile.save()
    
    context = {'profile': profile,'expenses':expenses}
    return render(request,"home.html",context)



def SignupPage(request):
    if request.method == "POST":
        username= request.POST.get("username")
        email   = request.POST.get("email")
        pass1   = request.POST.get("password1")
        pass2   = request.POST.get("password2")

        if pass1 != pass2:
            return HttpResponse("Confirm Password is Wrong!!!")
        
        my_user = User.objects.create_user(username,email,pass1)
        my_user.save()
        return redirect("login")
    return render(request,"signup.html")

def LoginPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request,username= uname,password=pass1)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            return HttpResponse("Username or Password is incorrect!!!")
    return render(request,"login.html")

def LogoutPage(request):
    logout(request)
    return redirect('login')
