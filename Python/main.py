from PyQt5 import uic, QtMultimedia, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QInputDialog
from PyQt5.QtWidgets import QListWidgetItem, QPushButton, QListWidget, QTextBrowser, QCheckBox
import sqlite3  # импортируем все необходимые для проекта библиотеки
import os
import sys
import time
from PIL import Image
import datetime
import shutil
from PyQt5.QtCore import Qt

# pyinstaller --onefile --noconsole Chat.py
# создаем тоблицу стилей для светлого оформления
LIGHT_STYLE_SHEET = 'QPushButton {\n' \
                    'background-color: #42e6ec;\n' \
                    'width: 2px;\n' \
                    'radius: 10px;\n' \
                    'color: white;\n' \
                    'border-radius: 10px;\n' \
                    'font: bold, Arial, 15px;\n' \
                    '}\n' \
                    'QMainWindow {\n' \
                    'background-color: #cdeaff;\n' \
                    'font: bold, Arial, 15px;\n' \
                    '}\n' \
                    'QLineEdit {\n' \
                    'border-radius: 10px;\n' \
                    'font: bold, Arial, 15px;\n' \
                    '}\n' \
                    'QLabel {\n' \
                    'font: bold, Arial, 15px;\n' \
                    '}\n' \
                    'QPushButton:pressed {\n' \
                    'background-color: #42d4da;\n' \
                    'border-style: inset;\n' \
                    '}\n' \
                    'QMainWindow {\n' \
                    'background-color: #cdeaff;\n' \
                    '}\n' \
                    'QTextBrowser {\n' \
                    'font: bold, Arial, 12px;\n' \
                    'background-color: #e0f5ff;\n' \
                    'border-color: black;\n' \
                    'border-radius: 10px;}\n' \
                    'QStatusBar {\n' \
                    'font: font: bold, Arial, 8px;\n' \
                    'color: red;}'
# создаем таблицу стилей для темного оформления
DARK_STYLE_SHEET = 'QPushButton {\n' \
                   'background-color: #707070;\n' \
                   'width: 2px;\n' \
                   'radius: 10px;\n' \
                   'color: white;\n' \
                   'border-radius: 10px;\n' \
                   'font: bold, Arial, 15px;\n' \
                   '}\n' \
                   'QMainWindow {\n' \
                   'background-color: #333333;\n' \
                   'font: bold, Arial, 15px;\n' \
                   '}\n' \
                   'QLineEdit {\n' \
                   'border-radius: 10px;\n' \
                   'font: bold, Arial, 15px;\n' \
                   'background-color: #5d5d5d;\n' \
                   'color: #ffffff;\n' \
                   '}\n' \
                   'QLabel {\n' \
                   'font: bold, Arial, 15px;\n' \
                   'color: #ffffff\n' \
                   '}\n' \
                   'QPushButton:pressed {\n' \
                   'background-color: #1d1d1d;\n' \
                   'border-style: inset;\n' \
                   '}\n' \
                   'QTextBrowser {\n' \
                   'font: bold, Arial, 12px;\n' \
                   'background-color: #8b8b8b;\n' \
                   'border-color: black;\n' \
                   'border-radius: 10px;\n' \
                   'color: #ffffff;\n' \
                   '}\n' \
                   'QStatusBar {\n' \
                   'font: font: bold, Arial, 8px;\n' \
                   'color: red;' \
                   'QCheckBox {' \
                   'color: #ffffff;\n' \
                   '}\n}'
# задаем светлую тему по умолчанию
CURRENT_STYLE_SHEET = LIGHT_STYLE_SHEET


class GlobalError(Exception):  # создаем новую, главную класс-ошибку для проекта
    pass


class AuthorizationsError(GlobalError):  # создаем класс-ошибку возникающую при авториции
    pass


class RegistrationError(GlobalError):  # создаем класс-ошибку возникающую при регистрации
    pass


class ChancheError(GlobalError):  # создаем класс-ошибку возникающую при изменении данных
    pass


class SendError(GlobalError):  # создаем ошибку возникающую при отправке сообщений
    pass


class Authorizations(QMainWindow):  # создаем класс для отображения окна авторизации
    def __init__(self):
        super().__init__()  # инициализируем и задаем таблицу стилей и друшие параметры
        uic.loadUi('../QTDesinger/authorizations.ui', self)
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.pixmap = QPixmap(f'../Структурные фото/PyChat150.png')
        self.label_3.setPixmap(self.pixmap)

        self.data_users_connect = sqlite3.connect('../Данные/users_data.db')
        self.data_users_cursor = self.data_users_connect.cursor()  # подключаем кнопки
        # к функциям и базы данных

        self.pushButton.clicked.connect(self.authorizations)
        self.pushButton_2.clicked.connect(self.registration)

    def registration(self):
        self.registration = Registration(self, self.data_users_cursor, self.data_users_connect)
        self.registration.show()  # реализуем функцию регистрации

    def authorizations(self):
        try:  # реализуем функцию авторизации и проверки вводимых данных
            login = list(self.data_users_cursor.execute(f"""SELECT user_login
             from user_data_main where user_login = \'{self.lineEdit.text()}\'
             AND user_password = \'{self.lineEdit_2.text()}\'""").fetchall())
            if login != []:
                login = login[0][0]
            else:
                raise AuthorizationsError()
            if login == []:
                raise AuthorizationsError()
            self.run_programm = Dialogs(login, self)
            self.run_programm.show()
            self.close()
        except AuthorizationsError:
            self.statusBar.showMessage('                 Неверный логин или пароль', 3000)


class Registration(QMainWindow):  # создаем класс для отображения окна регистрации
    def __init__(self, out_reg, cursor, connect):
        super().__init__()
        uic.loadUi('../QTDesinger/registration_2.ui', self)
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)  # инициализируем и задем
        # таблицы стилей и другие параметры, подключаем кнопки к их функциям

        self.pushButton_2.clicked.connect(self.run)
        self.out_reg = out_reg
        self.cursor = cursor
        self.connect = connect

    def run(self):  # реализуем функцию регистрации
        self.alphavit = 'qwertyuiopasdfghjklzxcvbnm_'
        try:
            self.check()
            os.mkdir(f"../Пользователи/{self.lineEdit.text()}")
            self.cursor.execute(f"""INSERT INTO
             user_data_main(user_login, user_password,
              user_icon, user_name, user_folder, who_to_chat_with, discussions)
               VALUES(\'{self.lineEdit.text()}\', \'{self.lineEdit_2.text()}\',
                \'../Структурные фото/Икона.png\',
                 \'{self.lineEdit.text()}\', \'../Пользователи/{self.lineEdit.text()}\',
                  \'\', \'\')""")
            self.cursor.execute(f"""INSERT INTO list_dialogs(user_login,
             where_dialog, who_to_chat_with)
            VALUES(\'{self.lineEdit.text()}\', \'\', \'\')""")
            self.connect.commit()
            self.out_reg.lineEdit.setText(self.lineEdit.text())
            self.out_reg.lineEdit_2.setText(self.lineEdit_2.text())
            self.close()
        except RegistrationError as e:
            self.statusbar.showMessage(str(e), 4000)

    def check(self):  # реализуем функцию проверки вводимых данных
        if True in [True if i2 not in self.alphavit and i2.isdigit() is False else False for i2
                    in self.lineEdit.text()] or self.lineEdit.text().isdigit():
            raise RegistrationError('             Логин может содержать только'
                                    ' латинские буквы, цифры и \"_\"!')
        # при неверных данных выводим ошибку
        if len(self.lineEdit.text()) > 30:
            raise RegistrationError('             Слишком длинный логин! Максимум 30 символов.')
        if len(self.lineEdit.text()) < 5:
            raise RegistrationError('                  Слишком короткий логин! Минимум 5 символов.')
        if self.cursor.execute(f"""SELECT user_name from 
        user_data_main where user_login = \'{self.lineEdit.text()}\'""").fetchall() != []:
            raise RegistrationError('                                Логин должен быть уникальным!')
        if self.lineEdit_2.text() != self.lineEdit_3.text():
            raise RegistrationError('                                          Пароли различаются!')
        if len(self.lineEdit_2.text()) < 8:
            raise RegistrationError('                 Слишком короткий пароль! Минимум 8 символов.')
        if (self.lineEdit_2.text().islower() or self.lineEdit_2.text().isupper()) or (
                True not in [True if i.isalpha() else False for i in self.lineEdit_2.text()]) \
                or True not in [True if i.isdigit() else False for i in self.lineEdit_2.text()]:
            raise RegistrationError('   Пароль не может состоять только'
                                    ' из букв или цифр одного регистра!')


