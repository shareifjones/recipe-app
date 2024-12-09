#Django authentication libraries           
from django.contrib.auth import authenticate, login, logout
#Django Form for authentication
from django.contrib.auth.forms import AuthenticationForm 

from django.shortcuts import render, redirect  


#define a function view called login_view that takes a request from user
def login_view(request):
   #initialize:
   #error_message to None                                 
    error_message = None   
   #form object with username and password fields                             
    form = AuthenticationForm() 

   #when user hits "login" button, then POST request is generated
    if request.method == 'POST':
        #read the data sent by the form via POST request 
        form = AuthenticationForm(data=request.POST)

#check if form is valid
        if form.is_valid():
            #read username
            username = form.cleaned_data.get('username')
            #read password
            password = form.cleaned_data.get('password')

#use Django authenticate function to validate the user
            user=authenticate(username=username, password=password)
            if user is not None:
#if user is authenticated then use pre-defined Django function to login
                login(request, user)
                #& send the user to desired page
                return redirect('recipes:recipes_list')
            else:
                error_message = "Oops... Something went wrong"

    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'auth/login.html', context)

def success_view(request):
    #the use pre-defined Django function to logout
    logout(request)
    #after logging out go to login form (or whichever page you want)
    return render(request, 'auth/success.html')


