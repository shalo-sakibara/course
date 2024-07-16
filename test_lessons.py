class Base_vid:

    @classmethod
    def __read_file(cls, link):
        res = []
        with open(link, 'r', encoding='utf-8') as file:
            for i in file:
                res.append(i.split('*'))
        return res

    def __init__(self, link) -> None:
        self.__link = link

    def get_less(self, number):
        if number == 'all':
            return self.__read_file(self.__link)
        if number == 1:
            return self.__read_file(self.__link)[0][1]
        if number == 2:
            return self.__read_file(self.__link)[1][1]


# b = Base_vid('t_lessons.txt')
