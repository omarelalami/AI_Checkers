import checker_model, checker_view
from config_file import *

import pygame

class CheckerController:
	# connexion backend / frontend
	def __init__(self):
		self.checker_model_object = checker_model.CheckerModel()
		self.checker_view_object = checker_view.CheckerView()
		self.run_game()



	def selected_piece(self, x, y):
		selected_piece = checker_view.CheckerView.compute_row_col_of_selected_piece(x, y)
		possible_moves = []

		if selected_piece in self.checker_model_object.dict_of_best_moves.keys():
			possible_moves = self.checker_model_object.dict_of_best_moves[selected_piece]

		return selected_piece, possible_moves


	def action_on_grid(self, selected_piece, possible_moves):
		clicked_position = pygame.mouse.get_pos()

		if not selected_piece or not possible_moves:
			selected_piece, possible_moves = self.selected_piece(*clicked_position)


		elif selected_piece and possible_moves:
			move = checker_view.CheckerView.compute_row_col_of_selected_piece(*clicked_position)
			
			if move in possible_moves: # quand la personne clique sur un point vert
				self.checker_model_object.move_piece(selected_piece, move)
				selected_piece = None
				possible_moves = []
			
			else: # quand la personne veut changer la pièce selectionnée:
				selected_piece, possible_moves = self.selected_piece(*clicked_position)

		return selected_piece, possible_moves


	def run_game(self):

		run = True
		clock = pygame.time.Clock()

		selected_piece = None
		possible_moves = []

		while run:

			clock.tick(FPS)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				
				if event.type == pygame.MOUSEBUTTONDOWN:
					selected_piece, possible_moves = self.action_on_grid(selected_piece, possible_moves)
					


			self.checker_view_object.update_grid(self.checker_model_object.checker_grid)

			if selected_piece and possible_moves:
				self.checker_view_object.show_possible_moves(selected_piece, possible_moves)

			pygame.display.update()

		pygame.quit()