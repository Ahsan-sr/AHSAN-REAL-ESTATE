from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from contacts.models import Contact

def register(request):
    if request.method == 'POST':
       #getting form values
       first_name = request.POST['first_name']
       last_name = request.POST['last_name']
       username = request.POST['username']
       email = request.POST['email']
       password = request.POST['password']
       password2 = request.POST['password2']

       #check if passwords match
       if password == password2:
           #checking username exists by bringing user model which is created by default
           if User.objects.filter(username=username).exists():
             messages.error(request,'USERNAME IS TAKEN')  
             return redirect('register')
           else:
                if User.objects.filter(email=email).exists():
                   messages.error(request,'EMAIL ALREADY IN USE')  
                   return redirect('register')
                else:
                    #everything is ok
                    user = User.objects.create_user(username=username, password=password, email=email,
                    first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request,'SUCCESSFULLY REGISTRED NOW LOGIN')
                    return redirect('login')
       else:
           messages.error(request,'Passwords do not match')
           return redirect('register')    
    else :
       return render(request, 'accounts/register.html')




def login(request):
    if request.method == 'POST':
        #LOGIN USER
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'YOU ARE NOW LOGGED IN')
            return redirect('dashboard')
        else:
            messages.error(request,'INVALID CREDENTIALS')
            return redirect('login')
    else :
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'YOU ARE LOGGED OUT')
        return redirect( 'index' )

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {  'contacts' : user_contacts }
    return render(request, 'accounts/dashboard.html',context)