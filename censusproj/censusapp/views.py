from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, AdultForm, ChildrenForm, AdminUserForm
from .models import Indigene, Adult, Child

from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

error = None
def check_user():
    users = User.objects.all()
    if len(users) == 0:
        users_exit = False
    else:
        users_exit = True
    return users_exit
# Create your views here.


class IndigeneUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    template_name = 'temp/indigene_update.html'
    form_class = NewUserForm
    model = Indigene

class IndigeneDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'temp/indigene_confirm_delete.html'
    model = Indigene
    success_url = reverse_lazy('censusapp:all_indigene')


def about(request):
    users_exit = check_user()
    return render(request, 'temp/about.html', {'users_exist': users_exit})

@login_required
def all_indigene(request):
    users_exit = check_user()
    indigenes = Indigene.objects.all()
    return render(request, 'temp/all.html', {'indigenes': indigenes, 'users_exist': users_exit})

def index(request):
    users_exit = check_user()
    return render(request, 'temp/index.html', {'users_exist': users_exit})


@login_required
def birth(request):
    users_exit = check_user()
    if request.method == 'POST':
        year = request.POST.get('year')
        indigenes = Indigene.objects.all()
        if indigenes:
            birth_years = [indigene for indigene in indigenes if int(indigene.date_of_Birth.year) == int(request.POST.get('year')) ]
            return render(request, 'temp/birth-query.html', {'birth_years':birth_years, 'total': len(indigenes), 'year': year, 'users_exist': users_exit}) 
        else:
            error = True
            return render(request, 'temp/birth.html', {'error':error}) 
    else:
        
        return render(request, 'temp/birth.html') 

@login_required
def create(request):
    users_exit = check_user()
    if request.method == 'POST':
        
        new_indigeneform = NewUserForm(data=request.POST)
        if new_indigeneform.is_valid():
            
            age = new_indigeneform.cleaned_data['age']
            new_indigeneform.save(commit=True)
            indigene = Indigene.objects.get(full_Name=new_indigeneform.cleaned_data['full_Name'])
            
            if age < 18:
                return redirect('censusapp:new_child', pk=indigene.pk)
            else:
                return redirect('censusapp:new_adult', pk=indigene.pk)
        else:
            global error
            error = new_indigeneform.errors
            return redirect('censusapp:create')
        

    else:
        
        form = NewUserForm()
        return render(request, 'temp/create.html', {'form': form, 'error': error, 'users_exist': users_exit})
    

@login_required
def create_adult(request, pk):
    users_exit = check_user()
    indigene = get_object_or_404(Indigene, pk=pk)
    if request.method == 'POST':
        adult_form = AdultForm(data=request.POST)
        if adult_form.is_valid():
            adult_form.save(commit=True)
            return render(request, 'temp/index.html', {'registered': True, 'users_exist': users_exit})

    else:
        adult_form = AdultForm()
        return render(request, 'temp/child.html', {'form': adult_form, 'indigene': indigene, 'users_exist': users_exit})


@login_required
def create_child(request, pk):
    users_exit = check_user()
    indigene = get_object_or_404(Indigene, pk=pk)
    
    if request.method == 'POST':
        child_form = ChildrenForm(data=request.POST)
        if child_form.is_valid():
            child_form.save(commit=True)
            return render(request, 'temp/index.html', {'registered': True, 'users_exist': users_exit})
            
    else:
        child_form = ChildrenForm()
        return render(request, 'temp/child.html', {'form': child_form, 'indigene': indigene, 'users_exist': users_exit})


@login_required
def get_query(request, query):
    users_exit = check_user()
    if query == 'tax':
        taxable_adults = Adult.objects.filter(employment_status=True).all()
        return render(request, 'temp/query.html', {'taxable_adults': taxable_adults, 'query': query, 'total': len(taxable_adults), 'users_exist': users_exit})
    elif query == 'death':
        dead_indigenes = Indigene.objects.filter(alive=False).all()
        return render(request, 'temp/query.html', {'dead_indigenes': dead_indigenes, 'query': query, 'total': len(dead_indigenes), 'users_exist': users_exit})
    else:
        primary_students = Child.objects.filter(primary_education=True).all()
        return render(request, 'temp/query.html', {'primary_students': primary_students, 'query': query, 'total': len(primary_students), 'users_exist': users_exit})


def register(request):
    users_exit = check_user()
    if request.method == 'POST':
        user_form = AdminUserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            return render(request, 'temp/index.html', {'admin_registered': True, 'users_exist': users_exit})

    else:
        user_form = AdminUserForm()
        return render(request, 'temp/registration.html', {'form': user_form, 'users_exist': users_exit})

def user_login(request):
    users_exit = check_user()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        print(user)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('censusapp:home'))
            else:
                return HttpResponse('Account Not Active')
        else:
            return HttpResponse('Invalid Login Details Supplied')
    else:
        return render(request, 'temp/login.html', {'users_exist': users_exit})
    

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('censusapp:user_login'))


    
