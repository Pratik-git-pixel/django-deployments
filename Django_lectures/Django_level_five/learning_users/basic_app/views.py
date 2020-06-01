from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm


from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request ,'basic_app/index.html')



# decorators and you wanna return something special
@login_required
def special(request):
    return HttpResponse("YOU ARE LOGGED IT , NICE!!")



# we cannot put only logout as we have imported it so userlogout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))




def register(request):
# intially keep regitered false
    registered = False
# check if there is any data inputted , if it is present then put that in user form and profile form
    if request.method =='POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
# check if the data is valid if it is the save to database using save()

        if user_form.is_valid() and profile_form.is_valid():

# saving user form data / set_password will hash the password
            user = user_form.save()
            user.set_password(user.password)
            user.save()
# double checking by using commit = false/ here profile_pic is present in html file and the is link to user built in
            profile = profile_form.save(commit=False)
            profile.user = user
                # for pdf or any kind of file use request.FILES it is a way to check that
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
# saving it to database
            profile.save()
# changing to registered-True
            registered = True

            # if the data is not valid they will seee an error
        else:
            print(user_form.errors,profile_form.errors)
# if the request method is not equal to post  then just set the form

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'basic_app/registration.html',
                    {'user_form':user_form,
                    'profile_form':profile_form,
                    'registered':registered})

def user_login(request):

        if request.method == 'POST':
            # getting the username and password that the user has given
            # here name=username in the .html file where name is present in input
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Django built-in authentication function

            user = authenticate(username=username,password=password)

    # built-in is_active function
            if user:
                if user.is_active:
                    # if it is active then we can let the user login by passing the request and the user
                    login(request,user)
    #  send the user to some page once they are login
                    return HttpResponseRedirect(reverse('index'))
    # diverting the user to some page once the login is sucessful
                else:
                    return HttpResponse("Account NOT ACTIVE")
                    # printing something in the console for the developer
            else:
                print("Someone tried to LOGIN and failed")
                print("Username: {} and password:{}".format(username,password))
                return HttpResponse("INVALID LOGIN DETAILS")
                # if the request is not POST the do following
        else:
            return render(request,'basic_app/login.html',{})
