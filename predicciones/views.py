from django.shortcuts import render
from django.shortcuts import render_to_response
from .models import *
from django.db.models import Sum, Max
import pandas as pd
from django.conf import settings
import threading
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

# Create your views here.

def porcentaje_partido(partido, trep=True):
    if Mesa.objects.all().count()>0:
        mesas=Mesa.objects.all()
        if trep:
            mesas=mesas.filter(trep=True)
        votos=mesas.aggregate(Sum(partido))[partido+'__sum']
        validos=mesas.aggregate(Sum('validos'))['validos__sum']
        porcentaje=(votos*100)/validos
        return porcentaje
    else:
        return 0

def leer_excel():
    datos=pd.read_excel(settings.MEDIA_ROOT+"/actas.xlsx")
    datos=pd.DataFrame(datos)
    datos=datos.to_dict('records')
    cont=0
    for fila in datos:
        flag_pais=Pais.objects.filter(nombre=fila['País']).count()
        if flag_pais==0:
            pais=Pais(nombre=fila['País'])
            pais.save()
        else:
            pais=Pais.objects.get(nombre=fila['País'])

        flag_dpto=Departamento.objects.filter(numero=fila['Número departamento']).count()
        if flag_dpto==0:
            dpto=Departamento(pais=pais, numero=fila['Número departamento'], nombre=fila['Departamento'])
            dpto.save()
        else:
            dpto=Departamento.objects.get(numero=fila['Número departamento'])

        flag_municipio=Municipio.objects.filter(nombre=fila['Municipio']).count()
        if flag_municipio==0:
            municipio=Municipio(departamento=dpto, nombre=fila['Municipio'])
            municipio.save()
        else:
            municipio=Municipio.objects.get(nombre=fila['Municipio'])

        flag_recinto=Recinto.objects.filter(nombre=fila['Recinto']).count()
        if flag_recinto==0:
            recinto=Recinto(municipio=municipio, nombre=fila['Recinto'])
            recinto.save()
        else:
            recinto=Recinto.objects.get(nombre=fila['Recinto'])
 
        flag_mesa=Mesa.objects.filter(numero=fila['Número Mesa']).count()
        if flag_mesa==0:
            estado=fila['Estado']
            cont+=1
            print("Actas nuevas Leídas:")
            print(cont)
            if estado==100:
                mesa=Mesa(recinto=recinto, numero=fila['Número Mesa'], codigo=fila['Código Mesa'], inscritos=fila['Inscritos'], trep=False)
                mesa.save()
            else:
                mesa=Mesa(recinto=recinto, numero=fila['Número Mesa'], codigo=fila['Código Mesa'], inscritos=fila['Inscritos'], cc=fila['CC'], fpv=fila['FPV'], mts=fila['MTS'], ucs=fila['UCS'], mas=fila['MAS - IPSP'], v1f=fila['21F'], pdc=fila['PDC'], mnr=fila['MNR'], panbol=fila['PAN-BOL'], validos=fila['Votos Válidos'], blancos=fila['Blancos'], nulos=fila['Nulos'], trep=True)
                mesa.save()

def get_trep_dict():
    cc=porcentaje_partido('cc')
    fpv=porcentaje_partido('fpv')
    mts=porcentaje_partido('mts')
    ucs=porcentaje_partido('ucs')
    mas=porcentaje_partido('mas')
    v1f=porcentaje_partido('v1f')
    pdc=porcentaje_partido('pdc')
    mnr=porcentaje_partido('mnr')
    panbol=porcentaje_partido('panbol')
    blancos=porcentaje_partido('blancos')
    nulos=porcentaje_partido('nulos')
    return dict(cc=cc, fpv=fpv, mts=mts, ucs=ucs, mas=mas, v1f=v1f, pdc=pdc, mnr=mnr, panbol=panbol, blancos=blancos, nulos=nulos)

def get_total_dict():
    cc=porcentaje_partido('cc', False)
    fpv=porcentaje_partido('fpv', False)
    mts=porcentaje_partido('mts', False)
    ucs=porcentaje_partido('ucs', False)
    mas=porcentaje_partido('mas', False)
    v1f=porcentaje_partido('v1f', False)
    pdc=porcentaje_partido('pdc', False)
    mnr=porcentaje_partido('mnr', False)
    panbol=porcentaje_partido('panbol', False)
    blancos=porcentaje_partido('blancos', False)
    nulos=porcentaje_partido('nulos', False)
    return dict(cc_c=cc, fpv_c=fpv, mts_c=mts, ucs_c=ucs, mas_c=mas, v1f_c=v1f, pdc_c=pdc, mnr_c=mnr, panbol_c=panbol, blancos_c=blancos, nulos_c=nulos)

def preparar_datos_trep():
    mesas_trep=Mesa.objects.filter(trep=True)
    X=[] 
    y=[]
    for mesa in mesas_trep:
        #tupla cc
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(1)
        X.append(tupla)
        y.append(mesa.cc)
        #tupla fpv
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(2)
        X.append(tupla)
        y.append(mesa.fpv)
        #tupla mts
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(3)
        X.append(tupla)
        y.append(mesa.mts)
        #tupla ucs
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(4)
        X.append(tupla)
        y.append(mesa.ucs)
        #tupla mas
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(5)
        X.append(tupla)
        y.append(mesa.mas)
        #tupla v1f
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(6)
        X.append(tupla)
        y.append(mesa.v1f)
        #tupla pdc
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(7)
        X.append(tupla)
        y.append(mesa.pdc)
        #tupla mnr
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(8)
        X.append(tupla)
        y.append(mesa.mnr)
        #tupla panbol
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(9)
        X.append(tupla)
        y.append(mesa.panbol)
        #tupla blancos
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(11)
        X.append(tupla)
        y.append(mesa.blancos)
        #tupla nulos
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(12)
        X.append(tupla)
        y.append(mesa.nulos)
    return np.array(X), np.array(y)

