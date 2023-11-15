def detect_user(user):
    if user.role == "CLIENT_MANAGER":
        redirect_url = "users:client_managers_dashboard"
        return redirect_url
    elif user.role == "ACCOUNT_MANAGER":
        redirect_url = "users:account_managers_dashboard"
        return redirect_url
    elif user.role == "ADMIN":
        redirect_url = "/ep_crm_portal"
        return redirect_url