class Dialogs(QMainWindow):  # реализуем класс для отображения
    def __init__(self, login, out_self):
        super().__init__()
        uic.loadUi('../QTDesinger/dialogs.ui', self)
        self.go_programm()
        self.login = login
        self.into = out_self
        self.update_window()  # инициализируем и задаем таблицу стилей и другие параметры

    def update_window(self):  # реализуем функцию обновления виджета
        # для обновления нужно очистить виджет и с помощью цикла задать новые значения
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.pushButton_3.setIcon(QIcon(list(self.into.data_users_cursor.execute(f"""SELECT user_icon
                 from user_data_main where user_login = \'{str(self.login)}\'""").fetchall())[0][0]))
        self.into.data_users_cursor.execute(f"""UPDATE user_data_main SET was_online =
                \'{':'.join(''.join(str(datetime.datetime.now()).split('.')[0]).split(':')[:-1])}\'
                WHERE user_login = \'{self.login}\'""")
        self.into.data_users_connect.commit()
        if self.into.data_users_cursor.execute(f"""
                                         SELECT who_to_chat_with from list_dialogs where user_login
                                          = \'{self.login}\'""").fetchall()[0][0] != ('',):
            self.listWidget.clear()
            self.push_button_list_open = [
                QPushButton(i.split('-')[1])
                if i.split('-')[0] == self.login else QPushButton(i.split('-')[0]) for i in
                self.into.data_users_cursor.execute(f"""
                                         SELECT who_to_chat_with from list_dialogs where user_login
                                          = \'{self.login}\'""").fetchall()[0][0].split('%$%')[1:]]
            for i in self.push_button_list_open:
                list_widget_item = QListWidgetItem()
                list_widget_item.setSizeHint(QSize(25, 50))
                list_widget_item.setIcon(QIcon(self.into.data_users_cursor.execute(f"""
                        SELECT user_icon from user_data_main
                         where user_login = \'{i.text()}\'""").fetchall()[0][0]))
                self.listWidget.addItem(list_widget_item)
                self.listWidget.setItemWidget(list_widget_item, i)
                i.setText(self.into.data_users_cursor.execute(f"""SELECT
                         user_name from user_data_main
                                        where user_login
                                         = \'{i.text()}\'""").fetchall()[0][0] + f" ({i.text()})")
                i.clicked.connect(self.open_dialog)
        if self.into.data_users_cursor.execute(f"""
        SELECT discussions from user_data_main where user_login 
        = \'{self.login}\'""").fetchall()[0][0] != ('',):
            self.push_button_list_global_open = \
                [QPushButton(i) for i in self.into.data_users_cursor.execute(f"""
            SELECT discussions from user_data_main
             WHERE user_login = \'{self.login}\'""").fetchall()[0][0].split('%$%')[1:]]
            for i in self.push_button_list_global_open:
                list_widget_item = QListWidgetItem()
                list_widget_item.setSizeHint(QSize(25, 50))
                list_widget_item.setIcon(QIcon(self.into.data_users_cursor.execute(f"""
                                        SELECT discussions_icon from discussions
                                         where identification_name
                                          = \'{i.text()}\'""").fetchall()[0][0]))
                i.setText(self.into.data_users_cursor.execute(f"""SELECT discussion_name
                from discussions WHERE identification_name =
                 \'{i.text()}\'""").fetchall()[0][0] + f' ({i.text()})')
                self.listWidget.addItem(list_widget_item)
                self.listWidget.setItemWidget(list_widget_item, i)
                i.clicked.connect(self.discussion)
                self.dis_name = i.text()

    def discussion(self):  # реализуем функцию открытия беседы
        sender = self.sender()
        self.open_discussion = OpenGlobalDialogs(self.login, self, sender.text().split()[-1][1:-1])
        self.open_discussion.show()

    def open_dialog(self):  # реализуем фнукцию отерытия личного диалога
        sender = self.sender()
        self.open_private_dialog = \
            OpenPrivateDialog(self.login, sender.text().split()[-1][1:-1], self.into, self)
        self.open_private_dialog.show()

    def go_programm(self):  # подключаем все кнопки к их функциям
        self.pushButton.clicked.connect(self.new_private_messenge)
        self.pushButton_2.clicked.connect(self.new_global_messenge)
        self.pushButton_3.clicked.connect(self.change_data)
        self.pushButton_5.clicked.connect(self.find)
        self.pushButton_6.clicked.connect(self.update_window)
        self.pushButton_4.clicked.connect(self.style_sheet)
        self.pushButton_7.clicked.connect(self.find_profile)

    def find_profile(self):  # реализуем функцию открытия поиска профилей
        self.find_profile = FindProfile(self.login, self.into)
        self.find_profile.show()

    def style_sheet(self):  # реализуем функцию функцию смены стилей
        global LIGHT_STYLE_SHEET
        global DARK_STYLE_SHEET
        global CURRENT_STYLE_SHEET
        if CURRENT_STYLE_SHEET == LIGHT_STYLE_SHEET:
            CURRENT_STYLE_SHEET = DARK_STYLE_SHEET
        else:
            CURRENT_STYLE_SHEET = LIGHT_STYLE_SHEET
        self.update_window()

    def find(self):  # реализуем фунцию поиска чатов в списке
        if self.into.data_users_cursor.execute(f"""
                                         SELECT who_to_chat_with from list_dialogs where user_login
                                          = \'{self.login}\'""").fetchall()[0][0] != ('',):
            self.listWidget.clear()
            self.push_button_list_open = [
                QPushButton(i.split('-')[1])
                if i.split('-')[0] == self.login else QPushButton(i.split('-')[0]) for i in
                self.into.data_users_cursor.execute(f"""
                                         SELECT who_to_chat_with from list_dialogs where user_login
                                          = \'{self.login}\'""").fetchall()[0][0].split('%$%')[1:]]
            for i in self.push_button_list_open:
                list_widget_item = QListWidgetItem()
                list_widget_item.setSizeHint(QSize(25, 50))
                list_widget_item.setIcon(QIcon(self.into.data_users_cursor.execute(f"""
                            SELECT user_icon from user_data_main
                             where user_login = \'{i.text()}\'""").fetchall()[0][0]))

                i.setText(self.into.data_users_cursor.execute(f"""SELECT
                             user_name from user_data_main
                                            where user_login
                                        = \'{i.text()}\'""").fetchall()[0][0] + f" ({i.text()})")
                if self.lineEdit.text().lower() in i.text().lower():
                    self.listWidget.addItem(list_widget_item)
                    self.listWidget.setItemWidget(list_widget_item, i)
                    i.clicked.connect(self.open_dialog)
        if self.into.data_users_cursor.execute(f"""
        SELECT discussions from user_data_main where user_login 
        = \'{self.login}\'""").fetchall()[0][0] != ('',):
            self.push_button_list_global_open = \
                [QPushButton(i) for i in self.into.data_users_cursor.execute(f"""
            SELECT discussions from user_data_main
             WHERE user_login = \'{self.login}\'""").fetchall()[0][0].split('%$%')[1:]]
            for i in self.push_button_list_global_open:
                list_widget_item = QListWidgetItem()
                list_widget_item.setSizeHint(QSize(25, 50))
                list_widget_item.setIcon(QIcon(self.into.data_users_cursor.execute(f"""
                                        SELECT discussions_icon from discussions
                                         where identification_name
                                          = \'{i.text()}\'""").fetchall()[0][0]))
                i.setText(self.into.data_users_cursor.execute(f"""SELECT discussion_name
                                from discussions WHERE identification_name =
                                 \'{i.text()}\'""").fetchall()[0][0] + f' ({i.text()})')
                if self.lineEdit.text().lower() in i.text().lower():
                    self.listWidget.addItem(list_widget_item)
                    self.listWidget.setItemWidget(list_widget_item, i)
                    i.clicked.connect(self.discussion)
                    self.dis_name = i.text()

    def new_private_messenge(self):  # реализуем функцию открытия окна создания переписки
        self.new_private = NewPrivateMessenge(self.into, self.login, self)
        self.new_private.show()

    def new_global_messenge(self):  # реализуем функцию открытия окна создания переписки
        self.new_global = NewGlobalMessenge(self.login, self)
        self.new_global.show()

    def change_data(self):  # реализуем функцию открытия окна изменения данных
        self.change_data = ChangeData(self.into, self.login, self)
        self.change_data.show()


class FindProfile(QMainWindow):  # создаем класс для показа окна поиска пользователей
    def __init__(self, login, into):
        super().__init__()
        uic.loadUi('../QTDesinger/find_profile.ui', self)
        self.my_login = login
        self.into = into
        self.pushButton.clicked.connect(self.find)
        self.update_widget()  # инициализируем и задаем таблицу стилей и другие параметры

    def find(self):
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.listWidget.clear()  # реализуем фунцию поиска пользователей в списке
        self.list_users = [QPushButton(i[0]) for i in self.into.data_users_cursor.execute(f"""SELECT
                 user_login from user_data_main""").fetchall()]
        for i in self.list_users:
            if i.text() != self.my_login:
                listWidgetItem = QListWidgetItem()
                listWidgetItem.setIcon(QIcon(self.into.data_users_cursor.execute(f"""SELECT
                                         user_icon from user_data_main where user_login
                                         = \'{i.text()}\'""").fetchall()[0][0]))
                i.setText(self.into.data_users_cursor.execute(f"""SELECT user_name
                                        from user_data_main WHERE user_login =
                                         \'{i.text()}\'""").fetchall()[0][0] + f' ({i.text()})')
                listWidgetItem.setSizeHint(QSize(25, 35))
                if self.lineEdit.text().lower() in i.text().lower():
                    i.clicked.connect(self.open_profile)
                    self.listWidget.addItem(listWidgetItem)
                    self.listWidget.setItemWidget(listWidgetItem, i)

    def update_widget(self):  # реализуем функцию обновления виджета
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.listWidget.clear()
        self.list_users = [QPushButton(i[0]) for i in self.into.data_users_cursor.execute(f"""SELECT
         user_login from user_data_main""").fetchall()]
        for i in self.list_users:
            if i.text() != self.my_login:
                listWidgetItem = QListWidgetItem()
                listWidgetItem.setIcon(QIcon(self.into.data_users_cursor.execute(f"""SELECT
                                 user_icon from user_data_main where user_login
                                 = \'{i.text()}\'""").fetchall()[0][0]))
                i.setText(self.into.data_users_cursor.execute(f"""SELECT user_name
                                from user_data_main WHERE user_login =
                                 \'{i.text()}\'""").fetchall()[0][0] + f' ({i.text()})')
                listWidgetItem.setSizeHint(QSize(25, 35))
                i.clicked.connect(self.open_profile)
                self.listWidget.addItem(listWidgetItem)
                self.listWidget.setItemWidget(listWidgetItem, i)

    def open_profile(self):  # реализуем функцию открытия окна с информацией о пользователе
        sender = self.sender()
        self.viewing_profile = ViewingProfile(sender.text().split()[-1][1:-1], self.into)
        self.viewing_profile.show()


class ViewingProfile(QMainWindow):  # создаем класс для отображения информации пользователя
    def __init__(self, login, into):
        super().__init__()  # инициализируем и задаем таблицу стилей и другие параметры
        uic.loadUi('../QTDesinger/viewing.ui', self)
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.pushButton.setIcon(QIcon(into.data_users_cursor.execute(f"""SELECT user_icon
        from user_data_main WHERE user_login = \'{login}\'""").fetchall()[0][0]))
        self.pushButton_2.setText(into.data_users_cursor.execute(f"""SELECT user_name
        from user_data_main WHERE user_login = \'{login}\'""").fetchall()[0][0])
        self.pushButton_3.setText(login)


