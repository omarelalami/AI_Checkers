class Move:
	def __init__(self, initial_piece_position, list_piece_positions, list_attacked_enemy_pieces):
		self.initial_piece_position = initial_piece_position
		self.list_piece_positions = list_piece_positions
		self.list_attacked_enemy_pieces = list_attacked_enemy_pieces


	def update_move(self, new_piece_postion, new_attacked_enemy_piece):
		self.list_piece_positions.append(new_piece_postion)
		self.list_attacked_enemy_pieces.append(new_attacked_enemy_piece)


	def get_depth(self):
		return len(self.list_attacked_enemy_pieces)


	def get_final_position(self):
		return self.list_piece_positions[-1]


	def extract_common_deplacement(self, extraction_depth):
		initial_piece_position = self.initial_piece_position
		list_piece_position = self.list_piece_position[: extraction_depth]
		list_attacked_enemy_pieces = self.list_attacked_enemy_pieces[: extraction_depth]

		return Move(initial_piece_position, list_piece_position, list_attacked_enemy_pieces)