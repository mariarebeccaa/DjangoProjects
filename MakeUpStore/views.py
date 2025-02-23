from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Categorie, Produs
from django.core.paginator import Paginator

# Create your views here.
def afis_template(request):
    return render(request, "categorii.html",
                {
                    "categorii":Categorie.objects.all()
                })

# lab4_Task_QuerySets -----------------------------------------------------------------------------
# Filtrarea produselor
def lista_produse(request):
    produse = Produs.objects.prefetch_related('marci').select_related('categorie').all()  # Se pornește de la toate produsele
# fiecare metodă precum .filter(), .exclude(), .order_by() 
# este aplicată pe un QuerySet derivat din Produs.objects
    # accesam valorile din query string folosind request.GET
    nume = request.GET.get('nume')
    pret_min = request.GET.get('pret_min')
    pret_max = request.GET.get('pret_max')
    descriere = request.GET.get('descriere')
    marca = request.GET.get('marca')
    categorie = request.GET.get('categorie')

    if nume:
        produse = produse.filter(nume__icontains=nume)

    if pret_min:
        produse = produse.filter(pret__gte=float(pret_min))
    if pret_max:
        produse = produse.filter(pret__lte=float(pret_max))

    if descriere:
        produse = produse.filter(descriere__icontains=descriere)

    if marca:
        produse = produse.filter(marci__nume__icontains=marca)

    if categorie:
        produse = produse.filter(categorie__nume__icontains=categorie)

    # Paginare - 5 produse pe pag
    paginator = Paginator(produse, 5)
    page_number = request.GET.get('page')  # Preluam numarul paginii din URL
    pagina_curenta = paginator.get_page(page_number)
    # pag curenta este preluata din parametrii URL-ului 

    # Renderizam template-ul
    return render(request, 'produse/lista_produse.html', {'produse': pagina_curenta})
# http://127.0.0.1:8000/proiect/lista_produse/


# LABORATOR 5

# lab5_Task1
#filtrare produse cu formular
from .models import Produs
from .forms import ProdusFilterForm

def filtreaza_produse(request):
    produse = Produs.objects.all()  # Obtinem toate produsele
    form = ProdusFilterForm(request.GET)  # Populam formularul cu date din query string

    if form.is_valid():
        # Aplicam filtrele pe baza datelor din formular
        if form.cleaned_data['nume']: #validam datele inainte de utilizare
            produse = produse.filter(nume__icontains=form.cleaned_data['nume'])
        if form.cleaned_data['pret_min']:
            produse = produse.filter(pret__gte=form.cleaned_data['pret_min'])
        if form.cleaned_data['pret_max']:
            produse = produse.filter(pret__lte=form.cleaned_data['pret_max'])
        if form.cleaned_data['descriere']:
            produse = produse.filter(descriere__icontains=form.cleaned_data['descriere'])
        if form.cleaned_data['marca']:
            produse = produse.filter(marci=form.cleaned_data['marca'])
        if form.cleaned_data['categorie']:
            produse = produse.filter(categorie=form.cleaned_data['categorie'])

    return render(request, 'produse/filtreaza_produse.html', {'form': form, 'produse': produse})

# http://127.0.0.1:8000/proiect/filtreaza_produse/


# lab5_Task2
# pagina de contact 
import os, re
import json
from django.shortcuts import render
from django.conf import settings
from django.utils.timezone import now
from .forms import ContactForm
from datetime import date

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Preprocesare date
            mesaj = form.cleaned_data['mesaj']
            mesaj = re.sub(r'\s+', ' ', mesaj.replace('\n', ' '))  # Eliminare linii noi și spații multiple

            data_nasterii = form.cleaned_data['data_nasterii']
            today = date.today()
            age_years = today.year - data_nasterii.year
            age_months = today.month - data_nasterii.month
            if today.day < data_nasterii.day:
                age_months -= 1
            if age_months < 0:
                age_years -= 1
                age_months += 12
            varsta = f"{age_years} ani si {age_months} luni"

            # Salvare în fișier JSON
            mesaj_data = {
                "nume": form.cleaned_data['nume'],
                "prenume": form.cleaned_data['prenume'],
                "varsta": varsta,
                "email": form.cleaned_data['email'],
                "tip_mesaj": form.cleaned_data['tip_mesaj'],
                "subiect": form.cleaned_data['subiect'],
                "minim_zile_asteptare": form.cleaned_data['minim_zile_asteptare'],
                "mesaj": mesaj,
            }
            # Crearea folderului `mesaje` dacă nu există
            folder_mesaje = os.path.join(settings.BASE_DIR, 'mesaje')
            os.makedirs(folder_mesaje, exist_ok=True)
            
            # Salvarea mesajului într-un fișier JSON-
            # fisier text care contine date structurate, usor de citit 
            timestamp = int(now().timestamp())  # Timpul curent în secunde
            file_path = os.path.join(folder_mesaje, f"mesaj_{timestamp}.json")
            with open(file_path, 'w') as json_file:
                json.dump(mesaj_data, json_file)

            return render(request, 'contact_succes.html', {'mesaj_data': mesaj_data})
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

