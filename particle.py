import random
import colorsys

class SandParticle:
	def __init__(self):
		self.color = random_color((0.1, 0.12), (0.5, 0.7), (0.7, 0.9))
		# Higher value = heavier (sinks through lighter particles)
		self.density = 2.0

	def update(self, grid, row, column):
		# 1. Try to fall straight down
		if grid.is_cell_empty(row + 1, column):
			return row + 1, column
		# 1b. If cell below is occupied by a less-dense particle, swap with it
		below = None
		if 0 <= row + 1 < grid.rows:
			below = grid.get_cell(row + 1, column)
		if below is not None and hasattr(below, 'density') and self.density > below.density:
			return row + 1, column
		# 2. Try to fall diagonally (down-left / down-right) into empty or swap if lighter
		offsets = [-1, 1]
		random.shuffle(offsets)
		for offset in offsets:
			new_column = column + offset
			# fall into empty diagonal
			if grid.is_cell_empty(row + 1, new_column):
				return row + 1, new_column
			# or swap with lighter diagonal particle
			if 0 <= row + 1 < grid.rows and 0 <= new_column < grid.columns:
				diag = grid.get_cell(row + 1, new_column)
				if diag is not None and hasattr(diag, 'density') and self.density > diag.density:
					return row + 1, new_column

		return row, column

class RockParticle:
	def __init__(self):
		self.color = random_color((0.0, 0.1), (0.1, 0.3), (0.3, 0.5))
		# Very heavy; other particles won't sink through rock
		self.density = 3.0

class WaterParticle:
	def __init__(self):
		self.color = random_color((0.55, 0.65), (0.6, 0.8), (0.7, 0.95))
		# Lightest
		self.density = 1.0

	def update(self, grid, row, column):
		# 1. Try to fall straight down
		if grid.is_cell_empty(row + 1, column):
			return row + 1, column
		# 1b. If cell below has a lighter particle, swap (water rises)
		below = None
		if 0 <= row + 1 < grid.rows:
			below = grid.get_cell(row + 1, column)
		if below is not None and hasattr(below, 'density') and self.density > below.density:
			return row + 1, column
		# 2. Try diagonals down-left / down-right into empty or swap if lighter
		offsets = [-1, 1]
		random.shuffle(offsets)
		for offset in offsets:
			new_column = column + offset
			if grid.is_cell_empty(row + 1, new_column):
				return row + 1, new_column
			if 0 <= row + 1 < grid.rows and 0 <= new_column < grid.columns:
				diag = grid.get_cell(row + 1, new_column)
				if diag is not None and hasattr(diag, 'density') and self.density > diag.density:
					return row + 1, new_column
		# 3. Move sideways like fluid
		for offset in offsets:
			new_column = column + offset
			if grid.is_cell_empty(row, new_column):
				return row, new_column

		return row, column

def random_color(hue_range, saturation_range, value_range):
	hue = random.uniform(*hue_range)
	saturation = random.uniform(*saturation_range)
	value = random.uniform(*value_range)
	r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
	return int(r * 255), int(g * 255), int(b * 255)