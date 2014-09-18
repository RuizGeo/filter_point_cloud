# -*- coding: utf-8 -*-
import numpy as np
import time
'''##############'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
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


class createDT:

    '''
    Create decision tree C50
    Input class (list) and trein (array numpy)
    Output conditional (string)
    '''
    def __init__(self,clas= -1, trein = -1):
        self.clas = clas
        self.trein = trein
    def createC50(self):
        #convert array to Factor R
        clas = robjects.FactorVector(self.clas)
        for i in self.trein.keys():
            self.trein[i]= robjects.FloatVector(self.trein[i])
        dataf = robjects.DataFrame(self.trein)
        ad=c50.C5_0(dataf,clas,triasl=20,control=(c50.C5_0Control(minCases = 2,noGlobalPruning = True, CF = 1)))
        self.ad =(base.summary(ad))
        return ad
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
        del listAuxAD

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
        return cond
