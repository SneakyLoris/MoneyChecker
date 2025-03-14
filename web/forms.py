from importlib.metadata import requires

from django import forms
from django.contrib.auth import get_user_model

from web.models import Purchase, PurchaseCategory

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["password2"]:
            self.add_error("password", "Пароли не совпадают")

        return cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "password", "password2")


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class MoneySpendForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.user = self.initial["user"]
        self.instance.is_planed = self.initial["is_planed"]
        return super().save(commit)

    class Meta:
        model = Purchase
        fields = ("title", "value", "date", "tags")
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M")
        }


class PurchaseCategoryForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.user = self.initial["user"]
        return super().save(commit)


    class Meta:
        model = PurchaseCategory
        fields = ("title",)


class FilterForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Поиск"}), required=False)