class NewPrivateMessenge(QWidget):  # создаем класс для
    # отображения окна создания нового приватного диалога
    def __init__(self, into, login, into_dialogs):
        super().__init__()
        uic.loadUi('../QTDesinger/new_private_messenge.ui', self)
        self.into = into  # инициализируем и задаем таблицу стилей и другие параметры
        self.login = login
        self.into_dialogs = into_dialogs
        global CURRENT_STYLE_SHEET  # подключаем все кнопки к их функциям
        self.setStyleSheet(CURRENT_STYLE_SHEET)

        self.pushButton.clicked.connect(self.find)

        self.push_button_list = [QPushButton(f'{i[1]} ({i[0]})') for
                                 i in self.into.data_users_cursor.execute(f"""
                                 SELECT user_login, user_name from
         user_data_main where user_login != \'{self.login}\'""").fetchall()]
        for i in self.push_button_list:
            i.clicked.connect(self.run_new_dialog)
        self.who_to_chat_with = self.into.data_users_cursor.execute(f"""
            SELECT who_to_chat_with from user_data_main
             where user_login = \'{self.login}\'""").fetchall()[0][0] \
            if self.into.data_users_cursor.execute(f"""SELECT who_to_chat_with from user_data_main
             where user_login =
              \'{self.login}\'
             """).fetchall() != [(None,)] and self.into.data_users_cursor.execute(f"""SELECT
                who_to_chat_with from user_data_main
             where user_login = \'{self.login}\'""").fetchall() != [('',)] else '1'
        for i in self.push_button_list[:]:
            if i.text().split()[-1][1:-1] not in self.who_to_chat_with:
                listWidgetItem = QListWidgetItem()
                listWidgetItem.setIcon(QIcon(self.into.data_users_cursor.execute(f"""SELECT
                 user_icon from user_data_main where user_login
                 = \'{i.text().split()[-1][1:-1]}\'""").fetchall()[0][0]))
                listWidgetItem.setSizeHint(QSize(25, 35))
                self.listWidget.addItem(listWidgetItem)
                i2 = i
                self.listWidget.setItemWidget(listWidgetItem, i2)

    def find(self):  # реализуем функцию поиска
        self.listWidget.clear()
        self.push_button_list = [QPushButton(f'{i[1]} ({i[0]})') for
                                 i in self.into.data_users_cursor.execute(f"""
                                 SELECT user_login, user_name from
         user_data_main where user_login != \'{self.login}\'""").fetchall()]
        for i in self.push_button_list:
            i.clicked.connect(self.run_new_dialog)
        for i in self.push_button_list:
            if i.text().split()[-1][1:-1] not in self.who_to_chat_with \
                    and self.lineEdit.text().lower() in i.text().lower():
                list_widget_item = QListWidgetItem()
                list_widget_item.setIcon(QIcon(self.into.data_users_cursor.execute(f"""SELECT
                                 user_icon from user_data_main where user_login
                                 = \'{i.text().split()[-1][1:-1]}\'""").fetchall()[0][0]))
                list_widget_item.setSizeHint(QSize(25, 35))
                self.listWidget.addItem(list_widget_item)
                self.listWidget.setItemWidget(list_widget_item, i)

    def run_new_dialog(self):  # реализуем функцию создания нового диалога
        sender = self.sender()
        add_user = self.into.data_users_cursor.execute(f"""SELECT who_to_chat_with from
        user_data_main WHERE user_login = \'{self.login}\'""").fetchall()[0][0]
        self.into.data_users_cursor.execute(f"""UPDATE user_data_main SET who_to_chat_with =
        \'{add_user + '%$%' + sender.text().split()[-1][1:-1]}\'
         WHERE user_login = \'{self.login}\'""")
        self.into.data_users_connect.commit()
        add_user = self.into.data_users_cursor.execute(f"""SELECT who_to_chat_with from
                user_data_main WHERE user_login = 
                \'{sender.text().split()[-1][1:-1]}\'""").fetchall()[0][0]
        self.into.data_users_cursor.execute(f"""UPDATE user_data_main SET who_to_chat_with =
                \'{add_user + '%$%' + self.login}\' WHERE user_login =
                 \'{sender.text().split()[-1][1:-1]}\'""")
        self.into.data_users_connect.commit()
        add_dialogs = self.into.data_users_cursor.execute(f"""SELECT who_to_chat_with
        from list_dialogs WHERE user_login = \'{self.login}\'""").fetchall()[0][0]
        self.into.data_users_cursor.execute(f"""UPDATE list_dialogs SET who_to_chat_with =
                \'{add_dialogs + '%$%' + self.login + '-' + sender.text().split()[-1][1:-1]}\'
                 WHERE user_login = \'{self.login}\'""")
        self.into.data_users_connect.commit()
        add_dialogs = self.into.data_users_cursor.execute(f"""SELECT who_to_chat_with
                    from list_dialogs WHERE user_login = \'{sender.text().split()[-1][1:-1]}\'
            """).fetchall()[0][0]
        self.into.data_users_cursor.execute(f"""UPDATE list_dialogs SET who_to_chat_with =
                        \'{add_dialogs + '%$%' + self.login + '-'
                           + sender.text().split()[-1][1:-1]}\'
                         WHERE user_login = \'{sender.text().split()[-1][1:-1]}\'""")
        add_where = self.into.data_users_cursor.execute(f"""SELECT where_dialog from list_dialogs
        WHERE user_login = \'{self.login}\'""").fetchall()[0][0]
        self.into.data_users_cursor.execute(f"""UPDATE list_dialogs SET where_dialog =
        \'{add_where + '%$%' + f'../Личные диалоги/{self.login}-{sender.text().split()[-1][1:-1]}'
                               f'.txt'}\' WHERE user_login =
        \'{self.login}\'""")
        add_where = self.into.data_users_cursor.execute(f"""SELECT where_dialog from list_dialogs
                WHERE user_login = \'{sender.text().split()[-1][1:-1]}\'""").fetchall()[0][0]
        self.into.data_users_cursor.execute(f"""UPDATE list_dialogs SET where_dialog =
                \'{add_where + '%$%' + f'../Личные диалоги/{self.login}-'
                                       f'{sender.text().split()[-1][1:-1]}.txt'}\'
                                        WHERE user_login = \'{sender.text().split()[-1][1:-1]}\'""")
        self.into.data_users_connect.commit()
        open(f'../Личные диалоги/{self.login}-{sender.text().split()[-1][1:-1]}.txt', mode='w',
             encoding='utf-8')
        self.into_dialogs.open_private_dialog = OpenPrivateDialog(self.login,
                                                                  sender.text().split()[-1][1:-1],
                                                                  self.into, self.into_dialogs)
        self.into_dialogs.open_private_dialog.show()
        self.into_dialogs.update_window()
        self.close()


