import click
import random
import sys
from typing import List

@click.command()
@click.option('--number_of_digits', default=4, help='enter number of digits', type=int)
def play(number_of_digits: int):
    """
    Click cmd line tool to determine number of digits in the number you are guessing for Pico Fermi Bagel
    Ex: python picofermibagel.py --number_of_digits 5
    """
    intro_string = """
    This is a python implementation of the classic number guessing game Pico
    Permi Bagel. The player tries to guess what number the computer is thinking
    of. A F (Fermi) means the digit is in the right place. A P (Pico) means the
    digit is in the number but in the wrong place. A B (Bagel) means the digit
    is not in the number. Example: Computer's number = 1234, Player guesses
    4278. The player's guess is a P, F, B, B. The default number of digits is
    4. Up the difficulty by playing with more digits ex: python
    picofermibagel.py --number_of_digits 5
    """
    print(intro_string)
    win = False
    while not win:
      win = pfb(number_of_digits)
    exit_condition = True
    while exit_condition:
        play_again = input("Play Again? (Y/N): ")
        print(play_again)
        valid_yes_answers = ['Yes', 'yes', 'y', 'Y']
        valid_no_answers = ['No', 'no', 'n', 'N']
        if play_again not in valid_yes_answers and play_again not in valid_no_answers:
            print("Not a valid entry! Try running the script again!")
            sys.exit()
        elif play_again in valid_yes_answers:
            new_digits = input(f"Enter the number of digits you want to play with: ")
            valid = int_check(new_digits)
            if valid:
                print(int(new_digits))
                pfb(int(new_digits))
        else:
            print("Thanks for playing!")
            sys.exit()

def pfb(number_of_digits: int):
    """
    main logic runs the pico fermi bagel game
    :param number_of_digits: numbero of digits to play with
    :return:
    """
    computer_number = create_computer_number(number_of_digits)
    digit_valid = True
    int_valid = True
    guessing = True
    while guessing:
        guess = input(f"Enter a {number_of_digits} digit number: ")
        print(guess)
        digit_valid = digit_check(guess, number_of_digits)
        int_valid = int_check(guess)
        while digit_valid and int_valid:
            pfb = evaluate_guess(guess, number_of_digits, computer_number)
            guessing = win_condition(pfb)
            digit_valid = False
            int_valid = False
    winner = True
    print(f"Congratualtions {computer_number} is the computer's number!")
    return winner

def digit_check(guess: int, number_of_digits: int):
    """
    Checks that user input is a valid guess
    :param guess: what the user guess is
    :param number_of_digits: what the number of digits in the guess is
    :return:
    """
    if len(guess) != number_of_digits:
        print("Guesses must have consistent number of digits")
        return False
    else:
        return True


def int_check(input: int):
    """
    helper function to check if input is an integer
    :param input:
    :return:
    """
    try:
        int(input)
        return True
    except ValueError:
        print(f"Invalid input {input} please enter a whole number")
        return False

def create_computer_number(number_of_digits: int):
    """
    Creates the computer's number for the player to guess
    :param number_of_digits: Number of digits the player has chosen
    :return:
    """
    lower_bound = '1'
    upper_bound = '9'
    for digits in range(1,number_of_digits):
        lower_bound = lower_bound + '0'
        upper_bound = upper_bound + '9'
    computer_number = random.randint(int(lower_bound), int(upper_bound))
    return computer_number

def evaluate_guess(guess: int, number_of_digits: int, computer_guess: int):
    """
    Evaluate the player's guess using the rules of Pico Fermi Bagel. The goal is to guess the number the computer is
    thinking of. On every guess the computer will return a Pico, Fermi, of Bagel for each number in a player's guess
    Pico = If a digit in the player's guess is in the computer's number but in the wrong place P
    Fermi = The digit in the player's guess is in the computer's number and in the right place F
    Bagel = The digit in the player's guess is NOT in the computer's number
    Example: Computers number is 1234
    Player Guesses 1542
    Computer returns FBPP A Fermi, Bagel, Pico, Pico
    :param guess:
    :param number_of_digits:
    :return:
    """
    computer_guess_list = [digit for digit in str(computer_guess)]
    user_guess = [digit for digit in str(guess)]
    same_place = ['F' if x == y else y for x, y in zip(computer_guess_list, user_guess)]
    fermi_bagel = ['B' if pfb not in computer_guess_list and pfb != 'F' else pfb for pfb in same_place]
    pico_fermi_bagel = ['P' if pfb in computer_guess_list and pfb != 'F' else pfb for pfb in fermi_bagel]
    print(pico_fermi_bagel)
    return pico_fermi_bagel

def win_condition(pico_fermi_bagel: List[str]):
    """
    Returns True if all F's (Fermis are returned) returns false for any other condition
    :param pico_fermi_bagel:
    :return:
    """
    return not all(i == 'F' for i in pico_fermi_bagel)


if __name__ == '__main__':
    play()

