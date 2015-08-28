import nltk
import os
from nltk.tag import pos_tag, map_tag
import numpy as np
import scipy

def parts_of_speech(text):
	words = nltk.word_tokenize(text)
	tags = pos_tag(words)
	return [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in tags]

def categorize_response(contents):
	num = 0
	if "luxuries" in contents or "conveniences" in contents or "independent" in contents:
		num = 3
	elif "coworkers" in contents:
		num = 5
	elif "camera" in contents or "pictures" in contents:
		num = 1
	elif "education" in contents and "standard" in contents:
		num = 2
	elif "mistake" in contents:
		num = 4
	elif "ubiquity" in contents or "phones" in contents:
		num = 5
	elif "field" in contents or "Japanese" in contents:
		num = 6
	else:
		num = 2
	return num

def read_transcripts(base_dir):
	'''Read out the transcript files from the directory they are stored in. Transcript files are signified by the string '-transcript.txt' at the end of their path. The results are returned in a dictionary by prompt number.'''
	transcripts = {}
	for path in os.listdir(base_dir):
		full_path = os.path.join(base_dir, path)
		if '-transcript.txt' in path:
			with open(full_path, 'r') as file:
				contents = file.read().replace('\xe2\x80\x99', "'")
				num = categorize_response(contents)
				if num in transcripts:
					transcripts[num].append(contents)
				else:
					transcripts[num] = [contents]
		elif os.path.isdir(full_path):
			newtranscripts = read_transcripts(full_path)
			for num, transs in newtranscripts.iteritems():
				if num in transcripts:
					transcripts[num] += transs
				else:
					transcripts[num] = transs
	return transcripts

def read_aligned_transcripts(base_dir):
	'''Read out the transcripts from alignment files in base_dir. Alignment files are signified by the string '-aligned.txt' at the end of their path. The results are returned in a dictionary by prompt number.'''
	transcripts = {}
	for path in os.listdir(base_dir):
		full_path = os.path.join(base_dir, path)
		if '-aligned.txt' in path:
			with open(full_path, 'r') as file:
				contents = ' '.join([line[:line.find(',')].lower() for line in file.readlines() if line[:2] != 'sp'])
				num = categorize_response(contents)
				if num in transcripts:
					transcripts[num].append(contents)
				else:
					transcripts[num] = [contents]
		elif os.path.isdir(full_path):
			newtranscripts = read_transcripts(full_path)
			for num, transs in newtranscripts.iteritems():
				if num in transcripts:
					transcripts[num] += transs
				else:
					transcripts[num] = transs
	return transcripts


def _pos_frequency(poss, target, *args):
	'''Calculates the frequency of a certain part of speech in the array of POS tags. Pass in additional parts of speech at the end of the arguments list to add them to this frequency measure.'''
	ct = poss.count(target)
	if args and len(args) > 0:
		for add_target in args:
			ct += poss.count(add_target)
	return float(ct) / float(len(poss)) * 100.0

def formality_score(pos_tags):
	'''Computes Heylighen and Dewaele's F-score for formality based on the NLTK tags provided by parts_of_speech.'''
	poss = [pos for word, pos in pos_tags]
	#The F-score formula is (noun + adj + preposition + article - pronoun - verb - adverb - interjection + 100) / 2
	positives = _pos_frequency(poss, "NOUN") + _pos_frequency(poss, "ADJ", "NUM") + _pos_frequency(poss, "ADP") + _pos_frequency(poss, "DET")	#Numbers are considered adjectives
	negatives = _pos_frequency(poss, "PRON") + _pos_frequency(poss, "VERB") + _pos_frequency(poss, "ADV") + _pos_frequency(poss, "X")
	return (positives - negatives + 100.0) / 2.0

def avg_word_length(trans):
	'''Computes the average word length of the words in the transcript.'''
	words = [w for w in trans.split(' ') if len(w) > 0]
	return float(sum(len(w) for w in words)) / float(len(words))

if __name__ == '__main__':
	transcripts = read_aligned_transcripts("/Users/venkatesh-sivaraman/Dropbox/Public/Stimuli/Formal")
	scores = []
	for key, transs in transcripts.iteritems():
		promptscores = []
		for trans in transs:
			promptscores.append(formality_score(parts_of_speech(trans)))
			scores.append((trans,
						   promptscores[-1],
						   avg_word_length(trans),
						   (trans.count(' uh ') + trans.count(' um ')) / float(len(trans.split(' '))),
						   trans.count(' and ') / float(len(trans.split(' ')))))
		print key, promptscores
	statscores = [x[1] for x in scores]
	print np.mean(statscores), np.std(statscores)

	transcripts = read_aligned_transcripts("/Users/venkatesh-sivaraman/Dropbox/Public/Stimuli/Informal")
	scores = []
	for key, transs in transcripts.iteritems():
		promptscores = []
		for trans in transs:
			promptscores.append(formality_score(parts_of_speech(trans)))
			scores.append((trans,
						   promptscores[-1],
						   avg_word_length(trans),
						   (trans.count(' uh ') + trans.count(' um ')) / float(len(trans.split(' '))),
						   trans.count(' and ') / float(len(trans.split(' ')))))
		print key, promptscores
	statscores2 = [x[1] for x in scores]
	print np.mean(statscores2), np.std(statscores2)
	print "T-test:", scipy.stats.ttest_ind(statscores, statscores2)

	'''for trans, fscore, wlen, um, andc in scores:
		print trans
		print fscore, wlen, um, andc'''