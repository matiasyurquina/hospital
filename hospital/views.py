#from queue import Empty
from email import message
from queue import Empty
from urllib import request
from django.db.utils import IntegrityError, InternalError
from django.shortcuts import render, HttpResponse
from Pais.models import Pais
from Localidad.models import Localidad
from Escuela.models import Escuela
from Escuela.forms import FormNewEsc
from persona.forms import *
from obraSocial.models import ObraSocial
from obraSocial.forms import FormNewObra
from persona.models import Persona
from django.core.paginator import Paginator
from django.db import connection
from persona.forms import FormNewPerson
from django.db.models import Q, Min 
from django.contrib.auth.hashers import make_password#, check_password
from datetime import datetime
from django.http import HttpResponse

import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

#*************QuerySets Varios***********
global paises 
paises = Pais.objects.all().order_by('pais')
global osociales 
osociales = ObraSocial.objects.all().order_by('obraSocial')
global localidades 
localidades = Localidad.objects.all()
global escuelas 
escuelas = Escuela.objects.all().order_by('escuela')
#*********************variables globales*************
anio=2022
isActivated = False

def set_anio(param):
    global anio 
    anio = param

def get_anio():
    return anio

byName = ''
def set_byName(param):
    global byName 
    byName = param

def get_byName():
    return byName

def handle_not_found(request, exception):
    return render(request, "not_found.html")


def isActivatedFunc():
    try:#selecciono el primer registro
        reg = Activator.objects.get(id=Activator.objects.aggregate(Min('id')).get('id__min')) #retorna el primer elemento
    except:
        reg = None #si no existe le doy valor nulo a reg

    if reg == None: #Si no tiene ningún registro
        try:
            reg = Activator()
            reg.activation_code = str(random.randint(1000000000, 9999999999))
            reg.activation_code_encoded = make_password(reg.activation_code)
            reg.save()
            #creo un registro con número de activación
            return False
        except:
            return False
    else:
        if reg.activated == False: #si no está activado
            return False
    return True

def isActivatedView(request): #Devuelve si no está activado
    if isActivatedFunc()==False: #no está activado
        reg = Activator.objects.get(id=Activator.objects.aggregate(Min('id')).get('id__min')) #retorna el primer elemento
        if request.POST.get('txtActivate') != None: #si se hizo submit
            if reg.activation_code_encoded == request.POST.get('txtActivate'): #si son iguales
                reg.activated = True #si son iguales, se activa
                reg.save()
                return render(request, "create/index.html", {'activated': 'El programa se activó correctamente'})
            else: #si no coinciden los códigos
                ctx = {'activation_code': reg.activation_code, 'error':'Código inválido'}
                return render(request, "activate.html", ctx)
        else:#NO se hizo submit
            ctx = {'activation_code': reg.activation_code}
            return render(request, "activate.html", ctx)
    else:#está activado
        updateList(1)
        updateList(2)
        return render(request, "create/index.html") 

def updateList(param):#actualizar Lista de escuelas u obras sociales
    if param == 1:
        osociales = ObraSocial.objects.all().order_by('obraSocial')
    else:
        escuelas = Escuela.objects.all().order_by('escuela')

def updateReg(request):

    if request.POST.get('update')=='True': #Si se hizo submit en el form para editar
        p = request.POST
        idPersona = f"{p.get('idPersona')}"
        name = f"'{p.get('name')}'"
        lname= f"'{p.get('lname')}'"
        dni = f"{p.get('dni')}"
        sexo = f"{p.get('sexo')}"

        if p.get('cel')==None:
            cel = 0
        else:
            cel = f"{p.get('cel')}"

        dir = f"'{p.get('dir')}'"
        email = f"'{p.get('email')}'"
        barrio = f"'{p.get('barrio')}'"
        dniTutor = f"{p.get('dniTutor')}"
        tutor = f"'{p.get('tutor')}'"
        nac = f"'{p.get('nac')}'"
        idObra = f"{p.get('idObra')}"
        idPais = f"{p.get('idPais')}"
        idLocalidad = f"{p.get('idLocalidad')}"
        idEsc = f"{p.get('idEsc')}"
        try:
            sql = connection.cursor()
            arg = f"SELECT * FROM editar_registro({idPersona}, {dni}, {name}, {lname}, {sexo}, {nac}, {email}, {cel}, {dir}, {barrio}, {idLocalidad}, {idPais}, {idEsc}, {idObra}, {tutor}, {dniTutor})"
            sql.execute(arg)
        except InternalError as msg:
            persona = Persona.objects.get(idPersona=idPersona)
            msgError = str(msg.__context__).split('\n')
            ctx = {'idPersona': idPersona, 'persona': persona, 'paises': paises, 'osociales': osociales, 'localidades':localidades, 'escuelas':escuelas, 'error': msgError[0]}
            return render(request, 'listado/verAlfa.html', ctx)
    
