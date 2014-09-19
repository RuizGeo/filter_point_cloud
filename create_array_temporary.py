# -*- coding: utf-8 -*-
import numpy as np
import time
'''##############'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

class createArrayMemory:
    '''
    Create array numpy and shapefile memory
    Input layer shapefile and index of fields
    Output shp temporary (QgsVector), datas (Numpy of table and IDs (Numpy)
    '''
    def __init__(self,layer_canvas = -1, idx_fields = -1):
        self.layer_canvas = layer_canvas
        self.idx_fields = idx_fields
        
    def createSHPMemoryArray (self):
            '''
            Creatte shapefile memory points
            Return shapefile memory points and numpy array data
            '''    
            #inicia variaveis
            data=[]
            array_id=[]
            # create layer temporary
            vl = QgsVectorLayer("Point?crs=EPSG:32722", "temporary_points", "memory")
            #Iniciar edicao 
            vl.startEditing()
            #Get provider
            pr = vl.dataProvider()

            #Inserir colunas
            fields_data = self.layer_canvas.pendingFields()
            fields_vl = [v for i, v in enumerate(fields_data) if i in [self.idx_fields]]
            pr.addAttributes(fields_vl)
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
                #print 'attrs_registro: ', attrs_registro 
                data.append(attrs_registro)
                fet = QgsFeature()
                fet.setGeometry( QgsGeometry.fromPoint(geom.asPoint() ))
                fet.setAttributes(attrs_registro)
                pr.addFeatures([fet])
                #atualizar
                vl.updateExtents()
            #Guardar dados shapefile memory
            vl.commitChanges()
            QgsMapLayerRegistry.instance().addMapLayer(vl)
            #return datas
            return vl, np.asarray(data), np.asarray(array_id)
