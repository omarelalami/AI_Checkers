from config_file import *

import numpy
import math

class CheckerModel:
	# attaquer un cellule adverse
	# detection du chemin le plus long
	# créer un fonction qui va permettre l'intégration du bot qui pourra prendre le role du joueur 2:
		# MinMax 
		# MonteCarlo
		# Neural Network

	def __init__(self, checker_grid=None):
		if checker_grid is None:
			self.create_grid()
		else:
			self.checker_grid = checker_grid
		self.turn = 1 # 1 : pour le joueur 1 et -1 pour le joueur 2

		self.dict_of_best_moves = self.get_best_moves()




	def create_grid(self):
		"""
		les cellules numpy.nan sont interdites
		les cellules positives : joueur 1
		les cellules négatives : joueur 2
		cellule normale la valeur aboslue vaut 1
		cellule reine la valeur absolue vaut 5
		"""

		self.checker_grid = numpy.zeros(shape=(ROWS, COLS))

		for row in range(0, ROWS):
			for col in range(0, COLS):
				if (row + col) % 2 == 0:
					self.checker_grid[row, col]= math.nan

		for row in range(0, ROWS):
			for col in range(0, COLS):

				if not numpy.isnan(self.checker_grid)[row, col] and row < 4: # joueur 2
					self.checker_grid[row, col] = -1

				elif not numpy.isnan(self.checker_grid)[row, col] and row > 5: # joueur 2
					self.checker_grid[row, col] = 1





	def move_piece(self, selected_piece, move):
		self.checker_grid[move] = self.turn
		self.checker_grid[selected_piece] = 0
		# détruire les pièces adverse
		self.turn = -1 if self.turn==1 else 1

		self.dict_of_best_moves = self.get_best_moves()


	@staticmethod
	def is_out_of_bound(row, col):
		return row < 0 or row >= ROWS or col < 0 or col >= COLS


	def is_busy(self, row, col):
		"""
		3 cas :
			- la cellule est vide                                      : accessible
			- la cellule est prise avec une pièce du joueur en cours   : inacessible
			- la cellule est prise avec une pièce du joueur adverse	   : on devra observer l'état des cellules en haut à droite/gauche de celle-ci
		"""
		if self.checker_grid[row, col] == 0:
			return "accessible"
		elif self.checker_grid[row, col] == self.turn:
			return "not_accessible"
		else : 
			# là ou on va gérer l'attaque d'une pièce adverse
			return "enemy"



	def get_best_moves(self):
		"""
		dict_of_possible_move :
			+ key : position des pièces du joueur en cours (row, col) : tuple position de la pièce
			+ value : les moves possibles <= ??????????
		"""
		dict_of_possible_moves = dict()

		for row in range(0, ROWS):
			for col in range(0, COLS):
				if self.checker_grid[row, col] == self.turn:
					dict_of_possible_moves[(row, col)] = self.get_possible_moves_for_current_piece(row, col, depth=0, possible_moves_for_current_piece=dict())


		dict_of_best_moves = {}
		max_depth = 0

		for piece, possible_moves_for_current_piece in dict_of_possible_moves.items():
			for depth, arrival_positions in possible_moves_for_current_piece.items():
				if depth > max_depth and arrival_positions:
					max_depth = depth
					dict_of_best_moves = {}
					dict_of_best_moves[piece] = arrival_positions
				elif depth == max_depth and arrival_positions:
					dict_of_best_moves[piece] = arrival_positions


		return dict_of_best_moves





	def get_possible_moves_for_current_piece(self, row, col, depth, possible_moves_for_current_piece):
		"""
		Algo du backtracking : Sudoku, Chemin plus court pour un cavalier, N-Queens
		Il s'agit d'un parcours en profondeur.
		ca renvoie un dictionnaire qui va indexé un déplacement final en fonction de sa profondeur


		on n'a pas encore gérer le cas où la pièce reine <=
		"""
		if depth not in possible_moves_for_current_piece.keys():
			possible_moves_for_current_piece[depth] = set()
		if depth+1 not in possible_moves_for_current_piece.keys():
			possible_moves_for_current_piece[depth+1] = set()

		row_to_check = row - self.turn 
		cols_to_check = [col-1, col+1]			



		for col_to_check in cols_to_check:
			if not CheckerModel.is_out_of_bound(row_to_check, col_to_check):

				is_busy_state =  self.is_busy(row_to_check, col_to_check)
				if is_busy_state == "accessible" and depth == 0:
					possible_moves_for_current_piece[depth].add((row_to_check, col_to_check))
				

				elif is_busy_state == "enemy":
					row_arrival, col_arrival = 2*row_to_check - row, 2*col_to_check - col
					
					if not CheckerModel.is_out_of_bound(row_arrival, col_arrival):
						if self.is_busy(row_arrival, col_arrival) == "accessible":
							
							self.checker_grid[row, col] = 0
							self.checker_grid[row_to_check, col_to_check] = 0
							self.checker_grid[row_arrival, col_arrival] = self.turn


							possible_moves_for_current_piece[depth+1].add((row_arrival, col_arrival))

							self.get_possible_moves_for_current_piece(row_arrival, col_arrival, depth+1, possible_moves_for_current_piece)

							self.checker_grid[row, col] = self.turn
							self.checker_grid[row_to_check, col_to_check] = - self.turn
							self.checker_grid[row_arrival, col_arrival] = 0


		return possible_moves_for_current_piece





if __name__ == '__main__':
	nan = numpy.nan
	test_grid = numpy.array([
							[nan, -1., nan, -1., nan, 0., nan, 0, nan, -1.,],
							[-1., nan, -1., nan, -1., nan, -1., nan, -1., nan],
							[nan, -1., nan, 0, nan, 0, nan, -1., nan, -1.,],
							[-1., nan, -1., nan, -1., nan, 0., nan, -1., nan],
							[nan, 1, nan, 1, nan,  0., nan,  0., nan,  0.,],
							[ 0., nan,  0, nan,  0., nan,  0., nan,  0., nan],
							[nan,  1., nan,  1., nan,  1., nan,  1., nan,  1.,],
							[ 1., nan,  1., nan,  1., nan,  1., nan,  1., nan],
							[nan,  1., nan,  1., nan,  1., nan,  1., nan,  1.,],
							[ 1., nan,  1., nan,  1., nan,  1., nan,  1., nan]
							])

	checker_grid_object = CheckerModel(test_grid)

	print(checker_grid_object.checker_grid)
	for piece, moves in checker_grid_object.dict_of_best_moves.items():
		print(piece, moves)