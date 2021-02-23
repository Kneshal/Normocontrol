from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import CheckForm, GroupForm
from .models import CheckOut
import mammoth
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.conf import settings

User = get_user_model()


def index(request):
    check_list = CheckOut.objects.all()
    paginator = Paginator(check_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
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
    context = {'page': page}
    return render(request, 'verify/index.html', context)


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
