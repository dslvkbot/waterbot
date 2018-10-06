import Database.ResetTables as reseterClass
import BotServer as bs
import Database.CreateTable as createClass
from threading import Thread


def create_table():
    createClass.create()


def reset_tables():
    reseterClass.ReseterClass(30).reset()


def bot_processing():
    vk_bot = bs.VkBot(token='')
    vk_bot.bot_processing()


class ResetThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        reset_tables()


create_table()
rthread = ResetThread()
rthread.start()
bot_processing()
