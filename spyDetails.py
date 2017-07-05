import datetime


# CLASS SPY USED TO DEFINE THE BASIC STRUCTURE OF A SPY OR USER/FRIEND
class Spy:
    def __init__(self, name, salutation, age, rating):
        self.name = name
        self.salutation = salutation
        self.age = age
        self.rating = rating
        self.is_online = True
        self.chats = []
        self.current_status = None
        self.average_words_spoken = 0.0


# CLASS CHAT USED TO DEFINE THE STRUCTURE OF THE CHAT MESSAGES THAT WILL BE EXCHANGED BETWEEN USERS
class Chat:
    def __init__(self, message, sent_by_me):
        self.message = message
        self.time = datetime.datetime.now().strftime("%c")
        self.sent_by_me = sent_by_me

# CREATING OBJECTS OF SPY CLASS
default_spy = Spy("OutwitYou", "Mr", 25, 3.0)
default_f1=Spy("Aanchal", "Ms", 20, 4.5)
default_f2=Spy("Sam", "Mr" ,23, 4.6)


# FRIENDS IS A LIST CONTAINING THE FRIENDS OF THE USER
FRIENDS=[default_f1, default_f2]
STATUS = ["Available for mission", "Come back with your shield, or on it", "SKADOOSH!"]