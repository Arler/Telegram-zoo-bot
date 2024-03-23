from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

# ----------------------------------------------- Тут вопросы викторины ------------------------------------------------
# Первая строка - вопрос, остальные - варианты ответов
# Чем больше вопросов, тем точнее будет результат викторины
# Варианты ответов должны быть такими же как и особенности животных
questions = (
	('Где бы вы хотели жить?',
	'Джунгли', 'Снежные леса', 'Лесные опушки', 'Заболоченные озёра'
	),
	('Чем бы вы предпочли заниматься в свободное время?',
	'Бег', 'Отдыхать у воды', 'Посидеть один дома', 'Плотно покушать', 'Быть в компании друзей', 'Потанцевать', 'Поиграть'
	),
	('Что бы вы выбрали в качесте своей уникальны черты?',
	'Надолго задержать дыхание под водой', 'Адаптация к сложным ситуациям', 'Умение петь', 'Покушать посреди ночи',
	'Быстренько спрятаться от ненужных проблем', 'Не люблю сидеть на одном месте', 'Умение выстраивать сильные связи'
	),
)

# ----------------------------------------------- Тут животные викторины -----------------------------------------------
# image - Фотография животного.
# url - Ссылка на страницу животного на сайте зоопарка.
# features - Особенности животного. Особенности должны быть такими же как и варианты ответов
animals = {
	'Восточно-сибирская рысь': {
		'image': 'images/vostochno-sibirskaya_ris.jpeg',
		'url': 'https://new.moscowzoo.ru/animals/kinds/vostochno_sibirskaya_rys',
		'features': (
			'Снежные леса', 'Бег', 'Адаптация к сложным ситуациям'
		)
	},
	'Капибара': {
		'image': 'images/capibara.png',
		'url': 'https://moscowzoo.ru/animals/gryzuny/kapibara/?sphrase_id=750778',
		'features': (
			'Джунгли', 'Отдыхать у воды', 'Надолго задержать дыхание под водой'
		)
	},
	'Манул': {
		'image': 'images/manul.jpg',
		'url': 'https://new.moscowzoo.ru/animals/kinds/manul',
		'features': (
			'Снежные леса', 'Посидеть один дома', 'Адаптация к сложным ситуациям'
		)
	},
	'Карликовый бегемот': {
		'image': 'images/karlikoviy_begemot.jpg',
		'url': 'https://new.moscowzoo.ru/animals/kinds/karlikovyy_begemot',
		'features': (
			'Джунгли', 'Плотно покушать', 'Отдыхать у воды', 'Быстренько спрятаться от ненужных проблем'
		)
	},
	'Ушастая сова': {
		'image': 'images/ushastaya_sova.jpeg',
		'url': 'https://new.moscowzoo.ru/animals/kinds/ushastaya_sova',
		'features': (
			'Лесные опушки', 'Быть в компании друзей', 'Покушать посреди ночи'
		)
	},
	'Японский журавль': {
		'image': 'images/yaponskiy_zhuravl.jpeg',
		'url': 'https://new.moscowzoo.ru/animals/kinds/yaponskiy_zhuravl',
		'features': (
			'Заболоченные озёра', 'Потанцевать', 'Быть в компании друзей', 'Умение петь'
		)
	},
	'Золотистый львиный тамарин': {
		'image': 'images/zolotistiy_lviniy_tamarin.jpeg',
		'url': 'https://new.moscowzoo.ru/animals/kinds/zolotistyy_lvinyy_tamarin',
		'features': (
			'Джунгли', 'Быть в компании друзей', 'Поиграть', 'Не люблю сидеть на одном месте'
		)
	},
	'Азиатский слон': {
		'image': 'images/aziatskiy_slon.jpeg',
		'url': 'https://new.moscowzoo.ru/animals/kinds/aziatskiy_slon',
		'features': (
			'Джунгли', 'Быть в компании друзей', 'Умение выстраивать сильные связи'
		)
	},
}

# ------------------------------- Тут настройки для отправки email сообщений сотрудникам -------------------------------
smtp_settings = {
	'server': 'smtp.yandex.ru',
	'port': 465,
	'username': os.getenv('SMTP_USERNAME'),
	'password': os.getenv('SMTP_PASSWORD'),
}

# ------------------------------------------------ Тут email контакты. -------------------------------------------------
# В .env файле, email адреса для контактов должны быть через запятую.
# Для feedback_contacts предполагается один email адрес.
contacts = os.getenv('CONTACTS').split(',')
feedback_contacts = os.getenv('FEEDBACK_CONTACTS')

# -------------------------------------------- Тут общие картинки для бота ---------------------------------------------
images = {
	'start_message_image': 'images/MZoo-logo-сircle-small-preview.jpg'
}

# --------------------------------------------------- Тут сообщения ----------------------------------------------------
messages = {
	# Текст для стартового сообщения
	'start_message': """
		Здравствуйте! Это бот для викторины от московского зоопарка.\n
		Московский зоопарк — один из старейших зоопарков Европы с уникальной коллекцией животных и профессиональным 
		сообществом.\n
		Благодаря боту вы узнаете о программе опеки которая помогает зоопарку заботиться о его обитателях. Викторина, 
		которую вы пройдёте, будет на тему вашего тотемного животного из московского зоопарка, готовы его узнать?\n
		Нажмите на кнопку "Викторина" для начала викторины.
		""",
	# Текст для кнопки "Узнать больше"
	'more_about_care_program': """
		Важная задача зоопарка — вносить вклад в сохранение биоразнообразия планеты. Сотрудники зоопарка пытаются 
		уберечь виды от вымирания и вернуть их в естественную среду обитания.\n
		Сейчас в Московском зоопарке живёт около 6 000 животных, представляющих примерно 1 100 биологических видов 
		мировой фауны. Каждое животное уникально, и все требуют внимание и уход.\n
		«Возьми животное под опеку» («Клуб друзей») — это одна из программ, помогающих зоопарку заботиться о его 
		обитателях. Программа позволяет с помощью пожертвования на любую сумму внести свой вклад в развитие зоопарка и 
		сохранение биоразнообразия планеты. Из ежедневного рациона питания животного как раз и рассчитывается стоимость его опеки.\n
		Взять под опеку можно разных обитателей зоопарка, например, слона, льва, суриката или фламинго. Это возможность 
		помочь любимому животному или даже реализовать детскую мечту подружиться с настоящим диким зверем. Почётный 
		статус опекуна позволяет круглый год навещать подопечного, быть в курсе событий его жизни и самочувствия. 
		Участником программы может стать любой неравнодушный: и ребёнок, и большая корпорация. Поддержка опекунов 
		помогает зоопарку улучшать условия для животных и повышать уровень их благополучия.\n
		Вы можете узнать больше о программе опеки на сайте московского зоопарка — https://moscowzoo.ru/my-zoo/become-a-guardian/
		"""
}
