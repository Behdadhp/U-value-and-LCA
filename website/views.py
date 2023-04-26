from django.views import generic


class index(generic.TemplateView):
    template_name = "index.html"
