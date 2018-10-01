from GUIClasses import Order
from KeyboardClasses import Button, KeyboardConstructor
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


# token = '489aa25f9b01a64d7e8be333f9116a31c8c0ea1fd25868e6f90ea6e0c635d30d80b1a7647b9832f6f4894'

class VkBot:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=token)
        self.orders = dict()
        self.clients = dict()

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
        if message.user_id in self.clients.keys():
            self.message_to_enter_count(message)
        else:
            self.write_msg(message.user_id, 'Введите номер комнаты с корпусом.')

    def message_to_enter_count(self, message):
        self.write_msg(message.user_id, 'Введите количество бутылей по 5 литров.')
        if message.user_id not in self.clients.keys():
            self.clients.update({message.user_id: message.text})

    def message_to_enter_time(self, message):
        global room
        if message.user_id in self.clients.keys():
            room = self.clients[message.user_id]
        new_order = Order.Order(room=room, count=int(message.text))
        if int(message.text) > 0:
            self.orders.update({message.user_id: new_order})
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
        if message.user_id in self.orders.keys():
            order_enter_type = self.orders[message.user_id]
        order_enter_type.change_time(message.text)
        self.orders.update({message.user_id: order_enter_type})
        button_bank = Button.Button('Перевод на банковскую карту', 'positive')
        button_cash = Button.Button('Наличными', 'negative')
        button_list = [button_bank, button_cash]
        position = [1, 1]
        keyboard = KeyboardConstructor.construct_keyboard(button_list, position)
        self.write_keyboard(message.user_id, 'Выберите способ оплаты.', keyboard)

    def message_order_registered(self, message):
        if message.user_id in self.orders.keys():
            order = self.orders[message.user_id]
            order.change_type(message.text)
            self.orders.update({message.user_id: order})
            self.write_msg(message.user_id,
                           'Заказ на ' + str(5 * order.count) + ' литров воды в комнату ' + order.room +
                           ' на ' + order.time + ' создан.\n' + message.text + '.')
            self.message_help(message)

    def message_delete_order(self, message):
        if message.user_id in self.orders.keys():
            self.orders.pop(message.user_id)
            self.write_msg(message.user_id, 'Заявка удалена.')
        else:
            self.write_msg(message.user_id, 'Заявка не найдена.')
        self.message_help(message)

    def message_list_orders(self, message):
        if message.user_id == 21838346:
            orderslist = self.orders.keys()
            for key in orderslist:
                try:
                    thisorder = self.orders[key]
                    self.write_msg(message.user_id,
                                   'Заказ в комнату ' + thisorder.room + ' на ' + str(5 * thisorder.count)
                                   + ' литров воды в ' + thisorder.time + '.\n' + thisorder.type_of_payment + '.')
                except KeyError:
                    print('Undefined behaviour')
            if len(orderslist) == 0:
                self.write_msg(message.user_id, 'Список пуст.')
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


vk_bot = VkBot(token='489aa25f9b01a64d7e8be333f9116a31c8c0ea1fd25868e6f90ea6e0c635d30d80b1a7647b9832f6f4894')
vk_bot.bot_processing()
