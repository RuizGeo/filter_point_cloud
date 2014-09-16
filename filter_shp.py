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
    Input conditional (string), datas (array numpy), fields (list) and array ID points
    Output ...
    '''
    def __init__(self,conditional = -1, datas = -1, fields=-1, array_id=-1):
        self.cond = conditional
        self.datas = datas
        self.fields = fields
        self.array_id = array_id
    def selectIDs(self):
        #criar as variaveis para cada atributo (coluna)
        for i, v in enumerate(self.fields):
            exec(v+'=self.datas[:,i]')
        #avaliar as condicionais, como resultado gera um array np 0 e 1
        cond_eval=eval(self.cond)
        #selecionar no array apenas os valores com classe igual a 1
        id_selec = self.array_id[np.where(cond_eval)]
        return id_selec
