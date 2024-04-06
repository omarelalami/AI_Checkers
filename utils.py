from config_file import *

def is_out_of_bound(row, col):
	return row < 0 or row >= ROWS or col < 0 or col >= COLS