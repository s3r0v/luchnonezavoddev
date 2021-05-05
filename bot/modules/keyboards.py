
from bot.modules.keyboard_maker import KeyboardInline, KeyboardReply

"""
keyboard v 1.0
:List of :Dicts where first is :Str name, last is :Str callback.
"""

start_menu = KeyboardInline([{"Начать": "start_game"},{"Правила игры": "rules"}]).get()
reply_main = KeyboardReply([["⭐️Главное меню"],["📢 Поделиться"],["🤖 О боте"]]).get()
yes_or_no =KeyboardInline([{"Да🥺": "yes"},{"Нет😀":"no"}]).get()
next = KeyboardInline([{"Продолжить": "next"}]).get()
back_from_the_rules = KeyboardInline([{"Назад": "backRules"}]).get()
back = KeyboardInline([{"Назад": "back"}]).get()
act1 = KeyboardInline([{"АКТ 1": "act1"}]).get()
act2 = KeyboardInline([{"АКТ 2": "act2"}]).get()
act3 = KeyboardInline([{"АКТ 3": "act3"}]).get()
end = KeyboardInline([{"Закончить": "end"}]).get()
ALLEND = KeyboardInline([{"Поделиться результатом": "ser"},{"Поделиться ботом": "share"},
                        {"Заново": "new"}]).get()

set_pers = KeyboardInline([{"1": "Творческого объединения"},
                           {"2": "Совета по качечтву обучения"},
                           {"3": "Студенческого совета"}]).get()

fourButton = KeyboardInline([{"1": "1","2": "2"},
                      {"3": "3","4": "4"}]).get()


positions_of_people = KeyboardInline([{"1)г 2)а 3)б 4)в": "1"},
                      {"1)в 2)а 3)г 4)б": "2"},
                      {"1)б 2)а 3)в 4)г": "3"},
                      {"1)в 2)г 3)б 4)а": "4"}]).get()
threeButton=KeyboardInline([{"1": "1"},
                      {"2": "2"},
                      {"3": "3"}]).get()

info = KeyboardInline([{"🤓 Создатели": "creators"},{"🧐 Для кого бот?": "users"},{"🙂 Обратная связь":"link"}]).get()
back_metric = KeyboardInline([{"Назад": "back_metric"}]).get()




