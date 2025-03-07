from datetime import datetime

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import render, redirect

from web.forms import RegistrationForm, AuthForm, MoneySpendForm
from web.models import Purchase

User = get_user_model()


def main_view(request):
    spends = Purchase.objects.all()
    return render(request, 'web\main_view.html', {
        'spends' : spends
    })


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'])
            user.set_password(form.cleaned_data["password"])
            user.save()
            is_success = True

            print(form.cleaned_data)

    return render(request, r'web\registration_view.html', {
        "form": form,
        "is_success": is_success
    })


def auth_view(request):
    form = AuthForm()

    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Введены неверные данные")
            else:
                login(request, user)
                return redirect("main")

    return render(request, r'web\auth_view.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect("main")


def edit_money_spend_view(request, id=None):
    spend = Purchase.objects.get(id=id) if id is not None else None
    form = MoneySpendForm(instance=spend)

    if request.method == 'POST':
        date = [int(i) for i in request.POST["date"].split('T')[0].split('-')]
        is_planed = True
        if date[1] <= datetime.now().month and date[-1] <= datetime.now().day:
            is_planed = False

        form = MoneySpendForm(data=request.POST, instance=spend, initial={"user": request.user, 'is_planed': is_planed})

        if form.is_valid():
            form.save()
            return redirect("main")

    return render(request, r'web\add_spend_money_view.html', {
        "form": form
    })
