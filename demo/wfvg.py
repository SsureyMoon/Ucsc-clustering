import numpy as np
import pywt
import matplotlib.pyplot as plt

wavelettype = 'haar'

def generate_feature_vectors(TS):
	TSwfv = {} # Wavelet feature vector
	TSsse = {} # Sum of Square Errors
	for TSname in TS:
		cL2 = pywt.wavedec(TS[TSname],wavelettype,level=2)
		cL4 = pywt.wavedec(TS[TSname],wavelettype,level=4)
		cL6 = pywt.wavedec(TS[TSname],wavelettype,level=6)
		# Generate array of feature vectors for this time series
		TSwfv[TSname] = [list(cL2[0])+list(cL2[1]), \
			list(cL4[0])+list(cL4[1]), \
			list(cL6[0])+list(cL6[1])]
		#print len(TSwfv[TSname][0])
		#print len(TSwfv[TSname][1])
		#print len(TSwfv[TSname][2])

		#print "TSwfv[{0}]:{1}".format(TSname,TSwfv[TSname])

		# Generate array of SSE values for this time series
		TSsse[TSname] = []
		# Level 2
		c = [cL2[0],cL2[1]]
		for i in range(2,len(cL2)):
			c.append([0]*len(cL2[i]))

		TSrecL2 = pywt.waverec(c,wavelettype)
		sse = sum([(TS[TSname][i]-TSrecL2[i])**2 for i,v in enumerate(TSrecL2)])
		TSsse[TSname].append(sse)
		# Level 4
		c = [cL4[0],cL4[1]]
		for i in range(2,len(cL4)):
			c.append([0]*len(cL4[i]))

		TSrecL4 = pywt.waverec(c,wavelettype)
		sse = sum([(TS[TSname][i]-TSrecL4[i])**2 for i,v in enumerate(TSrecL4)])
		TSsse[TSname].append(sse)
		# Level 6
		c = [cL6[0],cL6[1]]
		for i in range(2,len(cL6)):
			c.append([0]*len(cL6[i]))

		TSrecL6 = pywt.waverec(c,wavelettype)
		sse = sum([(TS[TSname][i]-TSrecL6[i])**2 for i,v in enumerate(TSrecL6)])
		TSsse[TSname].append(sse)

		# Plotting
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.plot(TS[TSname],label=TSname)
		ax.plot(TSrecL2,label=TSname+' (L2) SSE: '+str(int(TSsse[TSname][0])))
		ax.plot(TSrecL4,label=TSname+' (L4) SSE: '+str(int(TSsse[TSname][1])))
		ax.plot(TSrecL6,label=TSname+' (L6) SSE: '+str(int(TSsse[TSname][2])))
		plt.legend(prop={'size':6})
		plt.savefig(TSname+'.pdf',edgecolor='b', format='pdf')

	return TSwfv,TSsse