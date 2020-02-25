
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from lawyers.models import User, Lawyer, OtherStaff
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group


class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)

    email = forms.EmailField()
    #

    # is_lawyer = forms.BooleanField(label="Are You A Lawyer ?")

    # username = forms.CharField(label="", widget=forms.TextInput
    #                            (attrs={'class': 'form-control', 'placeholder': 'username'
    #                                    }))

    # first_name = forms.CharField(
    #     widget=forms.

    #     (attrs={'class': 'form-control'
    #             }))
    # last_name = forms.CharField(
    #     widget=forms.TextInput
    #     (attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', "phone")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        # user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_staff = True
            # user.is_lawyer = True
            user.save()
        return user


class OtherStaffForm(forms.ModelForm):

    class Meta:
        model = OtherStaff
        fields = ("role",)


class LawyerForm(forms.ModelForm):

    class Meta:
        model = Lawyer
        fields = ("bar_number", "lawyer_status")


class LawyerProfileForm(forms.ModelForm):
    email = forms.EmailField()
    # password1 = None
    # password2 = None

    class Meta:
        model = User
        fields = ("username", "email", "phone", "avatar")

    # def save(self, commit=True):
    #     user = super(LawyerProfileForm, self).save(commit=False)
    #     password = self.cleaned_data["password1"]
    #     if password1:
    #         user.set_password(password)
    #     if commit:
    #         user.save()
    #     return user


# class ChangePassForm(forms.ModelForm):

#     class Meta:
#         model = ChangePass
#         fields = ("",)


# class OtherStaffForm(forms.ModelForm):

#     class Meta:
#         model = OtherStaff
#         fields = ("role",)
#


class UpdateUserForm(UserChangeForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            '__all__'
        )
        # exclude=()

    def clean_password(self):
        # Password can't be changed in the admin
        return self.initial["password"]


class UpdateForm(forms.ModelForm):
    # password = None
    # user_group = Group.objects.all()
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_staff',
                  'is_superuser', 'phone', 'group')

    # def clean_password(self):
    #     # Password can't be changed in the admin
    #     return self.initial["password"]


class StaffUpdateForm(forms.ModelForm):
    # group = queryset = Group.objects.all()
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('__all__')

    def clean_password(self):
        # Password can't be changed in the admin
        return self.initial["password"]


class StaffProfileForm(forms.ModelForm):
    email = forms.EmailField()

    # password1 = None
    # password2 = None

    class Meta:
        model = User
        fields = ("username", "email", "phone", "avatar")
