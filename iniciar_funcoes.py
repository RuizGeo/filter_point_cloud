# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/luisfernando/Documentos/python')
import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Set up current path, so that we know where to look for mudules
import rpy2.robjects as robjects

import create_array_shp1 
reload(create_array_shp1)
import create_C50
reload(create_C50)
import filter_shp
reload (filter_shp)
 

#Acessar layer ativo em Canvas
canvas = qgis.utils.iface.mapCanvas()
allLayers = canvas.layers()
#Layer sample
idx_layer_sample = allLayers[1]
fields_sample = [2,3,4,5]
idx_classes = 9
idx_z_dados = 2


#Layer sampl e
layer_points_clould = allLayers[0]
#criar array e shp temporario
f = create_array_shp1.createArraySHP(idx_layer_sample,fields_sample,idx_classes)

train_df, classes_ar,nomes_fields = f.createSample()
print nomes_fields, type(nomes_fields)

#gerar os dados 
f_dados = create_array_shp1.createArraySHP(layer_points_clould,fields_sample)
vl, dados, array_id  = f_dados.createSHPMemoryArray()

DT =create_C50.createDT(classes_ar, train_df)
DT.createC50()
cond = DT.convertDTtoCond()

filt = filter_shp.filterSHP(cond,dados,nomes_fields,idx_z_dados,array_id,vl)
filt.deleteFeatures()
filt.filterNN()
