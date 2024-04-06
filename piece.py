class Piece:
	def __init__(self, row, col, player):
		self.row = row 
		self.col = col 
		self.player = player

		self.king = False


	def become_king(self):
		self.king = True



	def __repr__(self):
		return f"king {self.player}" if self.king else f"player {self.player}"