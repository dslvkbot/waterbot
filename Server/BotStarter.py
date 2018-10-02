import Database.ResetTables as reseterClass
import BotServer as bs
import Database.CreateTable as createClass
import Database.Table as Table


def create_table():
    createClass.create()


def reset_tables():
    reseter = reseterClass.ResetDatabase(reset_time=[3, 0, 0], radius=30)
    reseter.reset()


def bot_processing():
    vk_bot = bs.VkBot(token='')
    vk_bot.bot_processing()


create_table()
reset_tables()
bot_processing()
