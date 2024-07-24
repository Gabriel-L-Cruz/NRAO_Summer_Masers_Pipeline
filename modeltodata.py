def modeltodata(dname):
	tb.open(dname + '.ms')
	tc=tb.taql('update ' + dname + '.ms set DATA=DATA + MODEL_DATA')
	tc.done()
	tb.done()