class OpenPrivateDialog(QMainWindow):  # создаем класс открытия личного диалога
    def __init__(self, my_login, interlocutor_login, into, into_dialogs):
        super().__init__()
        uic.loadUi('../QTDesinger/private_dialog.ui', self)
        self.my_login = my_login
        self.interlocutor_login = interlocutor_login
        self.into = into
        self.into_dialogs = into_dialogs

        self.pushButton_3.setIcon(QIcon(list(self.into.data_users_cursor.execute(f"""SELECT
        user_icon from user_data_main where user_login = \'{str(self.interlocutor_login)}\'
        """).fetchall())[0][0]))
        self.pushButton_3.setText(list(self.into.data_users_cursor.execute(f"""SELECT user_name
        from user_data_main where user_login = \'{str(self.interlocutor_login)}\'
        """).fetchall())[0][0])
        self.label_2.setText(list(self.into.data_users_cursor.execute(f"""SELECT was_online
        from user_data_main where user_login = \'{str(self.interlocutor_login)}\'
        """).fetchall())[0][0])
        self.where_file = \
            [i if self.interlocutor_login in i else '' for i in
             self.into.data_users_cursor.execute(f"""SELECT where_dialog from list_dialogs
        WHERE user_login = \'{self.my_login}\'""").fetchall()[0][0].split('%$%')]
        self.where_file.sort()
        self.where_file = self.where_file[-1]
        self.pushButton_3.clicked.connect(self.open_profile)
        self.pushButton_4.clicked.connect(self.setting_open)
        self.pushButton_5.clicked.connect(self.update_qwidget)
        self.run_correspond()

    def setting_open(self):  # реализуем функцию открытия окна настроек
        self.setting = SettingPrivate(self.my_login, self.interlocutor_login,
                                      self.into_dialogs, self, self.where_file)
        self.setting.show()

    def open_profile(self):  # реализуем функцию открытия окна данных пользователя
        self.into_dialogs.check = CheckProfile(self.my_login, self.interlocutor_login,
                                               self.into_dialogs)
        self.into_dialogs.check.show()
        self.close()

    def run_correspond(self):  # подключаем кнопки к их функциям
        self.update_qwidget()
        self.pushButton.clicked.connect(self.send)
        self.pushButton_2.clicked.connect(self.add_file)

    def send(self):  # реализуем функцию поиска
        try:
            if '%$%' in \
                    self.plainTextEdit.toPlainText() \
                    or '%end%' in self.plainTextEdit.toPlainText():
                raise SendError('Не пишите в сообщении сочетаниz %$% и %end%')
            if self.plainTextEdit.toPlainText() != 'Ваше сообщение...' \
                    and set(self.plainTextEdit.toPlainText()) != set('\n') \
                    and set(self.plainTextEdit.toPlainText()) != set(' ') \
                    and set(self.plainTextEdit.toPlainText()) != set(''):
                reader = open(self.where_file, mode='r', encoding='utf-8').read()
                open(self.where_file, mode='w', encoding='utf-8').write(
                    reader + self.my_login + '%$%' + self.plainTextEdit.toPlainText() + '%end%')
                text_browser = QTextBrowser(self)
                text_browser.setPlainText(self.plainTextEdit.toPlainText())
                list_widget_item = QListWidgetItem()
                list_widget_item.setIcon(QIcon(self.into.data_users_cursor.execute(f"""SELECT
                                user_icon from user_data_main WHERE user_login
                                 = \'{self.my_login}\'""").fetchall()[0][0]))
                list_widget_item.setSizeHint(QSize(
                    10, 30 + (30 * (len(self.plainTextEdit.toPlainText()) // 65))))
                self.listWidget.addItem(list_widget_item)
                self.listWidget.setItemWidget(list_widget_item, text_browser)
                self.plainTextEdit.setPlainText('')
        except SendError as e:
            self.statusBar.showMessage(str(e), 6000)

    def add_file(self):  # реализуем функцию отправки файла
        try:
            self.fname = QFileDialog.getOpenFileName(self, 'Выбрать'
                                                           ' файл', '', )[0]
            shutil.copyfile(self.fname, f'../Пользователи/{self.my_login}'
                                        f'/{self.fname.split("/")[-1]}')
            reader = open(self.where_file, mode='r', encoding='utf-8').read()
            open(self.where_file, mode='w', encoding='utf-8').write(
                reader + self.my_login
                + '%$%' + f'add%*%file../Пользователи/{self.my_login}/{self.fname.split("/")[-1]}'
                + '%end%')
            qpushbutton_file = QPushButton(f'../Пользователи/'
                                           f'{self.my_login}/{self.fname.split("/")[-1]}')
            qpushbutton_file.clicked.connect(self.open_file)
            qpushbutton_file.setIcon(QIcon('../Структурные фото/прикрепить.png'))
            list_widget_item = QListWidgetItem()
            list_widget_item.setIcon(QIcon(self.into.data_users_cursor.execute(f"""SELECT
                                            user_icon from user_data_main WHERE user_login
                                             = \'{self.my_login}\'""").fetchall()[0][0]))
            list_widget_item.setSizeHint(QSize(
                10, 30 + (len(f'../Пользователи/'
                              f'{self.my_login}/{self.fname.split("/")[-1]}') // 65)))
            self.listWidget.addItem(list_widget_item)
            self.listWidget.setItemWidget(list_widget_item, qpushbutton_file)
        except AttributeError:
            pass
        except FileNotFoundError:
            pass

    def update_qwidget(self):  # реализуем функцию обновления окна
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.listWidget.clear()
        self.reader = open(self.where_file, mode='r', encoding='utf-8').read().split('%end%')
        if len(self.reader) > 40:
            self.statusBar.showMessage('Чтобы окно загружалось быстрее,'
                                       ' очистите историю переписки в настройках!', 15000)
        icon = self.into.data_users_cursor.execute(f'SELECT who_to_chat_with from'
                                                   f' list_dialogs'
                                                   f' WHERE user_login ='
                                                   f' \'{self.my_login}\'').fetchall()[0][0].split('%$%')
        for i in self.reader:
            one_messenge = i.split('%$%')
            if one_messenge != [''] and one_messenge[1][0:10] != 'add%*%file':
                text_browser = QTextBrowser(self)
                text_browser.setPlainText(one_messenge[1])
                list_widget_item = QListWidgetItem()
                list_widget_item.setIcon(QIcon(self.into.data_users_cursor.execute(f"""SELECT
                user_icon from user_data_main WHERE user_login
                 = \'{one_messenge[0]}\'""").fetchall()[0][0]))
                list_widget_item.setSizeHint(QSize(
                    10, 30 + (35 * (len(one_messenge[1]) // 65)) + (
                            20 * one_messenge[1].count('\n'))))
                self.listWidget.addItem(list_widget_item)
                self.listWidget.setItemWidget(list_widget_item, text_browser)
            elif one_messenge != [''] and one_messenge[1][0:10] == 'add%*%file':
                qpushbutton_file = QPushButton(one_messenge[1][10:])
                qpushbutton_file.clicked.connect(self.open_file)
                qpushbutton_file.setIcon(QIcon('../Структурные фото/прикрепить.png'))
                list_widget_item = QListWidgetItem()
                list_widget_item.setIcon(QIcon(self.into.data_users_cursor.execute(f"""SELECT
                                user_icon from user_data_main WHERE user_login
                                 = \'{one_messenge[1][10:].split("/")[-2]}\'""").fetchall()[0][0]))
                list_widget_item.setSizeHint(QSize(
                    10, 30 + (len(one_messenge[1][10:]) // 65)))
                self.listWidget.addItem(list_widget_item)
                self.listWidget.setItemWidget(list_widget_item, qpushbutton_file)

    def open_file(self):  # реализуем функцию открытия файла и просмотра фотографий
        development = ['png', 'jpg', 'bmp', 'jpeg']
        sender = self.sender()
        if sender.text().split('.')[-1] in development:
            self.open_photo = PhotoLooking(sender.text(),
                                           sender.text().split("/")[-1].split('.')[0],
                                           sender.text().split("/")[-1].split('.')[-1])
            self.open_photo.show()
        elif sender.text().split('.')[-1] == 'mp3':
            self.open_audi = OpenAudio(self, sender.text())
            self.open_audi.show()
        else:
            fname = QFileDialog.getExistingDirectory(self, "Скачать файл", ".")
            if fname != '':
                shutil.copyfile(sender.text(), f'{fname}/{sender.text().split("/")[-1]}')


class OpenAudio(QMainWindow):
    def __init__(self, into, file):
        super(OpenAudio, self).__init__()
        uic.loadUi('../QTDesinger/audio.ui', self)
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.into = into
        self.file = file
        self.initUI()

    def initUI(self):
        media = QtCore.QUrl.fromLocalFile(self.file)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        self.pushButton_3.clicked.connect(self.player.play)
        self.pushButton_2.clicked.connect(self.player.pause)
        self.pushButton.clicked.connect(self.player.stop)
        self.pushButton_4.clicked.connect(self.save_audio)

    def save_audio(self):
        fname = QFileDialog.getExistingDirectory(self, "Скачать файл", ".")
        if fname != '':
            shutil.copyfile(self.file, f'{fname}/{self.file.split("/")[-1]}')
            self.close()


class NewGlobalMessenge(QWidget):  # создаем класс для отображения окна создания беседы
    def __init__(self, my_login, into_dialog):
        super().__init__()
        uic.loadUi('../QTDesinger/new_global_messenge.ui', self)
        self.pushButton.clicked.connect(self.find)
        self.login = my_login  # инициализируем и задем таблицу стилей и другие параметры
        self.into_dialogs = into_dialog
        self.clicked_button = []
        self.pushButton_2.clicked.connect(self.input_parametrs)
        self.load_users()
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)

    def load_users(self):  # реализуем функцию загрузки списка пользователей
        self.users_list = \
            [QCheckBox(i.split("-")[1], self)
             if i.split('-')[0] == self.login else QCheckBox(i.split("-")[0], self)
             for i in self.into_dialogs.into.data_users_cursor.execute(f"""SELECT who_to_chat_with
        from list_dialogs WHERE user_login = \'{self.login}\'""").fetchall()[0][0].split('%$%')[1:]]
        for i in self.users_list:
            i.stateChanged.connect(self.check_status)
            if i.text() in self.clicked_button:
                i.setChecked(True)
            listWidgetItem = QListWidgetItem()
            listWidgetItem.setIcon(QIcon(f'../Пользователи/{i.text()}/{i.text()}.png'))
            i.setText(self.into_dialogs.into.data_users_cursor.execute(f"""SELECT
             user_name from user_data_main WHERE user_login = \'{i.text()}\'""").fetchall()[0][0]
                      + f' ({i.text()})')
            listWidgetItem.setSizeHint(QSize(10, 40))
            self.listWidget.addItem(listWidgetItem)
            self.listWidget.setItemWidget(listWidgetItem, i)

    def check_status(self):
        sender = self.sender()
        if sender.isChecked() and sender.text().split()[-1][1:-1] not in self.clicked_button:
            self.clicked_button.append(sender.text().split()[-1][1:-1])
        else:
            del self.clicked_button[self.clicked_button.index(sender.text().split()[-1][1:-1])]

    def find(self):  # реализуем функцию поиска
        self.listWidget.clear()
        self.users_list = \
            [QCheckBox(i.split("-")[1], self)
             if i.split('-')[0] == self.login else QCheckBox(i.split("-")[0], self)
             for i in self.into_dialogs.into.data_users_cursor.execute(f"""SELECT who_to_chat_with
                from list_dialogs WHERE user_login =
                 \'{self.login}\'""").fetchall()[0][0].split('%$%')[1:]]

        for i in self.users_list:
            listWidgetItem = QListWidgetItem()
            listWidgetItem.setIcon(QIcon(f'../Пользователи/{i.text()}/{i.text()}.png'))
            if i.text() in self.clicked_button:
                i.setChecked(True)
            i.setText(self.into_dialogs.into.data_users_cursor.execute(f"""SELECT
                     user_name from user_data_main WHERE user_login =
                      \'{i.text()}\'""").fetchall()[0][0]
                      + f' ({i.text()})')
            i.stateChanged.connect(self.check_status)
            if self.lineEdit.text().lower() in i.text().lower():
                listWidgetItem.setSizeHint(QSize(10, 40))
                self.listWidget.addItem(listWidgetItem)
                self.listWidget.setItemWidget(listWidgetItem, i)

    def input_parametrs(self):  # реализуем функцию открытия окна приняятия следующих параметров
        self.input_parametrs_open = \
            InputParametrs(self.login, self.into_dialogs, self.clicked_button)
        self.input_parametrs_open.show()
        self.close()


class InputParametrs(QMainWindow):  # создаем класс
    # для отображения окна принятия названия и изображения беседы
    def __init__(self, my_login, into_dialog, list_users):
        super().__init__()
        uic.loadUi('../QTDesinger/parametrs_global_dialog.ui', self)
        self.icon = '../Структурные фото/Икона.png'
        self.pushButton.clicked.connect(self.new_icon)
        self.lineEdit.textChanged.connect(self.new_name)
        self.pushButton_2.clicked.connect(self.create_global_messenge)
        self.my_login = my_login
        self.into_dialogs = into_dialog  # инициализируем и здааем таблицу
        # стилей и других параметров
        self.list_user = list_users
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        h = 0
        self.identification_name = ''.join(self.lineEdit.text().split())
        while self.into_dialogs.into.data_users_cursor.execute(f"""SELECT * from
                    discussions WHERE identification_name = \'{self.identification_name}\'""").fetchall() \
                != []:
            if len(self.identification_name.split('-')) == 1:
                self.identification_name = self.identification_name + '-0'
            else:
                self.identification_name = self.identification_name.split('-')[0] + '-' + str(h)
            h += 1

    def create_global_messenge(self):
        try:  # реализуем функцию создания новой беседы
            self.check_name()
            h = 0
            self.identification_name = ''.join(self.lineEdit.text().split())
            while self.into_dialogs.into.data_users_cursor.execute(f"""SELECT * from
            discussions WHERE identification_name = \'{self.identification_name}\'""").fetchall() \
                    != []:
                if len(self.identification_name.split('-')) == 1:
                    self.identification_name = self.identification_name + '-0'
                else:
                    self.identification_name = self.identification_name.split('-')[0] + '-' + str(h)
                h += 1
            open(f'../Беседы/{self.identification_name}.txt', mode='w', encoding='utf-8')
            self.into_dialogs.into.data_users_cursor.execute(f"""INSERT INTO
                    discussions(discussion_name, users, where_discussion, discussions_icon,
                    admin, identification_name) VALUES(\'{self.lineEdit.text()}\',
                     \'{'%$%' + '%$%'.join(self.list_user)}%$%{self.my_login}\', 
                    \'{f'../Беседы/{self.identification_name}.txt'}\', \'{self.icon}\',
                     \'{self.my_login}\', \'{self.identification_name}\')""")
            add_diss = self.into_dialogs.into.data_users_cursor.execute(f"""SELECT
                            discussions from user_data_main WHERE user_login
                             = \'{self.my_login}\'""").fetchall()[0][0]
            self.into_dialogs.into.data_users_cursor.execute(f"""UPDATE user_data_main
            SET discussions = \'{add_diss + '%$%' + self.identification_name}\' WHERE user_login
             = \'{self.my_login}\'""")
            for i in self.list_user:
                add_diss = self.into_dialogs.into.data_users_cursor.execute(f"""SELECT
                discussions from user_data_main WHERE user_login
                 = \'{i}\'""").fetchall()[0][0]
                self.into_dialogs.into.data_users_cursor.execute(f"""UPDATE
                 user_data_main SET discussions = \'{add_diss + "%$%" + self.identification_name}\'
                  WHERE user_login = \'{i}\'""")
            self.into_dialogs.into.data_users_connect.commit()
            self.into_dialogs.open_dialogs = \
                OpenGlobalDialogs(self.my_login,
                                  self.into_dialogs, self.identification_name)
            self.into_dialogs.open_dialogs.show()
            self.into_dialogs.update_window()
            self.close()
        except ChancheError as e:
            self.statusbar.showMessage(str(e), 2000)

    def new_name(self):  # реализуем функцию изменения названия беседы
        self.icon = '../Структурные фото/Икона.png'
        self.pushButton.setIcon(QIcon(self.icon))
        try:
            self.check_name()
        except ChancheError as e:
            self.statusbar.showMessage(str(e), 2000)

    def new_icon(self):  # реализуем функцию изменеия фото беседы
        try:
            self.check_name()
            fname = QFileDialog.getOpenFileName(self, 'Выбрать'
                                                      ' картинку', '',
                                                'Картинка (*.jpg);;Картинка'
                                                ' (*.png);;Картинка (*.bmp);;Картинка (*.jpeg)')[0]
            im = Image.open(fname)
            im.save(f'../Пользователи/{self.my_login}/{self.my_login}-{self.identification_name}.png')
            self.icon = f'../Пользователи/{self.my_login}/{self.my_login}-{self.identification_name}.png'
            self.pushButton.setIcon(
                QIcon(f'../Пользователи/{self.my_login}/{self.my_login}-{self.identification_name}.png'))
        except AttributeError as e:
            pass
        except ChancheError as e:
            self.statusbar.showMessage(str(e), 2000)

    def check_name(self):  # реализуем функцию изменения имени беседы
        if len(self.lineEdit.text()) <= 2:
            raise ChancheError('      Сначала введите имя! Минимум 3 символа!')
        if len(self.lineEdit.text()) > 30:
            raise ChancheError('      Слишком длинное имя! Максимум 30 символа!')
        if False in [False if i.isdigit() is False and i.isalpha() is False else True for i in
                     ''.join(self.lineEdit.text().split())]:
            raise ChancheError('Имя может содержать только буквы, цыфры и пробел!')
        h = 0
        self.identification_name = ''.join(self.lineEdit.text().split())
        while self.into_dialogs.into.data_users_cursor.execute(f"""SELECT * from
                    discussions WHERE identification_name
                     = \'{self.identification_name}\'""").fetchall() \
                != []:
            if len(self.identification_name.split('-')) == 1:
                self.identification_name = self.identification_name + '-0'
            else:
                self.identification_name = self.identification_name.split('-')[0] + '-' + str(h)
            h += 1


class OpenGlobalDialogs(QMainWindow):  # создаем класс для отображения окна беседы
    def __init__(self, my_login, into_dialog, identification_name):
        super().__init__()
        uic.loadUi('../QTDesinger/global _dialog.ui', self)
        self.my_login = my_login
        self.into_dialog = into_dialog
        self.identification_name = identification_name
        self.name_dialog = self.into_dialog.into.data_users_cursor.execute(f"""SELECT
         discussion_name from discussions WHERE identification_name
         = \'{self.identification_name}\'""").fetchall()[0][0]
        self.pushButton.clicked.connect(self.send)
        self.pushButton_2.clicked.connect(self.add_file)
        self.users = self.into_dialog.into.data_users_cursor.execute(f"""SELECT users
        users from discussions WHERE identification_name
         = \'{self.identification_name}\'""").fetchall()[0][0].split('%$%')[1:]
        self.where_file = self.into_dialog.into.data_users_cursor.execute(f"""
        SELECT where_discussion from discussions WHERE
         identification_name = \'{self.identification_name}\'""").fetchall()[0][0]
        self.icon = self.into_dialog.into.data_users_cursor.execute(f"""
        SELECT discussions_icon from discussions where 
        identification_name = \'{self.identification_name}\'""").fetchall()[0][0]
        self.pushButton_3.setText(f'{str(len(self.users))} участников')
        self.pushButton_3.clicked.connect(self.list_participant)
        self.pushButton_4.clicked.connect(self.setting)
        self.pushButton_5.clicked.connect(self.update_widget)
        self.update_widget()

    def setting(self):  # реализуем функцию открытия окна настроек
        self.setting = SettingGlobal(self.my_login, self, self.identification_name)
        self.setting.show()

    def list_participant(self):  # реализуем функцию открытия окна со списком участников
        self.list_participant_open = ListParticipant(self.my_login, self, self.identification_name)
        self.list_participant_open.show()

    def send(self):  # реализуем функцию отправки сообщения
        try:
            if '%$%' in \
                    self.plainTextEdit.toPlainText() \
                    or '%end%' in self.plainTextEdit.toPlainText():
                raise SendError('Не пишите в сообщении сочетаниz %$% и %end%')
            if self.plainTextEdit.toPlainText() != 'Ваше сообщение...' \
                    and set(self.plainTextEdit.toPlainText()) != set('\n') \
                    and set(self.plainTextEdit.toPlainText()) != set(' ') \
                    and set(self.plainTextEdit.toPlainText()) != set(''):
                reader = open(self.where_file, mode='r', encoding='utf-8').read()
                open(self.where_file, mode='w', encoding='utf-8').write(
                    reader + self.my_login + '%$%' + self.plainTextEdit.toPlainText() + '%end%')
                text_browser = QTextBrowser(self)
                text_browser.setPlainText(self.plainTextEdit.toPlainText())
                list_widget_item = QListWidgetItem()
                list_widget_item.setIcon(QIcon(self.into_dialog.into.data_users_cursor.execute(f"""SELECT
                                user_icon from user_data_main WHERE user_login
                                 = \'{self.my_login}\'""").fetchall()[0][0]))
                list_widget_item.setSizeHint(QSize(
                    10, 30 + (30 * (len(self.plainTextEdit.toPlainText()) // 65))))
                self.listWidget.addItem(list_widget_item)
                self.listWidget.setItemWidget(list_widget_item, text_browser)
                self.plainTextEdit.setPlainText('')
        except SendError as e:
            self.statusbar.showMessage(str(e), 6000)

    def add_file(self):  # реализуем функцию отправки файла
        try:
            self.fname = QFileDialog.getOpenFileName(self, 'Выбрать'
                                                           ' файл', '', )[0]
            shutil.copyfile(self.fname, f'../Пользователи/{self.my_login}/{self.fname.split("/")[-1]}')
            reader = open(self.where_file, mode='r', encoding='utf-8').read()
            open(self.where_file, mode='w', encoding='utf-8').write(
                reader + self.my_login
                + '%$%' + f'add%*%file../Пользователи/{self.my_login}/{self.fname.split("/")[-1]}'
                + '%end%')
            qpushbutton_file = QPushButton(f'../Пользователи/'
                                           f'{self.my_login}/{self.fname.split("/")[-1]}')
            qpushbutton_file.clicked.connect(self.open_file)
            qpushbutton_file.setIcon(QIcon('../Структурные фото/прикрепить.png'))
            list_widget_item = QListWidgetItem()
            list_widget_item.setIcon(QIcon(self.into_dialog.into.data_users_cursor.execute(f"""SELECT
                                            user_icon from user_data_main WHERE user_login
                                             = \'{self.my_login}\'""").fetchall()[0][0]))
            list_widget_item.setSizeHint(QSize(
                10, 30 + (len(f'../Пользователи/{self.my_login}/{self.fname.split("/")[-1]}') // 65)))
            self.listWidget.addItem(list_widget_item)
            self.listWidget.setItemWidget(list_widget_item, qpushbutton_file)
        except AttributeError:
            pass
        except FileNotFoundError:
            pass

    def open_file(self):  # реализуем функцию открытия файла
        development = ['png', 'jpg', 'bmp', 'jpeg']
        sender = self.sender()
        if sender.text().split('.')[-1] in development:
            self.open_photo = PhotoLooking(sender.text(),
                                           sender.text().split("/")[-1].split('.')[0],
                                           sender.text().split("/")[-1].split('.')[-1])
            self.open_photo.show()
        else:
            fname = QFileDialog.getExistingDirectory(self, "Скачать файл", ".")
            if fname != '':
                shutil.copyfile(sender.text(), f'{fname}/{sender.text().split("/")[-1]}')

    def update_widget(self):  # реализуем функцию обновления виджета
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.listWidget.clear()
        self.users = self.into_dialog.into.data_users_cursor.execute(f"""SELECT users
                users from discussions WHERE identification_name
                 = \'{self.identification_name}\'""").fetchall()[0][0].split('%$%')[1:]
        self.pushButton_3.setText(f'{str(len(self.users))} участников')
        self.reader = open(self.where_file, mode='r', encoding='utf-8').read().split('%end%')
        for i in self.reader:
            one_messenge = i.split('%$%')
            if one_messenge != [''] and one_messenge[1][0:10] != 'add%*%file':
                text_browser = QTextBrowser(self)
                text_browser.setPlainText(one_messenge[1])
                list_widget_item = QListWidgetItem()
                list_widget_item.setIcon(QIcon(self.into_dialog.into.data_users_cursor.execute(f"""
        SELECT user_icon from user_data_main where 
        user_login = \'{one_messenge[0]}\'""").fetchall()[0][0]))
                list_widget_item.setSizeHint(QSize(
                    10, 30 + (35 * (len(one_messenge[1]) // 65)) + (
                            20 * one_messenge[1].count('\n'))))
                self.listWidget.addItem(list_widget_item)
                self.listWidget.setItemWidget(list_widget_item, text_browser)
            elif one_messenge != [''] and one_messenge[1][0:10] == 'add%*%file':
                qpushbutton_file = QPushButton(one_messenge[1][10:])
                qpushbutton_file.clicked.connect(self.open_file)
                qpushbutton_file.setIcon(QIcon('../Структурные фото/прикрепить.png'))
                list_widget_item = QListWidgetItem()
                list_widget_item.setIcon(QIcon(self.icon))
                list_widget_item.setSizeHint(QSize(
                    10, 30 + (len(one_messenge[1][10:]) // 65)))
                self.listWidget.addItem(list_widget_item)
                self.listWidget.setItemWidget(list_widget_item, qpushbutton_file)


class PhotoLooking(QMainWindow):  # создаем класс для отображения окна просмотра фотографий
    def __init__(self, fname, name, development):
        super().__init__()
        uic.loadUi('../QTDesinger/photo_looking.ui', self)
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.fname = fname  # инициализируем и здааем таблицу
        # стилей и других параметров
        im = Image.open(fname)
        im = im.resize((440, 440))
        im.save(f'../Мусор/{name}.png')
        self.pixmap = QPixmap(f'../Мусор/{name}.png')
        self.label.setPixmap(self.pixmap)
        self.pushButton.clicked.connect(self.save_photo)
        self.name = name
        self.development = development

    def save_photo(self):  # реализуем функцию сохранения фото
        fname = QFileDialog.getExistingDirectory(self, "Скачать файл", ".")
        if fname != '':
            shutil.copyfile(self.fname, f'{fname}/{self.name}.{self.development}')


class ChangeData(QWidget):  # создаем класс для отображения окна изменения данных
    def __init__(self, out_self, login, out_self_2):
        super().__init__()
        uic.loadUi('../QTDesinger/chanche_data.ui', self)
        self.into_1 = out_self  # инициализируем и здааем таблицу
        # стилей и других параметров
        self.into_2 = out_self_2
        self.login = login
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)

        self.pushButton.setIcon(QIcon(list(out_self.data_users_cursor.execute(f"""SELECT user_icon
                 from user_data_main where user_login = \'{str(login)}\'""").fetchall())[0][0]))
        self.pushButton_2.setText(list(out_self.data_users_cursor.execute(f"""SELECT user_name
                 from user_data_main where user_login = \'{str(login)}\'""").fetchall())[0][0])
        self.pushButton_3.setText(str(login))
        # подключаем кнопки к их функциям
        self.pushButton.clicked.connect(self.chanche_icon)
        self.pushButton_2.clicked.connect(self.chanche_name)
        self.pushButton_4.clicked.connect(self.chanche_password)

    def chanche_icon(self):  # реализуем функцию изменения фотографии профиля
        try:
            fname = QFileDialog.getOpenFileName(self, 'Выбрать'
                                                      ' картинку', '',
                                                'Картинка (*.jpg);;Картинка'
                                                ' (*.png);;Картинка (*.bmp);;Картинка (*.jpeg)')[0]
            im = Image.open(fname)
            im.save(f'../Пользователи/{self.login}/{self.login}.png')
            self.into_1.data_users_cursor.execute(f"""UPDATE user_data_main
            SET user_icon = \'../Пользователи/{self.login}/{self.login}.png\'
            WHERE user_login = \'{self.login}\'""")
            self.into_1.data_users_connect.commit()
            self.into_2.update_window()
            self.pushButton.setIcon(QIcon(f'../Пользователи/{self.login}/{self.login}.png'))
        except AttributeError:
            pass

    def chanche_name(self):  # реализуем функцию изменения имени профиля
        self.chanche_name = ChancheName(self, self.login, self.into_1)
        self.chanche_name.show()

    def chanche_password(self):  # реализуем функцию изменения пароля
        self.chanche_password_df = ChanchePassword(self.into_1, self.login)
        self.chanche_password_df.show()


class ChanchePassword(QMainWindow):  # создаем класс для отображения окна изменения пароля
    def __init__(self, into, login):
        super().__init__()
        uic.loadUi('../QTDesinger/chanche_password.ui', self)
        global CURRENT_STYLE_SHEET  # инициализируем и здааем таблицу
        # стилей и других параметров
        self.setStyleSheet(CURRENT_STYLE_SHEET)

        self.pushButton.clicked.connect(self.check)
        self.into = into
        self.login = login

    def check(self):  # реализуем функцию проверки пароля
        try:
            if self.lineEdit.text() != self.lineEdit_2.text():
                raise ChancheError('                                 Пароли различаются!')
            if len(self.lineEdit.text()) < 8:
                raise ChancheError('        Слишком короткий пароль! Минимум 8 символов.')
            if (self.lineEdit.text().islower() or self.lineEdit.text().isupper()) or (
                    True not in [True if i.isalpha() else False for i in self.lineEdit.text()]) \
                    or True not in [True if i.isdigit() else False for i in self.lineEdit.text()]:
                raise ChancheError('Пароль не может состоять только'
                                   ' из букв или цифр одного регистра!')
            if self.lineEdit.text() == list(self.into.data_users_cursor.execute(f"""SELECT
             user_password from user_data_main where
              user_login = \'{self.login}\'""").fetchall())[0][0]:
                raise ChancheError('            Старый и новый пароли не должны совпадать!')
            self.into.data_users_cursor.execute(f"""UPDATE user_data_main
                     SET user_password = \'{self.lineEdit.text()}\'
                    WHERE user_login = \'{self.login}\'""")
            self.into.data_users_connect.commit()
            self.close()
        except ChancheError as e:
            self.statusbar.showMessage(str(e), 3000)


class ChancheName(QMainWindow):  # создаем класс для отображения окна изменения имени
    def __init__(self, into, login, into_1):
        super().__init__()
        uic.loadUi('../QTDesinger/chancne_name.ui', self)
        self.login = login
        self.into_1 = into_1  # инициализируем и здааем таблицу
        # стилей и других параметров
        self.into_2 = into
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)

        self.pushButton.clicked.connect(self.new_user_name)

    def new_user_name(self):  # реализуем функцию проверки имени
        try:
            if len(self.lineEdit.text()) <= 2:
                raise ChancheError('      Слишком короткое имя! Минимум 3 символа!')
            if len(self.lineEdit.text()) > 30:
                raise ChancheError('      Слишком длинное имя! Максимум 30 символа!')
            if False in [False if i.isdigit() is False and i.isalpha() is False else True for i in
                         ''.join(self.lineEdit.text().split())]:
                raise ChancheError('Имя может содержать только буквы, цыфры и пробел!')
            self.into_1.data_users_cursor.execute(f"""UPDATE user_data_main
                        SET user_name = \'{self.lineEdit.text()}\'
                        WHERE user_login = \'{self.login}\'""")
            self.into_1.data_users_connect.commit()
            self.into_2.pushButton_2.setText(self.lineEdit.text())
            self.close()
        except ChancheError as e:
            self.statusbar.showMessage(str(e), 2000)


class CheckProfile(QWidget):  # создаем класс для отображения окна просмотра профиля
    def __init__(self, my_login, interlocutor_login, into_dialogs):
        super().__init__()
        uic.loadUi('../QTDesinger/check_profile.ui', self)
        self.my_login = my_login  # инициализируем и здааем таблицу
        # стилей и других параметров
        self.interlocutor_login = interlocutor_login
        self.into_dialogs = into_dialogs
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)

        self.pushButton.setIcon(QIcon(list(into_dialogs.into.data_users_cursor.execute(f"""SELECT user_icon
                         from user_data_main where user_login
                          = \'{str(interlocutor_login)}\'""").fetchall())[0][0]))
        self.pushButton_2.setText(list(into_dialogs.into.data_users_cursor.execute(f"""SELECT user_name
                         from user_data_main where user_login
                          = \'{str(interlocutor_login)}\'""").fetchall())[0][0])
        self.pushButton_3.setText(str(interlocutor_login))

        self.pushButton_4.clicked.connect(self.open_new_dialog)

    def open_new_dialog(self):  # реализуем функцию проверки имени
        self.into_dialogs.open_dialogs = \
            OpenPrivateDialog(self.my_login, self.interlocutor_login,
                              self.into_dialogs.into, self.into_dialogs)
        self.into_dialogs.open_dialogs.show()
        self.close()


class SettingPrivate(QMainWindow):  # создаем класс для отображения окна настроек чата
    def __init__(self, my_login, interlocutor_login, into_dialogs, into_open_dialogs, where_file):
        super().__init__()
        uic.loadUi('../QTDesinger/setting_private.ui', self)
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)  # инициализируем и здааем таблицу
        # стилей и других параметров

        self.my_login = my_login
        self.interlocutor_login = interlocutor_login
        self.into_dialogs = into_dialogs
        self.into_open_dialogs = into_open_dialogs
        self.where_file = where_file

        self.pushButton.clicked.connect(self.clean_widget)
        self.pushButton_2.clicked.connect(self.clean_history)
        self.pushButton_3.clicked.connect(self.delete_dialog)

    def clean_widget(self):  # реализуем функцию очитски виджета
        self.into_open_dialogs.listWidget.clear()

    def clean_history(self):  # реализуем функцию очитски истории чата
        open(self.where_file, mode='w', encoding='utf-8').write('')
        self.into_open_dialogs.listWidget.clear()

    def delete_dialog(self):  # реализуем функцию удаления чата
        list_index = self.into_dialogs.into.data_users_cursor.execute(f"""SELECT who_to_chat_with
        from user_data_main WHERE user_login
         = \'{self.my_login}\'""").fetchall()[0][0].split('%$%').index(self.interlocutor_login)

        new_who_to_chat_with = self.into_dialogs.into.data_users_cursor.execute(f"""SELECT
         who_to_chat_with from user_data_main WHERE user_login
         = \'{self.my_login}\'""").fetchall()[0][0].split('%$%')
        del new_who_to_chat_with[list_index]
        self.into_dialogs.into.data_users_cursor.execute(f"""UPDATE user_data_main
        SET who_to_chat_with = \'{'%$%'.join(new_who_to_chat_with)}\' WHERE user_login 
        = \'{self.my_login}\'""")

        new_where_dialog = self.into_dialogs.into.data_users_cursor.execute(f"""SELECT
         where_dialog from list_dialogs WHERE user_login
                 = \'{self.my_login}\'""").fetchall()[0][0].split('%$%')
        del new_where_dialog[list_index]
        self.into_dialogs.into.data_users_cursor.execute(f"""UPDATE list_dialogs
                SET where_dialog = \'{'%$%'.join(new_where_dialog)}\'
        WHERE user_login = \'{self.my_login}\'""")

        new_who_to_chat_with = self.into_dialogs.into.data_users_cursor.execute(f"""SELECT
                                 who_to_chat_with from list_dialogs WHERE user_login
                                         = \'{self.my_login}\'""").fetchall()[0][0].split('%$%')
        del new_who_to_chat_with[list_index]
        self.into_dialogs.into.data_users_cursor.execute(f"""UPDATE list_dialogs
                                        SET who_to_chat_with = \'{'%$%'.join(new_who_to_chat_with)}\'
                                WHERE user_login = \'{self.my_login}\'""")

        list_index = self.into_dialogs.into.data_users_cursor.execute(f"""SELECT who_to_chat_with
                from user_data_main WHERE user_login
                 = \'{self.interlocutor_login}\'""").fetchall()[0][0].split('%$%').index(self.my_login)

        new_who_to_chat_with = self.into_dialogs.into.data_users_cursor.execute(f"""SELECT
                 who_to_chat_with from user_data_main WHERE user_login
                 = \'{self.interlocutor_login}\'""").fetchall()[0][0].split('%$%')
        del new_who_to_chat_with[list_index]
        self.into_dialogs.into.data_users_cursor.execute(f"""UPDATE user_data_main
                SET who_to_chat_with = \'{'%$%'.join(new_who_to_chat_with)}\' WHERE user_login 
                = \'{self.interlocutor_login}\'""")

        new_where_dialog = self.into_dialogs.into.data_users_cursor.execute(f"""SELECT
                 where_dialog from list_dialogs WHERE user_login
                         = \'{self.interlocutor_login}\'""").fetchall()[0][0].split('%$%')
        del new_where_dialog[list_index]
        self.into_dialogs.into.data_users_cursor.execute(f"""UPDATE list_dialogs
                        SET where_dialog = \'{'%$%'.join(new_where_dialog)}\'
                WHERE user_login = \'{self.interlocutor_login}\'""")

        new_who_to_chat_with = self.into_dialogs.into.data_users_cursor.execute(f"""SELECT
                                         who_to_chat_with from list_dialogs WHERE user_login
                                                 = \'{self.interlocutor_login}\'""").fetchall()[0][0].split('%$%')
        del new_who_to_chat_with[list_index]
        self.into_dialogs.into.data_users_cursor.execute(f"""UPDATE list_dialogs
                                                SET who_to_chat_with = \'{'%$%'.join(new_who_to_chat_with)}\'
                                        WHERE user_login = \'{self.interlocutor_login}\'""")

        self.into_dialogs.into.data_users_connect.commit()
        self.into_open_dialogs.close()
        self.into_dialogs.update_window()
        self.close()


class ListParticipant(QWidget):  # создаем класс для отображения окна со списком участников
    def __init__(self, my_login, into_open_dialogs, identification_name):
        super().__init__()
        uic.loadUi('../QTDesinger/list_participant.ui', self)

        self.my_login = my_login
        self.into_open_dialogs = into_open_dialogs  # инициализируем и здааем таблицу
        # стилей и других параметров
        self.identification_name = identification_name
        self.name_dialog = self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
        SELECT discussion_name from discussions
         WHERE identification_name = \'{self.identification_name}\'""").fetchall()[0][0]
        self.pushButton_2.setIcon(
            QIcon(self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
        SELECT discussions_icon from discussions WHERE identification_name =
         \'{self.identification_name}\'""").fetchall()[0][0]))
        self.label.setText(self.name_dialog)
        self.list_participant = \
            self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""SELECT
        users from discussions WHERE identification_name =
         \'{self.identification_name}\'""").fetchall()[0][0].split('%$%')[1:]

        self.update_widget()

    def update_widget(self):  # реализуем функцию обновления виджета
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.listWidget.clear()
        for i in self.list_participant:
            pushbutton = \
                QPushButton(self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
            SELECT user_name from user_data_main WHERE user_login = \'{i}\'""").fetchall()[0][0]
                            + f' ({i})')
            listWidgetItem = QListWidgetItem()
            listWidgetItem.setIcon(QIcon(
                self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
            SELECT user_icon from user_data_main where user_login
                             = \'{i}\'""").fetchall()[0][0]))
            listWidgetItem.setSizeHint(QSize(25, 35))
            pushbutton.setEnabled(False)
            self.listWidget.addItem(listWidgetItem)
            self.listWidget.setItemWidget(listWidgetItem, pushbutton)


class SettingGlobal(QMainWindow):  # создаем класс для отображения настроек беседы
    def __init__(self, my_login, into_open_dialogs, identification_name):
        super().__init__()
        uic.loadUi('../QTDesinger/setting_global.ui', self)
        self.my_login = my_login  # инициализируем и здааем таблицу
        # стилей и других параметров
        self.into_open_dialogs = into_open_dialogs
        self.identification_name = identification_name
        self.list_participant = \
            self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""SELECT
                users from discussions WHERE identification_name =
                 \'{self.identification_name}\'""").fetchall()[0][0].split('%$%')
        self.admin = self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""SELECT
        admin from discussions WHERE identification_name
         = \'{self.identification_name}\'""").fetchall()[0][0]
        self.pushButton_4.setIcon(
            QIcon(self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""SELECT
        discussions_icon from discussions WHERE
         identification_name = \'{self.identification_name}\'""").fetchall()[0][0]))
        if self.admin != self.my_login:
            self.run()
        else:
            self.run_admin()

    def update_widget(self):  # реализуем функцию обновления виджета
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.listWidget.clear()
        self.pushButton_4.setIcon(
            QIcon(self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""SELECT
                discussions_icon from discussions WHERE
                 identification_name = \'{self.identification_name}\'""").fetchall()[0][0]))
        self.list_participant = \
            self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""SELECT
                        users from discussions WHERE identification_name =
                         \'{self.identification_name}\'""").fetchall()[0][0].split('%$%')[1:]
        for i in self.list_participant:
            pushbutton = \
                QPushButton(self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
            SELECT user_name from user_data_main WHERE user_login = \'{i}\'""").fetchall()[0][0]
                            + f' ({i})')
            listWidgetItem = QListWidgetItem()
            listWidgetItem.setIcon(QIcon(
                self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
            SELECT user_icon from user_data_main where user_login
                             = \'{i}\'""").fetchall()[0][0]))
            listWidgetItem.setSizeHint(QSize(25, 35))
            pushbutton.setEnabled(False)
            self.listWidget.addItem(listWidgetItem)
            self.listWidget.setItemWidget(listWidgetItem, pushbutton)

    def run(self):  # реализуем функцию подстраивания окна под пользователя
        self.statusbar.showMessage('Так как вы не являетесь создателем беседы,'
                                   ' ваши действия ограничены!', 25000)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_7.setEnabled(False)
        self.pushButton.clicked.connect(self.clean_widget)
        self.pushButton_5.clicked.connect(self.exit)
        self.pushButton_6.clicked.connect(self.add_participant)
        self.update_widget()

    def add_participant(self):  # реализуем функцию добавления участника
        self.add_participant_open = \
            AddParticipant(self.my_login, self.into_open_dialogs,
                           self.identification_name, self, self.list_participant)
        self.add_participant_open.show()

    def exit(self):  # реализуем функцию выхода из беседы
        my_positional = self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""SELECT
        discussions from user_data_main WHERE user_login
         = \'{self.my_login}\'""").fetchall()[0][0].split('%$%')
        del my_positional[my_positional.index(self.identification_name)]
        self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""UPDATE user_data_main
        SET discussions = \'{'%$%'.join(my_positional)}\' WHERE user_login = \'{self.my_login}\'""")

        my_positional = self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""SELECT
        users from discussions WHERE
         identification_name = \'{self.identification_name}\'""").fetchall()[0][0].split('%$%')
        del my_positional[my_positional.index(self.my_login)]
        self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""UPDATE discussions
        SET users = \'{'%$%'.join(my_positional)}\'""")

        self.into_open_dialogs.into_dialog.into.data_users_connect.commit()
        self.into_open_dialogs.into_dialog.update_window()
        self.into_open_dialogs.close()
        self.close()

    def clean_widget(self):  # реализуем функцию очистки виджета
        self.into_open_dialogs.listWidget.clear()

    def run_admin(self):  # реализуем функцию подстраивания окна под создателя беседы
        self.statusbar.showMessage('Так как вы являетесь создателем беседы,'
                                   ' вы не можете выйти! А только удалить беседу!', 25000)
        self.update_widget()
        self.pushButton_6.clicked.connect(self.add_participant)
        self.pushButton_5.setText('Переименовать')
        self.pushButton_5.clicked.connect(self.rename)
        self.pushButton.clicked.connect(self.clean_widget)
        self.pushButton_2.clicked.connect(self.clean_history)
        self.pushButton_4.clicked.connect(self.new_icon)
        self.pushButton_7.clicked.connect(self.delete_participant)
        self.pushButton_3.clicked.connect(self.delete_dialog)

    def rename(self):  # реализуем функцию изменеия названия беседы
        self.rename = RenameDialog(self.into_open_dialogs, self.identification_name, self)
        self.rename.show()

    def delete_dialog(self):  # реализуем функцию удаления беседы
        for i in self.list_participant:
            new_discussions = self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
            SELECT discussions from user_data_main WHERE user_login
             = \'{i}\'""").fetchall()[0][0].split('%$%')
            del new_discussions[new_discussions.index(self.identification_name)]
            self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""UPDATE
            user_data_main SET discussions = \'{'%$%'.join(new_discussions)}\'
            WHERE user_login = \'{i}\'""")
        self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""DELETE from discussions
        WHERE identification_name = \'{self.identification_name}\'""")
        self.into_open_dialogs.into_dialog.update_window()
        self.into_open_dialogs.setting.close()
        self.into_open_dialogs.close()
        self.close()

    def delete_participant(self):  # реализуем функцию удаления участника
        self.delete_participant = \
            ManagementParticipant(self.my_login,
                                  self.into_open_dialogs, self.identification_name,
                                  self, self.list_participant)
        self.delete_participant.show()

    def new_icon(self):  # реализуем функцию изменения фотографии беседы
        try:
            fname = QFileDialog.getOpenFileName(self, 'Выбрать'
                                                      ' картинку', '',
                                                'Картинка (*.jpg);;Картинка'
                                                ' (*.png);;Картинка (*.bmp);;Картинка (*.jpeg)')[0]
            im = Image.open(fname)
            im.save(f'../Пользователи/{self.my_login}/{self.my_login}'
                    f'-{self.identification_name}.png')
            self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""UPDATE
            discussions SET discussions_icon
             = \'{f'../Пользователи/{self.my_login}/'
                  f'{self.my_login}-{self.identification_name}.png'}\'
             WHERE identification_name = \'{self.identification_name}\'""")
            self.into_open_dialogs.into_dialog.into.data_users_connect.commit()
            self.into_open_dialogs.update_widget()
            self.update_widget()
            self.into_open_dialogs.into_dialog.update_window()
        except AttributeError:
            pass

    def clean_history(self):  # реализуем функцию очитски истории беседы
        open(self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
        SELECT where_discussion from discussions WHERE identification_name = 
        \'{self.identification_name}\'""").fetchall()[0][0], mode='w', encoding='utf-8').write('')
        self.into_open_dialogs.listWidget.clear()


class RenameDialog(QMainWindow):  # создаем класс для отображения виджета изменения названия беседы
    def __init__(self, into_open_dialogs, identification_name, into_setting):
        super().__init__()
        uic.loadUi('../QTDesinger/rename_dialog.ui', self)
        self.pushButton.clicked.connect(self.rename)
        self.into_open_dialogs = into_open_dialogs  # инициализируем и здааем таблицу
        # стилей и других параметров
        self.identification_name = identification_name
        self.into_setting = into_setting
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)

    def rename(self):  # реализуем функцию изменеия названия беседы
        try:
            if len(self.lineEdit.text()) <= 2:
                raise ChancheError('      Сначала введите имя! Минимум 3 символа!')
            if len(self.lineEdit.text()) > 30:
                raise ChancheError('      Слишком длинное имя! Максимум 30 символа!')
            if False in [False if i.isdigit() is False and i.isalpha() is False else True for i in
                         ''.join(self.lineEdit.text().split())]:
                raise ChancheError('Имя может содержать только буквы, цыфры и пробел!')
            self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""UPDATE
            discussions SET discussion_name = \'{self.lineEdit.text()}\' WHERE
            identification_name = \'{self.identification_name}\'""")
            self.into_open_dialogs.update_widget()
            self.into_open_dialogs.into_dialog.update_window()
            self.into_setting.update_widget()
            self.close()
        except ChancheError as e:
            self.statusbar.showMessage(e, 6000)


class AddParticipant(QWidget):  # создаем класс для отображения окна добавления участника в беседу
    def __init__(self, my_login, into_open_dialogs,
                 identification_name, into_setting, list_participant):
        super().__init__()
        uic.loadUi('../QTDesinger/add_participant.ui', self)
        self.my_login = my_login  # инициализируем и здааем таблицу
        # стилей и других параметров
        self.into_open_dialogs = into_open_dialogs
        self.identification_name = identification_name
        self.into_setting = into_setting
        self.list_participant = list_participant
        self.name_dialog = self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
        SELECT discussion_name from discussions WHERE identification_name
         = \'{self.identification_name}\'""").fetchall()[0][0]
        self.pushButton.clicked.connect(self.find)
        self.update_widget()

    def update_widget(self):  # реализуем функцию обновления виджета
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.listWidget.clear()
        self.list_participant = \
            self.into_setting.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
            SELECT users from discussions WHERE identification_name =
                         \'{self.identification_name}\'""").fetchall()[0][0].split('%$%')
        if self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""SELECT
        who_to_chat_with from user_data_main WHERE user_login
         = \'{self.my_login}\'""").fetchall() != []:
            self.list_new_participant = \
                [QPushButton(i) for i in
                 self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
                 SELECT who_to_chat_with from user_data_main WHERE user_login =
                  \'{self.my_login}\'""").fetchall()[0][0].split('%$%')[1:]]
            for i in self.list_new_participant:
                if i.text() not in self.list_participant:
                    listWidgetItem = QListWidgetItem()
                    listWidgetItem.setIcon(QIcon(
                        self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
                                SELECT user_icon from user_data_main where user_login
                                                 = \'{i.text()}\'""").fetchall()[0][0]))
                    i.setText(self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
                    SELECT user_name from user_data_main WHERE user_login
                     = \'{i.text()}\'""").fetchall()[0][0] + f' ({i.text()})')
                    listWidgetItem.setSizeHint(QSize(25, 35))
                    self.listWidget.addItem(listWidgetItem)
                    self.listWidget.setItemWidget(listWidgetItem, i)
                    i.clicked.connect(self.add_participant)

    def find(self):  # реализуем функцию поиска
        self.listWidget.clear()
        self.list_participant = \
            self.into_setting.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
                    SELECT users from discussions WHERE identification_name =
                                 \'{self.identification_name}\'""").fetchall()[0][0].split('%$%')
        if self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""SELECT
                who_to_chat_with from user_data_main WHERE user_login
                 = \'{self.my_login}\'""").fetchall() != []:
            self.list_new_participant = \
                [QPushButton(i) for i in
                 self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
                         SELECT who_to_chat_with from user_data_main WHERE user_login =
                          \'{self.my_login}\'""").fetchall()[0][0].split('%$%')[1:]]
            for i in self.list_new_participant:
                if i.text() not in self.list_participant:
                    listWidgetItem = QListWidgetItem()
                    listWidgetItem.setIcon(QIcon(
                        self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
                                        SELECT user_icon from user_data_main where user_login
                                                         = \'{i.text()}\'""").fetchall()[0][0]))
                    i.setText(self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
                            SELECT user_name from user_data_main WHERE user_login
                             = \'{i.text()}\'""").fetchall()[0][0] + f' ({i.text()})')
                    listWidgetItem.setSizeHint(QSize(25, 35))
                    if self.lineEdit.text().lower() in i.text().lower():
                        self.listWidget.addItem(listWidgetItem)
                        self.listWidget.setItemWidget(listWidgetItem, i)
                        i.clicked.connect(self.add_participant)

    def add_participant(self):  # реализуем функцию добавления участника
        sender = self.sender()
        add_discussions = self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
        SELECT discussions from user_data_main WHERE
         user_login = \'{sender.text().split()[-1][1:-1]}\'""").fetchall()[0][0]
        self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""UPDATE user_data_main
        SET discussions = \'{add_discussions + '%$%' + self.identification_name}\' WHERE 
        user_login = \'{sender.text().split()[-1][1:-1]}\'""")

        add_discussions = self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
        SELECT users from discussions WHERE identification_name
         = \'{self.identification_name}\'""").fetchall()[0][0]
        self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""UPDATE
        discussions SET users = \'{add_discussions + '%$%' + sender.text().split()[-1][1:-1]}\'
        WHERE identification_name = \'{self.identification_name}\'""")

        self.into_open_dialogs.into_dialog.into.data_users_connect.commit()

        self.into_open_dialogs.update_widget()
        self.into_setting.update_widget()
        self.update_widget()


class ManagementParticipant(QWidget):  # создаем класс для отображения окна
    # удаления участника из беседы
    def __init__(self, my_login, into_open_dialogs,
                 identification_name, into_setting, list_participant):
        super().__init__()
        uic.loadUi('../QTDesinger/delete_participant.ui', self)
        self.my_login = my_login  # инициализируем и здааем таблицу
        # стилей и других параметров
        self.into_open_dialogs = into_open_dialogs
        self.identification_name = identification_name
        self.into_setting = into_setting
        self.list_participant = list_participant
        self.pushButton.clicked.connect(self.find)
        self.update_widget()

    def find(self):
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.listWidget.clear()
        self.list_participant = \
            self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
                                SELECT users from discussions WHERE identification_name =
                                             \'{self.identification_name}\'""").fetchall()[0][0].split('%$%')[1:]
        if self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""SELECT
                        who_to_chat_with from user_data_main WHERE user_login
                         = \'{self.my_login}\'""").fetchall() != []:
            self.list_new_participant = [QPushButton(i) for i in self.list_participant]
            for i in self.list_new_participant:
                if self.my_login != i.text():
                    listWidgetItem = QListWidgetItem()
                    listWidgetItem.setIcon(QIcon(
                        self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
                                            SELECT user_icon from user_data_main where user_login
                                                            = \'{i.text()}\'""").fetchall()[0][0]))
                    i.setText(self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
                                     SELECT user_name from user_data_main WHERE user_login
                                       = \'{i.text()}\'""").fetchall()[0][0] + f' ({i.text()})')
                    listWidgetItem.setSizeHint(QSize(25, 35))
                    if self.lineEdit.text().lower() in i.text().lower():
                        self.listWidget.addItem(listWidgetItem)
                        self.listWidget.setItemWidget(listWidgetItem, i)
                        i.clicked.connect(self.delete_participant)

    def update_widget(self):  # реализуем функцию обновления виджета
        global CURRENT_STYLE_SHEET
        self.setStyleSheet(CURRENT_STYLE_SHEET)
        self.listWidget.clear()
        self.list_participant = \
            self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
                    SELECT users from discussions WHERE identification_name =
                                 \'{self.identification_name}\'""").fetchall()[0][0].split('%$%')[1:]
        if self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""SELECT
                who_to_chat_with from user_data_main WHERE user_login
                 = \'{self.my_login}\'""").fetchall():
            self.list_new_participant = [QPushButton(i) for i in self.list_participant]
            for i in self.list_new_participant:
                if self.my_login != i.text():
                    listWidgetItem = QListWidgetItem()
                    listWidgetItem.setIcon(QIcon(
                        self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
                                            SELECT user_icon from user_data_main where user_login
                                                             = \'{i.text()}\'""").fetchall()[0][0]))
                    i.setText(self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
                             SELECT user_name from user_data_main WHERE user_login
                               = \'{i.text()}\'""").fetchall()[0][0] + f' ({i.text()})')
                    listWidgetItem.setSizeHint(QSize(25, 35))
                    self.listWidget.addItem(listWidgetItem)
                    self.listWidget.setItemWidget(listWidgetItem, i)
                    i.clicked.connect(self.delete_participant)

    def delete_participant(self):  # реализуем функцию удаления участника из беседы
        sender = self.sender()
        new_list_users = self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""
        SELECT users from discussions WHERE identification_name
         = \'{self.identification_name}\'""").fetchall()[0][0].split('%$%')
        del new_list_users[new_list_users.index(sender.text().split()[-1][1:-1])]
        self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""UPDATE 
        discussions SET users = \'{'%$%'.join(new_list_users)}\'""")

        new_discussions_list = \
            self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""SELECT
            discussions from user_data_main WHERE user_login
             = \'{sender.text().split()[-1][1:-1]}\'""").fetchall()[0][0].split('%$%')
        del new_discussions_list[new_discussions_list.index(self.identification_name)]
        self.into_open_dialogs.into_dialog.into.data_users_cursor.execute(f"""UPDATE 
        user_data_main SET discussions = \'{'%$%'.join(new_discussions_list)}\' WHERE user_login
         = \'{sender.text().split()[-1][1:-1]}\'""")

        self.into_open_dialogs.into_dialog.into.data_users_connect.commit()
        self.into_setting.update_widget()
        self.into_open_dialogs.into_dialog.update_window()
        self.into_open_dialogs.update_widget()
        self.update_widget()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Authorizations()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
