from datetime import datetime

from django.contrib.admin.templatetags.admin_list import pagination
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from web.forms import RegistrationForm, AuthForm, MoneySpendForm, PurchaseCategoryForm, FilterForm
from web.models import Purchase, PurchaseCategory

User = get_user_model()


@login_required
def main_view(request):
    spends = Purchase.objects.all()


    filter_form = FilterForm(request.GET)
    filter_form.is_valid()
    filters = filter_form.cleaned_data


    if filters["search"]:
        spends = spends.filter(title__icontains=filters["search"])


    page = request.GET.get("page", 1)
    paginator = Paginator(spends, 15)

    spends_count = len(spends)

    return render(request, 'web/main_view.html', {
        'spends' : paginator.get_page(page),
        "filter_form" : filter_form,
        "spends_count" : spends_count,
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

    return render(request, 'web/registration_view.html', {
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

    return render(request, 'web/auth_view.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect("main")


@login_required
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

    return render(request, 'web/add_spend_money_view.html', {
        "form": form
    })


@login_required
def purchase_category_view(request):
    categories = PurchaseCategory.objects.all()
    form = PurchaseCategoryForm()
    if request.method == "POST":
        form = PurchaseCategoryForm(data=request.POST, initial={"user": request.user})

        if form.is_valid():
            form.save()
            return redirect('categories')

    return render(request, 'web/categories.html', {
        'form': form,
        'tags': categories,
    })


def delete_purchase_category_view(request, id=None):
    category = PurchaseCategory.objects.get(id=id)
    category.delete()
    return redirect('categories')