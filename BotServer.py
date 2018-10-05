from Database.Table import Table
from GUIClasses import Order
from KeyboardClasses import Button, KeyboardConstructor
import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


# token = '489aa25f9b01a64d7e8be333f9116a31c8c0ea1fd25868e6f90ea6e0c635d30d80b1a7647b9832f6f4894'

# def add_order_to_archive(user_id, count):


class VkBot:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=token)
        self.ordersdict = dict()
        self.ordersdb = Table('orders')
        self.clients = Table('clients')
        self.archive = Table('archive')

    def write_msg(self, user_id, s):
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': s})

    def write_keyboard(self, user_id, message, keyboard):
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'keyboard': keyboard})

    def get_last_msg_text(self, peer_id):
        try:
            dictionary = self.vk_session.method('messages.getHistory', {'offset': 1, 'count': 1, 'peer_id': peer_id})
            items = dictionary['items']
            return items[0]['text']
        except IndexError:
            print('Fuck')

    def parse_message(self, message):
        if message.from_me:
            return
        elif message.text == 'Начать':
            self.message_help(message)
        elif message.text == 'Создать заявку':
            self.message_make_order(message)
        elif message.text == 'Удалить заявку':
            self.message_delete_order(message)
        elif message.text == 'Список':
            self.message_list_orders(message)
        else:
            last_text = self.get_last_msg_text(message.user_id)
            if last_text == 'Введите номер комнаты с корпусом.':
                self.message_to_enter_count(message)
            elif last_text == 'Введите количество бутылей по 5 литров.':
                self.message_to_enter_time(message)
            elif last_text == 'Выберите удобное время.':
                self.message_to_enter_type(message)
            elif last_text == 'Выберите способ оплаты.':
                self.message_order_registered(message)
            else:
                self.message_help(message)

    def message_help(self, message):
        makeorder_button = Button.Button('Создать заявку', 'positive')
        deleteorder_button = Button.Button('Удалить заявку', 'negative')
        button_list = [makeorder_button, deleteorder_button]
        position = [1, 1]
        keyboard = KeyboardConstructor.construct_keyboard(button_list, position)
        self.write_keyboard(message.user_id, 'Выберите один из вариантов.', keyboard)

    def message_make_order(self, message):
        if len(self.clients.get_info_by_user_id(message.user_id, ['room'])) != 0:
            self.message_to_enter_count(message)
        else:
            self.write_msg(message.user_id, 'Введите номер комнаты с корпусом.')

    def message_to_enter_count(self, message):
        self.write_msg(message.user_id, 'Введите количество бутылей по 5 литров.')
        if len(self.clients.get_info_by_user_id(message.user_id, ['room'])) == 0:
            self.clients.insert_into({'user_id': message.user_id, 'room': message.text})

    def message_to_enter_time(self, message):
        global room
        info = self.clients.get_info_by_user_id(message.user_id, ['room'])
        if len(info) != 0:
            room = info[0][0]
        new_order = Order.Order(room=room, count=int(message.text))
        if int(message.text) > 0:
            self.ordersdict.update({message.user_id: new_order})
            button_18 = Button.Button('18:00', 'default')
            button_19 = Button.Button('19:00', 'default')
            button_20 = Button.Button('20:00', 'default')
            button_21 = Button.Button('21:00', 'default')
            button_list = [button_18, button_19, button_20, button_21]
            position = [2, 2]
            keyboard = KeyboardConstructor.construct_keyboard(button_list, position)
            self.write_keyboard(message.user_id, 'Выберите удобное время.', keyboard)
        else:
            self.write_msg(message.user_id, 'Введите положительное число.')
            self.message_help(message)

    def message_to_enter_type(self, message):
        global order_enter_type
        if message.user_id in self.ordersdict.keys():
            order_enter_type = self.ordersdict[message.user_id]
        order_enter_type.change_time(message.text)
        self.ordersdict.update({message.user_id: order_enter_type})
        button_bank = Button.Button('Перевод на банковскую карту', 'positive')
        button_cash = Button.Button('Наличными', 'negative')
        button_list = [button_bank, button_cash]
        position = [1, 1]
        keyboard = KeyboardConstructor.construct_keyboard(button_list, position)
        self.write_keyboard(message.user_id, 'Выберите способ оплаты.', keyboard)

    def message_order_registered(self, message):
        if message.user_id in self.ordersdict.keys():
            order = self.ordersdict[message.user_id]
            order.change_type(message.text)
            self.ordersdict.update({message.user_id: order})
            cur_date = datetime.datetime.today()
            date = "{day}.{month}.{year}"
            date = date.format(day=str(cur_date.day), month=str(cur_date.month), year=str(cur_date.year))
            self.ordersdb.insert_into({'user_id': message.user_id, 'room': order.room, 'count': str(order.count),
                                       'time': order.time, 'type': order.type_of_payment, 'date': date})
            self.ordersdict.pop(message.user_id)
            now = datetime.datetime.now()
            self.archive.insert_into(
                {'user_id': message.user_id, 'count': str(order.count), 'date': now.strftime('%d-%m-%Y')})
            self.write_msg(message.user_id,
                           'Заказ на ' + str(5 * order.count) + ' литров воды в комнату ' + order.room +
                           ' на ' + order.time + ' создан.\n' + message.text + '.')
            self.message_help(message)

    def message_delete_order(self, message):
        self.ordersdb.delete_info_by_user_id(message.user_id)
        self.write_msg(message.user_id, 'Заявки удалены.')
        self.message_help(message)

    def message_list_orders(self, message):
        if message.user_id == 21838346:
            mes = self.ordersdb.select(['room', 'count', 'time', 'type'])
            longmes = ''
            for item in mes:
                longmes += ('Заказ в комнату ' + item[0] + ' на ' + str(5 * int(item[1])) + ' литров воды в ' + item[2]
                            + '. ' + item[3] + '.\n\n')
            if len(mes) == 0:
                self.write_msg(message.user_id, 'Список пуст.')
            else:
                self.write_msg(message.user_id, longmes)
            self.message_help(message)

    def bot_processing(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                self.parse_message(event)
                print('Новое сообщение:')
                if event.from_me:
                    print('От меня для: ', end='')
                elif event.to_me:
                    print('Для меня от: ', end='')
                if event.from_user:
                    print(event.user_id)
                elif event.from_chat:
                    print(event.user_id, 'в беседе', event.chat_id)
                elif event.from_group:
                    print('группы', event.group_id)
                print('Текст: ', event.text)
            elif event.type == VkEventType.USER_TYPING:
                print('Печатает ', end='')
                if event.from_user:
                    print(event.user_id)
                elif event.from_group:
                    print('администратор группы', event.group_id)
            elif event.type == VkEventType.USER_TYPING_IN_CHAT:
                print('Печатает ', event.user_id, 'в беседе', event.chat_id)
            elif event.type == VkEventType.USER_ONLINE:
                print('Пользователь', event.user_id, 'онлайн', event.platform)
            elif event.type == VkEventType.USER_OFFLINE:
                print('Пользователь', event.user_id, 'оффлайн', event.offline_type)
            else:
                print(event.type, event.raw[1:])