def preparar_datos_faltantes():
    mesas_faltantes=Mesa.objects.filter(trep=False)
    X=[]
    mesas_ids=[]
    for mesa in mesas_faltantes:
        #tupla cc
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(1)
        X.append(tupla)
        mesas_ids.append(mesa.id)
        #tupla fpv
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(2)
        X.append(tupla)
        mesas_ids.append(mesa.id)
        #tupla mts
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(3)
        X.append(tupla)
        mesas_ids.append(mesa.id)
        #tupla ucs
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(4)
        X.append(tupla)
        mesas_ids.append(mesa.id)
        #tupla mas
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(5)
        X.append(tupla)
        mesas_ids.append(mesa.id)
        #tupla v1f
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(6)
        X.append(tupla)
        mesas_ids.append(mesa.id)
        #tupla pdc
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(7)
        X.append(tupla)
        mesas_ids.append(mesa.id)
        #tupla mnr
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(8)
        X.append(tupla)
        mesas_ids.append(mesa.id)
        #tupla panbol
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(9)
        X.append(tupla)
        mesas_ids.append(mesa.id)
        #tupla blancos
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(11)
        X.append(tupla)
        mesas_ids.append(mesa.id)
        #tupla nulos
        tupla=[]
        tupla.append(mesa.recinto.municipio.departamento.pais.id)
        tupla.append(mesa.recinto.municipio.departamento.id)
        tupla.append(mesa.recinto.municipio.id)
        tupla.append(mesa.recinto.id)
        tupla.append(12)
        X.append(tupla)
        mesas_ids.append(mesa.id)
    return np.array(X), np.array(mesas_ids)

def entrenar_modelo():
    max_inscitos_by_mesa=Mesa.objects.all().aggregate(Max('inscritos'))['inscritos__max']
    print("preparando datos trep...")
    X, y = preparar_datos_trep()
    #y=to_categorical(y, num_classes=max_inscitos_by_mesa)
    print("Entrenando modelo...")
    poly=PolynomialFeatures(degree=2)
    X=poly.fit_transform(X)
    modelo=LinearRegression()
    modelo.fit(X,y)
    pred_test=modelo.predict(X)
    print("preparando datos faltantes...")
    X_faltantes, mesas_ids=preparar_datos_faltantes()
    X_not_transform=X_faltantes
    X_faltantes=poly.fit_transform(X_faltantes)
    print("completando datos...")
    predicciones=modelo.predict(X_faltantes)
    pos_x=0
    last_mesa_id=-1
    for fila in predicciones:
        fila=int(fila)
        mesa_id=mesas_ids[pos_x]
        partido=X_not_transform[pos_x][4]
        pos_x+=1
        if last_mesa_id!=mesa_id:
            mesa=Mesa.objects.get(id=mesa_id)
            last_mesa_id=mesa.id
        if partido==1:
            mesa.cc=fila
        if partido==2:
            mesa.fpv=fila
        if partido==3:
            mesa.mts=fila
        if partido==4:
            mesa.ucs=fila
        if partido==5:
            mesa.mas=fila
        if partido==6:
            mesa.v1f=fila
        if partido==7:
            mesa.pdc=fila
        if partido==8:
            mesa.mnr=fila
        if partido==9:
            mesa.panbol=fila
        if partido==11:
            mesa.blancos=fila
        if partido==12:
            mesa.nulos=fila
            mesa.validos=(mesa.cc+mesa.fpv+mesa.mts+mesa.ucs+mesa.mas+mesa.v1f+mesa.pdc+mesa.mnr+mesa.panbol)
            mesa.save()
    print("Los datos se han completado")
    
def comparativa_datos(request): 
    trep=get_trep_dict()
    D=trep
    plt.bar(range(len(D)), D.values(), align='center') 
    plt.xticks(range(len(D)), list(D.keys())) 
    plt.savefig(settings.MEDIA_ROOT+"/trep.png")
    completo=get_total_dict()
    D=completo
    plt.bar(range(len(D)), D.values(), align='center') 
    plt.xticks(range(len(D)), list(D.keys())) 
    plt.savefig(settings.MEDIA_ROOT+"/completo.png")
    plt.cla()
    completo.update(trep)
    return render_to_response('comparativa.html', completo)

def predecir_votos(request):
    hilo=threading.Thread(target=entrenar_modelo, daemon=True)
    hilo.start()
    return render_to_response('iniciarprediccion.html')

def cargar_datos(request):
    hilo=threading.Thread(target=leer_excel, daemon=True)
    hilo.start()
    return render_to_response('excelcargado.html')

def main(request): 
    trep=get_trep_dict()
    D=trep
    plt.bar(range(len(D)), D.values(), align='center') 
    plt.xticks(range(len(D)), list(D.keys())) 
    plt.savefig(settings.MEDIA_ROOT+"/trep.png")
    plt.cla()
    return render_to_response('index.html', trep)