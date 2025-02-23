from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Primul răspuns")

def pag1(request):
    return HttpResponse(2+3)

l=[]
def pag2(request):
    global l
    a=request.GET.get("a",10)
    print(request.GET)
    l.append(a)
    return HttpResponse(f"<b>Am primit</b>: {l}")
#  1
def mesaj(request):
    return HttpResponse("Buna ziua!")
# 2
import datetime
def data(request):
    now = datetime.datetime.now()
    return HttpResponse(f"Data si ora curenta: {now}")


nr = 0
def nr_accesari(request):
    global nr
    nr += 1
    return HttpResponse(f"Numarul de accesari: {nr}")


def suma(request):
    a = int(request.GET.get("a", 0))
    b = int(request.GET.get("b", 0))
    s = a+b
    return HttpResponse(f"Suma dintre {a} si {b} este: {s}")

texts = []
def text(request):
    global texts
    t = request.GET.get("t", "")
    if t.isalpha():
        texts.append(t)
    response_text = "".join([f"<p>{txt}</p>" for txt in texts])
    return HttpResponse(response_text)

# 6
def nr_parametri(request):
    num_params = len(request.GET)
    return HttpResponse(f"Numarul de parametri primiti este: {num_params}")

# 7
def operatie(request):
    a = int(request.GET.get("a", 0))
    b = int(request.GET.get("b", 0))
    op = request.GET.get("op", "sum")
    
    if op == "sum":
        result = a + b
    elif op == "dif":
        result = a - b
    elif op == "mul":
        result = a * b
    elif op == "div":
        result = a / b if b != 0 else "divizare cu zero!"
    elif op == "mod":
        result = a % b if b != 0 else "modulo cu zero!"
    else:
        result = "Operatie necunoscuta!"
    
    return HttpResponse(f"Rezultatul operației {op} dintre {a} și {b} este: {result}")

# 8
def tabel(request):
    m = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    tabel_html = "<table border='1'>"
    for linie in m:
        tabel_html += "<tr>"
        for elem in linie:
            tabel_html += f"<td>{elem}</td>"
        tabel_html += "</tr>"
    tabel_html += "</table>"
    return HttpResponse(tabel_html)

# 9
def lista(request):
    lista_cuvinte = ["mere", "prune", "cirese", "caise", "piersici"]
    cuvinte_param = request.GET.getlist("cuvinte")
    lista_html = "<ul>"  #lista neordonata
    for cuv in lista_cuvinte:
        if cuv in cuvinte_param:
            lista_html += f"<li><span style='color:red;'>{cuv}</span></li>"
        else:
            lista_html += f"<li>{cuv}</li>"
    return HttpResponse(lista_html)

# 10
lista_elevi = []
def elev(request):
    global lista_elevi
    nume = request.GET.get("nume", "")
    prenume = request.GET.get("prenume", "")
    clasa = request.GET.get("clasa", "")
    if nume and prenume and clasa.isdigit():
        lista_elevi.append({nume, prenume, int(clasa)})
    return HttpResponse(lista_elevi)
    

# lab2
def cum_il_cheama(request):
    lista_nume= request.GET.getlist('nume')
    lista_nume= ("si "+" si ".join(lista_nume)) if lista_nume else "anonim"
    return HttpResponse(f"Pe coleg îl cheama {lista_nume}")

#ex 1
import re
nr_cereri = 0
s = 0
def aduna_numere(request, id):
    global nr_cereri
    global s
    match = re.search(r'(\d+)$', id)
    if match:
        nr_cereri += 1 
        numar = int(match.group(1))
        s += numar
        return HttpResponse(f"numar cereri: {nr_cereri} suma numere: {s}")
    else:
        return HttpResponse("eroare")

#ex 2
# def afiseaza_liste(request):
#     param = len(request.GET)
#     for p in range
#     lista_param = request.GET.getlist("a")
#     lista_b = request.GET.getlist("b")
#     html = "<h2>Liste de valori</h2>"
#     if lista_a:
#         html += "<h3>a:</h3><ul>"
#         for val in lista_a:
#             html += f"<li>{val}</li>"
#         html += "</ul>"
#     if lista_b:
#         html += "<h3>b:</hr><ul>"
#         for val in lista_b:
#             html += f"<li>{val}</li>"
#         html += "</ul>"
#     return HttpRespondse(html)       

#ex 3
nr_nume = 0
def numara_nume(request, nume):
    global nr_nume
    pattern = r'^[A-Z][a-z]*(-[A-Z][a-z]+)?\+[A-Z][a-z]*$'
    if re.match(pattern, nume):
        nr_nume += 1
        return HttpResponse(f"Numarul de nume primite: {nr_nume}")
    
#ex 4
def cauta_subsir(request, sir):
    pattern4 = r'\d+([ab]+)\d+'
    match = re.match(pattern4, sir)
    if match:
        subsir_ab = match.group(1)
        l = len(subsir_ab)
        return HttpResponse(f"Lungimea subsirului format doar din a si b este: {l}")
    else:
        return HttpResponse("eroare")
    
#ex 5

def afiseaza_operatii(request):
    d = {
        "lista": [
            {
                "a": 10,
                "b": 20,
                "operatie": "suma"
            },
            {
                "a": 40,
                "b": 20,
                "operatie": "diferenta"
            },
            {
                "a": 25,
                "b": 30,
                "operatie": "suma"
            },
            {
                "a": 40,
                "b": 30,
                "operatie": "diferenta"
            },
            {
                "a": 100,
                "b": 50,
                "operatie": "diferenta"
            }
        ]
    }

    lista_operatii = []
    for element in d["lista"]:
        a = element["a"]
        b = element["b"]
        operatie = element["operatie"]
        if operatie == "suma":
            lista_operatii.append(f"{a} + {b} = {a+b}")
        elif operatie == "diferenta":
            lista_operatii.append(f"{a} - {b} = {a-b}")

    return render(request, "operatii_ex5.html", {"lista_operatii": lista_operatii})
