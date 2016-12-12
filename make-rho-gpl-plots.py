#!/usr/bin/env python
# encoding: utf-8
"""
test-1.py

Created by Peter Lepage on 2010-11-26.
Copyright (c) 2010/2011 Cornell University. All rights reserved.

"""

import os
import lsqfit
from corrfitter import Corr2,Corr3,CorrFitter
import numpy as np
from gvar import log,exp,evalcov
import gvar as gv
import sys

lsqfit.LSQFit.fmt_parameter = '%8.4f +- %8.4f'

DISPLAYPLOTS = False         # display plots at end of fitting

tmin = 2
svdcut = 1.0e-5


def main():
    dfile = sys.argv[1]  # data file
#    dfile = "rho-hisq-vc5-ptpt.gpl"  # data file
    data = make_data(dfile)
    pfile = "2pt.p" # last fit
    fitter = CorrFitter(models=build_models())

    #print data

    for nexp in [2,3,4,5,6,7,8]:
        print '=== nexp =',nexp,' tmin = ',tmin,' svdcut = ',svdcut
        fit = fitter.lsqfit(data=data,prior=build_prior(nexp),p0=pfile,maxit=10000,svdcut=svdcut)
        print_results(fit)
        print '\n\n'

    os.remove('2pt.p')

    if DISPLAYPLOTS:
        fitter.display_plots()
##

def print_results(fit):
    """ print out additional results from the fit """
    dErho = exp(fit.p['logdE:rho'])
    print 'rho:dE =',fmtlist(dErho[:3])
    print ' rho:E =',fmtlist([sum(dErho[:i+1]) for i in range(3)])
    arho = exp(fit.p['loga:rho'])
    print 'rho:a =',fmtlist(arho[:3])
    print 
    print
    Ee = fit.p['logdE:rho'][0]
    odict = {'E':Ee}
    idict = {'all':fit.prior['loga:rho'],
       'ass':fit.prior['rho:as1'],'stat':fit.y.buf,
       'logdE':fit.prior['logdE:rho']}
    print fit.fmt_partialsdev(odict,idict)
##

def fmtlist(x):
    return '  '.join([xi.fmt(5) for xi in x])
##

def build_prior(nexp):
    """ build prior """
    prior = gv.BufferDict()

    ## rho ##
    prior.add('loga:rho',[log(gv.gvar(0.1,0.05)) for i in range(nexp)])
    prior.add('rho:as1',[gv.gvar(0.01,0.01) for i in range(nexp)])
    prior.add('logdE:rho',[log(gv.gvar(0.5,0.3)) for i in range(nexp)])
    prior['logdE:rho'][0] = log(gv.gvar(0.6,0.2))
    prior.add('loga:rhoo', [log(gv.gvar(0.1,0.05)) for i in range(nexp)])
    prior.add('rhoo:as1', [gv.gvar(0.01,0.01) for i in range(nexp)])
    prior.add('logdE:rhoo',[log(gv.gvar(0.5,0.3)) for i in range(nexp)])
    prior['logdE:rhoo'][0] = log(gv.gvar(0.9,0.2))
    ##

    return prior
##

def build_models():
    """ build models """
#    tmin set at top
    tdata = range(48)
    tfit = range(tmin,49-tmin) # all ts
#    tfit = range(tmin,18) # all ts
    tp = 48 # periodic

    models = [

        Corr2(datatag='rho_pp',tp=tp,tdata=tdata,tfit=tfit,
            a=('loga:rho','loga:rhoo'),b=('loga:rho','loga:rhoo'),
            logdE=('logdE:rho','logdE:rhoo'),s=(1.,-1.)),

        Corr2(datatag='rho_ps',tp=tp,tdata=tdata,tfit=tfit,
            a=('loga:rho','loga:rhoo'),b=('rho:as1','rhoo:as1'),
            logdE=('logdE:rho','logdE:rhoo'),othertags=['rho_sp'],s=(1.,-1.)),

        Corr2(datatag='rho_sp',tp=tp,tdata=tdata,tfit=tfit,
            a=('rho:as1','rhoo:as1'),b=('loga:rho','loga:rhoo'),
            logdE=('logdE:rho','logdE:rhoo'),othertags=['rho_ps'],s=(1.,-1.)),

        Corr2(datatag='rho_ss',tp=tp,tdata=tdata,tfit=tfit,
            a=('rho:as1','rhoo:as1'),b=('rho:as1','rhoo:as1'),
            logdE=('logdE:rho','logdE:rhoo'),s=(1.,-1.))
    ]

    return models
##    

def make_data(filename):
    dset = gv.dataset.Dataset(filename)
    return gv.dataset.avg_data(dset)

if __name__ == '__main__':
    main()
