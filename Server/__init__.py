import Database.ResetTables as reseterClass
import BotServer as bs
import Database.CreateTable as createClass


def create_table():
    createClass.create()


def reset_tables():
    reseter = reseterClass.ReseteDatabase(reset_time=[3, 0, 0], radius=30)
    reseter.reset()


def bot_processing():
    vk_bot = bs.VkBot(token='489aa25f9b01a64d7e8be333f9116a31c8c0ea1fd25868e6f90ea6e0c635d30d80b1a7647b9832f6f4894')
    vk_bot.bot_processing()


create_table()
reset_tables()
bot_processing()
