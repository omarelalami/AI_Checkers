from config_file import *
from piece import Piece
import pygame


class CheckerView:
	# implémentation du front-end
	def __init__(self):
		self.window = pygame.display.set_mode((HEIGHT, WIDTH))




	def draw_squares(self):
		self.window.fill(OFF_WITH)
		for row in range(0, ROWS):
			for col in range(0, COLS):
				if (row + col) % 2 != 0:
					pygame.draw.rect(self.window, BROWN, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



	def draw_pieces(self, checker_grid):
		for row in range(0, ROWS):
			for col in range(0, COLS):
				if type(checker_grid[row][col]) == Piece:
					current_piece = checker_grid[row][col]
					piece_position = CheckerView.compute_piece_position_on_window(row, col)
					
					if current_piece.player == 1:
						pygame.draw.circle(self.window, WHITE, piece_position, PIECE_RADIUS)

					elif current_piece.player == -1:
						pygame.draw.circle(self.window, BLACK, piece_position, PIECE_RADIUS)


	def update_grid(self, checker_grid):
		self.draw_squares()
		self.draw_pieces(checker_grid)



	def show_possible_moves(self, selected_piece, possible_moves):
		selected_piece_position = CheckerView.compute_piece_position_on_window(*selected_piece)
		pygame.draw.circle(self.window, BLUE, selected_piece_position, 5)


		for possible_move in possible_moves:
			possible_move_position = CheckerView.compute_piece_position_on_window(*possible_move)
			pygame.draw.circle(self.window, GREEN, possible_move_position, 5)


	@staticmethod
	def compute_piece_position_on_window(row, col):
		x = SQUARE_SIZE * col + SQUARE_SIZE // 2
		y = SQUARE_SIZE * row + SQUARE_SIZE // 2
		return x, y


	@staticmethod
	def compute_row_col_of_selected_piece(x, y):
		row = y // SQUARE_SIZE
		col = x // SQUARE_SIZE
		return row, col