# http://127.0.0.1:8000/proiect/contact/


# Lab5 Task 2 ++ pagina de listare a mesajelor
# care le incarca din fisiere si permite filtrarea dupa tip sau nume
import os
import json
from django.conf import settings
from django.shortcuts import render

def lista_mesaje(request):
    folder_mesaje = os.path.join(settings.BASE_DIR, 'mesaje')  # Calea către folderul mesaje
    mesaje = []

    # Citirea tuturor fișierelor JSON din folder
    if os.path.exists(folder_mesaje):
        for file_name in os.listdir(folder_mesaje):
            if file_name.endswith('.json'):
                file_path = os.path.join(folder_mesaje, file_name)
                with open(file_path, 'r') as json_file:
                    mesaj = json.load(json_file)
                    mesaje.append(mesaj)

    # Filtrarea mesajelor
    tip_mesaj = request.GET.get('tip_mesaj')
    nume = request.GET.get('nume')

    if tip_mesaj:
        mesaje = [mesaj for mesaj in mesaje if mesaj['tip_mesaj'] == tip_mesaj]
    if nume:
        mesaje = [mesaj for mesaj in mesaje if nume.lower() in mesaj['nume'].lower()]

    return render(request, 'lista_mesaje.html', {'mesaje': mesaje, 'tip_mesaj': tip_mesaj, 'nume': nume})

#lab5_task 3
from django.shortcuts import render, redirect
from .forms import ProdusForm
from django.http import HttpResponseForbidden

def adauga_produs(request):
    if not request.user.has_perm('MakeUpStore.add_product'): 
        return render(request, '403.html', {
            'titlu': 'Eroare adaugare produse',
            'mesaj_personalizat': 'Nu ai voie să adaugi produse'
        })
    if request.method == 'POST':
        form = ProdusForm(request.POST)
        if form.is_valid():
            produs = form.save()
            marci = form.cleaned_data.get('marci')
            produs.marci.set(marci)  # Salvăm explicit relația many-to-many
            return redirect('lista_produse')
    else:
        form = ProdusForm()
    return render(request, 'produse/adauga_produs.html', {'form': form})

# lab6
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)#se creeaza un ob de tip form cu datele introduse
        if form.is_valid():
            user = form.save()
            user.generate_confirmation_code()  # Genereaza codul de confirmare
            trimite_mail_confirmare(user)  # Trimite e-mailul
            return render(request, 'confirmare_inregistrare.html', {'email': user.email})
    else:
        form = CustomUserCreationForm()
    return render(request, 'inregistrare.html', {'form': form})


