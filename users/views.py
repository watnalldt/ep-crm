from django.contrib import auth, messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import cache_control, never_cache
from django.views.generic import ListView, TemplateView

from clients.models import Client
from contracts.models import Contract
from core.decorators import account_manager_required
from core.views import HTMLTitleMixin

from .utils import detect_user, send_verification_email

User = get_user_model()


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("users:my_account")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd["username"], password=cd["password"])

            if user is not None:
                auth.login(request, user)
                messages.success(request, " You are logged in..")
                return redirect("users:my_account")
            else:
                messages.error(request, "Invalid login credentials..")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "You have successfully logged out.")
    return redirect("users:login")


@login_required(login_url="users:login")  # login required decorators
#  Function For MyAccount.
def my_account(request):
    user = request.user
    redirect_url = detect_user(user)
    return redirect(redirect_url)


# Account activation for client managers
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is activated")
        return redirect("users:my_account")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("users:my_account")


# Passwords
def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = "Reset Your Password"
            email_template = "users/emails/reset_password_email.html"
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, "Password reset link has been sent to your email address.")
            return redirect("users:login")
        else:
            messages.error(request, "Account does not exist")
            return redirect("users:forgot_password")
    return render(request, "users/forgot_password.html")


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.info(request, "Please reset your password")
        return redirect("users:reset_password")
    else:
        messages.error(request, "This link has been expired!")
        return redirect("users:my_account")


def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            pk = request.session.get("uid")
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("users:login")
        else:
            messages.error(request, "Password do not match!")
            return redirect("users:reset_password")

    return render(request, "users/reset_password.html")


@method_decorator([never_cache, account_manager_required], name="dispatch")
class AccountManagerView(LoginRequiredMixin, HTMLTitleMixin, TemplateView):
    # Returns the Account Manager's Dashboard on login.
    model = Client
    template_name = "account_managers/account_managers_dashboard.html"
    html_title = "My Dashboard"


@method_decorator([never_cache, account_manager_required], name="dispatch")
class AccountManagerClientList(LoginRequiredMixin, HTMLTitleMixin, ListView):
    # Lists out all their client's with a link to their respective contracts
    model = Client
    template_name = "account_managers/client_list.html"
    html_title = "Client List"
    login_url = "/users/login/"

    def get_queryset(self):
        return Client.objects.filter(account_manager=self.request.user)


def search_contracts(query):
    return Contract.objects.filter(
        Q(mpan_mpr__iexact=query)
        | Q(client__client__icontains=query)
        | Q(business_name__icontains=query)
        | Q(site_address__contains=query)
    )


@method_decorator([never_cache, account_manager_required], name="dispatch")
class ContractSearchView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = "account_managers/search_results.html"
    context_object_name = "results"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return search_contracts(query).distinct()
        else:
            return Contract.objects.all()
