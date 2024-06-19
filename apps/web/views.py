from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _



def home(request):
    if request.user.is_authenticated:
        return render(
            request,
            "web/app_home.html",
            context={
                "active_tab": "dashboard",
                "page_title": _("Dashboard"),
            },
        )
    else:
        return render(request, "web/landing_page.html")


def simulate_error(request):
    raise Exception("This is a simulated error.")

# @login_required
# def dashboard_view(request):
#     if Company.name == "Amwell":
#         return render(request, "amwell:list.html")
#     # elif Company.name == "company1":
#     #     return render(request, "company1:list.html")
#     else:
#         return render(request, "demo:demo_list.html")   
