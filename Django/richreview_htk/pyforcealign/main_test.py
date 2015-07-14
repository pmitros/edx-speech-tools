from align import *
import align
import align_output
import os

def force_align(mypath, wavfile, trsfile):
	""" Mypath: the location of the p2fa kit. In this test case, it is ~/p2fa.
		wavfile: The location of the sound file in WAV format. The file will be temporarily downsampled to 11,025 Hz.
		trsfile: A text file containing the transcript of the speech in wavfile.
		Returns an array of WordAlignment objects (see align_output.py) representing the slices of time in which each word is spoken.
		"""
	# If no model directory was said explicitly, get directory containing this script.
	hmmsubdir = ""
	align.sr_models = None
	surround_token = "sp"
	between_token = "sp"
	
	
	if mypath == None :
		mypath = os.path.dirname(os.path.abspath(sys.argv[0])) + "/model"
		print "Please specify a model path. We're just guessing here, but we think it might be {} so we'll go ahead and use that.".format(mypath)
	hmmsubdir = "FROM-SR"
	# sample rates for which there are acoustic models set up, otherwise
	# the signal must be resampled to one of these rates.
	align.sr_models = [8000, 11025, 16000]
	
	word_dictionary = "./tmp/dict"
	input_mlf = './tmp/tmp.mlf'
	output_mlf = './tmp/aligned.mlf'
	
	# create working directory
	prep_working_directory()
	
	# create ./tmp/dict by concatening our dict with a local one
	if os.path.exists("dict.local"):
		os.system("cat " + mypath + "/dict dict.local > " + word_dictionary)
	else:
		os.system("cat " + mypath + "/dict > " + word_dictionary)
	
	#prepare wavefile: do a resampling if necessary
	tmpwav = "./tmp/sound.wav"
	SR = prep_wav(wavfile, tmpwav, None, "0.0", None)
	if hmmsubdir == "FROM-SR" :
		hmmsubdir = "/" + str(SR)
	
	#prepare mlfile
	prep_mlf(trsfile, input_mlf, word_dictionary, surround_token, between_token)
 
	#prepare scp files
	prep_scp(tmpwav)
	
	# generate the plp file using a given configuration file for HCopy
	create_plp(mypath + hmmsubdir + '/config')
	
	# run Verterbi decoding
	#print "Running HVite..."
	mpfile = mypath + '/monophones'
	if not os.path.exists(mpfile) :
		mpfile = mypath + '/hmmnames'
	viterbi(input_mlf, word_dictionary, output_mlf, mpfile, mypath + hmmsubdir)

	# output the alignment as a Praat TextGrid
	#writeTextGrid(outfile, readAlignedMLF(output_mlf, SR, 0.0))
	# instead, return a nicely formatted object representation
	op = align_output.format_output(output_mlf, sample_rate=SR)
	align.cleanup_working_directory()
	return op

if __name__ == '__main__':
	basePath = "/Users/venkatesh-sivaraman/Desktop/RSI/RichReviewHtkTest/"
	align_output.write_output(force_align("/Users/venkatesh-sivaraman/p2fa/model", basePath + "sample1.wav", basePath + "transcript.txt"), basePath + "output1.txt")
	print "Done"
