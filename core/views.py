from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from .models import SiteSettings, Education, Skill, Project, Referee


def home(request, form=None):
    ctx = {
        "s": SiteSettings.load(),
        "education": Education.objects.filter(published=True),
        "skills": Skill.objects.filter(published=True),
        "projects": Project.objects.filter(published=True, featured=True),
        "referees": Referee.objects.filter(published=True),
        "form": form or ContactForm(),
    }
    return render(request, "index.html", ctx)


def contact(request):
    if request.method != "POST":
        return redirect("home")
    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Thank you! Your message has been sent.")
        return redirect("/#contact")
    messages.error(request, "Please correct the errors below.")
    return home(request, form)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, published=True)
    return render(request, "project_detail.html", {"s": SiteSettings.load(), "p": project})


def robots(request):
    return HttpResponse("User-agent: *\nDisallow: /admin/\n", content_type="text/plain")
