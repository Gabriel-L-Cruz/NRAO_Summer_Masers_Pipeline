import os
import numpy as np
from casatasks import *
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def maserfinder(momentmaptype = None, dname = None,
                    span = None, start = None, sigmanum = None,
                    numpixels = 1024, numchans = 1080):
    #creates directories that store spectra of candidates from
    #each field in the range
    for i in range(span):
        i = i + start
        spectratocsv(dname  + '_f' + str(i) + '.' + momentmaptype,
                         dname + '_f' + str(i), sigmanum, numpixels, numchans)
    spectratoim(dname,span,start)

#converts csv files of spectra to pngs
def spectratoim(dname, span, start):
    spectradir = dname + '_spectraims'
    if not os.path.isdir(spectradir):
        os.mkdir(spectradir)
    for i in range(span):
        i = i + start
        directory = dname + '_f' + str(i) + '_candidates'
        iter = 1
        if os.path.isdir(directory) :
           for filename in os.listdir(directory):
                pathstr = os.path.join(directory, filename)
                data = np.genfromtxt(pathstr, delimiter = ',')
                x = data[:,2][0]
                y = data[:,3][0]
                sig = data[:,4][0]
                pngname = dname + '_f' + str(i) + '_candidate' + str(format(iter,'02')) + '_sig' + str('{:.2}'.format(sig)) + '_x' + str(int(x)) + '_y' + str(int(y))  + ".png"
                fig = plt.figure()
                plt.plot(data[:,0],data[:,1])
                plt.xlabel('Channels')
                plt.ylabel(pngname +'\nFlux Density(Jy)')
                plt.title('Flux vs. Channel')
                plt.savefig(pngname)
                plt.close(fig)
                os.rename(pngname,spectradir + '/' + pngname) 
                smoothed_spec = gaussian_filter(data[:,1], 1, truncate = 6.0)
                pngname = dname + '_smoothed_f' + str(i) + '_candidate' + str(format(iter,'02')) + '_sig' + str('{:.2}'.format(sig)) + '_x' + str(int(x)) + '_y' + str(int(y))  + ".png"
                plt.plot(data[:,0], smoothed_spec)
                plt.xlabel('Channels')
                plt.ylabel(pngname +'\nFlux Density(Jy)')
                plt.title('Flux vs. Channel')
                plt.savefig(pngname)
                plt.close()
                os.rename(pngname,spectradir + '/' + pngname) 
                iter = iter + 1


def spectratocsv(momentmap = None, imagein = None, 
                 sigmanum = None, numpixels = 1024, numchans = 1080):
    casalog.origin('finding masers') #logs method
    dict = imstat(imagename = imagein + '.image')
    ia.open(momentmap) #grabs momentmap data
    data=ia.getchunk() #loads data
    sigma = dict['rms'][0] * sigmanum #threshold for marking pixels
    candidates = np.zeros((1,3)) #np array of pixels
    #loops through pixels and checks if flux is above threshold
    for i in range(numpixels):
        for j in range(numpixels):
            if data[i,j,0,0] > sigma:
                nsigmas = data[i,j,0,0]/ sigma * sigmanum
                if (candidates[0] == [0,0,0]).all():
                    candidates[0] = [i,j,nsigmas]
                else:
                    candidates = np.append(candidates, [[i,j,nsigmas]], axis = 0)
    ia.close()
    if(candidates[0] == [0,0,0]).all():
        print('no candidates for image ' + imagein)
        return
    ia.open(imagein + '.image')
    data = ia.getchunk()
    iter = 1
    candidatedir = imagein + "_candidates"
    if not os.path.isdir(candidatedir):
        os.mkdir(candidatedir)
    for pixel in candidates:
        x,y,sig = pixel
        spectra = np.zeros((1,5)) #first column is channel, second is flux
        print('x:' + str(x) + ' y:' + str(y) + ' sig:' + str(sig))
        for chan in range(numchans):
            if chan == 0:
                spectra[0] = [chan, data[int(x),int(y),0,chan],x ,y, sig]
            else:
                spectra = np.append(spectra, [[chan, data[int(x),int(y),0,chan], x, y, sig]], axis = 0) #appends channel and flux to spectra ndarray
        csvname = imagein + "_candidate" + str(format(iter,'02')) + '_sig' + str('{:.2}'.format(sig)) + '_x' + str(int(x)) + '_y' + str(int(y))  + ".csv"
        np.savetxt(csvname, spectra, delimiter = ",") #saves array as csv
        os.rename(csvname, imagein + '_candidates/' + csvname)
        iter = iter + 1
    ia.close()
