from typing import Callable

from quiz_settings import contacts, feedback_contacts, smtp_settings, images, messages
from email.mime.text import MIMEText
from telebot import TeleBot, types
from quiz import Quiz
import textwrap
import smtplib
import logging
import random

logging.basicConfig(
	level=logging.INFO,
	filename=f'{__name__}.log',
	filemode='w',
	format='%(asctime)s %(levelname)s %(message)s'
)


class QuizBot(Quiz, TeleBot):
	def __init__(self, *args, **kwargs):
		TeleBot.__init__(self, *args, **kwargs)
		Quiz.__init__(self)

	def send_start_message(self, tg_message):
		"""При старте бот посылает сообщение приветствия и выдаёт кнопку для начала викторины"""
		try:
			self.clear_step_handler(tg_message)
			mark = types.InlineKeyboardMarkup()
			mark.add(types.InlineKeyboardButton(text='Викторина', callback_data='Викторина'))
			cleaned_lines = [line.strip() for line in messages['start_message'].splitlines()]
			message = '\n'.join(cleaned_lines)
			self.send_photo(
				chat_id=tg_message.chat.id,
				photo=open(images['start_message_image'], 'rb'),
				caption=message,
				reply_markup=mark,
			)
		except Exception as err:
			logging.error(err, exc_info=True)
		else:
			logging.info('Стартовое сообщение успешно отправлено')

	def send_first_question(self, callback):
		"""Функция для начала викторины, отправка первого вопроса"""
		try:
			self.clear_step_handler(callback.message)
			self.set_settings()
			buttons = self.__create_buttons()
			self.send_message(
				chat_id=callback.message.chat.id,
				text=f'{self.questions[self.current_question_index][0]}\nВыберите вариант ответа',
				reply_markup=buttons,
			)
		except Exception as err:
			logging.error(f'{err}\ncurrent question index: {self.current_question_index}', exc_info=True)
		else:
			logging.info('Викторина успешно начата')

	def send_next_question(self, callback):
		"""Метод для отправки следующего вопроса викторины"""
		try:
			self.clear_step_handler(callback.message)
			buttons = self.__create_buttons()
			self.edit_message_text(
				chat_id=callback.message.chat.id,
				message_id=callback.message.message_id,
				text=f'{self.questions[self.current_question_index][0]}\nВыберите вариант ответа',
				reply_markup=buttons,
			)
		except Exception as err:
			logging.error(f'{err}\nquestion index: {self.current_question_index}\nquestions: {self.questions}', exc_info=True)
		else:
			logging.info(f'Вопрос №{self.current_question_index + 1} успешно отправлен')

	def collect_answer(self, callback):
		"""Метод для сбора ответа пользователя и добавления его в список ответов"""
		try:
			user_callback_answer = callback.data.lstrip('Ответ ')
			self.user_answers.append((self.current_question_index, int(user_callback_answer)))
			self.current_question_index += 1
		except Exception as err:
			logging.error(
				msg=f"{err}\nuser answers: {self.user_answers}\nquestions: {self.questions}",
				exc_info=True)
		else:
			logging.info(f'Ответ пользователя успешно обработан - {self.questions[self.user_answers[-1][0]][self.user_answers[-1][1]]}')

	def show_quiz_result(self, callback):
		"""Метод для вывода результата викторины пользователю и отправки возможности связаться с зоопарком"""
		try:
			self.clear_step_handler(callback.message)
			self.delete_message(
				chat_id=callback.message.chat.id,
				message_id=callback.message.message_id,
			)
			self.result = self.quiz_result()  # Определение результата викторины
			self.__send_result(callback)  # Отправка результата
		except Exception as err:
			logging.error(f'{err}\nresult: {self.result.name}', exc_info=True)
		else:
			logging.info(f'Результат викторины - {self.result.name}, успешно отправлен пользователю')

	def possibility_of_feedback(self, callback):
		"""Метод для возможности отправить обратную свзяь о боте"""
		try:
			self.clear_step_handler(callback.message)
			mark = types.InlineKeyboardMarkup()
			mark.add(types.InlineKeyboardButton(text='Отмена', callback_data='Отмена'))
			self.send_message(
				chat_id=callback.message.chat.id,
				text='Напишите вашу обратную связь',
				reply_markup=mark,
			)
			logging.info('Возможность отправить обратную связь отправлена')
			self.register_next_step_handler(callback.message, self.__send_feedback_email)
		except Exception as err:
			logging.error(err, exc_info=True)

	def contact_with_employee(self, callback):
		"""Метод для отправки email сотрудникам зоопарка"""
		try:
			self.clear_step_handler(callback.message)
			mark = types.InlineKeyboardMarkup()
			mark.add(types.InlineKeyboardButton(text='Отмена', callback_data='Отмена'))
			self.send_message(
				chat_id=callback.message.chat.id,
				text='Введите ваш адрес электронной почты и сотрудник свяжется с вами для консультации',
				reply_markup=mark,
			)
			self.register_next_step_handler(callback.message, self.__send_result_email)
		except Exception as err:
			logging.error(f'{err}\nmessage: {callback.message}', exc_info=True)
		else:
			logging.info('Email адрес пользователя успешно запрошен')

	def care_program_message(self, callback):
		"""Метод для отправки начального сообщения о программе опеки"""
		try:
			mark = types.InlineKeyboardMarkup()
			mark.row(types.InlineKeyboardButton(text='Узнать больше', callback_data='Узнать больше'))
			self.send_message(
				chat_id=callback.message.chat.id,
				text='Вы можете узнать больше о программе опеки\nНажмите на кнопку "Узнать больше"',
				reply_markup=mark,
			)
		except Exception as err:
			logging.error(err, exc_info=True)

	def learn_more_message(self, callback):
		"""Метод для развёрнутого сообщения о программе опеки"""
		try:
			cleaned_lines = [line.strip() for line in messages['more_about_care_program'].splitlines()]
			message = '\n'.join(cleaned_lines)
			self.edit_message_text(
				chat_id=callback.message.chat.id,
				message_id=callback.message.message_id,
				text=message,
			)
		except Exception as err:
			logging.error(err, exc_info=True)

	def cancel_next_step(self, callback):
		self.clear_step_handler(callback.message)
		self.delete_message(
			chat_id=callback.message.chat.id,
			message_id=callback.message.message_id,
		)

	def __send_result(self, callback):
		"""Отправка результата викторины и кнопок чтобы поделится или перезапустить викторину"""
		# Создание текста чтобы поделится в Вконтакте
		message = f"""\
			Моё тотемное животное из викторины московского зоопарка это {self.result.name}, хочешь узнать своё?
			Ты тоже можешь пройти викторину в телеграм боте московского зоопарка\
			https://t.me/{self.get_me().username}"""
		message = ' '.join(message.split())
		# Создание кнопок
		mark = types.InlineKeyboardMarkup()
		mark.row(
			types.InlineKeyboardButton(text='Поедлитсья', url=f'https://vk.com/share.php?comment={message}'),
			types.InlineKeyboardButton(text='Повторить', callback_data='Викторина')
		)
		mark.row(
			types.InlineKeyboardButton(text='Связаться', callback_data='Связаться'),
			types.InlineKeyboardButton(text='Обратная связь', callback_data='Обратная связь')
		)
		# Отправка фото животного и результата викторины
		self.send_photo(
			chat_id=callback.message.chat.id,
			photo=open(self.result.image, 'rb'),
			caption=textwrap.dedent(f"""\
				 Викторина закончена.
				 Поздравляю, ваше животное это {self.result.name}!
				 Узнать больше о животном на сайте зоопарка — {self.result.url}\n
				 Вы можете повторить викторину
				 Вы можете поделиться своим результатом в Вконтакте.
				 Вы можете связаться с зоопарком насчёт программы опеки.
				 Вы можете оставить обратную связь о боте.
			 """),
			reply_markup=mark,
		)

	def __send_result_email(self, message):
		"""Отправляет сообщение на электронную почту случайному сотруднику зоопарка"""
		employee = random.choice(contacts)
		if '@' not in message.text:
			self.send_message(
				chat_id=message.chat.id,
				text='Пожалуйста, введите действительный адрес электронной почты',
			)
			self.register_next_step_handler(message, self.__send_result_email)
		else:
			self.__send_mail(
				from_=smtp_settings['username'],
				to=employee,
				subject='Сообщение от пользователя',
				message=self.__collect_result_email_message(message),
			)
			self.send_message(
				chat_id=message.chat.id,
				text='Сообщение отправлено сотруднику зоопарка, он свяжется с вами через некоторое время',
			)

	def __send_feedback_email(self, message):
		"""Метод отправки сообщения об обратной связи на email"""
		if len(message.text) < 20:
			self.send_message(
				chat_id=message.chat.id,
				text='Обратная связь не должна быть такой короткой, напишите более развёрнуто',
			)
			self.register_next_step_handler(message, self.__send_feedback_email)
		else:
			self.__send_mail(
				from_=smtp_settings['username'],
				to=feedback_contacts,
				subject='Обратная связь от пользователя',
				message=message.text
			)
			self.send_message(
				chat_id=message.chat.id,
				text='Ваша обратная связь отправлена. Спасибо за вашу обратную связь.',
			)
			logging.info(f'Обратная связь отправлена на почту {feedback_contacts}')

	def __collect_result_email_message(self, message):
		"""Метод создания сообщения с результатом для email"""
		msg = [
			f'Пользователь {message.text} желает связаться',
			'Результат прохождения викторины:',
			f'Животное - {self.result.name}'
		]
		for question, answer in self.user_answers:
			msg.append(f"{self.questions[question][0]} Ответ: {self.questions[question][answer]}")
		msg = '\n'.join(msg)

		return msg

	def __create_buttons(self):
		"""Метод создания кнопок ответов для сообщения с вопросом викторины"""
		# Генерация ответов в виде кнопок
		mark = types.InlineKeyboardMarkup()
		for index, answer in enumerate(self.questions[self.current_question_index][1:]):
			mark.row(types.InlineKeyboardButton(
					text=answer,  # Текст ответа
					# + 1 нужно потому что enumerate при использовании среза [1:] видит список ответов без вопроса
					# в кортеже, и соответственно первый ответ для кнопки будет по индексу 0
					callback_data=f'Ответ {index + 1}'
				))

		return mark

	@staticmethod
	def __send_mail(from_=None, to=None, subject=None, message=None):
		"""Отправляет сообщение на электронную почту"""
		with smtplib.SMTP_SSL(smtp_settings['server'], port=smtp_settings['port']) as server:
			server.login(
				user=smtp_settings['username'],
				password=smtp_settings['password']
			)

			msg = MIMEText(message)
			msg['Subject'] = subject
			msg['From'] = from_
			msg['To'] = to

			server.sendmail(
				from_addr=smtp_settings['username'],
				to_addrs=to,
				msg=msg.as_string()
			)
