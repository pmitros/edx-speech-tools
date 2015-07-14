import sys
import align

class WordAlignment(object):
	"""Instances of the WordAlignment class are simple: they contain a string `word` and two floats `start` and `end`, representing the time offsets in seconds in which the word appears."""
	def __init__(self, w, s, e):
		self.word = w
		self.start = s
		self.end = e

	def __repr__(self):
		return "<WordAlignment: %(word)s, %(st)f-%(end)f sec>" % {"word": self.word, "st": self.start, "end": self.end}

	def is_pause(self):
		return self.word.lower() == "sp" or self.word.lower() == "br" or self.word.lower() == "sl" or self.word.lower() == "ns"

def format_output(raw_output, sample_rate=22050):
	"""This function takes the .mlf file produced by align.py and converts into a nice object representation which can be easily written to file. (This function borrows from the writeTextGrid method of align.py.)"""
	# make the list of just phone alignments
	word_alignments = align.readAlignedMLF(raw_output, sample_rate, 0.0)
	
	phons = []
	for wrd in word_alignments :
		phons.extend(wrd[1:]) # skip the word label
	
	# make the list of just word alignments
	# we're getting elements of the form:
	#   ["word label", ["phone1", start, end], ["phone2", start, end], ...]
	wrds = []
	for wrd in word_alignments :
		# If no phones make up this word, then it was an optional word
		# like a pause that wasn't actually realized.
		if len(wrd) == 1 :
			continue
		wrds.append(WordAlignment(wrd[0], wrd[1][1], wrd[-1][2])) # word label, first phone start time, last phone end time
	return wrds

def write_output(words, outfile):
	"""Writes the array of words into outfile (in plain text format). The format is:
		WORD,START,END
		for example:
		THE,1.29482,1.38369"""
	with open(outfile, "w") as file:
		for word in words:
			file.write("{0.word},{0.start:.6f},{0.end:.6f}\n".format(word))

def output_string(words, escaped=False):
	ret = ""
	for word in words:
		if escaped:
			ret += "{0.word},{0.start:.6f},{0.end:.6f}\\n".format(word)
		else:
			ret += "{0.word},{0.start:.6f},{0.end:.6f}\n".format(word)
	return ret

if __name__ == '__main__':
	if len(sys.argv) < 2:
		raise ValueError, "Need another argument (the filename to apply output formatting to)"
	filename = sys.argv[1]
	words = format_output(filename)
	for word in words:
		print word