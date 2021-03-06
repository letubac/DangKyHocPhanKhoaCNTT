from django import forms 
from django.forms import Form


class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))

    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
    birthday = forms.DateField(label="birthday", required=False, widget=forms.DateInput(attrs={"class":"form-control",'id':'datepicker'}))

class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    gender_list = (
        ('Nam','Nam'),
        ('N???','N???')
    )
    
    gender = forms.ChoiceField(label="Gi???i T??nh", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="???nh Ch??n Dung", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
    birthday = forms.DateField(label="birthday", required=False, widget=forms.DateInput(attrs={"class":"form-control",'id':'datepicker'}))

