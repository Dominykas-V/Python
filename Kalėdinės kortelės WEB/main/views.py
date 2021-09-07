#from django.contrib import auth
from os import terminal_size
from django.forms.forms import Form
from django.http import request, response
from django.shortcuts import render, redirect
from .models import Zmogus, WebZinute
from random import randrange

#-----------------------------AUTH-IMPORTS---------------------------
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

#-----------------------------GLOBALS---------------------------
global GLOBAL_SLAPTAZODIS
GLOBAL_SLAPTAZODIS = 'RandomPass1!'

#-----------------------------CLASSES---------------------------
class errorMsg:
    def __init__(self, prob=None, fix=None, link=None, linktxt=None, fix2=None) -> None:
        self.problem = prob
        self.fix = fix
        self.link = link
        self.linktxt = str(linktxt).upper()
        self.fix2 = fix2

    def getProblem(self):
        return self.problem

    def getFix(self):
        return self.fix

    def getLink(self):
        return self.link

    def getLinkText(self):
        return self.linktxt

    def getFix2(self):
        return self.fix2
#---------
class poruAtrinkimoInfo():
    def __init__(self, A=None, B=None, C=None, kieklist=None, allkiek=None) -> None:
        self.Alist = A
        self.Blist = B
        self.Clist = C
        self.Kiekliste = kieklist
        self.AllKiek = allkiek

    def getA(self):
        return self.Alist
    def getB(self):
        return self.Blist
    def getC(self):
        return self.Clist
    def getKiekliste(self):
        return self.Kiekliste
    def getAllkiek(self):
        return self.AllKiek

#-----------------------------ALG------------------------------------
def ZmoniuListoDalinimas3x():
    zmones = Zmogus.objects.all()
    A = []
    B = []
    C = []
    KIEK = 0
    for i in range(0, len(zmones), 3):
        if len(zmones) > i and zmones[i] != None:
            A.append(zmones[i])
        else:
            A.append("")
        if len(zmones) > i+1 and zmones[i+1] != None:
            B.append(zmones[i+1])
        else:
            B.append("")
        if len(zmones) > i+2 and zmones[i+2] != None:
            C.append(zmones[i+2])
        else:
            C.append("")
        KIEK += 1
    return poruAtrinkimoInfo(A=A, B=B, C=C, kieklist=KIEK, allkiek=len(zmones))

#---------
def PridetiPrieSaraso(vardas):
    
    if str(vardas).isalpha() == False:  
        return errorMsg(prob="Vardas gali turėti tik abėcėlės raides! Vardas negali turėti tarpų( ) ar skaičių(0123...).", fix="Galite tiesiog eiti į", link="/rinkimas", linktxt="ATRINKIMĄ", fix2=", bet nematysite savo poros.")
    for name in Zmogus.objects.all():       
        if str(name).upper() == str(vardas).upper():
            return errorMsg(prob="Jūsų įvestas vardas jau yra sistemoje!", fix="Galite tiesiog eiti į", link="/rinkimas", linktxt="ATRINKIMĄ", fix2=", bet nematysite savo poros.")
    z = Zmogus()
    z.vardas = str(vardas)
    z.save()
    user = User.objects.create_user(username=vardas, password=GLOBAL_SLAPTAZODIS)
    return True

#---------
def DeleteUser(name):
    if name == "Domas" or name == "Admin":
        try:
            z = Zmogus.objects.get(vardas=name)
            z.delete()
            return f"{name} - pašalintas iš sąrašo, bet 'MAIN VARTOTOJŲ' duomenų bazėje liko. ~(apsaugotas vardas)~"
        except Zmogus.DoesNotExist:
            return f"!{name} - sąraše nėra. 'db.sqlite3'"
    try:
        u = User.objects.get(username = name)
        u.delete()                
    except User.DoesNotExist:
        return f"!{name} - buvo nepašalintas! {name} - nėra duomenų bazėje. 'MAIN VARTOTOJŲ'"
    try:
        z = Zmogus.objects.get(vardas=name)
        z.delete()
    except Zmogus.DoesNotExist:
        return f"!{name} - buvo nepašalintas! {name} - nėra duomenų bazėje. 'db.sqlite3'"
    return f"{name} - pašalintas sėkmingai!"

#---------
def DeleteUsers(zmones):

    klaidos = 0 
    for vardas in zmones:
        if DeleteUser(vardas)[:1] == "!":
            klaidos += 1 
    return klaidos
#---------
def PoruAtrinkimas():
    zmones = Zmogus.objects.all()
    if float(len(zmones)) % 2 != 0: 
        return False
    for item in zmones:
       item.pora = "________"
       item.arPanaudotas = False
       item.save(update_fields=['pora', 'arPanaudotas'])
    for i in range(0, len(zmones)):
        while zmones[i].pora == "________":
            key = randrange(0, len(zmones))
            if zmones[key].arPanaudotas == False and key != i:
                zmones[key].arPanaudotas = True
                zmones[i].pora = zmones[key].vardas
                zmones[i].save(update_fields=['pora'])
                zmones[key].save(update_fields=['arPanaudotas'])   
    return True

