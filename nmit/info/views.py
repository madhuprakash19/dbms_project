from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from datetime import datetime
# Create your views here.
@login_required()
def home(request):
    day = datetime.today().strftime('%A')
    return render(request,'home.html',{'day':day})
