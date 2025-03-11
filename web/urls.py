from django.contrib import admin
from django.urls import path

from web.views import *

urlpatterns = [
    path('', main_view, name='main'),
    path('registration/', registration_view, name='registration'),
    path('auth/', auth_view, name='auth'),
    path('logout/', logout_view, name='logout'),
    path('analytics/', analytic_view, name='analytics'),
    path('money_spend/add/', edit_money_spend_view, name='add_spend_money'),
    path('money_spend/<int:id>/', edit_money_spend_view, name='edit_spend_money'),
    path('categories/', purchase_category_view, name='categories'),
    path('categories/<int:id>/delete', delete_purchase_category_view, name='delete_purchase_category'),
]
