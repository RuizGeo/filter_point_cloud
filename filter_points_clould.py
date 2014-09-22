# -*- coding: utf-8 -*-
#Import Numpy
import numpy as np
#Import time
import time

'''Import library to QGIS'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
#Import Utils to use Canvas
import qgis.utils
#import library RPY2
'''##############'''
import rpy2.robjects as robjects
r = robjects.r

from rpy2.robjects.packages import importr
#Try import C50, if error install package
try:
    c50 = importr('C50')
    base = importr('base')
except:
    utils = importr('utils')
    utils.install_packages('C50')
    c50 = importr('C50')
    base = importr('base')


class filterPointsClould:
    
    def __init__ (self, idx_layer_sample =-1, idx_fields_sample =-1,idx_field_class =-1, idx_layer_datas =-1, idx_fields_datas =-1, idx_z_datas = -1):
        #Start variables files Sample
        self.idx_layer_sample= idx_layer_sample
        self.idx_fields_sample = idx_fields_sample
        self.idx_field_class = idx_field_class
        #Start variables files Datas
        self.idx_layer_datas = idx_layer_datas
        self.idx_fields_datas = idx_fields_datas
        self.idx_z_datas = idx_z_datas
    
    def createSample(self):
        '''
        Input sample shapefile points
        Create array from shapefile points
        Output training (dict) and class (list)
        '''
        #index layer canvascanvas = qgis.utils.iface.mapCanvas()
        canvas = qgis.utils.iface.mapCanvas()
        allLayers = canvas.layers()
        layer_sample = allLayers[self.idx_layer_sample]
        #iniciar variaveis auxiliares
        classes=[]
        training={}
        #Iterando sobre a geometria
        layer_features = layer_sample.getFeatures()
        fields = layer_sample.pendingFields()
        #Atribuir os fields em list
        fields_sample = [str(v.name ()) for i, v in enumerate(fields) if i in self.idx_fields_sample]
        #Gerar dict of training
        for i in fields_sample:
            training[i] = []
        if self.idx_field_class != -1:
            #percorrer layer samples
            for feat in layer_features:
                #Obter atributos
                attrs = feat.attributes()
                #Criar array para as classes de amostras
                classes.append(attrs[self.idx_field_class])
                #criar array para os valores z,r,g e b
                for i, v in enumerate(self.idx_fields_sample):
                    training[fields_sample[i]].append(attrs[v])
            
            #retorna da funcao
            print 'Finish create sample'
            self.clas = classes
            self.trein = training
            #Delete variables
            del(classes)
            del(training)
            del(fields)
            del(fields_sample)
            del(canvas)
            del(allLayers)

        else:
            print 'Error create array'
            
    def createC50(self):
        print 'Entrou em CreateC50'
        #convert array to Factor R
        level = r['levels']

        clas = robjects.FactorVector(self.clas,levels=robjects.FactorVector([1,0]))
        
        print level(clas)
        for i in self.trein.keys():
            self.trein[i]= robjects.FloatVector(self.trein[i])
        dataf = robjects.DataFrame(self.trein)
        
        ad=c50.C5_0(dataf,clas,triasl=5,control=(c50.C5_0Control(minCases = 2,noGlobalPruning = True, CF = 0.8)))
        predict= r['predict']
        self.ad =(base.summary(ad))
        print self.ad,(base.summary(clas))
    
        
        #Delete variables
        del(ad)
        del(clas)
        del(dataf)
        del(self.clas)
        del(self.trein)
        
    def convertDTtoCond(self):
        
        strAD= str(self.ad)
        listAD = strAD.split('\n')
        listAuxAD = strAD.split('\n')
        #contar o numero de ponto-virgula
        listAuxAD = [w.replace(':...','#')for w in listAD]
        listAuxAD = [w.replace(':   ','#')for w in listAuxAD]
        listAuxAD = [w.replace('    ','#')for w in listAuxAD]
        #contar o numero de espacos das linhas
        numEsp = [w.count('#')for w in listAuxAD]
        

        #Inicio da AD
        inicioAD = listAD.index('Decision tree:')
        #inicia as variaveis

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
        self.cond = cond
        
        #delete variable
        del(cond)
        del (listAuxAD)
        
    def createDatas (self):
            '''
            Creatte shapefile memory points
            Return shapefile memory points, data (numpy), arra IDs (Numpy) and fields names (List)
            '''    
            #index layer canvascanvas = qgis.utils.iface.mapCanvas()
            canvas = qgis.utils.iface.mapCanvas()
            allLayers = canvas.layers()
            self.layer_datas = allLayers[self.idx_layer_datas]
            #inicia variaveis
            attrs_registro=[]
            data=[]
            array_id=[]
            datas_dict={}
            print "Iniciou varia aux"
            # create layer temporary
            vl = QgsVectorLayer("Point?crs=EPSG:32722", "temporary_points", "memory")
            
            #Get provider
            pr = vl.dataProvider()
            #Iniciar edicao 
            vl.startEditing()
            #Inserir colunas
            self.fields_datas = self.layer_datas.pendingFields()
            #obter apenas fields dos indexs
            fields_vl = [self.fields_datas[v] for v in self.idx_fields_datas]
            #Create fields names
            fields_names=[ f.name() for f in fields_vl]
            #Add QgsFileds in temporary file
            pr.addAttributes(fields_vl)
            #Create dict to predict
            for i in fields_names:
                datas_dict[i] = []
            #Iterando sobre a geometria
            layer_features = self.layer_datas.getFeatures()
            for feat in layer_features:
                #obter geometria
                geom =feat.geometry()
                #Obter 
                attrs = feat.attributes()
                #obter IDs como List
                array_id.append(feat.id())
                #Insert values attributes in variables
                for i, v in enumerate(self.idx_fields_datas):
                    datas_dict[fields_names[i]].append(attrs[v])
                    attrs_registro.append(attrs[i])
                #criar array para os valores z,r,g e b
                #attrs_registro = [attrs[i] for i in self.idx_fields_datas]
                #Add attributes in data array
                data.append(attrs_registro)
                fet = QgsFeature()
                #Set geometry
                fet.setGeometry( QgsGeometry.fromPoint(geom.asPoint() ))
                #Set attributes in temporary
                fet.setAttributes(attrs_registro)
                #Use provider to add features
                pr.addFeatures([fet])
                #update temporary
                vl.updateExtents()
            #commite changes
            vl.commitChanges()
            print "finish create points temporary"
            #Test predict in R
            for i in datas_dict.keys():
                datas_dict[i]= robjects.FloatVector(datas_dict[i])
            df_datas = robjects.DataFrame(datas_dict)
            predict= r['predict']
            #print predict(ad, df_datas)
            self.vl = vl
            self.array_datas = np.asarray(data)
            self.array_ids_datas = np.asarray(array_id)
            self.fields_names_vl =  fields_names
            #Delete vairiables
            del(canvas)
            del(allLayers)
            del(data)
            del(array_id)
            del(fields_names)
            del(vl)
            
    def deleteFeaturesDatas(self):
        #criar as variaveis para cada atributo (coluna)
        for i, v in enumerate(self.fields_names_vl):
            exec(v+'= self.array_datas[:,i]')
            #print v ,'----',self.array_datas[:,i],'\n'
        #avaliar as condicionais, como resultado gera um array np 0 e 1
        cond_eval = eval(self.cond)
        print cond_eval
        #selecionar no array apenas os valores com classe igual a 1
        id_selec = self.array_ids_datas[np.where(cond_eval)]
        print 'id_selec: ', id_selec
        #Delete features of conditional
        self.vl.dataProvider().deleteFeatures(id_selec.tolist())
        #Guardar dados shapefile memory
        self.vl.updateExtents()
        
        print 'Finish delete features datas'
        QgsMapLayerRegistry.instance().addMapLayer(self.vl)
    
    def filterNN(self):
        #Open edition layer temporary
        self.vl.startEditing()
        print 'Entrou em FilterNN'
        #Get index field Z in datas original
        #fields_vl = self.vl.pendingFields()
        fields_names_data = [str(i.name()) for i in self.fields_datas]
        #print 'fields_data: ',fields_data
        #Get index Z in self.fields
        
        idx_z = self.fields_names_vl.index(fields_names_data[self.idx_z_datas])
        #Get Z values
        z = self.array_datas[:,idx_z]
        print 'Z.shape: ', z.shape
        #create spatial index
        spIndex = QgsSpatialIndex()
        #Inserir features para gerar os grupos de distancias
        for f in self.vl.getFeatures():
            spIndex .insertFeature(f)
        #start variables 
        ids_gel=[]
        weight_stedv = 0.1
        #Filter nearestNeighbo
        print 'len self.layer.: ',self.vl.featureCount()
        print 'Entrou no for'
        cont=0
        sobrou=0
        for feature in self.vl.getFeatures():
            
            #Get Z attributes
            z_datas = feature.attributes()[idx_z]
            #Get geometry of features
            geom = feature.geometry()
            #Get IDs from Nearest Neighbor
            nearestIds = spIndex.nearestNeighbor(geom.asPoint(),30)
            
            #Select values Z from IDs points
            '''tem que tentar selecionar no array_id'''
            #nearestIds_idx=[self.array_id.tolist().index(i) for i in nearestIds]
            #Get value Z file datas
            values_datas = z[np.where(np.in1d(self.array_ids_datas,np.asarray(nearestIds)))]
            #print 'value_datas: ',values_datas
            #Calculate mean
            mean = values_datas.sum()/len(values_datas)
            stedv = values_datas.std(ddof=1)
            stedv = abs(stedv)
            
            dv = stedv * weight_stedv
            #print 'z_datas: ',z_datas
            if z_datas > (mean - dv) and z_datas < (mean + dv):
                pass
            else:
                #ids_del.append(feature.id())
                try:
                    self.vl.deleteFeature(feature.id())   
                    self.vl.updateExtents()
                    #print 'Deletou FID: ',feature.id()
                except:
                    sobrou+=1
                    pass
                    
                    #print 'Error delete FID: ',feature.id()
            cont+=1
        #Send changes layer temporary
        self.vl.commitChanges()
        print 'Estatistico: ',mean,' - ', stedv,' - ' ,z_datas
        print 'Cont: ', cont, 'Sobrou: ',sobrou
ini=time.time()
#Layer sample
idx_layer_sample = 0
fields_sample_idx = [2,3,4,5]
idx_classes = 10
#Layer Datas
idx_layer_datas =1
idx_fields_datas = [2,3,4,5]
idx_z_dados = 2

#Create Sample 
func = filterPointsClould(idx_layer_sample,fields_sample_idx,idx_classes,idx_layer_datas,idx_fields_datas,idx_z_dados)
#create sample
func.createSample()
#create C50
ad=func.createC50()
#convert DT to conditional
func.convertDTtoCond()
#Create func Dataset
func.createDatas()
#Delete features os datas from conditional
func.deleteFeaturesDatas()
#Filtrar NN
func.filterNN()
fim = time.time()
print "Tempo em minutos: ", (fim-ini)/60



