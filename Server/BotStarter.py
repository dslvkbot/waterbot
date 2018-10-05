import Database.ResetTables as reseterClass
import BotServer as bs
import Database.CreateTable as createClass
import Database.Table as Table


def create_table():
    createClass.create()


def reset_tables():
    reseterClass.ReseterClass(30).reset()


def bot_processing():
    vk_bot = bs.VkBot(token='')
    vk_bot.bot_processing()


create_table()
reset_tables()
bot_processing()