def create(request):#index
    if isActivatedFunc()==False:
        return isActivatedView(request) 

    if request.method == "POST":
        frm=FormNewPerson(request.POST)
        if frm.is_valid(): #se validaron los datos
            try:
                    for p in request.POST:
                        p.strip() #le hago trim() a todos los parámetros

                    P = request.POST #P mayúscula, la otra es minúscula
                    #asigno los valores del form al objeto persona
                    p = Persona()
                    p.idPersona = Persona.objects.all().__len__()+1
                    p.nombre = P['name'].upper()
                    p.apellido = P['lname'].upper()
                    p.dni = P['dni']
                    if p.cel == None:
                        p.cel =  0
                    else:
                        p.cel =  P['cel']

                    p.calle = P['dir'].upper()
                    p.email = P['email']
                    p.barrio = P['barrio'].upper()
                    p.dniTutor = P['dniTutor']
                    p.pmot = P['tutor'].upper() #padre madre o tutor
                    p.idPais = Pais.objects.get(idPais=P['pais'])
                    p.sexo = P['sexo']
                    p.idObra = ObraSocial.objects.get(idOsocial=P['osocial'])
                    p.idLocalidad = Localidad.objects.get(idLocalidad=P['localidad'])
                    p.idEsc = Escuela.objects.get(idEsc=P['escuela'])
                    p.nac = P['nac']
                    p.save()

                    return render(request, "create/success.html")
            except IntegrityError:#error de llaves duplicadas
                return render(request, "create/error.html", {'error': 'El DNI ingresado ya existe!'})
            except:
                return render(request, "create/error.html", {'error': 'Ocurrió un error inesperado, intente nuevamente!'})
        else:#se ingresa por primera vez
            return render(request, "create/index.html")
    else:#Si el método es distintoa POST
        return render(request, "create/index.html", {'paises': paises, 'osociales': osociales, 'localidades': localidades, 'escuelas': escuelas})

def update(request):
    form=FormNewPerson(request.POST)
    return render(request, "update/index.html")
#********************************************BUSCAR POR DNI**************************************
def buscarPorDNI(request):#Vista nueva Obra Social
    if isActivatedFunc()==False:
        return isActivatedView(request) 

    P = request.POST.get('dni')
    
    updateReg(request)
    
    if P == None: #si el dni no se ingresó
        return render(request, "listado/buscarPorDNI/index.html")
    else: #si el dni SE INGRESÓ
        try:
            persona = Persona.objects.get(dni=P)
            ctx = {'paises': paises, 'osociales': osociales, 'localidades': localidades, 'escuelas':escuelas, 'persona':persona}
            return render(request, "listado/verAlfa.html", ctx)
        except:
            error = 'No se encontró el DNI ingresado'
            return render(request, "listado/buscarPorDNI/index.html", {'error': error})
        

def listado(request):
    if isActivatedFunc()==False:
        return isActivatedView(request) 
    return render(request, "listado/index.html")
#************************************LISTADO POR NOMBRE************************************
def buscarPorNombre(request):#EDIT
    #TERCERO
    if isActivatedFunc()==False:
        return isActivatedView(request) 

    updateReg(request)
    if request.POST.get('byName') != None:
        set_byName(request.POST.get('byName'))
    if request.POST.get('idPersona') != None:#se aprieta el botón VER
        P = request.POST.get('idPersona')
        persona = Persona.objects.get(pk=P)
        try:
            ctx = {'idPersona': P, 'persona': persona, 'paises': paises, 'osociales': osociales, 'localidades':localidades, 'escuelas':escuelas}
            return render(request, 'listado/verAlfa.html', ctx)
        except:
            return render(request, 'listado/buscarPorNombre/index.html', {'error': 'Ocurrió un error insperado'})

    if get_byName() == '': #Recién ingresa
        return render(request, 'listado/buscarPorNombre/index.html')
    else: #Se busca un nombre
        chicos = Persona.objects.all().filter(Q(nombre__icontains=get_byName())|Q(apellido__icontains=get_byName()))
        if chicos: #Se encuentra un pendejo
            paginator = Paginator(chicos, 10)
            page = request.GET.get('page')
            chicos = paginator.get_page(page)
            return render(request, 'listado/buscarPorNombre/index.html', {'chicos': chicos}) #se muestran resultados
        else:#No se encuentra ningún pendejo
            return render(request, 'listado/buscarPorNombre/index.html', {'error': 'No se encontró ningún niño con el nombre indicado'})
