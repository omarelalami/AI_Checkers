from config_file import *
from utils import *


from piece import Piece
from move import Move

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

		self.dict_of_possible_moves = self.get_possible_moves()




	def create_grid(self):
		"""
		les cellules numpy.nan sont interdites
		les cellules positives : joueur 1
		les cellules négatives : joueur 2
		cellule normale la valeur aboslue vaut 1
		cellule reine la valeur absolue vaut 5
		"""


		self.checker_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

		for row in range(0, ROWS):
			for col in range(0, COLS):
				if (row + col) % 2 == 0:
					self.checker_grid[row][col]= math.nan

		for row in range(0, ROWS):
			for col in range(0, COLS):
				if (row + col) % 2 != 0:
					if row < FILLED_ROWS: # joueur 2
						self.checker_grid[row][col] = Piece(row, col, player=-1)

					elif row > ROWS - FILLED_ROWS -1 : # joueur 1
						self.checker_grid[row][col] = Piece(row, col, player=1)





	def move_piece(self, selected_piece_position, move_position):
		
		row_selection, col_selection = selected_piece_position

		current_piece = self.checker_grid[row_selection][col_selection]

		current_piece.row, current_piece.col = move_position

		self.checker_grid[row_selection][col_selection] = 0

		self.checker_grid[current_piece.row][current_piece.col] = current_piece


		for possible_move_object in self.dict_of_possible_moves[selected_piece_position]:
			if possible_move_object.get_final_position() == move_position:
				for attacked_piece_position in possible_move_object.list_attacked_enemy_pieces:
					row_to_attack, col_to_attack = attacked_piece_position
					self.checker_grid[row_to_attack][col_to_attack] = 0


		self.turn = -1 if self.turn==1 else 1

		self.dict_of_possible_moves = self.get_possible_moves()





	def get_cell_state(self, row, col):

		if is_out_of_bound(row, col):
			return "is_out_of_bound" # rien à faire


		elif self.checker_grid[row][col] == 0:
			return "accessible" # déplacement simple de profondeur 0

		elif type(self.checker_grid[row][col]) == Piece: 

			piece = self.checker_grid[row][col]
			if piece.player == self.turn:
				return "not_accessible" # rien à faire
			
			else : 
				return "enemy" # là ou on va gérer l'attaque d'une pièce adverse



	def get_possible_moves(self):
		"""
		dict_of_possible_move :
			+ key : position des pièces du joueur en cours (row, col) : tuple position de la pièce
			+ value : les moves possibles <= ??????????
		"""
		dict_of_all_moves = dict()

		for row in range(0, ROWS):
			for col in range(0, COLS):
				if type(self.checker_grid[row][col]) == Piece:
					current_piece = self.checker_grid[row][col]
					if current_piece.player == self.turn :
						depth, possible_moves_for_current_piece = self.get_possible_moves_for_current_piece(current_piece, depth=0, all_moves_for_current_piece=[])

						dict_of_all_moves[(row, col)] = depth, possible_moves_for_current_piece

		# les moves possibles sont les moves à depth maximale
		dict_of_possible_moves = {} # à remplir
		max_depth = 0

		for piece, (depth, possible_moves_for_current_piece) in dict_of_all_moves.items():
			if depth > max_depth:
				max_depth = depth 
				dict_of_possible_moves = {piece: possible_moves_for_current_piece}
			elif depth == max_depth:
				dict_of_possible_moves[piece] = possible_moves_for_current_piece
		
		return dict_of_possible_moves





	def get_possible_moves_for_current_piece(self, current_piece, depth, all_moves_for_current_piece):
		"""
		Algo du backtracking : Sudoku, Chemin plus court pour un cavalier, N-Queens
		Il s'agit d'un parcours en profondeur.
		ca renvoie un dictionnaire qui va indexé un déplacement final en fonction de sa profondeur


		on n'a pas encore gérer le cas où la pièce reine <=
		"""
		row, col = current_piece.row, current_piece.col

		row_to_check = row - self.turn 
		cols_to_check = [col-1, col+1]			



		for col_to_check in cols_to_check:

			cell_state =  self.get_cell_state(row_to_check, col_to_check)
			if cell_state == "accessible" and depth == 0:
				move_object = Move(initial_piece_position=(row, col),\
								  list_piece_positions=[(row_to_check, col_to_check)],\
								  list_attacked_enemy_pieces=[])
				
				all_moves_for_current_piece.append(move_object)
			

			elif cell_state == "enemy":
				row_arrival, col_arrival = 2*row_to_check - row, 2*col_to_check - col

				if self.get_cell_state(row_arrival, col_arrival) == "accessible":
					
					attacked_piece = self.checker_grid[row_to_check][col_to_check]
					self.checker_grid[row][col] = 0
					self.checker_grid[row_to_check][col_to_check] = 0
					self.checker_grid[row_arrival][col_arrival] = current_piece
					current_piece.row, current_piece.col = row_arrival, col_arrival

					# actualiser ma list all_moves_for_current_piece
					if depth == 0 :
						move_object = Move(initial_piece_position=(row, col),\
										   list_piece_positions=[(row_arrival, col_arrival)],\
								  		   list_attacked_enemy_pieces=[(row_to_check, col_to_check)])
						all_moves_for_current_piece.append(move_object)

					else:
						if depth < all_moves_for_current_piece[-1].get_depth():
							current_move_object = all_moves_for_current_piece[-1].extract_common_deplacement(extraction_depth=depth-1)
							all_moves_for_current_piece.append(current_move_object)

						all_moves_for_current_piece[-1].update_move(new_piece_postion=(row_arrival, col_arrival),\
															   new_attacked_enemy_piece=(row_to_check, col_to_check))


					self.get_possible_moves_for_current_piece(current_piece, depth+1, all_moves_for_current_piece)

					
					current_piece.row, current_piece.col = row, col
					self.checker_grid[row][col] = current_piece
					self.checker_grid[row_to_check][col_to_check] = attacked_piece
					self.checker_grid[row_arrival][col_arrival] = 0


		max_depth = 0
		possible_moves_for_current_piece = []

		for current_move in all_moves_for_current_piece:
			current_move_depth = current_move.get_depth()
			if current_move_depth > max_depth:
				max_depth = current_move_depth
				possible_moves_for_current_piece = [current_move]
			
			elif current_move_depth == max_depth:
				possible_moves_for_current_piece.append(current_move)


		return max_depth, possible_moves_for_current_piece





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
	for piece, moves in checker_grid_object.dict_of_possible_moves.items():
		print(piece, moves)