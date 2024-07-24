#plots phase vs frequency(finds delay)
def phasefreq(dname,dtype,datacolumn):
        corr = ''
        if(dtype == '.ms'):     
                corr = 'RR,LL'
        plotms(vis = dname + dtype, xaxis = 'frequency', yaxis = 'phase'
        , field = '0~3', spw = '0', antenna = 'ea01&ea26',correlation=corr, avgtime = '100s'
        , iteraxis = 'field', ydatacolumn = datacolumn,coloraxis = 'spw'
        , gridcols = 2, gridrows = 2, plotrange = [-1,-1,-180,180])

#plots phase vs time(checks for antenna phase stability)
def phasetime(dname, dtype, datacolumn):
        corr = ''
        if(dtype == '.ms'):
                corr = 'RR,LL'
        plotms(vis = dname + dtype, xaxis = 'time', yaxis = 'phase'
        , field = '0',correlation=corr, iteraxis = 'antenna'
        , plotrange = [-1,-1,-180,180], ydatacolumn = datacolumn
        , coloraxis = 'corr')

#plots amplitude vs time(RFI at certain times)
def amptime(dname, dtype, datacolumn):
        corr = ''
        if(dtype == '.ms'):
                corr = 'RR,LL'
        plotms(vis = dname + dtype, xaxis = 'time', yaxis = 'amp'
        , field = '', spw = '0', antenna = '', correlation = corr
        , avgchannel = '', ydatacolumn = datacolumn, coloraxis = 'antenna2')

#plots amplitude vs frequency(RFI in certain spectral windows)
def ampfreq(dname, dtype, datacolumn):
        corr = ''
        if(dtype == '.ms'):
                corr = 'RR,LL'
        plotms(vis = dname + dtype, xaxis = 'frequency', yaxis = 'amp'
        , field = '0', spw = '',correlation = corr
	, iteraxis = '',  coloraxis = 'baseline'
	, ydatacolumn = datacolumn)

