#from PyDictionary import PyDictionary
import enchant
import json
import string
import random as rand
from math import ceil, floor


d = enchant.Dict("en_UK")
file = open("dictionary.json")
data = json.load(file)
#print(len(data))
data = list(data.keys())


def which_letter(data, already_guessed, letters):
    half = floor(0.5*len(data))
    #print(data)
    #print(half)
    tempo = letters
    for i in data:
        for j in list(set(i)):
            if j not in already_guessed:    
                tempo[j] += 1
    lst = list(tempo.keys())
    #print(lst)
    #print(tempo)
    temp = min(tempo, key=lambda x: abs(tempo[x] - half))
    #print(temp)
    return temp


def sort_data(cho, places, data, num, to_do):

    if to_do == "use_letters":
        new_data = []
        for j in data:
            res = [i for i in range(len(j)) if j.startswith(cho, i)]
            if res == places:
                new_data.append(j)
        data = new_data
    else:
        char_list = [cho]
        data = [ele for ele in data if all(ch not in ele for ch in char_list)]
    #print(len(data))
    return data



def guess_word(ray, cho, places):
    if ray ==[]:
        guessing = [" " for i in range(0, num)]
        return guessing
    else:
        for i in places:
            ray[i] = cho
        return ray
    
def generate_spaces(guessing):
    #print()
    for i in range(0, num):
        print(" "+spaces[i], end="  ")
    print()
    for i in range(0, num):
        print("|"+guessing[i]+"|", end=" ")
    print()
    for i in range(0, num):
        print(" "+str(i+1), end="  ")
        
    return num
def start_hangman(guessing, data, num):
    prime=True
    count = 9
    already_guessed = []
    letters = dict.fromkeys(string.ascii_lowercase, 0)
    letters["-"] = 0
    while prime:
        letters = dict.fromkeys(letters, 0)
        max_let = which_letter(data, already_guessed, letters)
        #cho = rand.choice(list(letters.items()))[0]
        cho = max_let
        verify = str(input("Is " + cho + " in your word?(y/n)"))
        already_guessed.append(cho)
        while verify.lower() != "y" and verify.lower() != "n":
            verify = str(input("Is " + cho + " in your word?(y/n)"))
            
        if verify == "y":
            ask_place = str(input("At what place/s?\nSeparate with commas: "))
        
            if " " in list(ask_place):
                places= ask_place.split(", ")
            else:
                places = ask_place.split(",")
            for i in range(0, len(places)):
                places[i] = int(places[i]) -1
            
            guessing = guess_word(guessing, cho, places)
            del letters[cho]
            data = sort_data(cho, places, data, num, to_do="use_letters")
            #print(data)
            generate_spaces(guessing)
            print()
        else:
            generate_spaces(guessing)
            del letters[cho]
            data = sort_data(cho, None, data, num, to_do="del_letters")
            print()
            count -= 1
            
        for w in data:
            if d.check(w) == False:
                data.remove(w)
        #print(data)
        #print(len(data))
        if len(data) == 1:
            #print(list(data[0]))
            guessing = list(data[0])
            generate_spaces(guessing)
            print()
            print("Your word is " + data[0].upper()+"!")
            prime=False
        else:
            if count == 1:
                print(str(count) + " chance left!")
            else:
                print(str(count) + " chance left!")
            
            if " " in guessing and count == 0:
                print("Failed!")
                print("Words left: ", end="")
                for i in data:
                    print(i+", ", end="")
                prime=False


num = int(input("Enter length of word: "))
start_data = []
for i in data:
    if len(i)==num:
        start_data.append(i)
data = start_data
spaces = ["_" for i in range(0, num)]

guessing = guess_word([], None, None)
    
generate_spaces(guessing)
print()
start_hangman(guessing, data, num)
