# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:05:04 2014

@author: ruiz
"""
#import pandas.rpy.common as com
#import pandas as pd
import rpy2.robjects as robjects
r = robjects.r

from rpy2.robjects.packages import importr
c50 = importr('C50')

#Ler a tabela do shapefile em DBF com R

#Criar a arvore de decisao na linguagem R
#Converter a AD para testes condicionais
#Aplicar os testes para a nuvem de pontos
#Aplicar o calculo do DP para esses pontos selecionados 
#Criar um novo shapefile com o resultado
r("library(foreign)")
r("dados= read.dbf('/media/Documentos/TESTES/points_cloud/SHP/pt_amostras1.dbf.dbf')")
r("classes = factor(dados$classe_id)")
#r("USO = factor(dados$USO)")
r("training = data.frame(dados$z,dados$R,dados$G,dados$B,dados$tex_DV_0,dados$tex_ASM_0)")
r("nomes = names(training)")
uso= r("nomes[1]")
o =[]
o.append(uso[0])
print o

r("library(C50)")

r("oneTree<-C5.0(training,classes, control=(C5.0Control(minCases = 40, CF = 0.8)))")
ad = r("summary(oneTree)")

strAD = str(ad)

#print strAD
#Transformar AD em Lista
listAD = strAD.split('\n')
#Verifica os colchetes fora de lugar
for i, v in enumerate(listAD):   
     if '{' in v and '}' not in v :
         if '{' in v and '}' not in listAD[i+1] :
             listAD[i+1] = listAD[i+1].replace(':','')
             listAD[i+2] = listAD[i+2].replace(':','')
             listAD[i] = v.strip() + listAD[i+1].strip()+ listAD[i+2].strip()
             listAD.remove(listAD[i+2])
             listAD.remove(listAD[i+1])            
         else:
             listAD[i+1] = listAD[i+1].replace(':','')
             listAD[i] = v.strip() + listAD[i+1].strip()
             listAD.remove(listAD[i+1])
     else:
         pass
     
     
#Contar o número de espaços
#Transformar AD em Lista
listAuxAD = strAD.split('\n')
#contar o numero de ponto-virgula
listAuxAD = [w.replace(':...','#')for w in listAD]
listAuxAD = [w.replace(':   ','#')for w in listAuxAD]
listAuxAD = [w.replace('    ','#')for w in listAuxAD]
#contar o numero de espacos das linhas
numEsp = [w.count('#')for w in listAuxAD]
del listAuxAD

#Verificar a lista 
for i, v in enumerate(listAD):
    p = 'USO'
    
    if v.find(p) != -1:
        limiteNumEsp = numEsp[i-1]
        while limiteNumEsp <  numEsp[i]:
            #print limiteNumEsp, v
            limiteNumEsp = numEsp[i]
        #while limiteNumEsp != numEsp[i] :
        #print v
            
#Inicio da AD
inicioAD = listAD.index('Decision tree:')
#inicia as variáveis

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
                cond = cond+'CASE WHEN '+str(valueLista[0])+str(valueLista[1])+str(valueLista[2])+' THEN '+ str(valueLista[3])+ ' ELSE '
            else:
                cond = cond+'CASE WHEN '+str(valueLista[0])+str(valueLista[1])+str(valueLista[2])+' THEN '
    #Analisa as linhas que contem ":..."
    elif listAD[index].find(':...') != -1:        
        #Analisa se há '{' e '('
        if listAD[index].find('{') != -1 and listAD[index].find('(') != -1: 
            aux = str(valueLista)[str(valueLista).index('{')+1:str(valueLista).index('}')]
            aux = ' '+ valueLista[0]+' = ' + aux.replace(',',' OR '+valueLista[0]+' = ')
            cond= cond+'CASE WHEN '+aux +' THEN '+ str(valueLista[3])+ ' ELSE '           
            
        #Analisa se há '('   
        elif listAD[index].find('{') != -1: 
            aux = str(valueLista)[str(valueLista).index('{')+1:str(valueLista).index('}')]
            aux = ' '+ valueLista[0]+' = ' + aux.replace(',',' OR '+valueLista[0]+' = ')
            cond= cond+'CASE WHEN '+aux +' THEN '           
            
        elif listAD[index].find('(') != -1:
            cond = cond +' CASE WHEN '+ str(valueLista[0])+str(valueLista[1])+str(valueLista[2])+' THEN '+  str(valueLista[3]) + ' ELSE '
            
        else:
            cond = cond +' CASE WHEN '+ str(valueLista[0])+str(valueLista[1])+str(valueLista[2])+' THEN '
            
    #Analisa as linhas que não contem ":..."
    else:
        if numEsp[index] > numEsp[index+1]: numEsp[index]-numEsp[index+1]
        #Analisa se há '{' e '('
        if listAD[index].find('{') != -1 and listAD[index].find('(') != -1:
            if listAD[index+1]== '':             
                cond= cond +' '+str(valueLista[3])+ (' END '* (numEsp[index]-numEsp[index+1]))                
            else:            
                cond= cond +' '+str(valueLista[3])+ (' END '* (numEsp[index]-numEsp[index+1]))+ ' ELSE '
 
        elif  listAD[index].find('(') != -1: 
            if listAD[index+1]== '':
                cond= cond +' '+str(valueLista[3])+ (' END '* (numEsp[index]-numEsp[index+1]))
            else:  
                cond= cond +' '+str(valueLista[3])+ (' END '* (numEsp[index]-numEsp[index+1]))+ ' ELSE '          
                
        else:
           pass  
        

    

cond = cond +' END '
print cond
