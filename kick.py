from aminofix import Client, SubClient, exceptions
from time import sleep
import threading
import os

os.system('cls' if os.name == 'nt' else 'clear')

print("""
█▄▀ █ █▀▀ █▄▀ ░ █▀█ █▄█|ᵇʸ ᵈᵉˡᵃᶠᵃᵘˡᵗ
█░█ █ █▄▄ █░█ ▄ █▀▀ ░█░
""")

def gd_print(value):
    green_color = '\033[32m'
    reset_color = '\033[0m'
    result = f"\n>{green_color} {value} {reset_color}\n"
    print(result)

def bd_print(value):
    red_color = '\033[31m'
    reset_color = '\033[0m'
    result = f"\n>{red_color} {value} {reset_color}\n"
    print(result)

def kick_user(sub_clientz, chatId, userId):
    try:
        sub_clientz.kick(chatId=chatId, userId=userId, allowRejoin=True)
        gd_print(f"Кикнули пользователя с ID: {userId}")
    except exceptions.IpTemporaryBan:
        bd_print("Ошибка: вас забанили по ip. Скрипт продолжит работу через 360 секунд")
        sleep(360)
    except Exception as error:
        bd_print(f"Ошибка при кике пользователя с ID '{userId}': {error}")

def main():
    while True:
        try:
            clientz = Client()
            clientz.login(email = input("E-mail: "), password = input("пароль: "))
            gd_print(f"Вошли в аккаунт '{clientz.profile.nickname}'")
            break
        except exceptions.VerificationRequired as e:
            bd_print(f"Ошибка: требуется верификация аккаунта. Пройдите капчу и попробуйте войти снова: {e})")
        except Exception as error:
            bd_print(f"Ошибка: {error}")

    while True:
        try:
            chat_link = clientz.get_from_code(input("Ссылка на чат: "))
            comId = chat_link.comId
            chatId = chat_link.objectId
            sub_clientz = SubClient(comId = comId, profile = clientz.profile)
            gd_print(f"Получили информацию о чате '{sub_clientz.get_chat_thread(chatId).title}'")
            break
        except exceptions.UnexistentData as e:
            bd_print(f"Ошибка: чат не найден: {e}")
        except Exception as error:
            bd_print(f"Ошибка: {error}")

    while True:
        try:
            min_level = int(input("Уровень, ниже которого все пользователи будут кикнуты: "))

            chat_users = sub_clientz.get_chat_users(chatId=chatId, start=0, size=100)
            users_to_kick = []

            for user in chat_users.userId:
                if sub_clientz.get_user_info(user).level < min_level:
                    users_to_kick.append(user)

            if users_to_kick:
                threads = []
                for user_to_kick in users_to_kick:
                    thread = threading.Thread(target=kick_user, args=(sub_clientz, chatId, user_to_kick))
                    thread.start()
                    threads.append(thread)

                for thread in threads:
                    thread.join()

            messages = sub_clientz.get_chat_messages(chatId=chatId, size=20)
            for message in messages.messageId:
                if sub_clientz.get_message_info(chatId, message).messageType == 101:
                    sub_clientz.delete_message(chatId=chatId, messageId=message)

            else:
                gd_print(f"Нет пользователей с уровнем меньше {min_level}")
            break
        except exceptions.IpTemporaryBan:
            bd_print("Ошибка: вас забанили по ip. Скрипт продолжит работу через 360 секунд")
            sleep(360)
        except exceptions.AccountLimitReached or exceptions.TooManyRequests:
            bd_print("Ошибка: Слишком много запросов. Скрипт остановлен")
            exit()
        except Exception as error:
            bd_print(f"Ошибка: {error}*")



if __name__ == '__main__':
    main()
    print("---")
    print()
    gd_print(f"Скрипт завершил свою работу!")
