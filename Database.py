from abc import ABC, abstractmethod
import pandas as pd

class Database(ABC):

    @abstractmethod
    def __init__(self):
        pass


    def load_questions(self, amount, category, difficulty, type):

        """

        :param self:
        :param amount:
        :param category:
        :param difficulty:
        :param type:
        :return:

        a pandas Series of dictionaries, for database api to manage.
        """


        url = f"https://opentdb.com/api.php?amount={amount}"
        if (category):
            url += f"&category={category}"
        if (difficulty):
            url += f"&difficulty={difficulty}"
        if (type):
            url += f"&type={type}"

        data = list(pd.read_json(url).results)
        return data
