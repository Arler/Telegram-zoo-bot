from quiz_settings import questions, animals
import logging


logging.basicConfig(
	level=logging.INFO,
	filename=f'{__name__}.log',
	filemode='w',
	format='%(asctime)s %(levelname)s %(message)s'
)


class Animal:
	def __init__(self, name, image, url, features):
		self.name = name
		self.image = image
		self.url = url
		self.features = features


class Quiz:
	"""Класс для настройки викторины"""

	def set_settings(self):
		"""Метод для установки настроек викторины"""
		self.questions: tuple[tuple[str]] = questions
		self.animals: list[Animal] = self.__collect_animals(animals)
		self.result = None
		self.user_answers = []
		self.current_question_index = 0

	def quiz_result(self):
		"""Метод для определения результата викторины. Возвращает объект Animal"""
		try:
			quiz_rating = {}
			result_animal = None

			for animal in self.animals:
				for question_index, answer_index in self.user_answers:
					if self.questions[question_index][answer_index] in animal.features and animal.name in quiz_rating.keys():
						quiz_rating[animal.name] += 1
					elif self.questions[question_index][answer_index] in animal.features and animal.name not in quiz_rating.keys():
						quiz_rating[animal.name] = 1

			# Определение животного с максимальным количеством совпадений.
			# Если животные будут иметь равное количество совпадений, выбирается первое из словаря
			max_rating_animal = max(quiz_rating, key=quiz_rating.get)

			for animal in self.animals:  # Определение объекта животного
				if animal.name is max_rating_animal:
					result_animal = animal

			if not result_animal:
				raise ValueError(f'Не удалось обработать список животных из ответов')
		except Exception as err:
			logging.error(f'user_answers: {self.user_answers}', exc_info=True)
		else:
			logging.info('Результат викторины успешно определён')
			return result_animal

	@staticmethod
	def __collect_animals(animals: dict):
		"""Метод для создания объектов животных из файла с настройками"""
		animals_list = []
		for animal_name in animals.keys():
			animals_list.append(Animal(
				name=animal_name,
				image=animals[animal_name]['image'],
				url=animals[animal_name]['url'],
				features=animals[animal_name]['features']
			))

		return animals_list
