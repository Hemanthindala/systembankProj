from django.urls import re_path,path
from . import views

app_name = "profiles"

urlpatterns = [
    re_path(r"^account_status/$", views.index, name = "account_status"),
    re_path(r"^money_transfer/", views.money_transfer, name = "money_transfer"),
    re_path(r"^loan_app/$", views.loan, name = "loan_app"),
    re_path(r"^ewallet/$", views.ewallet, name = "ewallet"),
    re_path(r"^online_pay/$", views.online_pay, name = "online_pay"),
    re_path(r"settings/$", views.settings, name = "settings"),
    re_path(r"edit_details/", views.edit_details, name = "edit_details"),
    re_path(r"delete_account/$", views.delete_account, name = "delete_account"),
    path('authorize_payment/<int:request_id>/', views.authorize_payment, name="authorize_payment"),
    path('fetch_all_transactions_of_user/<int:account_number>/', views.fetch_all_transactions_of_user, name="fetch_all_transactions_of_user"),
    path('fetch_all_requests_not_resolved/', views.fetch_all_requests_not_resolved,name="fetch_all_requests_not_resolved"),
    path('fetch_all_transactions/', views.fetch_all_transactions,name="fetch_all_transactions"),
    re_path(r"^transaction_requests/$", views.transaction_requests, name="transaction_requests")
]
