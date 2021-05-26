import time
import os
import random
import copy

def load_words(filename, type):
	with open(filename) as word_file:
		if type == "set":
			valid_words = set(word_file.read().split())
		if type == "list":
			valid_words = list(word_file.read().split())

	return valid_words


def build_3_plus_word_list(english_words):
	with open('words_3plus.txt','w') as f:
		for word in english_words:
			if len(word)>2 and '%' not in word:
				f.write(word+"\n")


def unique_letters(word):
	return len(set(list(word)))
	

def get_random_boggle_board():
	cubes = [list("RIFOBX"),
				list("IFEHEY"),
				list("DENOWS"),
				list("UTOKND"),
				list("HMSRAO"),
				list("LUPETS"),
				list("ACITOA"),
				list("YLGKUE"),
				["Q","B","M","J","O","A"],
				list("EHISPN"),
				list("VETIGN"),
				list("BALIYT"),
				list("EZAVND"),
				list("RALESC"),
				list("UWILRG"),
				list("PACEMD")]
	#print("CUBES:",cubes)
	board = [[],[],[],[]]
	
	for i, cube in enumerate(cubes):
		index = random.randint(0,5)
		board[int(i/4)].append(cube[index])
	
	return board


def find_valid_words(board, english_words):
	valid_words = set()
	if len(board) != 4:
		return valid_words
	board_letters = set(list(board[0])+list(board[1])+list(board[2])+list(board[3]))
	#print("BOARD LETTERS", board_letters)
	for word in english_words:
		# check if all letters exist in board
		if board_letters >= set(list(word.upper())):
			if is_valid_word(board, word.upper()):
				valid_words.add(word.upper())
				#print("ADDED WORD:",word.upper())
				
	return valid_words


def is_valid_word(board, word):
	#print("CHECKING BOARD:",board,"FOR WORD:",word)
	if len(word) == 0:
		return True
	board_letters = set(list(board[0])+list(board[1])+list(board[2])+list(board[3]))
	if '*' in board_letters:
		# find replaced letter in board
		x = 0
		y = 0
		for y1, line in enumerate(board):
			for x1, cube in enumerate(line):
				if board[y1][x1] == '*':
					x = x1
					y = y1
		if y-1 >= 0 and x-1 >= 0 and board[y-1][x-1]==word[0]:
			wb = copy.deepcopy(board)
			wb[y-1][x-1] = '*'
			wb[y][x] = '#'
			if is_valid_word(wb,word[1:]):
				return True
		if y-1 >= 0 and board[y-1][x]==word[0]:
			wb = copy.deepcopy(board)
			wb[y-1][x] = '*'
			wb[y][x] = '#'
			if is_valid_word(wb,word[1:]):
				return True
		if y-1 >= 0 and x+1 < len(board) and board[y-1][x+1]==word[0]:
			wb = copy.deepcopy(board)
			wb[y-1][x+1] = '*'
			wb[y][x] = '#'
			if is_valid_word(wb,word[1:]):
				return True
		if x-1 >= 0 and board[y][x-1]==word[0]:
			wb = copy.deepcopy(board)
			wb[y][x-1] = '*'
			wb[y][x] = '#'
			if is_valid_word(wb,word[1:]):
				return True
		if x+1 < len(board) and board[y][x+1]==word[0]:
			wb = copy.deepcopy(board)
			wb[y][x+1] = '*'
			wb[y][x] = '#'
			if is_valid_word(wb,word[1:]):
				return True
		if y+1 < len(board) and x-1 >= 0 and board[y+1][x-1]==word[0]:
			wb = copy.deepcopy(board)
			wb[y+1][x-1] = '*'
			wb[y][x] = '#'
			if is_valid_word(wb,word[1:]):
				return True
		if y+1 < len(board) and board[y+1][x]==word[0]:
			wb = copy.deepcopy(board)
			wb[y+1][x] = '*'
			wb[y][x] = '#'
			if is_valid_word(wb,word[1:]):
				return True
		if y+1 < len(board) and x+1 < len(board) and board[y+1][x+1]==word[0]:
			wb = copy.deepcopy(board)
			wb[y+1][x+1] = '*'
			wb[y][x] = '#'
			if is_valid_word(wb,word[1:]):
				return True
		return False
	else:
		for y, line in enumerate(board):
			for x, cube in enumerate(line):
				if board[y][x] == word[0]:
					wb = copy.deepcopy(board)
					wb[y][x] = '*'
					if is_valid_word(wb,word[1:]):
						return True
		return False
		

def start_game(board, valid_words):
	guessed_words = []
	points = 0
	last_guess = ""
	possible_total = 0
	total_words = len(valid_words)
	for word in valid_words:
		possible_total += len(word)-2
	while True:
		os.system('cls')
		print("******** MY BOGGLE *********")
		print(" ")
		print("POINTS:", points,'/',possible_total)
		print("WORDS FOUND:", len(guessed_words), '/', total_words)
		print(guessed_words)
		print(" ")
		for line in board:
			if len(line) == 4:
				print(line[0] + " " + line[1] + " " + line[2] + " " + line[3])
		print(" ")
		if last_guess != "":
			print(last_guess)
		guess = str(input())
		if guess == "Q":
			print("WORDS YOU MISSED:")
			print(valid_words)
			break
		if guess.upper() in valid_words:
			guessed_words.append(guess.upper())
			valid_words.remove(guess.upper())
			points += len(guess)-2
			last_guess = guess.upper() + " IS A VALID WORD! You got " + str(len(guess)-2) + " points!"
			if len(valid_words) == 0:
				print(last_guess)
				print("CONGRATULATIONS! YOU FOUND ALL THE VALID WORDS! YOUR SCORE: " + str(points))
				break
		else:
			if guess.upper() in guessed_words:
				last_guess = guess + " HAS ALREADY BEEN FOUND. TRY AGAIN."
			else:
				last_guess = guess + " IS AN INVALID WORD. TRY AGAIN."
		



if __name__ == '__main__':
	#build_3_plus_word_list(load_words('2of12inf.txt',"list"))
	english_words = load_words('words_3plus.txt',"set")
	
	board = get_random_boggle_board()
	#board = [['B', 'Y', 'S', 'N'], ['O', 'T', 'C', 'G'], ['B', 'E', 'I', 'I'], ['N', 'S', 'W', 'A']]
	wb = copy.deepcopy(board)
	valid_words = find_valid_words(wb, english_words)
	#print("RESULT:",is_valid_word(wb, "BOY"))
	
	#print("BOARD:",board)
	#print("valid words:", valid_words)
	
	start_game(board,valid_words)