#******************************************LISTADO ALFABÉTICO********************************
def listado_alf(request):#EDIT

    if isActivatedFunc()==False:
        return isActivatedView(request) 

    updateReg(request)
    
    # if request.POST.get('dni') != None and request.POST.get('idPersona') == None:
    #     persona = Persona.objects(dni=request.POST.get('dni'))
    #     request.POST['idPersona'] = persona.idPersona
    
    P = request.POST.get('idPersona')

    if P == None : #Si no se apretó ningun botón "Ver"
        chicos = Persona.objects.all().order_by('apellido', 'nombre')
        paginator = Paginator(chicos, 10)
        page = request.GET.get('page')
        chicos = paginator.get_page(page)
        return render(request, "listado/listarAlfabetico.html", {'chicos': chicos, 'idPersona':P})
    else: #Si se apretó Algún botón "ver"

        persona = Persona.objects.get(idPersona=P)
        ctx = {'idPersona': P, 'persona': persona, 'paises': paises, 'osociales': osociales, 'localidades':localidades, 'escuelas':escuelas}
        return render(request, 'listado/verAlfa.html', ctx)
#*************************************LISTADO POR AÑO*************************************
def listado_porAnio(request):

    if isActivatedFunc()==False:
        return isActivatedView(request) 
        
    updateReg(request)
    P = request.POST.get('idPersona')
    if P != None:
        persona = Persona.objects.get(idPersona=P)
        ctx = {'idPersona': P, 'persona': persona, 'paises': paises, 'osociales': osociales, 'localidades':localidades, 'escuelas':escuelas}
        return render(request, 'listado/verAlfa.html', ctx)

    
    if request.POST.get('anio') != None:
        set_anio(request.POST.get('anio'))

    arg = f"select * from get_all_years()"
    sql = connection.cursor()
    sql.execute(arg)
    anios = list() #creo lista vacia

    for tupla in sql: #guardo las tuplas en la lista anios
        anios.append(str(tupla).strip("('',)") )    
    chicos = Persona.objects.filter(fecha_registro__year=get_anio ())
    paginator = Paginator(chicos, 10)
    page = request.GET.get('page')
    chicos = paginator.get_page(page)
    ctx = {'paises': paises, 'osociales': osociales, 'localidades':localidades, 'escuelas':escuelas, 'chicos': chicos, 'anios': anios}
    return render(request, "listado/listarPorAnio.html", ctx)

def NewOS(request):#Vista nueva Obra Social
    if isActivatedFunc()==False:
        return isActivatedView(request) 

    if request.method == "POST":
        frm=FormNewObra(request.POST)
        if frm.is_valid():
            try:
                P = request.POST #P mayúscula, la otra es minúscula
                ob = ObraSocial()
                ob.idOsocial = ObraSocial.objects.all().__len__()+1
                ob.obraSocial = P['name'].strip().upper()
                ob.save()
                return render(request, "obraSocial/success.html")
            except IntegrityError:
                return render(request, "obraSocial/error.html", {'error': 'La Escuela ingresada ya se encuentra registrada'})
            except:
                return render(request, "obraSocial/error.html", {'error': 'Ocurrió un eror inesperado'})
        else:
            return render(request, "obraSocial/index.html")
    else:
        return render(request, "obraSocial/index.html")
    

def NewEsc(request): #Nueva Escuela

    if isActivatedFunc()==False:
        return isActivatedView(request) 

    if request.method == "POST":  
        frm=FormNewObra(request.POST)
        if frm.is_valid():
            try:
                P = request.POST #P mayúscula, la otra es minúscula
                esc = Escuela()
                esc.idEsc = Escuela.objects.all().__len__()+1
                esc.escuela = P['name'].strip().upper()
                esc.save()
                return render(request, "Escuela/success.html")
            except IntegrityError:
                return render(request, "Escuela/error.html", {'error': 'La Escuela ingresada ya se encuentra registrada'})
            except:
                return render(request, "Escuela/error.html", {'error': 'Ocurrió un error inesperado'})
        else:
            return render(request, "Escuela/index.html")
    else:
        return render(request, "Escuela/index.html")

