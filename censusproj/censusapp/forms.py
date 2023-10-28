from django import forms
from django.contrib.auth.models import User
from .models import Adult, Child, Indigene, AdminUser


class AdminUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class NewUserForm(forms.ModelForm):
    class Meta:
        model = Indigene
        fields = '__all__'

        widgets = {
            'full_Name': forms.TextInput(attrs={'placeholder':'e.g FName Mname Lname', 'class':'form-control'}),
            'date_of_Birth': forms.TextInput(attrs={'placeholder':'e.g YYYY-M-D', 'class':'form-control'}),
            'age': forms.NumberInput(attrs={'placeholder':'Your age', 'class':'form-control'}),
        }

        
class AdultForm(forms.ModelForm):
    class Meta:
        model = Adult
        fields = '__all__'

class ChildrenForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = '__all__'