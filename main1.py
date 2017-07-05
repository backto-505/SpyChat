from spyDetails import Spy, Chat, FRIENDS, default_spy, STATUS
import sys
from steganography.steganography import Steganography
from termcolor import colored
import chardet

# THESE ARE THE LISTS CONTAINING THE ACCEPTABLE VALUES OF THEIR RESPECTIVE FIELDS
VALID_SALUTATION = ['Mr', 'Ms', 'Mrs']
SPECIAL_WORDS = ['911', 'SOS', 'TIMEOUT']


# FUNCTION TO ADD A STATUS
def add_status(current_status):
    if current_status is None:
        print "\nYou don't have any status set\n"
    else:    # DISPLAY THE CURRENT STATUS MESSAGE
        print "\nYour current status message is: %s\n" % current_status

    ques_status = "Do you want to choose from your older statuses? Y/N "
    ans = raw_input(ques_status)
    while True:  # THIS LOOP WILL TERMINATE ONLY IF USER TYPES Y,N OR BYE
        if ans.upper() == 'Y':
            # DISPLAY THE LIST OF STATUSES
            index = 1
            print "Choose from the displayed list:"
            for status_msg in STATUS:  # LOOP TO PRINT PREVIOUS STATUSES
                print "%d. %s" % (index, status_msg)
                index += 1
            user_choice = int(raw_input())
            while True:
                if (user_choice < index) and (user_choice > 0):
                    updated_status = STATUS[user_choice - 1]
                    break
                else:
                    user_choice = int(raw_input("Invalid. Please choose again: "))
            break   # BREAK FROM THE LOOP TO RETURN UPDATED STATUS
        elif ans.upper() == 'N':
            # ASK FOR THE NEW STATUS TO BE APPENDED AND UPDATED
            new_status = raw_input("Enter the new status: ")
            while True:
                if len(new_status) > 0:  # APPEND ONLY IF NEW STATUS IS NOT BLANK
                    STATUS.append(new_status)
                    updated_status = new_status
                    break
                else:
                    new_status = raw_input("Status cannot be empty.\nEnter the new status: ")
            break  # BREAK FROM THE LOOP TO RETURN UPDATED STATUS
        elif ans.upper() == 'BYE':  # IF THE USER DOES NOT WISH TO UPDATE THEN OLD STATUS WILL BE RETURNED
            return current_status
        else:
            ans = raw_input("Invalid choice. Please type Y or N to continue or type bye to return to main menu: ")
    return updated_status


# FUNCTION TO ADD A NEW FRIEND
def add_friend(spy_rating):

    # INPUTTING THE DETAILS OF THE FRIEND
    friend = Spy('', '', 0, 0.0)
    print "Enter the details of your friend to be added"
    fname = (raw_input("Enter the name of the friend: ")).title()
    fsalutation = (raw_input("Enter the salutation- Mr, Ms or Mrs: ")).title()
    fage = int(raw_input("Enter the age: "))
    frating = float(raw_input("Enter the rating: "))
    if len(fname) > 0 and (fsalutation in VALID_SALUTATION) and fage > 12 and frating >= spy_rating:
        friend.name = fname
        friend.salutation = fsalutation
        friend.age = fage
        friend.rating = frating
        FRIENDS.append(friend)
    else:
        print "Sorry, we could not add your friend."

    return len(FRIENDS)


# FUNCTION TO SEND A SECRET MESSAGE. ENCRYPTION WILL BE PERFORMED HERE
def send_message():

    friend_choice = select_a_friend()
    image = raw_input("Enter the path of the image you want to encode: ")
    output = raw_input("Enter the path of the output image: ")
    secret_msg = raw_input("Enter your secret message: ")
    Steganography.encode(image, output, secret_msg)
    new_chat = Chat(secret_msg, True)  # AN OBJECT OF CLASS CHAT WILL BE CREATED CONTAINING DETAILS ABOUT THE MESSAGE
    FRIENDS[friend_choice].chats.append(new_chat)   # OBJECT APPENDED TO THE LIST OF CHATS OF THE FRIEND SELECTED
    print "\nYour secret message image is ready!\n"


