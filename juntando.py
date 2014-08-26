# -*- coding: utf-8 -*-
import numpy as np
import time
from osgeo import ogr
'''##############'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
############################
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
c50 = importr('C50')
############################
ini = time.time()
#Create file numpy tmp
file_temp = file("tmp.bin","wb")
# get the driver
driver = ogr.GetDriverByName('ESRI Shapefile')
#Acessar layer ativo em Canvas
layer = qgis.utils.iface.activeLayer()
#Obter caminho shape
pathSHP =layer.dataProvider().dataSourceUri()
pathSHP = pathSHP.split('|')
#Ler layer OGR
shapefile = ogr.Open(str(pathSHP[0]))
#Obter layer
layerOGR = shapefile.GetLayer()
#Iterando sobre a geometria
features = layer.getFeatures()
dados=[]
classes=[]
mean_std=[]
featureOGR = layerOGR.GetFeature(0)
for i, feat in enumerate (features):
    featureOGR = layerOGR.GetFeature(i)
    #Ainserir na lista os valores dos atributos
    dict_values = featureOGR.items()
    classes.append(dict_values['class'])
    dados.append([round(dict_values['z'],2),dict_values['r'],dict_values['g'],dict_values['b']])
    layerOGR.SetSpatialFilter(featureOGR.GetGeometryRef().Buffer(1))
    d=[layerOGR.GetFeature(j).GetField("z") for j in xrange(layerOGR.GetFeatureCount())]
    d = np.asarray(d)
    mean = d.sum()/len(d)
    stedv = d.std(ddof=1)
    mean_std.append([round(mean, 2),round(stedv, 2)])
#Guardar dados em arquivo bin
np.save(file_temp, np.asarray(dados))
np.save(file_temp, np.asarray(mean_std))
file_temp.close()
#Clear memory

del(dados)
del(mean_std)
del(layer)
del(pathSHP)
del(shapefile)
#Leitura do arquivo numpy
file_temp = file("tmp.bin","rb")
data = np.load(file_temp)
mean_std_n = np.load(file_temp)
#print "Data: ", data[-1]," - ","Mean_std: ",mean_std[-1], "d: ",d
fim = time.time()
print 'Tempo minutos: ',(fim - ini)/60

#Decision tree
clas = robjects.FactorVector(classes)
dict_data={'z':robjects.FloatVector(data[:,0]),'r':robjects.IntVector(data[:,1]),'g':robjects.IntVector(data[:,2]),'b':robjects.IntVector(data[:,3])}
dataf = robjects.DataFrame(dict_data)
ad=c50.C5_0(dataf,clas,triasl=20,control=(c50.C5_0Control(minCases = 2, CF = 0.8)))
base = importr('base')
ad=(base.summary(ad))
'''
#create classes factor
res = robjects.FactorVector(d[0,:])
c50.C5_0()
#Create DataFrame
r=np.array([20,23,34,45,56])
r_n=robjects.FactorVector(r)
dataf = robjects.DataFrame({})
d={'r':r_n,'g':g_n,'b':b_n}
dataf = robject.DataFrame(d)
ad=c50.C5_0(dataf,classes,triasl=10,control=(c50.C5_0Control(minCases = 2, CF = 0.2)))
#Ler ad
base = importr('base')
print(base.summary(ad))

