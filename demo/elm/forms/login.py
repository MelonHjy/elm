from django import forms
from ..models import User

class LoginForm(forms.Form):
    account = forms.CharField(max_length=12, min_length=6, required=True,
                               error_messages={"required": '用户账号不能为空',"invalid": '格式错误'},
                               widget=forms.TextInput(attrs={'id': 'account', 'placeholder': "手机/账号"}))
    passwd = forms.CharField(max_length=16, min_length=6, required=True,
                             widget=forms.PasswordInput(attrs={'id': 'pass', 'placeholder': "密码"}))


class registerForm(forms.Form):
    account = forms.CharField(max_length=12, min_length=6, required=True,
                               widget=forms.TextInput(attrs={'id': 'account', 'placeholder': "账号"}))
    passwd = forms.CharField(max_length=16, min_length=6, required=True,
                             widget=forms.PasswordInput(attrs={'id': 'passwd', 'placeholder': "密码"}))
    check = forms.CharField(max_length=16, min_length=6, required=True,
                             widget=forms.PasswordInput(attrs={'id': 'check', 'placeholder': "确认密码"}))
    name = forms.CharField(max_length=12, min_length=2, required=True,
                               widget=forms.TextInput(attrs={'id': 'name', 'placeholder': "昵称"}))
    tel = forms.CharField(max_length=11, min_length=8, required=True,
                               widget=forms.TextInput(attrs={'id': 'tel', 'placeholder': "手机"}))
    img = forms.FileField(required=False,widget=forms.FileInput(attrs={'id': 'img', 'placeholder': "头像"}))
