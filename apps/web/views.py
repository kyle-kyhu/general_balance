from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from apps.workflows.models import Workflow

from health_check.views import MainView


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


class HealthCheck(MainView):
    def get(self, request, *args, **kwargs):
        tokens = settings.HEALTH_CHECK_TOKENS
        if tokens and request.GET.get("token") not in tokens:
            raise Http404
        return super().get(request, *args, **kwargs)


class AppHomeView(TemplateView):
    template_name = "web/app_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workflows"] = Workflow.objects.all().order_by("-created_at")
        return context
