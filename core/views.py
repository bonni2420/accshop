from django.shortcuts import render


def index(request):
    return render(request, "core/index.html")

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)