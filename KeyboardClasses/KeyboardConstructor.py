import json


def construct_keyboard(button_list, position):
    size = len(button_list)
    i = 0
    buttons_array = list()

    for posY in range(0, len(position)):
        buttons_array.append(list())
        for posX in range(0, position[posY]):
            item = button_list[i]
            temp = dict()
            temp.update({'type': 'text'})
            temp.update({'label': 'message' + str(i)})
            button = dict()
            button.update({'action': temp})
            button.update({'color': item.color})
            buttons_array[posY].append(button)
            i += 1

    keyboard = json.dumps(
        {'one_time': True,
         'buttons': buttons_array})
    for i in range(0, size):
        keyboard = keyboard.replace('message' + str(i), button_list[i].label)
    return keyboard
