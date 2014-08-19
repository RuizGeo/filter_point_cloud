import numpy as np
import time

from osgeo import ogr

'''##############'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
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
mean_std=[]
featureOGR = layerOGR.GetFeature(0)
#print featureOGR.items().values()
print layerOGR, pathSHP[0]
for i, feat in enumerate (features):
        featureOGR = layerOGR.GetFeature(i)  
        #Ainserir na lista os valores dos atributos
        dict_values = featureOGR.items()
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
print 'Da: ',data[19],data[20], 'len(d): ',d
fim = time.time()
print 'Tempo minutos: ',(fim - ini)/60
del(layer)
del(pathSHP)
del(shapefile)

    