# FUNCTION TO READ THE SECRET MESSAGE
def read_message():
    sender = select_a_friend()
    output = raw_input("Enter the path of the secret message: ")
    secret_text = Steganography.decode(output)  # THIS WILL EXTRACT THE SECRET MESSAGE FROM THE IMAGE

    if is_encoded(secret_text):     # CALLS FUNCTION TO CHECK IF VALID MESSAGE IS RECEIVED
        new_chat = Chat(secret_text, False)     # AN OBJECT OF CHAT CLASS IS CREATED
        FRIENDS[sender].chats.append(new_chat)
        words_in_msg = (len(new_chat.message.split()))

        # AVERAGE WORDS SPOKEN ARE UPDATED
        FRIENDS[sender].average_words_spoken = update_average_words(sender, words_in_msg)
        print "AVERAGE WORDS SPOKEN BY YOUR FRIEND: %s" % FRIENDS[sender].average_words_spoken
        if secret_text in SPECIAL_WORDS:  # CONDITION TO CHECK IF THE SECRET MESSAGE IS A SPECIAL WORD
            display_special_text(secret_text)

        # CONDITION TO CHECK IF THE FRIEND IS SENDING TOO LONG MESSAGES
        if words_in_msg > 100:
            print colored("\nTHIS SPY IS A BIT TALKATIVE. REMOVING FRIEND...\n", 'green')
            remove_a_friend(FRIENDS[sender])

        print "Your secret message has been saved!"
    else:
        print "Sorry! No message could be extracted."  # THIS WILL BE PRINTED IF IMAGE IS NOT ENCRYPTED


# FUNCTION TO READ CHAT HISTORY
def read_chat_history():
    friend_chosen = select_a_friend()
    for chat in FRIENDS[friend_chosen].chats:
        time_color = colored(chat.time, 'blue')  # THIS COLORS THE CHAT TIME IN BLUE
        spy_color = colored('You', 'red')  # THIS COLORS THE USER(YOU) IN RED
        # COLORING THE FRIEND'S NAME IN RED
        spy_friend = colored((FRIENDS[friend_chosen].salutation + " " + FRIENDS[friend_chosen].name), 'red')
        if chat.sent_by_me:
            print '[%s] %s: %s' % (time_color, spy_color, chat.message)
        else:
            print '[%s] %s: %s' % (time_color, spy_friend, chat.message)


# FUNCTION TO SELECT A FRIEND FROM A LIST OF FRIENDS
def select_a_friend():
    index = 0
    for friend in FRIENDS:
        print '%d. %s %s aged %d with rating %.2f is online' \
              % (index + 1, friend.salutation, friend.name, friend.age,  friend.rating)
        index += 1
    while True:     # THIS LOOP WILL ONLY TERMINATE IF A VALID INDEX IS CHOSEN FROM THE LIST OF FRIENDS DISPLAYED
        friend_choice = raw_input("\nChoose from your friends: ")
        friend_choice_position = int(friend_choice) - 1
        if friend_choice_position > len(FRIENDS) - 1:
            print "Invalid."
            continue
        return friend_choice_position


# FUNCTION TO REMOVE A FRIEND FROM THE LIST OF FRIENDS OF THE SPY AND DISPLAY TOTAL NUMBER OF FRIENDS
def remove_a_friend(friend):
    FRIENDS.remove(friend)
    print "Total number of friends you have now is: %s" % (len(FRIENDS))


# FUNCTION TO DISPLAY THE SPECIAL MESSAGES CORRESPONDING TO THE SPECIAL WORDS SENT
def display_special_text(msg):
    print "\nHEY THERE IS A SPECIAL MESSAGE:"
    if msg == '911':
        print colored("\n911! Your friend needs you to call them!\n", 'green')
    elif msg == 'SOS':
        print colored("\nSOS! Your fellow spy is lonely! Make sure to assist them in their mission :)\n", 'green')
    elif msg == 'TIMEOUT':
        print colored("\nTIMEOUT! Your friend needs a snack break. They'll be back soon!\n", 'green')


# FUNCTION TO CHECK WHETHER OR NOT THE IMAGE HAS BEEN ENCRYPTED
def is_encoded(text):
    if chardet.detect(text)['encoding'] == 'ascii' and len(text) > 0:  # THIS WILL ALSO ENSURE THAT MESSAGE ISN'T BLANK
        return True
    else:
        return False


# FUNCTION TO UPDATE THE AVERAGE WORDS SPOKEN BY A SPY
def update_average_words(sender, words):
    words_spoken = FRIENDS[sender].average_words_spoken
    if words_spoken > 0:
        return (FRIENDS[sender].average_words_spoken + words) / 2
    else:
        return words


