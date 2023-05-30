from django.shortcuts import render


def index(request):
    """Главная страница информационной системы."""
    return render(request, 'verify/index.html')

def manual(request):
    """Методические рекомендации."""
    return render(request, 'verify/manual.html')