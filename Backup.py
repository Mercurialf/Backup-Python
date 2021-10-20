"""Консольное приложение для создания резервных копий в формате zip."""
import os
import time
import zipfile
import shutil

__version__ = '0.04'


# Используем функцию которая содержит путь к каталогу по умолчанию, но даём возможность выбрать путь пользователю.
def Path():
    default_path = 'E:\\Document'
    user_choice = input('Указать путь к каталогу, '
                        'или использовать по умолчанию ({0})? Y or N\n'.format(default_path))

    # Используем цикл для проверки ввода пользователя
    while True:
        if user_choice == 'Y':
            user_path = input('Введите путь к каталогу который нужно архивировать.\n')
            return user_path
        elif user_choice == 'N':
            print('Будет использован путь к каталогу по умоланию.')
            return default_path


# Функция которая получает путь в котором должен оказаться архив, либо используем по умолчанию.
def target_Path():
    default_path = 'E:\\Backup'
    user_choice = input('Указать путь сохранения архива, '
                        'или использовать по умолчанию ( {0})? Y or N\n'.format(default_path))

    while True:
        if user_choice == 'Y':
            user_path = input('Введите путь сохранения каталога.\n')
            return user_path
        elif user_choice == 'N':
            print('Будет использован путь к каталогу по умолчанию.')
            return default_path


print('BackUp ver.{0}'.format(__version__))
# Получаем адрес каталога с помощью функции, далее переходим в него.
path = Path()
os.chdir(path)

s = """
Вызываем функцию чтобы получить каталог назначения архива от пользователя, или используем путь по умолчанию.
Используем системный разделитель пути для кроссплатформенности. Далее получаем текущую дату которую используем
как название подкаталога, и текущее время для названия архива.
"""
today = target_Path() + os.sep + time.strftime('%Y%m%d')


# Создаем каталог в котором будет архив, если его ещё нет.
if not os.path.exists(today):
    os.mkdir(today)  # Создание каталога
    print('Каталог {0} успешно создан.'.format(today))


# Функция которая позволяет добавлять комментарий к архиву
def User_Comment():
    user_comment = input('Введите комментарий --> ')
    time_now = time.strftime('%H%M%S')

    if len(user_comment) == 0:
        return time_now + '.zip'
    else:
        return time_now + '_' + user_comment.replace(' ', '_') + '.zip'


"""
Вызываем функцию которая проверяет - добавляет ли пользователь комментарий к архиву,
если да, то возвращаем название архива + комментарий.
Далее мы создаем архив, используя время как имя архива.
"""
now = User_Comment()
zip_file = zipfile.ZipFile(now, 'w')

# Рекурсивный перебор в указаном каталоге 'path'
for root, dirs, files in os.walk(path):
    for file in files:
        zip_file.write(os.path.join(root, file))

# Закрываем архив и перемещаем архив
zip_file.close()
shutil.move(now, today)
