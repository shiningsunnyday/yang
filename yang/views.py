# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import YangForm

def yang_view(request):
    print(request.POST)
    if request.method == 'POST':
        if request.POST.get('input') == 'Andrew Yang':
            return render(request, 'congrats.html')
        else:
            return render(request, 'boo.html')

    form = YangForm()
    return render(request, 'yang.html', {'form': form})