import Database.ResetTables as reseterClass


def reset_tables():
    reseter = reseterClass.ReseteDatabase(reset_time=[3, 0, 0], radius=30)
    reseter.reset()


reset_tables()
