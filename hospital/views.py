from django.db.utils import IntegrityError, InternalError
from django.shortcuts import render, HttpResponse, redirect
from Pais.models import Pais
from Localidad.models import Localidad
from Escuela.models import Escuela
from persona.forms import *
from obraSocial.models import ObraSocial
from persona.models import Persona
from django.core.paginator import Paginator
from django.db.models import Q, Min 
from django.contrib.auth.hashers import make_password#, check_password
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.db.models import F, Func



def login_adm(request):
    
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            msg = "El usuario y/o contraseña ingresados no son correctos, intente nuevamente."
            return render(request, 'login.html', {'msg': msg})
            
            
    return render(request, 'login.html')

def logout_adm(request):
    logout(request)
    return redirect('login')


def enable_admin(request):
    if request.user.is_superuser == False:
        return redirect('home')
    
    admins = User.objects.all().filter(is_superuser='False').order_by('last_name', 'first_name')
    
    if request.POST.get("id_user"):
        id = request.POST.get("id_user")
        admin = User.objects.get(id=id)
        hab = request.POST.get("habilitar")
        
        if admin.is_active: 
            admin.is_active = False
            saveReg(admin)
        else:
            admin.is_active = True
            saveReg(admin)

        return render(request, 'habilitar_admin/index.html', {'admins': admins, 'admin': admin,'id_user': id})
    return render(request, 'habilitar_admin/index.html', {'admins': admins})

    

def create_user_login(request):
    if request.user.is_superuser == False:
        return redirect('home')

    if request.POST:
        try:
            adm_user = request.POST.get('admin_user').strip(" ")
            adm_pass = request.POST.get('admin_pass')

            username = request.POST.get('username')
            password = request.POST.get('password')
            name = request.POST.get('name').strip(" ").upper()
            lname = request.POST.get('lname').strip(" ").upper()
            email = request.POST.get('email').strip(" ").upper()

            test = authenticate(request, username=adm_user, password=adm_pass)

            if test == request.user:#el usuario es validado
                user = User.objects.create_user(username, email, password)
                user.first_name = name
                user.last_name = lname
                user.is_superuser = False
                user.is_staff = True
                user.email = email
                user.save()
                msg = f"El usuario {username} se creó correctamente"
                return render(request, 'crear_admin/success.html', {'msg':msg})
            else:
                msg = f"Error al ingresar los datos del administrador actual, ingrese nuevamente el usuario y contraseña"
                return render(request, 'crear_admin/error.html', {'msg':msg})    

        except IntegrityError:
            msg = f"El usuario {username} ya existe"
            return render(request, 'crear_admin/error.html', {'msg':msg})
        except:
            msg = "Ocurrió un error inesperado"
            return render(request, 'crear_admin/error.html', {'msg':msg})
    else:
         return render(request, 'crear_admin/index.html', {})


def edit_user_login(request):
    if request.POST:#se hizo submit
        try:
            adm_user = request.POST.get('admin_user').strip(" ")
            adm_pass = request.POST.get('admin_pass')

            username = request.POST.get('username')
            password = request.POST.get('password')
            name = request.POST.get('name').strip(" ").upper()
            lname = request.POST.get('lname').strip(" ").upper()
            email = request.POST.get('email').strip(" ").upper()

            test = authenticate(request, username=adm_user, password=adm_pass)

            if test == request.user:
                user = User.objects.get(username=request.user)
                user.first_name = name
                user.last_name = lname
                user.email = email
                user.is_staff = True
                user.password = make_password(password)
                user.username = username
                user.save()
                msg = f"El usuario {request.user} se editó correctamente"
                return render(request, 'editar_admin/success.html', {'msg':msg})
            else:
                msg = f"Error al ingresar los datos del administrador actual, ingrese nuevamente el usuario y contraseña"
                return render(request, 'editar_admin/error.html', {'msg':msg})    

        except IntegrityError:
            msg = f"El usuario {username} ya existe"
            return render(request, 'editar_admin/error.html', {'msg':msg})
        except:
            msg = "Ocurrió un error inesperado"
            return render(request, 'editar_admin/error.html', {'msg':msg})
    else:#No se hizo submit
         
        try:
            user = User.objects.get(username=request.user)
        except:
            user = None
         
    return render(request, 'editar_admin/index.html', {'user': user})


    
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
def getPaises():
    return Pais.objects.all().order_by('pais')

def getOSociales():
    return ObraSocial.objects.all().order_by('obraSocial')

def getLocalidades():
    return Localidad.objects.all().order_by('localidad')

def getEscuelas():
    return Escuela.objects.all().order_by('escuela')

fechaActual = datetime.now()
anio = fechaActual.year
byName = ''
isActivated = False

def set_anio(param):
    global anio 
    anio = param

def get_anio():
    return anio

def getPersonabyID(p)->Persona:
    try:
        return Persona.objects.get(idPersona=p)
    except:
        return None
    
