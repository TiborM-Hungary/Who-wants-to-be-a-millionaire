#######################################################################################################
# Author:       TiborM-Hungary                                                                        #
# Date:         March 2020                                                                            #
# Description:  ConsoleProgram in Python - based on the Who want to be a millionaire game             #
#######################################################################################################


import Questions
import random
import time
import sys

# Funkciók

def waiting_a_bit(szoveg, i):
    """ Write out dots when waiting, little visual effect """
    print("\n\n {}".format(szoveg))
    for i in range(i):
        print(".", flush=True)
        time.sleep(1)
        sys.stdout.flush()

def initial_question(level):
    """ Progressing with the dialogue"""
    level += 1
    balance = game_money_level[level - 1]
    v = [0 for i in range(9)]
    v[0] = "Let's go with question from level %s, which iw worth %s HUFs." % (level, balance)
    v[1] = "Let's continue with level %s, for %s HUFs." % (level, balance)
    v[2] = "The %s question is next, for %s HUFs." % (level, balance)
    v[3] = "We are in round %s, the correct answers worth %s HUFs." % (level, balance)
    v[4] = "Round %s is upon us for %s HUFs." % (level, balance)
    v[5] = "Would you like to go home with %s HUFs? Let's see question number %s !" % (balance, level)
    v[6] = "Let's see how much time do you need for question %s, which goes for %s HUFs." % (level, balance)
    v[7] = "The next level is the %s, for %s HUFs!" % (level, balance)
    v[8] = "Would you like to win %s HUFs? Let's go for question %s!" % (balance, level)
    n = int (random.random() * 9)
    return v[n]

def ask_the_question(level):
    """ Call a random question from Questions.py """
    # Save the question
    # Based on the length of the question draw a line
    returned_question = "\n " + initial_question(level) + "\n "
    returned_question += "=" * (len(returned_question) - 3) + "\n "
    # Mechanics of random_question:
    # random.random()
    # Return the next random floating point number in the range [0.0, 1.0).
    # 1.0 nem veszélyes, mert már nem része a range-nek
    # int cast lekerekíti
    question_number = int (random.random() * 10)

    global question
    question = Questions.get_question(level, question_number)
    returned_question += question[0]
    returned_question += "\n A. " + question[1] + "\t\t B. " + question[2]
    returned_question += "\n C. " + question[3] + "\t\t D. " + question[4]

    global correct_answer
    correct_answer = question[5]
    return returned_question

