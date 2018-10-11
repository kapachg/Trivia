from Database import Database
from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd

class MongoDb(Database):

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.TriviaDB
        self.questions = self.db.questions

    def load_questions(self, amount=10, category=None, difficulty=None, type=None):
        data = super().load_questions(amount, category, difficulty, type)
        self.questions.insert_many(data)

    def get_question(self, category, difficulty, size):

        question = self.db.questions.aggregate([
#            {"$sample" : {"size" : size}},
            {"$match" : {"category" : category, "difficulty" : difficulty}},
            {"$sample": {"size": int(size)}}
#            ,{"$project" : {"_id": 0, "title": 1}}
            ]
        )

# REMOVE IT
#        oid = ObjectId("5bbdbcef8be1541d5c28d2c6")
#        question = self.db.questions.find_one({"_id": oid})
#        print([question])
#        return [question]
        return list(question)#.next()

    def update_db(self, id, user, answer):
        oid = ObjectId(id)
        self.db.questions.update_one({"_id": oid}, {"$addToSet" : {"user_answers" : {user : str(answer)}}})

    def add_question(self, question):
        self.db.questions.insert_one(question)

    def remove_duplicates(self):
        pass



if (__name__ == "__main__"):
    mongo = MongoDb()
    mongo.load_questions()
    q = pd.DataFrame(mongo.get_question("Mythology", "medium", 800))

    print(len(q))
#    for i in range(len(q)):
#         print(q.iloc[i])
    # print()
#    for i in q:
 #       print(i)
#    for i in range(10):
 #       q = mongo.get_question("Mythology", "medium", 2)
  #      print(*q)