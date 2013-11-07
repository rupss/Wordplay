import re, string, datetime

def read_file(): 
	file = open('sowpods.txt')
	return [word.strip() for word in file.readlines()]

def find_uu(): 
	words = read_file()
	for word in words: 
		if 'UU' in word: 
			print word

def find_q_without_u(): 
	words = read_file()
	for word in words: 
		if re.match('.*Q[^U].*', word):  
			print word

# def bsearch(letter, list): 
# 	curr_index = len(list)/2
# 	word = list[curr_index]
# 	if re.match(".*" + letter + letter + ".*", word): 
# 		return true

def find_never_doubled_letters_slow(): 
	words = read_file()
	letters = set(string.ascii_uppercase)
	for word in words: 
		to_remove = set()
		for letter in letters: 
			if re.match(".*" + letter + letter + ".*", word): 
				to_remove.add(letter)
		letters = letters - to_remove
	print letters

def find_never_doubled_letters_faster(): 
	words = read_file()
	letters = set(string.ascii_uppercase)
	for word in words: 
		match = re.match("(.*(?P<letter>[A-Z])(?P=letter).*)+", word)
		if match: 
			letter = match.group(2)
			if letter in letters: 
				letters.remove(letter)
	print letters


def qsort(list, cmpfn): 
	if len(list) <= 1: 
		return list
	pivot_index = len(list)/2
	pivot = list[pivot_index]
	less = [curr_word for curr_word in list if cmpfn(curr_word, pivot) is False and curr_word != pivot]
	greater = [curr_word for curr_word in list if cmpfn(curr_word, pivot) is True and curr_word != pivot]
	return qsort(less, cmpfn) + [pivot] + qsort(greater, cmpfn)

def compare_length(one, two): 
	return (len(one) >= len(two))

def find_longest_palindrome(): 
	words = read_file()
	result = []
	for word in words: 
		if word == word[::-1]: 
			result.append(word)
	result_sorted = qsort(result, compare_length)
	print 'The longest palindrome is:', result_sorted[-1]

def all_vowels_and_y_alphabetical_order(): 
	words = read_file()
	for word in words: 
		if re.match("(.*[A].*[E].*[I].*[O].*[U].*[Y].*)", word): 
			print word

def all_vowels_and_y_any_order(): 
	words = read_file()
	vowels_and_y = set('AEIOUY')
	for word in words: 
		if vowels_and_y.issubset(word): 
			print word

def compare_freq_word_list_tuples(one, two): 
	return (one[1][0] >= two[1][0])

"Using string.count to count the instances of a letter in a string. "
def letter_with_most_appearances_in_word1(): 
	words = read_file()
	letters = set(string.ascii_uppercase)
	letter_to_frequency_and_word_dict = dict([(letter, (-1, list())) for letter in letters])
	for word in words: 
		for letter in letters: 
			curr_count = word.count(letter)
			(frequency, max_word_list) = letter_to_frequency_and_word_dict[letter]
			if curr_count > frequency: 
				letter_to_frequency_and_word_dict[letter] = (curr_count, [word])
			elif curr_count == frequency: 
				max_word_list.append(word)
				letter_to_frequency_and_word_dict[letter] = (curr_count, max_word_list)

	sorted_list = qsort(letter_to_frequency_and_word_dict.items(), compare_freq_word_list_tuples)
	best = sorted_list[-1]
	print 'Most appearances by the letter', best[0]
	print 'Occurs', best[1][0], 'times in the following words: '
	print best[1][1]

"Regex for finding all instances of letter in a string is much slower"
def letter_with_most_appearances_in_word2(): 
	words = read_file()
	letters = set(string.ascii_uppercase)
	letter_to_frequency_and_word_dict = dict([(letter, (-1, list())) for letter in letters])
	for word in words: 
		for letter in letters: 
			curr_count = len(re.findall(letter, word))
			(frequency, max_word_list) = letter_to_frequency_and_word_dict[letter]
			if curr_count > frequency: 
				letter_to_frequency_and_word_dict[letter] = (curr_count, [word])
			elif curr_count == frequency: 
				max_word_list.append(word)
				letter_to_frequency_and_word_dict[letter] = (curr_count, max_word_list)

	sorted_list = qsort(letter_to_frequency_and_word_dict.items(), compare_freq_word_list_tuples)
	best = sorted_list[-1]
	print 'Most appearances by the letter', best[0]
	print 'Occurs', best[1][0], 'times in the following words: '
	print best[1][1]

def run_and_time_function(func, *args): 
	t1 = datetime.datetime.now()
	if len(args) == 0: 
		func()
	elif len(args) == 1: 
		func(args[0])
	t2 = datetime.datetime.now()
	print 'Elapsed time = ', t2-t1

# run_and_time_function(all_vowels_and_y_alphabetical_order)
# run_and_time_function(letter_with_most_appearances_in_word1)
# run_and_time_function(letter_with_most_appearances_in_word2)
# run_and_time_function(find_longest_palindrome)
# run_and_time_function(all_vowels_and_y_any_order)
run_and_time_function(scrabble_cheater, 'ZAEFIEE')
# print get_combinations('ABCD')