def check_answer(level):
    """ Checking the question; main flow of the program"""

    answer = input("\n Your answer is: --> ")
    answer = answer.lower()
    global correct_answer, question, lifeline_friend, lifeline_50_50, lifeline_audience

    # Let's check, if the answer is correct

    if not (answer in acceptable_answers):
        print("\nI am not what you are thinking Mr./Ms. {}. Please select a letter between 'a' and 'd', "
              "or the 'help' word, maybe the 'end' word in order to exit".format(player))
        check_answer(level)

    # In case lifeline is called
    # Looping through the lifelines

    elif (answer == "help"):
        print("")
        if (lifeline_50_50): print(" " * 5 + lifeline_lets_go_50_50)
        if (lifeline_50_50): print(" " * 5 + lifeline_call_friend)
        if (lifeline_audience):  print(" " * 5 + lifeline_ask_audience)
        if not (lifeline_50_50 or lifeline_friend or lifeline_audience):
            print("\n" + " " * 5 + "I am sorry Mr./Ms. {}, you don't have any more lifelines left.".format(player))
        check_answer(level)

    elif (answer == "friend"):
        if (lifeline_friend):
            lifeline_friend = False
            friend = input("How may I address your friend?: --> ")
            if (random.random() < 1): # just to make sure to get a good input
                print("Greetings Mr./Ms. {}!".format(friend))
                waiting_a_bit("I am calling because your friend is looking for an answer for a question...", 4)
                print("\n Your friend, Mr./Ms. {} is a great person, the answer according to him/her is {}.".format(friend, correct_answer))
                check_answer(level)

        else:
            print("\nYou already used this lifeline, please type in 'help' to see what is available.")
            check_answer(level)

    elif (answer == "50-50"):
        if (lifeline_50_50):
            lifeline_50_50 = False
            removed_answers = 0 # track the ID of the removed answers
            while True:
                if removed_answers == 2:
                    break
                i = int (random.random()*4 + 1)
                # if the answers is removed or the correct, I can't remove it!
                # I overwrite it with ""
                if (correct_answer != question[i] and question[i] != ""):

                    removed_answers += 1
                    question[i] = ""


            print("\nWe remove 2 incorrect answers, the remaining are::")
            temp = [" A. ", " B. ", " C. ", " D. "]

            for i in range(1,5):
                if (question[i] != ""):
                    print(temp[i-1] + question[i] + "\t\t")
            print("")
            check_answer(level)

        else:
            print("\nYou already used this lifeline, please type in 'help' to see what is available.")
            check_answer()

    elif (answer == "audience"):

        if (lifeline_audience):
            lifeline_audience = False
            while True: # Generate a decent random number about the % of audience voted for the option
                audience_correct_portion = random.random()
                if (audience_correct_portion > 0.45):
                    audience_correct_portion = int(audience_correct_portion*100)
                    break

            if (random.random() < 0.8):
                audience_answer = correct_answer

            else: # In case the answer was eliminated in the 50-50 lifeline
                while True:
                    i = int(random.random()*4 + 1)
                    if (answer[i] != ""):
                        audience_answer = question[i]
                        break

            waiting_a_bit("The audience is voting, one moment please.", 4)
            print("\nThe majority of the audience which is ({}%), voted for {}.".format(audience_correct_portion, audience_answer))
            check_answer(level)

        else:
            print("\nYou already used this lifeline, please type in 'help' to see what is available.")
            check_answer(level)

    elif (answer == "end"):
        print("\nYou have chosen to end the game, {}. The reward is {}. Congratulations!".format(player, game_money_level[level]))
        quit()

    elif (answer == "a" or answer == "b" or answer == "c" or answer == "d"):

    # Check the correct answers, also checking in the answers index is correct
    # does it match?  answer["value of the letter and the matching index element"] with answer[5] item index, which is the correct answer

    #   print(ord('a'))    # 97-96              -->    answer[1]
    #   print(ord('b'))    # 98-96              -->    answer[2]
    #   print(ord('c'))    # 99-96              -->    answer[3]
    #   print(ord('d'))    # 100-96             -->    answer[4]
    #   correct answer is always answer[5]      -->    answer[5]

    # answer[1] == answer[5],  "a" is correct, else, sorry, wrong answer

        if (correct_answer == question[ord(answer) - 96]):
            if (level == 14):
                print(" **********           Congratulations, {}!          *************".format(player.upper()))
                print(" **********    You won the 50 000 000 HUFs!         *************")
                print(" **********        Thank you for playing!           *************")
            else:
                print("\n The correct answer is {}!\n You already have {} HUFs.\n Let's go on to question {}!".format(player, game_money_level[level + 1], level + 2))
                print(ask_the_question(level + 1))
                check_answer(level + 1)

        else:
            print("\n Opps, incorrect answer.\n The correct answer is:%s.", correct_answer)
            print(" Thank you for playing!")

            player_decision_continue_or_not = input("\n\n Would you like to go on? (y/n)  ")
            if (player_decision_continue_or_not.lower() == "y"):
                lifeline_audience = True
                lifeline_50_50 = True
                lifeline_friend = True
                print (ask_the_question(0))
                check_answer(0)

# Main program

game_money_level = [10000, 20000, 50000, 100000, 250000, 500000, 750000, 1000000, 15000000, 2000000, 5000000, 10000000, 15000000, 25000000, 50000000]
level = 0   # level we are on
correct_answer = ""
question = []
acceptable_answers = ["a", "b", "c", "d", "50", "help", "50-50", "audience", "friend", "end"]
lifeline_lets_go_50_50 = "\"To select the\" \"50:50 chance\",type in '50-50'"
lifeline_50_50 = True
lifeline_call_friend = "\"To call a friend\",type in 'friend'."
lifeline_friend = True
lifeline_ask_audience = "\"For the audience\",type in 'audience'"
lifeline_audience = True

print (" *********************************************************")
print (" *         //          Welcome to the               \\\  *")
print (" *         ||     WHO WANTS TO BE A MILLIONAIRE      ||  *")
print (" *         \\\              game                     //  *")
print (" *********************************************************\n")

print (" Welcome to the show \"Let's be a millionaire!\"\n")
player = input(" How may I call you? ---> ")

print ("\n Let's get started Mr./Ms %s! \n\
 You will get 15 questions, each harder than the prior one. \n\
 We start with the easy one for less money.  \n\
 Each question has 4 possible answers, only 1 correct. \n\
 If you answer the 15th question, you get 50 000 000 HUFs! \n\n\
 Please remember, you have 3 lifelines:\n\
      %s\n\
      %s\n\
      %s\n\n\
 You can access them anytime with 'help' keyword.\n\n\""
 " Let's begin!\n"
       % (player, lifeline_lets_go_50_50, lifeline_call_friend, lifeline_ask_audience))

print (ask_the_question(0))
check_answer(0)