#-----------------------------URL-LOGIC-----------------------------------
def LogIn(response):
    if response.user.is_authenticated:
        if response.method == "POST":
            if response.POST['but'] == "Atrinkimas":
                return redirect("Rinkimas")
            if response.POST['but'] == "Atsijungti":
                return redirect("/acc/logout")
        error = errorMsg(prob="Jūs jau esate prisijungęs!")
        return render(response, 'main/LogIn.html', {"pavadinimas":"PRISIJUNGIMAS", "Error": error})
    else:
        if response.method == "POST":
            error = PridetiPrieSaraso(response.POST['vardas'])
            if error != True:         
                return render(response, 'main/LogIn.html', {"pavadinimas":"PRISIJUNGIMAS", "Error": error})       
            userauth = authenticate(username=str(response.POST['vardas']), password=GLOBAL_SLAPTAZODIS)
            login(response, userauth)  
            return redirect("Rinkimas")
        return render(response, 'main/LogIn.html', {"pavadinimas":"PRISIJUNGIMAS"})

#---------
def Rinkimas(response):
    zmoniulistas = ZmoniuListoDalinimas3x()
    if response.user.is_authenticated:
        zm = Zmogus.objects.get(vardas=response.user.username)
    else:
        zm = False      
    return render(response, 'main/Rinkimas.html', {"pavadinimas":"ATRINKIMAS", "Zinute": str(WebZinute.objects.all()), "ZmoniuListas": zmoniulistas, "User": zm})

#---------    
def AdminLogIn(response):
    if response.method == "POST":
        if response.POST['adminkey'] == "raktas123":
            zm = Zmogus.objects.get(vardas=response.user.username)
            zm.admin = True
            zm.save()
            return redirect('AdminPanel')
    return render(response, 'main/AdminLogIn.html', {"pavadinimas":"ADMIN PRISIJUNGIMAS"})

#---------
def AdminPanel(response):
    zmoniulistas = ZmoniuListoDalinimas3x()
    if response.method == "POST":
        if response.POST['ButtonPress'] == "IŠRINKTI VISIEM PORAS":
            if PoruAtrinkimas():
                zm = Zmogus.objects.all()
                for z in zm:
                    print(f"{z.vardas:10} {z.pora:10} {z.arPanaudotas:5}")
                return render(response, 'main/AdminPanel.html', {"pavadinimas":"VALDYMO SKYDAS", "ZmoniuListas": zmoniulistas, "PRANESIMAS": "Žmonės sugrupuoti."})   
            else:
                return render(response, 'main/AdminPanel.html', {"pavadinimas":"VALDYMO SKYDAS", "ZmoniuListas": zmoniulistas, "PRANESIMAS": "Žmonės nesugrupuoti. Nelyginis skaičius žmonių!"})
        if response.POST['ButtonPress'] == "Vygdyti":
            if response.POST['komanda'] == 'none' or None:
                return render(response, 'main/AdminPanel.html', {"pavadinimas":"VALDYMO SKYDAS", "ZmoniuListas": zmoniulistas, "PRANESIMAS": "Nepasirinkote jokios komandos!"})
            if response.POST['komanda'] == 'add':
                res = PridetiPrieSaraso(response.POST['vardas'])
                if res != True:
                    return render(response, 'main/AdminPanel.html', {"pavadinimas":"VALDYMO SKYDAS", "ZmoniuListas": zmoniulistas, "PRANESIMAS": res})
                return render(response, 'main/AdminPanel.html', {"pavadinimas":"VALDYMO SKYDAS", "ZmoniuListas": zmoniulistas, "PRANESIMAS": f"{response.POST['vardas']} - pridėtas prie sąrašo!"})
            if response.POST['komanda'] == 'del':
                return render(response, 'main/AdminPanel.html', {"pavadinimas":"VALDYMO SKYDAS", "ZmoniuListas": zmoniulistas, "PRANESIMAS": DeleteUser(response.POST['vardas'])})   
            if response.POST['komanda'] == 'surastipora':
                zmogus = Zmogus.objects.get(vardas=response.POST['vardas']) 
                return render(response, 'main/AdminPanel.html', {"pavadinimas":"VALDYMO SKYDAS", "ZmoniuListas": zmoniulistas, "PRANESIMAS": f"{zmogus.vardas} --PORA--> {zmogus.pora}"})               
            if response.POST['komanda'] == 'clear':
                if response.POST['vardas'].upper() == 'TVIRTINU':
                    klaidos = DeleteUsers(Zmogus.objects.all())
                    return render(response, 'main/AdminPanel.html', {"pavadinimas":"VALDYMO SKYDAS", "ZmoniuListas": zmoniulistas, "PRANESIMAS": f"Klaidų išvalant sąrašą: {klaidos}"})
                else:
                    return render(response, 'main/AdminPanel.html', {"pavadinimas":"VALDYMO SKYDAS", "ZmoniuListas": zmoniulistas, "PRANESIMAS": "Blogas raktinis žodis"})
    return render(response, 'main/AdminPanel.html', {"pavadinimas":"VALDYMO SKYDAS", "ZmoniuListas": zmoniulistas, "PRANESIMAS": "~PRANEŠIMAS~"})

#---------
def testhtml(response):
    zmoniulistas = ZmoniuListoDalinimas3x()    
    return render(response, 'main/testhtml.html', {"pavadinimas":"ATRINKIMAS", "ZmoniuListas": zmoniulistas})

#--------------------------------------------------------------------
    