'''
strAD = str(ad)

#print strAD
#Transformar AD em Lista
listAD = strAD.split('\n')
#Verifica os colchetes fora de lugar
for i, v in enumerate(listAD):   
     if '{' in v and '}' not in v :
         if '{' in v and '}' not in listAD[i+1] :
             listAD[i+1] = listAD[i+1].replace(':','')
             listAD[i+2] = listAD[i+2].replace(':','')
             listAD[i] = v.strip() + listAD[i+1].strip()+ listAD[i+2].strip()
             listAD.remove(listAD[i+2])
             listAD.remove(listAD[i+1])            
         else:
             listAD[i+1] = listAD[i+1].replace(':','')
             listAD[i] = v.strip() + listAD[i+1].strip()
             listAD.remove(listAD[i+1])
     else:
         pass
     
     
#Contar o número de espaços
#Transformar AD em Lista
listAuxAD = strAD.split('\n')
#contar o numero de ponto-virgula
listAuxAD = [w.replace(':...','#')for w in listAD]
listAuxAD = [w.replace(':   ','#')for w in listAuxAD]
listAuxAD = [w.replace('    ','#')for w in listAuxAD]
#contar o numero de espacos das linhas
numEsp = [w.count('#')for w in listAuxAD]
del listAuxAD

#Verificar a lista 
for i, v in enumerate(listAD):
    p = 'USO'
    
    if v.find(p) != -1:
        limiteNumEsp = numEsp[i-1]
        while limiteNumEsp <  numEsp[i]:
            #print limiteNumEsp, v
            limiteNumEsp = numEsp[i]
        #while limiteNumEsp != numEsp[i] :
        #print v
            
#Inicio da AD
inicioAD = listAD.index('Decision tree:')
#inicia as variáveis

cond=''
controlePrimeiraLinha = 0

#Analise da AD
for index,value in enumerate(listAD):
    #Transforma String em Lista      
    valueLista = value.split()
    #remover impurezas   
    valueLista =[i.replace(':...','') for i in valueLista]  
    valueLista =[i.replace(':','') for i in valueLista]
    valueLista =[i for i in valueLista if i != '']
    #print valueLista
    #Remove o começo da AD
    if index < (inicioAD+2):     
        pass
    #Remove o final
    elif listAD[index].find('Evaluation') != -1:
        break
    
    #Transformando primeira linha
    elif controlePrimeiraLinha == 0:    
            #Controle da primeira linha   
            controlePrimeiraLinha =1
            #Se tiver parenteses tiver parentese inserir 'ELSE'
            if listAD[index].find('(') != -1:
                cond = cond+'CASE WHEN '+str(valueLista[0])+str(valueLista[1])+str(valueLista[2])+' THEN '+ str(valueLista[3])+ ' ELSE '
            else:
                cond = cond+'CASE WHEN '+str(valueLista[0])+str(valueLista[1])+str(valueLista[2])+' THEN '
    #Analisa as linhas que contem ":..."
    elif listAD[index].find(':...') != -1:        
        #Analisa se há '{' e '('
        if listAD[index].find('{') != -1 and listAD[index].find('(') != -1: 
            aux = str(valueLista)[str(valueLista).index('{')+1:str(valueLista).index('}')]
            aux = ' '+ valueLista[0]+' = ' + aux.replace(',',' OR '+valueLista[0]+' = ')
            cond= cond+'CASE WHEN '+aux +' THEN '+ str(valueLista[3])+ ' ELSE '           
            
        #Analisa se há '('   
        elif listAD[index].find('{') != -1: 
            aux = str(valueLista)[str(valueLista).index('{')+1:str(valueLista).index('}')]
            aux = ' '+ valueLista[0]+' = ' + aux.replace(',',' OR '+valueLista[0]+' = ')
            cond= cond+'CASE WHEN '+aux +' THEN '           
            
        elif listAD[index].find('(') != -1:
            cond = cond +' CASE WHEN '+ str(valueLista[0])+str(valueLista[1])+str(valueLista[2])+' THEN '+  str(valueLista[3]) + ' ELSE '
            
        else:
            cond = cond +' CASE WHEN '+ str(valueLista[0])+str(valueLista[1])+str(valueLista[2])+' THEN '
            
    #Analisa as linhas que não contem ":..."
    else:
        if numEsp[index] > numEsp[index+1]: numEsp[index]-numEsp[index+1]
        #Analisa se há '{' e '('
        if listAD[index].find('{') != -1 and listAD[index].find('(') != -1:
            if listAD[index+1]== '':             
                cond= cond +' '+str(valueLista[3])+ (' END '* (numEsp[index]-numEsp[index+1]))                
            else:            
                cond= cond +' '+str(valueLista[3])+ (' END '* (numEsp[index]-numEsp[index+1]))+ ' ELSE '
 
        elif  listAD[index].find('(') != -1: 
            if listAD[index+1]== '':
                cond= cond +' '+str(valueLista[3])+ (' END '* (numEsp[index]-numEsp[index+1]))
            else:  
                cond= cond +' '+str(valueLista[3])+ (' END '* (numEsp[index]-numEsp[index+1]))+ ' ELSE '          
                
        else:
           pass  
        

    

cond = cond +' END '
print cond
