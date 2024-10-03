import os
import shutil


class Base_vid:

    def __read_file(self):
        a = dict()
        with open(self.__link, 'r', encoding='utf-8') as f:
            for i in f:
                if i != '\n':
                    i = i.split('*')
                    names = i[0].split()
                    path = i[1][:-1]
                    number, name = int(names[0]), ' '.join(names[1:])
                    a[number] = [name, path]

        return a

    def sort_list_less(self):
        """Функция сортировки видео в файле. (Будет использоваться часто!!!)"""
        a = self.__read_file()
        a = dict(sorted(a.items(), key=lambda item: item[0]))

        # очистка файла
        with open(self.__link, 'w', encoding='utf-8') as f:
            f.write('')

        # Записть в файл сортированного списка
        with open(self.__link, 'a', encoding='utf-8') as f:
            for k, v in a.items():
                st = f'{k} {v[0]}*{v[1]}\n'
                f.write(st)

        return True

    def __add_video(self, file_path, downloaded_file):
        """Функция добавляет видеофайл в папку со всеми видео"""
        # file_name = os.path.basename(file_path)  # получаем имя файла
        # destination_path = os.path.join(
        #     self.__path_direct, file_name)  # создаем ссылку
        # print(destination_path)
        # shutil.move(file_path, destination_path)  # Переносим файл
        # return os.path.abspath(file_name)
        # Сохраняем файл на диск
        with open(f'{file_path}.mp4', 'wb') as new_file:
            new_file.write(downloaded_file)
        return True

    def __init__(self, path_file_videos, path_direct) -> None:
        self.__link = path_file_videos
        self.__path_direct = path_direct.replace('/', '\\')

    def get_less(self, number):
        if number == 'all':
            return self.__read_file()
        number = int(number)
        return (self.__read_file()[number][0], self.__read_file()[number][1])

    def set_less(self, name, down_file):
        new_name = ''.join(name.split()[1:])
        # path_file = self.__add_video(os.path.abspath(name))
        path_file = f'{self.__path_direct}\{new_name}'
        print(path_file)
        self.__add_video(path_file, down_file)
        text = f'\n{name}*{path_file}.mp4 '
        with open(self.__link, 'a', encoding='utf-8') as file:
            file.write(text)
        self.sort_list_less()
        return True

    def del_less(self, number):
        arr = self.__read_file()
        if number in arr.keys():
            path = self.__read_file()[number][-1]
            os.remove(path=path)
            arr.pop(number)
            new_arr = ''
            for i in arr:
                mes = f'{i} {arr[i][0]}*{arr[i][1]}\n'
                new_arr += mes
            with open(self.__link, 'w', encoding='utf-8') as file:
                file.write(new_arr)
            return True
        else:
            return False

    def edit_name_less(self, number: int, new_name: str):
        lessons = self.__read_file()
        lessons[number][0] = new_name

        with open(self.__link, 'w', encoding='utf-8') as f:
            f.write('')

        # Записть в файл сортированного списка
        with open(self.__link, 'a', encoding='utf-8') as f:
            for k, v in lessons.items():
                st = f'{k} {v[0]}*{v[1]}\n'
                f.write(st)
        return True

    def edit_vid_less(self, number, new_vid):
        pass
