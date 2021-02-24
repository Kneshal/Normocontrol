from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import CheckForm, GroupForm
from .models import CheckOut

User = get_user_model()
# Контекст процессор для расчета количества заявок


def index(request):
    check_list = CheckOut.objects.all().filter(status=False)
    paginator = Paginator(check_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page}
    return render(request, 'verify/index.html', context)


@login_required
def archive(request):
    check_list = CheckOut.objects.all().filter(status=True)
    paginator = Paginator(check_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'paginator': paginator, 'page': page}
    return render(request, 'verify/index.html', context)


@login_required
def check_view(request, check_id):
    check_item = get_object_or_404(CheckOut, id=check_id)
    context = {
        'check_item': check_item,
    }
    return render(request, 'verify/check_view.html', context)


@login_required
def check_archive(request, check_id):
    check_item = get_object_or_404(CheckOut, id=check_id)
    check_item.status = True
    check_item.save()
    return redirect('verify:index')


@login_required
def check_delete(request, check_id):
    get_object_or_404(CheckOut, id=check_id).delete()
    return redirect('verify:index')


@login_required
def new_check(request):
    form = CheckForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'verify/new_check.html', {'form': form})
    check = form.save(commit=False)
    check.student = request.user
    check.save()
    return redirect('verify:index')


@login_required
def new_group(request):
    form = GroupForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'verify/new_group.html', {'form': form})
    form.save()
    return redirect('verify:index')

    '''
    file = check_list[0].docx_file
    urls = settings.MEDIA_ROOT+'fileload/'
    fs = FileSystemStorage(location=urls, base_url=urls)
    filename = fs.save(file.name, file)
    filepath = urls + file.name
    print(filename)
    print(filepath)
    html = ''
    with open(filepath, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value

    context = {'page': page, 'html': html}
    '''
