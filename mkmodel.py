import os
from casatasks import *

def mkmodelimage(imagein = None,
                 imageout = None,
                 xcoord = None,
                 ycoord = None,
                 fluxval = None,
		 chans = None,
                 doft = None,
                 vis = None):

    casalog.origin('mkmodelimage')

    os.system('cp -rp '+imagein+' '+imageout)

    ia.open(imageout)
    data=ia.getchunk()
    data[:, :, 0, :] = data[:, :, 0, :]*0
    for i in range(3):
        for j in range(3):
            data[xcoord - 1 + i, ycoord - 1 + j, 0, chans] = fluxval
    ia.putchunk(data)
    ia.close()

    if doft:
        ft(vis, model=imageout)