def getPersonabyDNI(p):
    try:
        return Persona.objects.get(dni=p)
    except:
        return None

def handle_not_found(request, exception):
    return render(request, "not_found.html")


def saveReg(reg):

    try:
        reg.save()
        result = 0
        return result
    except IntegrityError:
        result = 1
        return result
    except:
        result = 2
        return result


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
        osociales = getOSociales()
    else:
        escuelas = getEscuelas()

def updateReg(request):
    
    if request.POST.get('update')=='True': #Si se hizo submit en el form para editar
        p = request.POST
        idPersona = p.get('idPersona')

        pers = getPersonabyID(idPersona)#Persona.objects.get(idPersona=idPersona)
        pers.nombre = p.get('name').upper().strip(" ")
        pers.apellido = p.get('lname').upper().strip(" ")
        pers.dni = p.get('dni')
        pers.sexo = p.get('sexo')

        if p.get('cel')==None:
            pers.cel = 0
        else:
            pers.cel = p.get('cel')

        pers.dir = p.get('dir').upper().strip(" ")
        pers.email = p.get('email').upper().strip(" ")
        pers.barrio = p.get('barrio').upper().strip(" ")
        pers.dniTutor = p.get('dniTutor')
        pers.pmot = p.get('pmot').upper().strip(" ")
        pers.nac = p.get('nac')
        pers.idPais = Pais.objects.get(idPais=p.get('idPais'))
        pers.idObra = ObraSocial.objects.get(idOsocial=p.get('idObra'))
        pers.idLocalidad = Localidad.objects.get(idLocalidad=p.get('idLocalidad'))
        pers.idEsc = Escuela.objects.get(idEsc=p.get('idEsc'))
        res = saveReg(pers)
        return res
    else:
        return -1
    
def create(request):#index
    if isActivatedFunc()==False:
        return isActivatedView(request) 
    
    if request.POST:
        P = request.POST #P mayúscula, la otra es minúscula
        #asigno los valores del form al objeto persona
        p = Persona()
        p.idPersona = Persona.objects.all().__len__()+1
        p.nombre = P['name'].upper().strip(" ")
        p.apellido = P['lname'].upper().strip(" ")
        p.dni = P['dni']
        if P.get('cel') == "":
            p.cel =  0
        else:
            p.cel = P['cel']

        p.dir = P['dir'].upper().strip(" ")
        p.email = P['email'].upper().strip(" ")
        p.barrio = P['barrio'].upper().strip(" ")
        p.dniTutor = P['dniTutor']
        p.pmot = P['pmot'].upper().strip(" ") #padre madre o tutor
        p.sexo = P['sexo']
        p.idPais = Pais.objects.get(idPais=P['pais'])
        p.idObra = ObraSocial.objects.get(idOsocial=P['osocial'])
        p.idLocalidad = Localidad.objects.get(idLocalidad=P['localidad'])
        p.idEsc = Escuela.objects.get(idEsc=P['escuela'])
        p.nac = P['nac']

        res = saveReg(p)

        if res == 0:
            return render(request, "create/success.html")
        elif res == 1:
            return render(request, "create/error.html", {'error': 'El DNI ingresado ya existe!'})
        else:
            return render(request, "create/error.html", {'error': 'Ocurrió un error inesperado, intente nuevamente!'})
    else:#Si No hay nada en el POST
        return render(request, "create/index.html", {'paises': getPaises(), 'osociales': getOSociales(), 'localidades': getLocalidades(), 'escuelas': getEscuelas()})

#********************************************BUSCAR POR DNI**************************************
def buscarPorDNI(request):#Vista nueva Obra Social
    if isActivatedFunc()==False:
        return isActivatedView(request)
    updateReg(request)

    P = getPersonabyDNI(request.POST.get('dni'))
    if P == None:
        P = getPersonabyID(request.POST.get('idPersona'))

    if request.POST:#se hizo submit
        if P == None: #si el dni no se ingresó o si no se encuentra nada
            error = 'No se encontró el DNI ingresado'
            return render(request, "listado/buscarPorDNI/index.html", {'error': error})
        else: #si el dni SE INGRESÓ
            ctx = {'paises': getPaises(), 'osociales': getOSociales(), 'localidades': getLocalidades(), 'escuelas':getEscuelas(), 'persona':P}
            return render(request, "listado/verAlfa.html", ctx)
    else:
        return render(request, "listado/buscarPorDNI/index.html")
        

def listado(request):
    if isActivatedFunc()==False:
        return isActivatedView(request) 
    return render(request, "listado/index.html")
