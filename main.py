from dotenv import load_dotenv, find_dotenv
from quiz_bot import QuizBot
import os

load_dotenv(find_dotenv())

quiz_bot = QuizBot(token=os.getenv('TOKEN'))


@quiz_bot.message_handler(commands=['start', 'help'])
def launch_bot(message):
	quiz_bot.send_start_message(message)


@quiz_bot.callback_query_handler(lambda call: call.data == 'Викторина')
def start_quiz(callback):
	quiz_bot.send_first_question(callback)


@quiz_bot.callback_query_handler(lambda call: 'Ответ' in call.data)
def process_response(callback):
	quiz_bot.collect_answer(callback)

	if quiz_bot.current_question_index == len(quiz_bot.questions):  # Последний вопрос? Вывести результат
		quiz_bot.show_quiz_result(callback)
		quiz_bot.care_program_message(callback)
	else:  # Не последний? Отправить следующий вопрос
		quiz_bot.send_next_question(callback)


@quiz_bot.callback_query_handler(lambda call: call.data == 'Связаться')
def contact_with_zoo(callback):
	quiz_bot.contact_with_employee(callback)


@quiz_bot.callback_query_handler(lambda call: call.data == 'Обратная связь')
def feedback(callback):
	quiz_bot.possibility_of_feedback(callback)


@quiz_bot.callback_query_handler(lambda call: call.data == 'Узнать больше')
def learn_more(callback):
	quiz_bot.learn_more_message(callback)


@quiz_bot.callback_query_handler(lambda call: call.data == 'Отмена')
def cancel(callback):
	quiz_bot.cancel_next_step(callback)


if __name__ == '__main__':
	quiz_bot.infinity_polling()
