import numpy as np
import time
from sklearn import cluster
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
ini = time.time()
#Acessar layer ativo em Canvas
layer = qgis.utils.iface.activeLayer()
#Obtendo os registros, gera um iterador
features = layer.getFeatures()
#iterando sobre os registros
i=0
dados = np.array([])
coordenadas=[]
for f in features:
    i+=1
    if i < 3001:
        geom = f.geometry()
        pt = geom.asPoint() 
        coordenadas.append(pt)
        attrs = f.attributes()
        idx_z = layer.fieldNameIndex('z')
        dados = np.append(dados, f.attributes()[idx_z])
        idx_r = layer.fieldNameIndex('r')
        dados = np.append(dados, f.attributes()[idx_r])
        idx_g = layer.fieldNameIndex('g')
        dados = np.append(dados, f.attributes()[idx_g])
        idx_b = layer.fieldNameIndex('b')
        dados = np.append(dados, f.attributes()[idx_b])
    else:
        break
print dados.shape

print len(coordenadas)
dados = dados.reshape(3000,4)
print dados.shape

#Cluster com kmeans SkLearn
k = 15
kmeans = cluster.KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300)

kmeans.fit(dados)
labels = kmeans.labels_
#shapefile memoryCache# create layer
vl = QgsVectorLayer("Point", "temporary_points", "memory")
#Iniciar edicao vetor
vl.startEditing()
#acessar provedor 
pr = vl.dataProvider()
print labels
print dados
# add fields
pr.addAttributes([QgsField("class", QVariant.Int),QgsField("fid", QVariant.Int)])
#iterar sobre as coordenadas
# add a feature

#print 'len coo: ',len(coordenadas),'- ',len(labels)
for i in range((len(coordenadas)-1)):
    fet = QgsFeature()
    fet.setGeometry( QgsGeometry.fromPoint(coordenadas[i]) )
    fet.setAttributes([int(labels[i]),int(i)])
    pr.addFeatures([fet])

    vl.updateExtents()
#Emviar mudancas
vl.commitChanges()
QgsMapLayerRegistry.instance().addMapLayer(vl)
fim = time.time()
print "Tempo: ", (fim - ini)/60,' minutos'
