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
    
    def createArraySample(self):
        '''
        input shapefile points
        Creatte array from shapefile points
        Output numpy array sample
        '''
        #iniciar variaveis auxiliares
        training=[]
        classes=[]
        #Iterando sobre a geometria
        layer_features = self.layer_canvas.getFeatures()
        if self.idx_field_class != -1:
            #percorrer layer samples
            for feat in layer_features:
                #Obter atributos
                attrs = feat.attributes()
                #Criar array para as classes de amostras
                classes.append(attrs[self.idx_field_class])
                #criar array para os valores z,r,g e b
                attrs_registro = [attrs[i] for i in self.idx_fields]
                training.append(attrs_registro)
            #retorna da funcao
            return training

        else:
            print 'Error create array'
            
    def createSHPMemory (self):
            '''
            Creatte shapefile memory points
            Return shapefile memory points numpy array data
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
            return vl, data
