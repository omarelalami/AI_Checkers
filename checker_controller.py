import checker_model, checker_view

class CheckerController:
	# connexion backend / frontend
	def __init__(self):
		self.check_model_object = checker_model.CheckerModel()