import pandas as pd
from MongoDb import MongoDb
from ui import UI
import html


class Game:

    def __init__(self, db):
        if (db == "mongo"):
            self.dbserver = MongoDb()

#        self.dbserver.load_questions()
        self.ui = UI()

        self.categories = pd.DataFrame.from_records(pd.read_json("https://opentdb.com/api_category.php").trivia_categories)
        self.categories.set_index("id", inplace=True)

        self.start_game("normal")

    def update_db(self, batch):
        for i in range(len(batch)):
            self.dbserver.update_db(batch.iloc[i].name, batch.iloc[i].user_name, batch.iloc[i].correct_answer)


    def user_mode(self):

        self.user_name = self.ui.input("Please enter your name: ")
        self.display_categories("Choose a category of questions: \n")
#        self.ui.display("\n".join(self.categories["name"]))
        self.user_category = str.title(self.ui.input("\n"))
        self.user_difficulty = str.lower(self.ui.input("Choose difficulty level (easy, medium, hard): "))
        self.user_number_of_questions = self.ui.input("Please enter number of questions: ")

        self.session = pd.DataFrame(self.dbserver.get_question(self.user_category, self.user_difficulty, self.user_number_of_questions))
        batch = {}

        while len(self.session):
            question = self.session.iloc[len(self.session)-1]
            self.session = self.session.drop(len(self.session)-1)
            self.ui.displayHTMLchars(question["question"])
            answers = question["incorrect_answers"]
            correct_answer = html.unescape(question["correct_answer"])
            answers.append(correct_answer)
            while len(answers):
                self.ui.displayHTMLchars(answers.pop())
            answer = self.ui.input("\nPlease enter your answer: ")
            is_correct_answer = (answer == correct_answer)
            if is_correct_answer:
                self.ui.display("Correct!")
            else:
                self.ui.display("Wrong")

            batch[question["_id"]] = (self.user_name, is_correct_answer)

        batch = pd.DataFrame.from_dict(batch, orient="index", columns=["user_name", "correct_answer"])
        self.ui.display(f"You answered correctly to {batch.correct_answer.sum()} out of {batch.correct_answer.count()} questions!")
        self.update_db(batch)

    def display_categories(self, intro_text):
        self.ui.display(intro_text)
        self.ui.display("\n".join(self.categories["name"]))

    def add_category(self):
        self.display_categories("Current categories: ")
        category = self.ui.input("\nEnter your new category: ")
        self.categories.loc[self.categories.index.max() + 1, "name"] = category


# TODO : categories should be stored in the database

    def remove_category(self):
        self.display_categories("Current categories: ")
        category = self.ui.input("\nEnter category id to be removed: ")
        self.categories.drop(index=category, inplace=True)

    def add_question(self):
        self.display_categories("Choose a category: ")
        category = str.title(self.ui.input("\n"))
        qtype = None
        while (qtype != "boolean" or qtype != "multiple"):
            qtype = self.ui.input("What is the type of the question? boolean or multiple choice [boolean/multiple] ")
        difficulty = None
        while (difficulty not in ["easy","medium","hard"]):
            difficulty = str.lower(self.ui.input("Choose difficulty level (easy, medium, hard): "))
        question = self.ui.input("Enter your question:\n")
        if (qtype == "boolean"):
            correct_answer = None
            while (correct_answer != "True" or correct_answer != "False"):
                correct_answer = str.capitalize(self.ui.input("Enter correct answer (True/False): "))
            if (correct_answer) == "True":
                incorrect_answer = ["False"]
            else:
                incorrect_answer = ["True"]
        else:
            correct_answer = self.ui.input("Enter correct answer:\n")
            incorrect_answer = []
            for i in range(3):
                incorrect_answer.append(self.ui.input(f"Enter incorrect answer number {i+1}:\n"))

        new_question = {
            "category": category,
            "type": qtype,
            "difficulty": difficulty,
            "question": question,
            "correct_answer": correct_answer,
            "incorrect_answers": incorrect_answer
        }
        self.dbserver.add_question(new_question)

    def load_questions(self):
        amount = self.ui.input("How many questions would you like to load from online database? ")
        self.dbserver.load_questions(amount)

    def admin_menu(self):
        self.ui.display("1. Add a category")
        self.ui.display("2. Remove a category")
        self.ui.display("3. Add a question")
        self.ui.display("4. Load questions from database")
        self.ui.display("5. Get game statistics")
        return self.ui.input("Enter your choice [1-5]: ")

    def admin_statistics(self):
        self.ui.display("1. Correct answers by category")
        self.ui.display("2. Correct answers by difficulty level")
        self.ui.display("3. Users' statistics")
        choice = 4
        while not (choice >= 1 and choice <= 3):
            choice = int(self.ui.input("Please enter your choice [1-3]: "))


    def admin_mode(self):
        menu = self.admin_menu()
        if (menu == 1):
            self.add_category()
        elif (menu == 2):
            self.remove_category()
        elif (menu == 3):
            self.add_question()
        elif (menu == 4):
            self.load_questions()
        elif (menu == 5):
            self.admin_statistics()


    def start_game(self, mode="normal"):
        if (mode == "normal"):
            self.user_mode()
        if (mode == "admin"):
            self.admin_mode()



if (__name__ == "__main__"):
    game = Game("mongo")