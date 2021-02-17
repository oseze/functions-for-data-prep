#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:18:53 2020

@author: osezeiyore
"""
import numpy as np
import pandas as pd
import datetime
import time
from functools import wraps

def timer(function):    
    @wraps(function)
    def wrapper(*args,**kwargs):
        before=time.time()
        rv = function(*args,**kwargs)
        after=time.time()
        print('elapsed',after-before)
        return rv
    return wrapper

@timer
def modifychar(bad_np_array): 
    '''
    remove unwated characters from elements
    in a numpyarray, convert each element to str
    and return them as a list 
    '''
    # would it be possible to use map instead of loops?
    badChar=["ï","¿","»","[","]","'"]
    new_list=len(bad_np_array)*[None]
    for iter_bad in range(len(bad_np_array)):
        x=np.array_str(bad_np_array[iter_bad])
        for iter_char in range(len(badChar)):
            x=x.replace(badChar[iter_char],"")      
        new_list[iter_bad]=x    
    return new_list

def struct2df(struct,nturb,nyears):
    '''
    convert the 'nested' 4 dim matlab struct 
    to two dimensional dataframe 
    '''
    arr=np.squeeze(struct)
    arr=np.squeeze(np.stack(arr, axis = 0))
    arr=np.stack(arr, axis = 0)
    arr=arr.reshape(nturb*nyears,)
    arr=np.concatenate([arr[i] for i in range(nturb*nyears)]) 
    df=pd.DataFrame(arr)
    return df

def datenum_to_datetime(datenum):
    """
    Convert Matlab datenum into Python datetime.
    :param datenum: Date in datenum format
    :return:        Datetime object corresponding to datenum.
    """
    seconds = datenum*(24*60*60)-62167312800+60*60
    dt = datetime.datetime.fromtimestamp(round(seconds))
    return dt

def hourtime(numpydatetime):
    """
    convert timestamp with minute resultion to 
    hour resultion in following steps
    1) convert numpydatetime to string
    2) replace minute marker with zero
    3) convert back to numpydatetime    
    """
    string=str(numpydatetime)
    string=string[:14]+'00:'+string[17:]
    npdatetime=np.datetime64(string)

    return npdatetime
