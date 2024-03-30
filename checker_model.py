import numpy
import math

class CheckerModel:
	# attaquer un cellule adverse
	# detection du chemin le plus long
	# créer un fonction qui va permettre l'intégration du bot qui pourra prendre le role du joueur 2:
		# MinMax 
		# MonteCarlo
		# Neural Network

	def __init__(self):
		self.create_grid()
		self.turn = 1 # 1 : pour le joueur 1 et -1 pour le joueur 2

		print(self.checker_grid)
		for key, value in self.get_all_possible_moves().items():
			print(key, value)


	def create_grid(self):
		"""
		les cellules numpy.nan sont interdites
		les cellules positives : joueur 1
		les cellules négatives : joueur 2
		"""

		self.checker_grid = numpy.zeros(shape=(10, 10))

		for row in range(0, 10):
			for col in range(0, 10):
				if (row + col) % 2 == 0:
					self.checker_grid[row, col]= math.nan

		for row in range(0, 10):
			for col in range(0, 10):

				if not numpy.isnan(self.checker_grid)[row, col] and row < 4: # joueur 2
					self.checker_grid[row, col] = -1

				elif not numpy.isnan(self.checker_grid)[row, col] and row > 5: # joueur 2
					self.checker_grid[row, col] = 1



	@staticmethod
	def is_out_of_bound(row, col):
		return row < 0 or row >= 10 or col < 0 or col >= 10


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
			return "check_more_in_depth"



	def get_all_possible_moves(self):
		dict_of_possible_moves = dict()
		for row in range(0, 10):
			for col in range(0, 10):
				if self.checker_grid[row, col] == self.turn:
					dict_of_possible_moves[(row, col)] = []

					row_to_check = row - self.turn 
					left_col = col - 1
					right_col = col + 1
					
					if not CheckerModel.is_out_of_bound(row_to_check, left_col):

						is_busy_state =  self.is_busy(row_to_check, left_col)
						if is_busy_state == "accessible":

							dict_of_possible_moves[(row, col)].append((row_to_check, left_col))
						elif is_busy_state == "check_more_in_depth":
							pass


					if not CheckerModel.is_out_of_bound(row_to_check, right_col):
						is_busy_state =  self.is_busy(row_to_check, right_col)
						if is_busy_state == "accessible":
							dict_of_possible_moves[(row, col)].append((row_to_check, right_col))
						elif is_busy_state == "check_more_in_depth":
							pass

		


		return dict_of_possible_moves
