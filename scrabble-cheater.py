import string, sys
from collections import defaultdict

def read_file(): 
	"""
	Reads in the scrabble word dictionary file
	"""
	file = open('sowpods.txt')
	return [word.strip() for word in file.readlines()]

def qsort(list, cmpfn):
	"""
	Quick sort implementation, since I felt like writing it from scratch.
	"""
	if len(list) <= 1: 
		return list
	pivot_index = len(list)/2
	pivot = list[pivot_index]
	less = [curr_word for curr_word in list if cmpfn(curr_word, pivot) is False and curr_word != pivot]
	greater = [curr_word for curr_word in list if cmpfn(curr_word, pivot) is True and curr_word != pivot]
	return qsort(less, cmpfn) + [pivot] + qsort(greater, cmpfn)

def score_word(word): 
	"""
	Returns the score for word
	"""
	scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, \
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, \
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, \
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, \
         "x": 8, "z": 10}
	word = list(word.lower())
	return sum([scores[letter] for letter in word])

def build_word_dict(words):
	"""
	Builds a dict that maps sorted strings to a list of valid words that one can make from
	the letters in the string. 
	e.g 'AELD' maps to ['LADE', 'DEAL', 'LEAD', 'DALE']
	"""
	sorted_strings_to_corresponding_word_list = defaultdict(lambda: [], dict())
	for word in words: 
		key = ''.join(sorted(word))
		new_list = sorted_strings_to_corresponding_word_list[key]
		new_list.append(word)
		sorted_strings_to_corresponding_word_list[key] = new_list
	return sorted_strings_to_corresponding_word_list

def sort(word): 
	"""
	Returns word with its letters sorted in alphabetical order (as a string)
	"""
	return ''.join(sorted(word))

def get_combinations(letters): 
	"""
	letters is a string. Returns a set of all possible combinations of the letters
	in letters (strings). 
	e.g get_combations('ABC') would return set(['A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC'])
	"""
	if len(letters) == 1: 
		return set(letters)
	prev_combos = get_combinations(letters[1:])
	combos_to_add = set([combo+letters[0] for combo in prev_combos])
	combos_to_add.add(letters[0])
	return prev_combos.union(combos_to_add)

def get_possible_words(sorted_strings_to_corresponding_word_list, letters): 
	"""
	Returns all the possible words that can be made by letters.
	"""
	combinations = get_combinations(letters)
	possible_words = set()
	for combo in combinations: 
		print sorted_strings_to_corresponding_word_list[sort(combo)]
		possible_words = possible_words.union(set(sorted_strings_to_corresponding_word_list[sort(combo)]))
	return possible_words

def alternate_get_possible_words(string_to_word_list, letters): 
	combinations = get_combinations(letters)
	possible_words = []
	for combo in combinations: 
		possible_words.extend(string_to_word_list[sort(combo)])
	return possible_words

def compare_word_score_tuples(one, two): 
	"""
	Comparison function for sorting (word, score) tuples. 
	"""
	return one[1] <= two[1]

def scrabble_cheater(letters): 
	"""
	Prints a sorted list of legal moves that you could make with the 
	given letters and the score of each, from best to worst.
	"""
	all_words = read_file()
	sorted_strings_to_corresponding_word_list = build_word_dict(all_words)
	possible_words = alternate_get_possible_words(sorted_strings_to_corresponding_word_list, letters)
	scored_words = qsort([(word, score_word(word)) for word in possible_words], compare_word_score_tuples)
	for (word, score) in scored_words: 
		print score, word

if __name__ == "__main__": 
	if len(sys.argv) != 2: 
		print 'Usage: python scrabble-cheater.py <LETTERS>'
		print 'e.g python scrabble-cheater.py ZAEFIEE'
	else: 
		scrabble_cheater(sys.argv[1])