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
#Acessar layer ativo em Canvas
canvas = qgis.utils.iface.mapCanvas()
allLayers = canvas.layers()
#Layer sample
layer_sample = allLayers[0]
#Layer sample
layer_points_clould = allLayers[1]
#Iterando sobre a geometria
features_samples = layer_sample.getFeatures()
features_point_clould = layer_points_clould.getFeatures()
training=[]
classes=[]
mean_std=[]
array_id =[]
data=[]
#Obter index da coluna layer sample
idx_z = layer_sample.fieldNameIndex('z')
idx_r = layer_sample.fieldNameIndex('r')
idx_g = layer_sample.fieldNameIndex('g')
idx_b = layer_sample.fieldNameIndex('b')
idx_clas = layer_sample.fieldNameIndex('class')
for feat in features_samples:
    #Obter 
    attrs = feat.attributes()
    #Criar array para as classes de amostras
    classes.append(attrs[idx_clas])
    #criar array para os valores z,r,g e b
    training.append([round(attrs[idx_z],2),attrs[idx_r],attrs[idx_g],attrs[idx_b]])
#Obter index da coluna layer point clould
idx_z_pc = layer_points_clould.fieldNameIndex('z')
idx_r_pc = layer_points_clould.fieldNameIndex('r')
idx_g_pc = layer_points_clould.fieldNameIndex('g')
idx_b_pc = layer_points_clould.fieldNameIndex('b')
for feat_pc in features_point_clould:
    #Obter valores atributos
    attrs = feat_pc.attributes()
    
    #obter IDs como List
    array_id.append(feat_pc.id())
    #criar array para os valores z,r,g e b
    data.append([round(attrs[idx_z_pc],2),attrs[idx_r_pc],attrs[idx_g_pc],attrs[idx_b_pc]])
#Guardar dados em arquivo bin
np.save(file_temp, np.asarray(training))
np.save(file_temp, np.asarray(array_id))
np.save(file_temp, np.asarray(data))
file_temp.close()
#Clear memory
del(data)
del(training)
del(array_id)

#Leitura do arquivo numpy
file_temp = file("tmp.bin","rb")
#ler o primeiro array do arquivo bin
training = np.load(file_temp)


#print "Data: ", data[-1]," - ","Mean_std: ",mean_std[-1], "d: ",d
#Acessar valores de cada varivavel no array
z_train=training[:,0]
r_train=training[:,1]
g_train=training[:,2]
b_train=training[:,3]
#Decision tree
clas = robjects.FactorVector(classes)
dict_data={'z':robjects.FloatVector(z_train),'r':robjects.IntVector(r_train),'g':robjects.IntVector(g_train),'b':robjects.IntVector(b_train)}
dataf = robjects.DataFrame(dict_data)
ad=c50.C5_0(dataf,clas,triasl=20,control=(c50.C5_0Control(minCases = 2,noGlobalPruning = True, CF = 1)))
base = importr('base')
ad=(base.summary(ad))
#converter AD para string
strAD = str(ad)
print strAD
#Contar o número de espaços
#Transformar AD em Lista
#Transformar AD em Lista
listAD = strAD.split('\n')
listAuxAD = strAD.split('\n')
#contar o numero de ponto-virgula
listAuxAD = [w.replace(':...','#')for w in listAD]
listAuxAD = [w.replace(':   ','#')for w in listAuxAD]
listAuxAD = [w.replace('    ','#')for w in listAuxAD]
#contar o numero de espacos das linhas
numEsp = [w.count('#')for w in listAuxAD]
del listAuxAD

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
                cond = cond+'np.where( '+str(valueLista[0])+str(valueLista[1])+str(valueLista[2])+' , '+ str(valueLista[3])+ ' , '
            else:
                cond = cond+'np.where( '+str(valueLista[0])+str(valueLista[1])+str(valueLista[2])+' , '
    #Analisa as linhas que contem ":..."
    elif listAD[index].find(':...') != -1:                   
            
        if listAD[index].find('(') != -1:
            cond = cond +' np.where('+ str(valueLista[0])+str(valueLista[1])+str(valueLista[2])+' , '+  str(valueLista[3]) + ' , '
            
        else:
            cond = cond +' np.where( '+ str(valueLista[0])+str(valueLista[1])+str(valueLista[2])+' , '
            
    #Analisa as linhas que não contem ":..."
    else:
        if numEsp[index] > numEsp[index+1]: numEsp[index]-numEsp[index+1]
 
        if  listAD[index].find('(') != -1: 
            if listAD[index+1]== '':
                cond= cond +' '+str(valueLista[3])+ (' ) '* (numEsp[index]-numEsp[index+1]))
            else:  
                cond= cond +' '+str(valueLista[3])+ (' ) '* (numEsp[index]-numEsp[index+1]))+ ' , '          
                
        else:
           pass  

cond = cond +' ) '
print cond
#ler o segundo array do arquivo bin
array_id = np.load(file_temp)
data = np.load(file_temp)

z = data[:,0]
r = data[:,1]
g = data[:,2]
b = data[:,3]
cond_eval=eval(cond)

#selecionar no array apenas os valores com classe igual a 1
id_selec = array_id[np.where(cond_eval)]
#trabalhamdo com OGR
# get the driver
driver = ogr.GetDriverByName('ESRI Shapefile')

#Obter caminho shape
pathSHP =layer_points_clould.dataProvider().dataSourceUri()
pathSHP = pathSHP.split('|')
#Ler layer OGR
shapefile = ogr.Open(str(pathSHP[0]))
#Obter layer
layerOGR = shapefile.GetLayer()

for id in id_selec:
    featureOGR = layerOGR.GetFeature(int(id))
    #Ainserir na lista os valores dos atributos
    dict_values = featureOGR.items()
    #Obter Z
    z_id_selec = layerOGR.GetFeature(int(id)).GetField("z")
    #Selecionar com buffer
    layerOGR.SetSpatialFilter(featureOGR.GetGeometryRef().Buffer(1))
    d=[layerOGR.GetFeature(j).GetField("z") for j in xrange(layerOGR.GetFeatureCount())]
    d = np.asarray(d)
    mean = d.sum()/len(d)
    stedv = d.std(ddof=1)
    #print round(mean, 3),' - ',round(stedv, 3), ' - ',id
    mean_std.append([round(mean, 3),round(stedv, 3)])
fim = time.time()
print 'Tempo minutos: ',(fim - ini)/60
