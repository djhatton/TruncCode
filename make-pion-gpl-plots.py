#!/usr/bin/env python
# encoding: utf-8
"""
test-1.py

Created by Peter Lepage on 2010-11-26.
Copyright (c) 2010/2011 Cornell University. All rights reserved.
Edited by Dan Hatton December 2016
"""

import os
import sys
import lsqfit
from corrfitter import Corr2,Corr3,CorrFitter
import numpy as np
from gvar import log,exp,evalcov
import gvar as gv

lsqfit.LSQFit.fmt_parameter = '%8.4f +- %8.4f'

DISPLAYPLOTS = False
tmin = 3
svdcut = 1.0e-8

def main():
    dfile = sys.argv[1]  # data file
    data = make_data(dfile)
    pfile = "2pt.p" # last fit
    fitter = CorrFitter(models=build_models())

    for nexp in [7,8]:
        print '=== nexp =',nexp,' tmin = ',tmin,' svdcut = ',svdcut
        fit = fitter.lsqfit(data=data,prior=build_prior(nexp),p0=pfile,maxit=20000,svdcut=svdcut)
        print_results(fit)
        print '\n\n'
    if DISPLAYPLOTS:
        fitter.display_plots()
##
      
def print_results(fit):
    dEpion = exp(fit.p['logdE:pion'])
    print 'pion:dE =',fmtlist(dEpion[:3])
    print ' pion:E =',fmtlist([sum(dEpion[:i+1]) for i in range(3)])
    print
    print
    al = exp(fit.p['logal:pion'])
    print 'pion:al =',fmtlist(al[:3])
    print
    print
    Ee = fit.p['logdE:pion'][0]
    odict = {'E':Ee}
    idict = {'all':fit.prior['logal:pion'],
       'ass':fit.prior['as1:pion'],'stat':fit.y.buf,
       'logdE':fit.prior['logdE:pion']}
    print fit.fmt_partialsdev(odict,idict)
##

def fmtlist(x):
    return '  '.join([xi.fmt(5) for xi in x])
##
    
def build_prior(nexp):
    prior = gv.BufferDict()

    prior.add('logal:pion',[log(gv.gvar(0.5,0.4)) for i in range(nexp)])
    prior.add('as1:pion',[gv.gvar(0.001,0.01) for i in range(nexp)])
    prior.add('logdE:pion',[log(gv.gvar(0.5,0.3)) for i in range(nexp)])
    prior['logdE:pion'][0] = log(gv.gvar(0.1,0.05))

    return prior
##

def build_models():
 
    tdata = range(48)
    tfit = range(tmin,49-tmin) # all ts
    
    tp = 48 # periodic
    models = [
        Corr2(datatag='pion_pair00',tp=tp,tdata=tdata,tfit=tfit,
            a=('logal:pion',None),b=('logal:pion',None),
            logdE=('logdE:pion',None),s=(1.,-1.)),

        Corr2(datatag='pion_pair11',tp=tp,tdata=tdata,tfit=tfit,
            a=('logal:pion',None),b=('as1:pion',None),
            logdE=('logdE:pion',None),othertags=['pion_pair22'],s=(1.,-1.)),
            
        Corr2(datatag='pion_pair22',tp=tp,tdata=tdata,tfit=tfit,
            a=('as1:pion',None),b=('logal:pion',None),
            logdE=('logdE:pion',None),othertags=['pion_pair11'],s=(1.,-1.)),

        Corr2(datatag='pion_pair33',tp=tp,tdata=tdata,tfit=tfit,
            a=('as1:pion',None),b=('as1:pion',None),
            logdE=('logdE:pion',None),s=(1.,-1.))

    ]
    return models
##    

def make_data(filename):
    dset = gv.dataset.Dataset(filename)
    print len(dset['pion_pair00'])
    return gv.dataset.avg_data(dset)

if __name__ == '__main__':
    main()

