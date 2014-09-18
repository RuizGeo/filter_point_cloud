# -*- coding: utf-8 -*-
import numpy as np
import time
'''##############'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


class filterSHP:

    '''
    Filter points clould
    Input conditional (string), datas (array numpy), fields (list), index z (int), ID points (array numpy) and layer datas
    Output ...
    '''
    def __init__(self,conditional = -1, datas = -1, fields=-1,idx_z_data =-1, array_id=-1, layer=-1):
        self.cond = conditional
        self.datas = datas
        self.fields = fields
        self.idx_z_data= idx_z_data
        self.array_id = array_id
        self.layer=layer
    def deleteFeatures(self):
        print 'self.fields: ',type(self.fields), len(self.fields)
        print 'self.datas :',type(self.datas), self.datas.shape
        #criar as variaveis para cada atributo (coluna)
        for i, v in enumerate(self.fields):
            exec(v+'=self.datas[:,i]')
        #avaliar as condicionais, como resultado gera um array np 0 e 1
        cond_eval=eval(self.cond)
        #selecionar no array apenas os valores com classe igual a 1
        id_selec = self.array_id[np.where(cond_eval)]
            
        #Delete features of conditional
        self.layer.dataProvider().deleteFeatures(id_selec.tolist())
        #Guardar dados shapefile memory
        self.layer.updateExtents()
        self.layer.commitChanges()
    def filterNN(self):
        #Get index field Z in datas
        fields_layer = self.layer.pendingFields()
        fields_data = [str(i.name()) for i in fields_layer]
        print 'fields_data: ',fields_data
        #Get index Z in self.fields
        idx_z = self.fields.index(fields_data[self.idx_z_data])
        #Get Z values
        z=self.datas[:,idx_z]
        print 'Z.shape: ', z.shape
        #create spatial index
        spIndex = QgsSpatialIndex()
        #Inserir features para gerar os grupos de distancias
        for f in self.layer.getFeatures():
            spIndex .insertFeature(f)
        #start variables 
        ids_gel=[]
        weight_stedv = 4
        #Filter nearestNeighbo
        for  feature in self.layer.getFeatures():
            #Get Z attributes
            z_datas = feature.attributes()[self.idx_z_data]
            #Get geometry of features
            geom = feature.geometry()
            #Get IDs from Nearest Neighbor
            nearestIds = spIndex.nearestNeighbor(geom.asPoint(),30)
            print 'nearestIds: ',nearestIds
            #Select values Z from IDs points
            '''tem que tentar selecionar no array_id'''
            values_datas = z[self.array_id[np.asarray(nearestIds)]]
            mean = d.sum()/len(d)
            stedv = d.std(ddof=1)
            stedv = abs(stedv)
            dv = stedv * weight_stedv
            if z_datas > (mean - dv) and z_datas < (mean + dv):
                pass
            else:
                ids_del.append(i)
        self.layer.dataProvider().deleteFeatures(ids_del)
        QgsMapLayerRegistry.instance().addMapLayer(self.layer)
            
