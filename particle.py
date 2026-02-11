import random
import colorsys

class SandParticle:
	def __init__(self):
		# 💤 Sistema de repouso
		self.sleeping = False
		self.sleep_counter = 0
		self.sleep_threshold = 5  # frames parado antes de dormir
		
		self.color = random_color((0.1, 0.12), (0.5, 0.7), (0.7, 0.9))
		self.density = 2.0

		# 🔧 Ajustáveis
		self.slide_chance = 0.6      # chance de tentar deslizar
		self.settle_chance = 0.15    # chance de micro-ajuste mesmo estável

	def update(self, grid, row, column):

		offsets = [-1, 1]
		random.shuffle(offsets)

		# 1️⃣ Cair direto
		if grid.is_cell_empty(row + 1, column):
			return row + 1, column

		# 2️⃣ Trocar com partícula menos densa abaixo
		if 0 <= row + 1 < grid.rows:
			below = grid.get_cell(row + 1, column)
			if below is not None and hasattr(below, 'density'):
				if self.density > below.density:
					return row + 1, column

		# 3️⃣ Deslizamento diagonal natural
		for offset in offsets:
			new_col = column + offset

			if grid.is_cell_empty(row + 1, new_col):
				return row + 1, new_col

			if 0 <= row + 1 < grid.rows and 0 <= new_col < grid.columns:
				diag = grid.get_cell(row + 1, new_col)
				if diag is not None and hasattr(diag, 'density'):
					if self.density > diag.density:
						return row + 1, new_col

		# 4️⃣ 🔹 Verificação de estabilidade (empacotamento granular)

		left_support = None
		right_support = None

		if 0 <= column - 1 < grid.columns:
			left_support = grid.get_cell(row + 1, column - 1)

		if 0 <= column + 1 < grid.columns:
			right_support = grid.get_cell(row + 1, column + 1)

		# Se só tem suporte de um lado → pode deslizar
		if random.random() < self.slide_chance:
			if left_support is None and right_support is not None:
				if grid.is_cell_empty(row, column - 1):
					return row, column - 1

			if right_support is None and left_support is not None:
				if grid.is_cell_empty(row, column + 1):
					return row, column + 1

		# 5️⃣ 🔹 Micro ajuste ("encaixe granular")
		# Mesmo estável, pequena chance de reorganizar

		if random.random() < self.settle_chance:
			for offset in offsets:
				new_col = column + offset
				if 0 <= new_col < grid.columns:
					if grid.is_cell_empty(row, new_col) and not grid.is_cell_empty(row + 1, new_col):
						return row, new_col

		return row, column

class RockParticle:
	#Cor
	def __init__(self):
		self.color = random_color((0.0, 0.1), (0.1, 0.3), (0.3, 0.5))
		# Very heavy; other particles won't sink through rock
		self.density = 3.0

class WaterParticle:
	def __init__(self):
		# 💤 Sistema de repouso
		self.sleeping = False
		self.sleep_counter = 0
		self.sleep_threshold = 5  # frames parado antes de dormir

		self.color = random_color((0.55, 0.65), (0.6, 0.8), (0.7, 0.95))
		self.density = 1.0
		
		# 🔧 Ajustáveis
		self.dispersion_rate = 0.35        # chance base de espalhar
		self.max_dispersion_distance = 3   # alcance lateral
		self.fall_chance = 0.95            # chance de cair mesmo se puder

	def update(self, grid, row, column):

		offsets = [-1, 1]
		random.shuffle(offsets)

		# 1️⃣ Tentar cair para baixo (com leve aleatoriedade)
		if grid.is_cell_empty(row + 1, column):
			if random.random() < self.fall_chance:
				return row + 1, column

		# 2️⃣ Trocar com partícula mais leve abaixo
		if 0 <= row + 1 < grid.rows:
			below = grid.get_cell(row + 1, column)
			if below is not None and hasattr(below, 'density'):
				if self.density > below.density:
					return row + 1, column

		# 3️⃣ Tentar diagonais
		for offset in offsets:
			new_column = column + offset

			if grid.is_cell_empty(row + 1, new_column):
				return row + 1, new_column

			if 0 <= row + 1 < grid.rows and 0 <= new_column < grid.columns:
				diag = grid.get_cell(row + 1, new_column)
				if diag is not None and hasattr(diag, 'density'):
					if self.density > diag.density:
						return row + 1, new_column

		# 4️⃣ Espalhamento lateral com efeito de pressão
		# Se chegou aqui, está bloqueada verticalmente
		pressure_multiplier = 1.8
		dispersion_chance = self.dispersion_rate * pressure_multiplier

		if random.random() < dispersion_chance:
			for distance in range(1, self.max_dispersion_distance + 1):
				for direction in offsets:
					new_column = column + direction * distance

					if 0 <= new_column < grid.columns:
						if grid.is_cell_empty(row, new_column):
							return row, new_column

		return row, column

#Cor random
def random_color(hue_range, saturation_range, value_range):
	hue = random.uniform(*hue_range)
	saturation = random.uniform(*saturation_range)
	value = random.uniform(*value_range)
	r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
	return int(r * 255), int(g * 255), int(b * 255)