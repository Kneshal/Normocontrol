from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import CheckForm, GroupForm
from .models import CheckOut
from users.models import Group

User = get_user_model()


def user_check(func):
    """Декоратор. Проверяет доступность страницы для текущего пользователя."""
    def check_user(request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        if request.user != user:
            return render(request, 'misc/403.html')
        return func(request, *args, **kwargs)
    return check_user


def user_access(func):
    """Декоратор. Проверяет наличие прав для доступа к странице."""
    def check_user(request, *args, **kwargs):
        if not request.user.allow_manage:
            return render(request, 'misc/403.html')
        return func(request, *args, **kwargs)
    return check_user


def new_remark(request):
    pass


def index(request):
    """Главная страница информационной системы."""
    return render(request, 'verify/index.html')


@login_required
@user_access
def student_list(request):
    """Выводит таблицу всех зарегистрированных студентов."""
    students = User.objects.all().exclude(username='admin')
    students = students.exclude(allow_manage=True)
    context = {'students': students}
    return render(request, 'verify/student_list.html', context)


@login_required
@user_access
def group_list(request):
    """Выводит таблицу всех зарегистрированных групп."""
    group_list = Group.objects.all()
    context = {'group_list': group_list}
    return render(request, 'verify/group_list.html', context)


@login_required
@user_access
def group_students(request, slug):
    """Выводит таблицу студентов заданной группы."""
    group = get_object_or_404(Group, slug=slug)
    students = group.user.all()
    context = {'students': students, 'group': group}
    return render(request, 'verify/student_list.html', context)


@login_required
@user_check
def check_list(request, username):
    """Выводит список активных заявок для запрошенного пользователя."""
    user = get_object_or_404(User, username=username)
    check_list = CheckOut.objects.all().filter(status=False)
    if not user.allow_manage:
        check_list = check_list.filter(student__username=username)
    paginator = Paginator(check_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'active': True}
    return render(request, 'verify/check_list.html', context)


@login_required
@user_check
def archive(request, username):
    """Выводит список архивных заявок для зпрошенного пользователя."""
    check_list = CheckOut.objects.all().filter(status=True)
    paginator = Paginator(check_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'active': False}
    return render(request, 'verify/check_list.html', context)


@login_required
@user_check
def check_view(request, username, check_id):
    """Выводит данные по конкретной заявке для запрошенного пользователя."""
    check_item = get_object_or_404(CheckOut, id=check_id)
    context = {
        'check_item': check_item,
    }
    return render(request, 'verify/check_view.html', context)


@login_required
@user_check
def check_archive(request, username, check_id):
    """Отправляет определенную заявку в архив."""
    check_item = get_object_or_404(CheckOut, id=check_id)
    check_item.status = True
    check_item.save()
    return redirect('verify:check_list', username)


@login_required
@user_check
def check_delete(request, username, check_id):
    """Удаляет определенную заявку из БД."""
    get_object_or_404(CheckOut, id=check_id).delete()
    return redirect('verify:check_list', username)


@login_required
@user_check
def new_check(request, username):
    """Создает новую заявку от лица текущего пользователя."""
    form = CheckForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'verify/new_check.html', {'form': form})
    check = form.save(commit=False)
    check.student = request.user
    check.save()
    return redirect('verify:check_list', username)


@login_required
@user_access
def new_group(request):
    """Создает новую студенческую группу."""
    form = GroupForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'verify/new_group.html', {'form': form})
    form.save()
    return redirect('verify:check_list')
