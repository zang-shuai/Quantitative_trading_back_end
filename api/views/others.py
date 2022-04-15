from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def count(request):
    res = 0
    for i in request.POST:
        res += int(request.POST.get(i))
    return redirect('http://127.0.0.1:8080/#/lab/result?res=' + str(res))
