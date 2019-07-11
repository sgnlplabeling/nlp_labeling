from collections import defaultdict, namedtuple


Metrics = namedtuple('Metrics', 'tp fp fn prec rec fscore')

class EvalCounts(object):
	def __init__(self):
		self.correct = 0			# 'O'를 포함하여 세는 것. accuracy를 위해.
		self.correct_tags = 0		# 'O'를 제외하고 세는 것.
		self.found_correct = 0		#
		self.found_guessed = 0		# number of identified arguments
		self.num_words = 0		# token counter (ignores sentence breaks)

		# counts by type
		self.t_correct_tags = defaultdict(int)
		self.t_found_correct = defaultdict(int)
		self.t_found_guessed = defaultdict(int)

def get_final_report(counts):
	overall, by_type = metrics(counts)

	c = counts
	final_report = []
	line = []
	line.append('processed %d eojeols ; ' % (c.num_words))
	line.append('found: %d arguments; correct: %d.\n' % (c.found_guessed, c.correct_tags))
	final_report.append("".join(line))

	if c.num_words > 0:
		line = []
		line.append('accuracy: %6.2f%%; ' % (100. * c.correct / c.num_words))
		line.append('precision: %6.2f%%; ' % (100. * overall.prec))
		line.append('recall: %6.2f%%; ' % (100. * overall.rec))
		line.append('FB1: %6.2f\n' % (100. * overall.fscore))
		final_report.append("".join(line))

	for i, m in sorted(by_type.items()):
		line = []
		line.append('%17s: ' % i)
		line.append('precision: %6.2f%%; ' % (100. * m.prec))
		line.append('recall: %6.2f%%; ' % (100. * m.rec))
		line.append('FB1: %6.2f  %d\n' % (100. * m.fscore, c.t_found_guessed[i]))
		final_report.append("".join(line))

	return final_report

def metrics(counts):
	c = counts
	overall = calculate_metrics(c.correct_tags, c.found_guessed, c.found_correct)
	by_type = {}
	for t in uniq(list(c.t_found_correct) + list(c.t_found_guessed)):
		by_type[t] = calculate_metrics(c.t_correct_tags[t], c.t_found_guessed[t], c.t_found_correct[t])
	return overall, by_type

def calculate_metrics(correct, guessed, total):
	tp, fp, fn = correct, guessed-correct, total-correct
	p = 0 if tp + fp == 0 else 1.*tp / (tp + fp)
	r = 0 if tp + fn == 0 else 1.*tp / (tp + fn)
	f = 0 if p + r == 0 else 2 * p * r / (p + r)
	return Metrics(tp, fp, fn, p, r, f)

def uniq(iterable):
	seen = set()
	return [i for i in iterable if not (i in seen or seen.add(i))]

