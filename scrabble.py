# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, "*": 0, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    
    first_component = sum([SCRABBLE_LETTER_VALUES.get(i, 0) for i in word])
    second_component = max(1, 7*len(word)-3*(n-len(word)))
    
    return first_component + second_component

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
        
    hand["*"] = 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.
    
    Has no side effects: does not modify hand.
    
    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    
    temp = dict(hand)
    for i in range(len(word)):
        temp[word[i]] = temp.get(word[i], 0) - 1
        
    temp = {key:val for key, val in temp.items() if val > 0}
            
    return temp 
            
        
        
    
    
    
    pass  # TO DO... Remove this line when you implement this function

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    temp = hand.copy()
                
                
    if "*" in word: 
        for candidate in word_list: 
            index = word.find("*")
            if "".join(list(word).pop(index)) == "".join(list(candidate).pop(index)) and candidate[index] in VOWELS:
                break 
            else: 
                return False 
                    
                            
    
    if word in word_list: 
        for i in range(len(word)):
            temp[word[i]] = temp.get(word[i], 0) - 1
    else: 
        return False 
    
    for i in temp.keys(): 
        if i<0: 
            return False 
    
    return True 


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    return len(hand)

def play_hand(hand, word_list):

    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    Total_score = 0 
    # As long as there are still letters left in the hand:
    while calculate_handlen(hand)>0: 
        # Display the hand
        print("Current Hand: ")
        display_hand(hand)
        
        # Ask user for input
        user_input = input("Enter word, or '!!' to indicate that you are finished:")
        
        # If the input is two exclamation points:
        if user_input == "!!":
            # End the game (break out of the loop)
            break
        # Otherwise (the input is not two exclamation points):
        else:
            if is_valid_word(user_input, hand, word_list):

            # If the word is valid:
                # Tell the user how many points the word earned,
                points = get_word_score(user_input, calculate_handlen(hand))
                print(user_input + " earned "+points)
            
                # and the updated total score
                Total_score += points
                print("Total: "+Total_score)

            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("That is not a valid word. Please choose another word.")
            # update the user's hand by removing the letters of their inputted word
            update_hand(hand, user_input)

    # Game is over (user entered '!!' or ran out of letters),
    print("Game is over")
    
    # so tell user the total score
    print("Your total score is " + str(Total_score))

    # Return the total score as result of function
    return Total_score



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
    #total pool of letters
    total_letters = VOWELS + CONSONANTS
    
    #generate random letter from total_letters
    random_letter = random.choice(total_letters)
    
    #add this letter to the current hand 
    hand[random_letter] = hand[letter]
    
    #delete letter of choice from hand 
    del hand[letter]
    
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    #global variable
        #final_score = 0 
        
    final_score = 0 
    
    #ask user how many number of hands they want to play 
    
    user_input = input("Enter total number of hands: ")
    
    #while number of hands to play...
    
    while int(user_input)>0: 
        
        #deal hand
        hand = deal_hand(7)
    
        #show them current hand; display_hand()
        print("Current hand: ")
        display_hand(hand)
        
        #if ask user if he wants to subsitute hands
        sub = input("Would you like to substitute a letter?")
        if sub.lower() == "yes": 
            
            letter = input("Which letter would you like to replace: ")
            
            #substitute_hand() 
            substitute_hand(hand, letter)
        
        #play_hand()
        firstgame = play_hand(hand, word_list)
        
        
        #if he would like to replay the hand
        again = input("Would you like to replay the hand?")
        if again.lower() == "yes": 
            secondgame = play_hand(hand, word_list)
        else: 
            secondgame = 0 
            
        #update score 
        final_score += max(firstgame, secondgame)
        
        print("Total score for this hand: " + max(firstgame, secondgame))
        
    print("Total score over all hands: " + final_score)
            


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
