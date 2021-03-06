from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django_twofactor.forms import (
    ResetTwoFactorAuthForm, DisableTwoFactorAuthForm, GridCardActivationForm)


@login_required(login_url="/")
def change_settings(request):
    reset_form = None
    disable_form = None
    gridcard_form = None
    if request.method == "POST":
        post = request.POST
        if post.get("reset_confirmation"):
            reset_form = ResetTwoFactorAuthForm(request.user, data=post)
            if reset_form.is_valid():
                reset_form.save()
                return redirect("auth-enabled")
        elif post.get("disable_confirmation"):
            disable_form = DisableTwoFactorAuthForm(request.user, data=post)
            if disable_form.is_valid():
                disable_form.save()
                return redirect("change-settings")
        else:
            gridcard_form = GridCardActivationForm(request.user, data=post)
            if gridcard_form.is_valid():
                gridcard_form.save()
                return redirect("auth-enabled-gridcard")

    return render(request, "twofactor_demo/settings.html", {
        "reset_form": reset_form or ResetTwoFactorAuthForm(request.user),
        "disable_form": disable_form or DisableTwoFactorAuthForm(request.user),
        "gridcard_form": gridcard_form or GridCardActivationForm(request.user),
    })


auth_enabled = login_required(login_url="/")(
    TemplateView.as_view(template_name="twofactor_demo/auth_enabled.html")
)

auth_enabled_gridcard = login_required(login_url="/")(
    TemplateView.as_view(template_name="twofactor_demo/auth_enabled_gridcard.html")
)
