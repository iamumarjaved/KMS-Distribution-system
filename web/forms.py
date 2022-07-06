from django import forms
from web.models import MyUser, Order



# from django import forms
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
#
# from .models import User
#
#
# class UserCreationForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(
#         label='Password confirmation', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('email', 'phone', 'type')
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#
#
# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'phone','type',
#                   'is_active', 'is_admin')
#
#     def clean_password(self):
#         return self.initial["password"]


# class RegistrationForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('email', 'phone', 'type')
#         widgets = {
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'phone': forms.NumberInput(attrs={'class': 'form-control'}),
#             'type': forms.Select(attrs={'class': 'form-control'}),
#         }







class RegistrationForm(forms.ModelForm):
    TYPE_CHOICES = (
        ('director', 'Director Sales and Marketing'),
        ('zone', 'Zonal Manager'),
        ('sales', 'Sales Representative'),
    )
    type = forms.ChoiceField(choices=TYPE_CHOICES)
    class Meta:

        model = MyUser
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'class': ' input100 '}),
            'email': forms.EmailInput(attrs={'class': ' input100 '}),
            'password': forms.PasswordInput(attrs={'class': ' input100 '}),
            # 'password2': forms.PasswordInput(attrs={'class': 'wrap-input100 validate-input input100 focus-input100'}),
            'first_name': forms.TextInput(attrs={'class': 'input100'}),
            'last_name': forms.TextInput(attrs={'class': ' input100 '}),
            'phone': forms.TextInput(attrs={'class': ' input100 '}),
            'type': forms.Select(attrs={'class': 'input100'}),
        }

        def clean_username(self):
            username = self.cleaned_data.get('username')
            if MyUser.objects.filter(username=username).exists():
                raise forms.ValidationError('Username already exists')
            return username

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if MyUser.objects.filter(email=email).exists():
                raise forms.ValidationError('Email already exists')
            return email

        def clean_first_name(self):
            first_name = self.cleaned_data.get('first_name')
            if not first_name:
                raise forms.ValidationError('First name is required')
            return first_name

        def clean_last_name(self):
            last_name = self.cleaned_data.get('last_name')
            if not last_name:
                raise forms.ValidationError('Last name is required')
            return last_name

        def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            if not phone:
                raise forms.ValidationError('Phone number is required')
            return phone

        def clean_password(self):
            password = self.cleaned_data.get('password')
            if not password:
                raise forms.ValidationError('Password is required')
            return password

        # def clean_password2(self):
        #     password = self.cleaned_data.get('password')
        #     password2 = self.cleaned_data.get('password2')
        #     if password != password2:
        #         raise forms.ValidationError('Passwords do not match')
        #
        #     return password2


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'input100'}),
            'quantity': forms.TextInput(attrs={'class': 'input100'}),
            'rate': forms.TextInput(attrs={'class': 'input100'}),
            'packing': forms.TextInput(attrs={'class': 'input100'}),
        }

        def clean_name(self):
            name = self.cleaned_data.get('name')
            if not name:
                raise forms.ValidationError('Name is required')
            return name

        def clean_quanity(self):
            quanity = self.cleaned_data.get('quanity')
            if not quanity:
                raise forms.ValidationError('Quanity is required')
            return quanity

        def clean_rate(self):
            rate = self.cleaned_data.get('rate')
            if not rate:
                raise forms.ValidationError('Rate is required')
            return rate

        def clean_packing(self):
            packing = self.cleaned_data.get('packing')
            if not packing:
                raise forms.ValidationError('Packing is required')
            return packing
