#applies quack flag
def quickflags(dname):
	flagdata(vis = dname + '.ms', mode = 'quack'
	, quackinterval = 6.0, quackmode='beg')
	flagdata(vis = dname + '.ms', mode = 'clip'
	, clipzeros = True, flagbackup = False)
	flagdata(vis = dname + '.ms', mode = 'shadow'
	, tolerance = 0.0, flagbackup = False)
#corrects potential antennae position error - creates antpos table
def antposcorrec(dname):
	gencal(vis = dname + '.ms', caltable = dname + '.antpos', 
	caltype = 'antpos') 

#lists flux calibrator models
def setjylist(dname):
	setjy(vis = dname + '.ms', listmodels=True)

#once flux calibrator is chosen, use setjy to apply it
def setjyshort(dname, flux_field, modelname):
	setjy(vis = dname + '.ms', field = flux_field,model = modelname)

#find bandpass solution to remove bad antennae
def bandpasssol(dname, flux_field, phase_field, ref, spw_short):
        fields = flux_field + ',' + phase_field
        gaincal(vis = dname + '.ms', caltable = dname + '.G0all'
        , field = fields, refant = ref, spw = spw_short, gaintype = 'G'
        , calmode = 'p', solint = 'int', minsnr = 5
        , gaintable = [dname + '.antpos'])

#initial phase calibration - creates G0 table
#use '*:x~y' to apply only to intermediate section of all spws
def initphasecal(dname, flux_field, ref, spw_short):
        gaincal(vis = dname + '.ms', caltable = dname + '.G0'
        , field = flux_field, refant = ref, spw = spw_short, gaintype = 'G'
        , calmode = 'p', solint = 'int', minsnr = 5
        , gaintable = [dname + '.antpos'])

#calibrates delay - creates K0 table
def delaycal(dname, flux_field, ref, spw_wide):
	gaincal(vis = dname + '.ms', caltable = dname + '.K0'
	, field = flux_field, refant = ref, spw = spw_wide 
	, gaintype = 'K', solint = 'inf', combine = 'scan'
        , minsnr = 5, gaintable = [dname + '.antpos', dname + '.G0'])

#calibrates bandpass - creates B0 table
def bandpasscal(dname, flux_field, ref):
	bandpass(vis = dname + '.ms', caltable = dname + '.B0'
	, field = flux_field, refant = ref, spw = ''
	, combine = 'scan', solint = 'inf', bandtype = 'B'
	, gaintable = [dname + '.antpos', dname + '.G0', dname + '.K0'])

#calibrates gain for flux calibrator - creates G1 table
def gaincal1(dname, flux_field, ref, spw_wide):
	gaincal(vis = dname + '.ms', caltable = dname + '.G1'
	, field = flux_field, refant = ref, spw = spw_wide 
	, solint = 'inf', gaintype = 'G', calmode = 'ap', solnorm = False
	, gaintable = [dname + '.antpos', dname + '.K0', dname + '.B0']
	, interp = ['','','nearest'])

#calibrates gain for phase calibrator - appends to G1 table
def gaincal2(dname, phase_field, ref, spw_wide):
	gaincal(vis = dname + '.ms', caltable = dname + '.G1'
	, field = phase_field, refant = ref, spw = spw_wide 
	, solint = 'inf', gaintype = 'G', calmode = 'ap'
	, gaintable = [dname + '.antpos', dname + '.K0', dname + '.B0']
	, append = True)

#does both gain calibrations in a row
def gaincalfull(dname,flux_field, phase_field, ref, spw_wide):
	gaincal1(dname,flux_field, ref, spw_wide)
	gaincal2(dname,phase_field, ref, spw_wide)

#makes flux calibration table fluxscale1
def fluxcal(dname, flux_field, phase_field):
	myscale = fluxscale(vis = dname + '.ms', caltable = dname + '.G1'
	, fluxtable = dname + '.fluxscale1', reference = flux_field
	, transfer = [phase_field], incremental = False)

#applies calibration tables to flux calibrator
def applycal1(dname, flux_field):
	applycal(vis = dname + '.ms', field = flux_field
	, gaintable = [dname + '.antpos', dname + '.fluxscale1'
	,dname +'.K0', dname + '.B0'], gainfield = ['',flux_field,'','']
	, interp = ['','nearest', '', '']
	, calwt = False)

#applies calibration tables to phase calibrator
def applycal2(dname, phase_field):
	applycal(vis = dname + '.ms', field = phase_field
	, gaintable = [dname + '.antpos', dname + '.fluxscale1'
	, dname +'.K0', dname + '.B0'], gainfield = ['',phase_field,'','']
	, interp = ['','nearest', '', '']
	, calwt = False)

#applies calibration tables to all fields
def applycal3(dname, phase_field, target_fields):
	applycal(vis = dname + '.ms', field = target_fields
	, gaintable = [dname + '.antpos', dname + '.fluxscale1'
	,dname +'.K0', dname + '.B0'], gainfield = ['',phase_field,'','']
	, interp = ['','linear', '', '']
	, calwt = False)

#applies all 3 applycals
def applycalfull(dname, flux_field, phase_field, target_fields):
	applycal1(dname, flux_field)
	applycal2(dname, phase_field)
	applycal3(dname, phase_field, target_fields)

#creates all calibration tables and applies them
def fullcalibration(dname, modelname, flux_field, phase_field, target_fields
, ref, spw_short, spw_wide):
        antposcorrec(dname)
        setjyshort(dname, flux_field, modelname)
        initphasecal(dname, flux_field, ref, spw_short)
        delaycal(dname, flux_field, ref, spw_wide)
        bandpasscal(dname, flux_field, ref)
        gaincalfull(dname,flux_field, phase_field, ref, spw_wide)
        fluxcal(dname, flux_field, phase_field)
        applycalfull(dname, flux_field, phase_field, target_fields)

#splits data
def splitstat(dname, fieldrange):
        split(vis = dname + '.ms', outputvis = dname + '_split.ms',
        datacolumn = 'corrected',field = fieldrange, correlation = 'RR,LL')
        statwt(vis = dname + '_split.ms', datacolumn = 'data')

#produces primary beam corrected image
def impbcorshort(dname):
        impbcor(imagename= dname + '.image', pbimage = dname +  '.pb'
        , outfile = dname + '.pbcorimage')
