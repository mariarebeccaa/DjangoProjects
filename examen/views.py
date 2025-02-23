from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Comanda
from .forms import ComandaForm
from django.core.mail import send_mail

def lista_clienti(request):
    clienti = Client.objects.all()
    return render(request, 'lista_clienti.html', {'clienti': clienti})

def detalii_comanda(request, client_id): 
    client = get_object_or_404(Client, id=client_id) # gaseste clientul dupa id sau returneza 404
    comenzi = Comanda.objects.filter(client=client)
    return render(request, 'detalii_comanda.html', {'client': client, 'comenzi': comenzi})

def adauga_comanda(request):
    if request.method == 'POST':
        form = ComandaForm(request.POST)
        if form.is_valid():
            comanda = form.save()
            client = comanda.client

            if Comanda.objects.filter(client=client).count() == 3:
                # Send an email
                send_mail(
                    'Happy happy happy!',
                    f'Salut {client.nume} {client.prenume}, ai facut comanda cu nr 3!',
                    'edu.mariarebecca.django@gmail.com',
                    [client.email, 'edu.mariarebecca.django@gmail.com'],
                    fail_silently=False,
                )
            return redirect('lista_clienti')
    else:
        form = ComandaForm()
    return render(request, 'adauga_comanda.html', {'form': form})