# FUNCTION TO START THE CHAT THAT TAKES OBJECT OF CLASS SPY AS PARAMETER
def start_chat(spy):
    opt = 1
    print colored("Welcome to Spy Chat, " + spy.salutation + " " + spy.name + "\nHere are you details:", 'blue')
    print colored("You are %s years old with a spy rating of %s" % (spy.age, spy.rating), 'blue')
    menu = colored("\n--MAIN MENU--\n", 'blue')
    # VARIOUS OPERATIONS THAT A USER CAN CHOOSE TO PERFORM
    menu_options = "1) Add a status update\n2) Add a friend\n3) Send a secret message\n" \
        "4) Read a secret message\n5) Read chats from a user\n6) Quit"

    while opt == 1:     # LOOP TO DISPLAY MAIN MENU
        spy_choice = raw_input(menu + menu_options + "\nEnter your choice: ")
        if len(spy_choice) == 0:
            print "Invalid choice. Choose again"
            continue
        spy_choice = int(spy_choice)
        if spy_choice == 1:
            print colored("--ADD STATUS--", 'blue')
            spy.current_status = add_status(spy.current_status)
            print "YOUR STATUS IS SET TO: %s " % spy.current_status
        elif spy_choice == 2:
            print colored("--ADD A FRIEND--", 'blue')
            no_of_friends = add_friend(spy.rating)
            print "Total number of friends you have is: %s" % no_of_friends
        elif spy_choice == 3:
            print colored("--SEND A SECRET MESSAGE--", 'blue')
            send_message()
        elif spy_choice == 4:
            print colored("--READ A SECRET MESSAGE--", 'blue')
            read_message()
        elif spy_choice == 5:
            print colored("--READ CHAT HISTORY--", 'blue')
            read_chat_history()
        elif spy_choice == 6:
            print colored("Thankyou to choosing Spy Chat! See you soon", 'blue')
            sys.exit()  # TO TERMINATE THE PROGRAM
        else:
            print "Invalid choice, Please choose from the menu provided."
        opt = int(raw_input("\nTO GO TO MAIN MENU, PRESS 1: "))


# FUNCTION TO CREATE A NEW SPY
def create_new_spy():

    spy = Spy('', '', 0, 0.0)    # INITIALIZING OBJECT OF CLASS SPY
    print "Welcome new user! Please fill in your details "
    spy_name = raw_input("Enter your name: ")

    while True:     # THIS LOOP IS USED TO TAKE DETAILS ABOUT THE USER. IT WILL TERMINATE ONLY IF VALID NAME IS ENTERED
        if len(spy_name) != 0:
            spy.name = spy_name.title()  # NAME WILL ALWAYS BEGIN WITH A CAPITAL LETTER
            print "\nHello " + spy.name + "\n"
            spy_salutation = raw_input("Should we refer to you as Mr, Ms or Mrs? ")

            while True:     # THIS LOOP WILL TERMINATE ONLY IF VALID SALUTATION IS ENTERED
                if spy_salutation.title() in VALID_SALUTATION:   # TO CHECK FOR VALID SALUTATION
                    spy.salutation = spy_salutation.title()
                    print "Alright " + spy.salutation + " " + spy.name + "! Let's get to know you better."
                    spy_age = int(raw_input("Enter your age: "))
                    if (spy_age > 12) and (spy_age < 50):   # TO CHECK IF SPY IS IN VALID AGE RANGE
                        spy.age = spy_age
                        spy_rating = float(raw_input("Enter your spy rating between 0 to 5: "))

                        while True:  # THIS LOOP WILL TERMINATE ONLY IF A VALID SPY RATING IS ENTERED
                            if (spy_rating >= 0) and (spy_rating <= 5):
                                spy.rating = spy_rating
                                print "Your rating is %s. We have a message for you: " % spy_rating
                                if spy_rating >= 4.5:
                                    print "YOU'RE ONE OF THE GOOD ONES!"
                                elif (spy_rating < 4.5) and (spy_rating >= 3):
                                    print "YOU CAN DO BETTER"
                                elif (spy_rating < 3) and (spy_rating >= 2.5):
                                    print "THERE IS ALWAYS SOME ROOM FOR IMPROVEMENT!"
                                else:
                                    print "DON'T WORRY, WE WILL TRAIN YOU!"
                                spy.is_online = True     # THE SPY IS NOW ONLINE
                                break
                            else:
                                spy_rating = float(raw_input("Invalid rating. Enter your spy rating between 0 to 5: "))
                        break
                    else:
                        print "Sorry, your age is not appropriate to be a spy."
                        sys.exit()   # IF THE AGE IS NOT APPROPRIATE THEN THE PROGRAM WILL TERMINATE
                else:
                    spy_salutation = raw_input("Invalid Salutation. Should we refer to you as Ms, Mr or Mrs? ")
            break
        else:
            spy_name = raw_input("Invalid name. Please enter a valid spy name: ")
    return spy      # FINALLY THE COMPLETE OBJECT CONTAINING INFO OF THE USER IS RETURNED

print "Hello! Let's get started"
question = "\nDo you want to continue as "+default_spy.salutation+" "+default_spy.name+"? (Y/N): "
answer = raw_input(question)
validation = ''
while True:  # LOOP TO CHECK IF NEW USER IS TO BE MADE
    if answer.upper() == 'Y':
        start_chat(default_spy)
        break
    elif answer.upper() == 'N':
        # ASK FOR THE DETAILS OF THE NEW USER
        new_member = create_new_spy()
        start_chat(new_member)
        break
    elif answer.upper() == 'BYE':
        sys.exit()
    else:
        answer = raw_input("Invalid choice. Please type Y or N to continue or type bye to exit: ")