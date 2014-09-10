import numpy as np
import time
from osgeo import ogr
'''##############'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

class create_Array_SHP:
    '''
    Gerar dois arrays numpy para cada arquivo shapefile de pontos
    '''
    def __init__(self,layer = -1, idx_fields = -1, idx_field_class = -1)
        '''
        Iniciar variaveis
        layer = QgsVectorLayer; inicia -1
        idx_fields = list; inicia [None]
        idx_field_class = int; inicia -1
        
        '''
        self.layer = layer
        self.idx_fields = idx_fields
        self.idx_field_class = idx_field_class
        
    def createArray(self):
        '''
        Creatte array from shapefile points
        '''
        #iniciar variaveis auxiliares
        training=[]
        classes=[]
        array_id =[]
        data=[]
        #Iterando sobre a geometria
        self.layer_features = self.layer_sample.getFeatures()
        if idx_field_class != -1:
            #percorrer layer samples
            for feat in layer_features:
                #Obter atributos
                attrs = feat.attributes()
                #Criar array para as classes de amostras
                classes.append(attrs[self.idx_field_class])
                #criar array para os valores z,r,g e b
                training.append(attrs[i] for i in self.idx_fields)
        else:
            #percorrer layer 
            for feat in layer_features:
                #Obter 
                attrs = feat.attributes()
                #criar array para os valores z,r,g e b
                training.append(attrs[i] for i in self.idx_fields)
            
    
    
    
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
#Obter provedor
provider_pints_clould=layer_points_clould.dataProvider()
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

# create layer temporary
vl = QgsVectorLayer("Point?crs=EPSG:32722", "temporary_points", "memory")
vl.startEditing()
pr = vl.dataProvider()
for feat_pc in features_point_clould:
    #Obter valores atributos
    attrs = feat_pc.attributes()
    #Obter geometria
    geom = feat_pc.geometry()
    
    #Obter valores da tabela
    attrs_registro=[round(attrs[idx_z_pc],2),attrs[idx_r_pc],attrs[idx_g_pc],attrs[idx_b_pc]]
    #obter IDs como List
    array_id.append(feat_pc.id())
    #criar array para os valores z,r,g e b
    data.append(attrs_registro)
    fet = QgsFeature()
    fet.setGeometry( QgsGeometry.fromPoint(geom.asPoint() ))
    fet.setAttributes(attrs_registro)
    pr.addFeatures([fet])
    vl.updateExtents()
#Guardar dados em arquivo bin
np.save(file_temp, np.asarray(training))
np.save(file_temp, np.asarray(array_id))
np.save(file_temp, np.asarray(data))
file_temp.close()
print "Data: ", data[-1]
#Clear memory
del(data)
del(training)
del(array_id)
