from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import CheckForm, GroupForm
from .models import CheckOut

User = get_user_model()
# Контекст процессор для расчета количества заявок


def converter(request):
    return redirect('verify:index')


def new_remark(request):
    pass


def index(request):
    return render(request, 'verify/index.html', {})


def check_list(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return render(request, 'misc/403.html')
    check_list = CheckOut.objects.all().filter(status=False)
    if not user.allow_manage:
        check_list = check_list.filter(student__username=username)
    paginator = Paginator(check_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page}
    return render(request, 'verify/check_list.html', context)


@login_required
def archive(request, username):
    check_list = CheckOut.objects.all().filter(status=True)
    paginator = Paginator(check_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'paginator': paginator, 'page': page}
    return render(request, 'verify/check_list.html', context)


@login_required
def check_view(request, username, check_id):
    check_item = get_object_or_404(CheckOut, id=check_id)
    context = {
        'check_item': check_item,
    }
    return render(request, 'verify/check_view.html', context)


@login_required
def check_archive(request, username, check_id):
    check_item = get_object_or_404(CheckOut, id=check_id)
    check_item.status = True
    check_item.save()
    return redirect('verify:check_list', username)


@login_required
def check_delete(request, username, check_id):
    get_object_or_404(CheckOut, id=check_id).delete()
    return redirect('verify:check_list', username)


@login_required
def new_check(request, username):
    form = CheckForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'verify/new_check.html', {'form': form})
    check = form.save(commit=False)
    check.student = request.user
    check.save()
    return redirect('verify:check_list', username)


@login_required
def new_group(request):
    # Добавить проверку пользователя
    form = GroupForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'verify/new_group.html', {'form': form})
    form.save()
    return redirect('verify:check_list')

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
    '''
    filename = 'media/test_docx.docx'
    output = pypandoc.convert(filename, 'html')
    filename, ext = os.path.splitext(filename)
    filename = "{0}.html".format(filename)
    with open(filename, 'w') as f:
        # Python 2 "fix". If this isn't a string, encode it.
        if type(output) is not str:
            output = output.encode('utf-8')
        f.write(output)

    print("Done! Output written to: {}\n".format(filename))
    '''