# -*- coding: utf-8 -*-
import numpy as np
import time
'''##############'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

class createArraySHP:
    '''
    Create array numpy and shapefile memory
    '''
    def __init__(self,layer_canvas = -1, idx_fields = -1, idx_filed_class = -1):
        self.layer_canvas = layer_canvas
        self.idx_fields = idx_fields
        self.idx_field_class = idx_filed_class
        #print type(self.layer_canvas,  self.idx_fields,self.idx_filed_class)
    
    def createSample(self):
        '''
        input shapefile points
        Creatte array from shapefile points
        Output dict {} sample
        '''
        #iniciar variaveis auxiliares
        classes=[]
        training={}
        #Iterando sobre a geometria
        layer_features = self.layer_canvas.getFeatures()
        fields = self.layer_canvas.pendingFields()
        #Atribuir os fields em list
        fields_sample = [v.name () for i, v in enumerate(fields) if i in self.idx_fields]
        #Gerar dict of training
        for i in fields_sample:
            training[str(i)] = []
        if self.idx_field_class != -1:
            #percorrer layer samples
            for feat in layer_features:
                #Obter atributos
                attrs = feat.attributes()
                #Criar array para as classes de amostras
                classes.append(attrs[self.idx_field_class])
                #criar array para os valores z,r,g e b
                for i, v in enumerate(self.idx_fields):
                    training[fields_sample[i]].append(attrs[v])
                #attrs_registro = [attrs[i] for i in self.idx_fields]
                #training.append(attrs_registro)
            #retorna da funcao
            return training, classes

        else:
            print 'Error create array'
            
    def createSHPMemoryData (self):
            '''
            Creatte shapefile memory points
            Return shapefile memory points and numpy array data
            '''    
            #inicia variaveis
            data=[]
            array_id=[]
            # create layer temporary
            vl = QgsVectorLayer("Point?crs=EPSG:32722", "temporary_points", "memory")
            vl.startEditing()
            pr = vl.dataProvider()
            #percorrer layer 
            #Iterando sobre a geometria
            layer_features = self.layer_canvas.getFeatures()
            for feat in layer_features:
                #obter geometria
                geom =feat.geometry()
                #Obter 
                attrs = feat.attributes()
                #obter IDs como List
                array_id.append(feat.id())
                #criar array para os valores z,r,g e b
                attrs_registro = [attrs[i] for i in self.idx_fields]
                data.append(attrs_registro)
                fet = QgsFeature()
                fet.setGeometry( QgsGeometry.fromPoint(geom.asPoint() ))
                fet.setAttributes(attrs_registro)
                pr.addFeatures([fet])
                vl.updateExtents()
            #Guardar dados shapefile memory
            vl.updateExtents()
            vl.commitChanges()
            #return datas
            return vl, np.asarray(data)
    
    
    
