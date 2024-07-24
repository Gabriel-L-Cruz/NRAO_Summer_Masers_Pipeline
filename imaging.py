def cleanfields(dsets, imout,span,start):
	for i in range(span):
		i = i + start
		tclean(vis = dsets, field = str(i), spw = '*:401~1500'
		, datacolumn = 'data', imagename = imout + '_f' + str(i)
		, imsize = [1024,1024], cell = ['3.4arcsec', '3.4arcsec'], specmode = 'cubedata'
		, nchan = 1100, perchanweightdensity = True, pblimit = -1, weighting = 'briggs'
		, niter = 500, outframe = 'BARY', restfreq = '6.668519GHz'
		, threshold = '3mJy', savemodel = 'modelcolumn')

def subchansimage(dname, span, start):
        for i in range(span):
                i = i + start
                imsubimage(imagename = dname + '_f'+ str(i) + '.image'
                , outfile = dname + '_subbed_f' + str(i) + '.image'
		, chans = '20~1099')

def momentmaps(dname, span, start):
        for i in range(span):
                i = i + start
                immoments(imagename = dname + '_f'+ str(i) + '.image'
                , moments = [0,3,6,8], chans = '20~1099'
                , outfile = dname + '_f' + str(i)) 