#************************************LISTADO POR NOMBRE************************************
def buscarPorNombre(request):#EDIT
    #TERCERO
    byName = ""
    if isActivatedFunc()==False:
        return isActivatedView(request)
    res = updateReg(request)

    if request.POST.get('idPersona') != None:#se aprieta el botón VER
        persona = getPersonabyID(request.POST.get('idPersona'))
        ctx = {'persona': persona, 'paises': getPaises(), 'osociales': getOSociales(), 'localidades':getLocalidades(), 'escuelas':getEscuelas()}
        return render(request, 'listado/verAlfa.html', ctx)

    if request.POST.get('byName') != None and request.POST.get('byName').strip(" ") != "":# se buscó algo
        
        byName = request.POST.get('byName')
        chicos = Persona.objects.all().filter(Q(nombre__icontains=byName)|Q(apellido__icontains=byName))
        if chicos: #Se encuentra un pendejo
            paginator = Paginator(chicos, 10)
            page = request.GET.get('page')
            chicos = paginator.get_page(page)
            return render(request, 'listado/buscarPorNombre/index.html', {'chicos': chicos}) #se muestran resultados
        else:#No se encuentra ningún pendejo
            return render(request, 'listado/buscarPorNombre/index.html', {'error': 'No se encontró ningún niño con el nombre indicado'})
    else:#no se buscó nada

        return render(request, 'listado/buscarPorNombre/index.html')
   
#******************************************LISTADO ALFABÉTICO********************************
def listado_alf(request):#EDIT

    if isActivatedFunc()==False:
        return isActivatedView(request) 
    P = request.POST.get('idPersona')

    if P == None : #Si no se apretó ningun botón "Ver"
        chicos = Persona.objects.all().order_by('apellido', 'nombre')
        paginator = Paginator(chicos, 10)
        page = request.GET.get('page')
        chicos = paginator.get_page(page)
        return render(request, "listado/listarAlfabetico.html", {'chicos': chicos, 'idPersona':P})
    else: #Si se apretó Algún botón "ver"
        updateReg(request)
        persona = Persona.objects.get(idPersona=P)
        ctx = {'idPersona': P, 'persona': persona, 'paises': getPaises(), 'osociales': getOSociales(), 'localidades': getLocalidades(), 'escuelas':getEscuelas()}
        return render(request, 'listado/verAlfa.html', ctx)
#*************************************LISTADO POR AÑO*************************************
def listado_porAnio(request):

    if isActivatedFunc()==False:
        return isActivatedView(request)
        
    updateReg(request)

    P = request.POST.get('idPersona')
    if P != None:
        persona = getPersonabyID(P)
        ctx = {'idPersona': P, 'persona': persona, 'paises': getPaises(), 'osociales': getOSociales(), 'localidades': getLocalidades(), 'escuelas':getEscuelas()}
        return render(request, 'listado/verAlfa.html', ctx)

    anios = Persona.objects.dates('fecha_registro', 'year').distinct()
    listAnios = []
    for a in anios:
        listAnios.append(a.year)

    if len(listAnios) != 0:#si hay registros
        anio_selected = request.POST.get('anio')#si se seleccionó un año
        
        if anio_selected != None:#se seleccionó un año
            chicos = Persona.objects.filter(fecha_registro__year=anio_selected)
            paginator = Paginator(chicos, 10)
            page = request.GET.get('page')
            chicos = paginator.get_page(page)
            ctx = {'anios': listAnios, 'chicos': chicos}
            return render(request, "listado/listarPorAnio.html", ctx)
        else: #No se seleccionó nada todavía; Muestra todos los años
            ctx = {'anios': listAnios}
            return render(request, "listado/listarPorAnio.html", ctx)

    else:#si no existen registros
        ctx = {'error': 'No existen registros todavía en esta base de datos'}
        return render(request, "listado/listarPorAnio.html", ctx)


def NewOS(request):#Vista nueva Obra Social
    if isActivatedFunc()==False:
        return isActivatedView(request) 

    if request.POST:
        os = request.POST #P mayúscula, la otra es minúscula
        ob = ObraSocial()
        ob.idOsocial = ObraSocial.objects.all().__len__()+1
        ob.obraSocial = os['name'].strip().upper()
                
        res = saveReg(ob)
        if res == 0: 
            return render(request, "obraSocial/success.html")
        elif res == 1:
            return render(request, "obraSocial/error.html", {'error': 'La obra social ingresada ya se encuentra registrada'})
        else:
            return render(request, "obraSocial/error.html", {'error': 'Ocurrió un error inesperado'})
    else:
        return render(request, "obraSocial/index.html")
    

def NewEsc(request): #Nueva Escuela
    print(request)
    if isActivatedFunc()==False:
        return isActivatedView(request)

    if request.POST:
        e = request.POST #P mayúscula, la otra es minúscula
        esc = Escuela()
        esc.idEsc = Escuela.objects.all().__len__()+1
        esc.escuela = e['name'].strip().upper()
        res = saveReg(esc)
        if res == 0:
            return render(request, "Escuela/success.html")
        elif res == 1: 
            return render(request, "Escuela/error.html", {'error': 'La Escuela ingresada ya se encuentra registrada'})
        else:
            return render(request, "Escuela/error.html", {'error': 'Ocurrió un error inesperado'})
    else:
        return render(request, "Escuela/index.html")

