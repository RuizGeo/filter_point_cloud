# -*- coding: utf-8 -*-
import numpy as np
import time
'''##############'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


class filterSHP:

    '''
    Create decision tree C50
    Input class (list) and trein (array numpy)
    Output ...
    '''
    def __init__(self,conditional = -1, trein = -1):
        self.clas = clas
        self.trein = trein