from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, request=request)
        if form.is_valid():
            user = form.get_user() #obtine user ul din fromular
            # modif lab 7
            
            # Verificare email confirmat
            if not user.email_confirmat:
                return HttpResponse("E-mailul nu a fost confirmat! Te rugăm să verifici inbox-ul și să accesezi linkul de confirmare.")

            # end modif lab 7
            login(request, user)
            
            #gestionam sesiunea de logare
            if not form.cleaned_data.get('ramane_logat'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(24*60*60)  # o zi în secunde            
            return redirect('profile')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Profil
from django.contrib.auth.decorators import login_required
@login_required
def profile_view(request):
    user_data = {
        'username': request.user.username,
        'email': request.user.email,
        'telefon': request.user.telefon,
        'data_nasterii': request.user.data_nasterii,
        'oras': request.user.oras,
        'ocupatie': request.user.ocupatie,
        'descriere': request.user.descriere,
    }
    return render(request, 'profile.html', {'user_data': user_data})

# views.py
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm
from django.contrib import messages
@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            #actualizeaza sesiunea de autentificare
            
            messages.success(request, 'Parola a fost actualizata')
            return redirect('profile')
        else:
            messages.error(request, 'Exista erori.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'schimba_parola.html', {'form': form})

# lab7
from django.core.mail import send_mail
from django.template.loader import render_to_string

def trimite_mail_confirmare(user):
    context = {
        'nume': user.first_name,
        'prenume': user.last_name,
        'username': user.username,
        'cod': user.cod,
    }
    subject = 'Confirmare cont'
    html_content = render_to_string('confirmare_email.html', context)
    send_mail(
        subject='Confirmare cont',
        message='Salut. Ce mai faci?',
        html_message=html_content,
        from_email='edu.mariarebecca.django@gmail.com',
        recipient_list=['edu.mariarebecca.django@gmail.com'],
        fail_silently=False,
    )
    
from django.http import HttpResponse
from .models import CustomUser

def confirma_mail(request, cod):
    try:
        user = CustomUser.objects.get(cod=cod)
        user.email_confirmat = True
        user.cod = None  # Resetează codul după confirmare
        user.save()
        return render(request, 'email_confirmat.html')
    except CustomUser.DoesNotExist:
        return HttpResponse("Cod de confirmare invalid.")


# Lab7_Task2
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Promotie, CustomUser, Categorie, Vizualizari
from .forms import PromotieForm
from django.db.models import Count
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta

@login_required
def creeaza_promotie(request):
    if request.method == 'POST':
        form = PromotieForm(request.POST)
        if form.is_valid():
            promotie = form.save(commit=False)
            promotie.data_creare = timezone.now()
            promotie.data_expirare = promotie.data_creare + timedelta(days=form.cleaned_data['durata'])
            promotie.save()
            form.save_m2m()
            messages.success(request, 'Promoția a fost creată cu succes.')

            # Logica pentru trimiterea emailurilor în masă
            user_view_counter = {}
            selected_categories = form.cleaned_data['categorii']
            print(f"Selected categories: {selected_categories}")
            for categorie in selected_categories:
                print(f"Processing category: {categorie.nume}")
                for view in Vizualizari.objects.filter(produs__categorie=categorie):
                    print(f"User {view.utilizator} viewed product {view.produs} in category {categorie.nume}")
                    if view.utilizator in user_view_counter:
                        user_view_counter[view.utilizator] += 1
                    else:
                        user_view_counter[view.utilizator] = 1

            print(f"User view counter: {user_view_counter}")
            liable_users = [user for user, views in user_view_counter.items() if views >= 3]
            print(f"Liable users: {liable_users}")

            message_machiaj = render_to_string('promotii/machiaj_promotii.html', {'subiect': promotie.nume, 'data_expirare': promotie.data_expirare})
            message_general = render_to_string('promotii/general_promotie.html', {'subiect': promotie.nume, 'data_expirare': promotie.data_expirare})

            emails = [user.email for user in liable_users]
            emails.append('edu.mariarebecca.django@gmail.com')
            print(f"Emails to be sent: {emails}")

            datadict = {
                'Machiaj': (promotie.nume, message_machiaj, 'edu.mariarebecca.django@gmail.com', emails),
                'General': (promotie.nume, message_general, 'edu.mariarebecca.django@gmail.com', emails),
            }

            datalist = []
            category_names = {categorie.nume for categorie in selected_categories}
            print(f"Category names: {category_names}")

            if 'Machiaj' in category_names and 'General' in category_names:
                datalist.append(datadict['Machiaj'])
                datalist.append(datadict['General'])
                print("Sending emails for Machiaj and General categories")
                send_mass_mail(datalist)
            elif 'Machiaj' in category_names:
                datalist.append(datadict['Machiaj'])
                print("Sending emails for Machiaj category")
                send_mass_mail(datalist)
            elif 'General' in category_names:
                datalist.append(datadict['General'])
                print("Sending emails for General category")
                send_mass_mail(datalist)

            print(f"Emails sent to: {emails}")
            return redirect('lista_promotii')
        else:
            messages.error(request, 'Formularul conține erori.')
            print("Form is not valid")
    else:
        form = PromotieForm()
    return render(request, 'promotii/creeaza_promotie.html', {'form': form})


def urmareste_vizualizare(request, produs_id):
    """
    View pentru înregistrarea vizualizărilor produselor.
    Se apelează automat când un utilizator vizualizează un produs.
    """
    Vizualizari.objects.create(utilizator=request.user, produs_id=produs_id)
    print(f"User {request.user.username} viewed product {produs_id}")
    return redirect('detalii_produs', produs_id=produs_id)

def lista_promotii(request):
    """
    View pentru afișarea listei de promoții active.
    """
    promotii = Promotie.objects.all().order_by('-data_creare')
    return render(request, 'promotii/lista_promotii.html', {'promotii': promotii})

def detalii_produs(request, produs_id):
    produs = get_object_or_404(Produs, id=produs_id)
    return render(request, 'produse/detalii_produs.html', {'produs': produs})

def index(request):
    # trimite_email()
    return HttpResponse("Primulll raspuns")

#lab8_Task1
from django.shortcuts import render
from django.http import HttpResponseForbidden

def custom_403_view(request, exception=None):
    if request.user.is_authenticated:
        salut = f"Salut {request.user.username}"
    else:
        salut = "Salut preastimate anonim"
    
    context = {
        'titlu': 'Acces Interzis',
        'mesaj_personalizat': 'Nu aveți permisiunea de a accesa această resursă.',
        'salut': salut,
    }
    return render(request, '403.html', context)

from django.http import HttpResponseForbidden

# def test_403_view(request):
#     return HttpResponseForbidden()

from django.shortcuts import render

def test_403_view(request):
    return render(request, '403.html', {
        'titlu': 'Eroare 403',
        'mesaj_personalizat': 'Nu este permis accesul la resursa curentă.'
    })