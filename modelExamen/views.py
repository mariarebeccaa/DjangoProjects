from django.shortcuts import render
from django.core.mail import send_mail
# Create your views here.
from django.shortcuts import get_object_or_404
from .models import Elev

def lista_elevi(request):
    elevi = Elev.objects.all()
    return render(request, 'lista_elevi.html', {'elevi': elevi})
# http://127.0.0.1:8000/modelExamen/elevi/

def detalii_elev(request, elev_id):
    elev = get_object_or_404(Elev, id=elev_id) # gaseste elevul dupa id sau returneza 404
    return render(request, 'detalii_elev.html', {'elev': elev})

from django.shortcuts import redirect
from .models import Elev
from .forms import ElevForm

def adauga_elev(request):
    if request.method == 'POST':
        form = ElevForm(request.POST)
        if form.is_valid():
            elev = form.save()
            if Elev.objects.count() == 4:
                # Send an email
                send_mail(
                    'Adaugare Elev',
                    f'Numele vostru: Edu Maria-Rebecca, Grupa: 231, Elev: {elev.nume} {elev.prenume}',
                    'edu.mariarebecca.django@gmail.com',
                    ['edu.mariarebecca.django@gmail.com'],
                    fail_silently=False,
                )
            return redirect('lista_elevi')
    else:
        form = ElevForm()
    return render(request, 'adauga_elev.html', {'form': form})

# http://127.0.0.1:8000/modelExamen/adauga_elev/