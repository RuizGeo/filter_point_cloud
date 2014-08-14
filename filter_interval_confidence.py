# -*- coding: utf-8 -*-
import time
import math
from osgeo import ogr
import numpy as np



# get the driver
driver = ogr.GetDriverByName('ESRI Shapefile')

shapefile = ogr.Open('/media/Documentos/TESTES/points_cloud/SHP/amostras_point_cloud_classe.shp',1)
layer = shapefile.GetLayer()
#fldDef = ogr.FieldDefn('std_dev2', ogr.OFTInteger)
#layer.CreateField(fldDef)
#Conta quantos registros tem no shp
#numFeatures = layer.GetFeatureCount()
# get the FeatureDefn for the output layer
#featureDefn = layer.GetLayerDefn()

#inFeature = layer.GetNextFeature()
#-------PostGIS--------#
import psycopg2
try:
    connection = psycopg2.connect("dbname= 'bd_point_cloud' user='postgres' host='localhost' password='mdt'")
except:
    print "I am unable to connect to the database"

cursor = connection.cursor()
#=====================================#
    
print layer.GetFeatureCount()  
inicio = time.time()
for i in xrange(100):#layer.GetFeatureCount()):
    feature = layer.GetFeature(i)  
    layer.SetSpatialFilter(feature.GetGeometryRef().Buffer(1))
    for j in xrange(layer.GetFeatureCount()):
        layer.GetFeature(j).GetField("Z")
        #feat.GetField("Z")

    #[feat.GetField("Z") for feat in layer]
    #cursor.execute("SELECT AVG(p.z)  FROM point_cloud as p WHERE ST_Intersects(" +"p.geom,"+"ST_GeometryFromText('"+ str(layer.GetSpatialFilter())+"',32722))"  )
fim = time.time()
#print [j[0] for j in cursor]
#feat= layer.GetNextFeature()

#teste = shapefile.ExecuteSQL('select AVG(z) from "%s" WHERE z > 1800' % layer.GetName())




#    bf = geomRefFeat.Buffer(1)
#    layer.SetSpatialFilter(bf)

#    #now make the change permanent
##Usando Postgis SELECT * FROM geotable WHERE ST_DWithin(geocolumn, 'POINT(1000 1000)', 100.0);
#    valores = [feat.GetField("Z") for feat in layer]
#    #calculo desvio padrao
#    mean = sum(valores, 0.0) / len(valores)
#    d = [ (i - mean) ** 2 for i in valores]
#    std_dev = math.sqrt(sum(d) / len(d))
#    if feat.GetField("Z") - mean < 0:     
#        difZMean = (feat.GetField("Z") - mean)* -1
#        #print difZMean,' * -1 ', std_dev
#    else:
#        difZMean = (feat.GetField("Z") - mean)
        #print difZMean,'  ', std_dev
        
#    #print std_dev, '---',feat.GetField("Z") - mean
#    if difZMean < std_dev:
#            feature.SetField('std_dev1', 1)
#            layer.SetFeature(feature)
#            feature.Destroy()
#    else:
#            feature.SetField('std_dev1', 0)
#            layer.SetFeature(feature)
#            feature.Destroy()
    
#shapefile.Destroy()


print (fim-inicio)/60,' minutos ',' i '
