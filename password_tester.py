## Here lies my password strength tester scripted in Python
## It checks for length, character variety, common passwords, sequences, and repeated characters to determine the strength of a users password.

import hashlib
import urllib.request


## Sequence is being used to check for common patterns in passwords, like 'abcd' or '1234' The leet dictionary is used to check for common substitutions in passwords, like '4' for 'a' or '3' for 'e'.

SEQUENCES = ["abcdefghijklmnopqrstuvwxyz", "0123456789", "qwertyuiop", "asdfghjkl", "zxcvbnm"]
LEET = { "@": "a", "4": "a", "3": "e", "1": "i", "!": "i", "0": "o", "$": "s", "5": "s", "+": "t", "7": "t" }
LEET["@"]


## check_length function checks the length of the password and returns a score based on its length. The scoring is as follows:
## Less than 8 characters: 0 points
## 8-11 characters: 1 point
## 12-15 characters: 2 points
## 16 or more characters: 3 points
def check_length(password):
    length = len(password)

    if length < 8:
        return 0
    elif length >= 8 and length <=11:
        return 1
    elif length >= 12 and length <= 15:
        return 2
    elif length >= 16: 
        return 3

## check_characters function checks for the presence of lowercase letters, uppercase letters, digits, and special characters in the password. It returns a score based on the number of character types present, as well as boolean values indicating the presence of each character type. The scoring is as follows:
## 1 point for each character type present (lowercase, uppercase, digit, special character

def check_characters(password):
    has_lower  = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    points = 0

    if has_lower:
        points += 1
    if has_upper:
        points += 1
    if has_digit:
        points += 1
    if has_special:
        points += 1

    return points, has_lower, has_upper, has_digit, has_special


## load_common_passwords function loads a list of common passwords from a file called "common_password.txt" and returns a set of those passwords. The function reads each line of the file, strips any whitespace, and adds the password to the set. If an empty line is encountered, it also adds an empty string to the set.

def load_common_passwords():
    common = set()
    with open("common_passwords.txt") as f:
        for line in f:
            common.add(line.strip())
            if line.strip() == "":
                common.add(line.strip())


          
          
    return common

## undo_leet function takes a password as input and replaces any leet characters (e.g., "4" for "a", "3" for "e") with their corresponding letters. It returns the modified password.

def undo_leet(password):
    result = ""
    for c in password.lower():
        if c in LEET:
            result += LEET[c]
            
        else:
            result += c
            
    return result

## check_common function checks if a password is common or contains common words. It takes a password and a set of common passwords as input. It returns two boolean values: is_common True if the password is in the common set and has_common_word True if the password contains any common words of length 4 or more after undoing leet substitutions).

def check_commmon(password, common):
    is_common = password.lower() in common

    normalized = undo_leet(password)
    has_common_word = False
    for word in common:
       if len(word) >= 4 and word in normalized:
           has_common_word = True
           

    return is_common, has_common_word

## has_sequences function checks if a password contains any sequences of characters (e.g., "abcd", "1234") from the predefined SEQUENCES list. It returns True if a sequence is found, and False otherwise.

def has_sequences(password):
    lower = password.lower()
    for seq in SEQUENCES:
        for s in [seq, seq[::-1]]:
            for i in range(len(s) - 3):
                window = s[i:i+4]
                if window in lower:
                    return True
    return False

## has_repeats function checks if a password contains any repeated characters (e.g., "aaa", "111"). It returns True if a repeat is found, and False otherwise.

def has_repeats(password):
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            return True
    return False

## calculating_rating function calculates the overall strength score and rating of a password based on various factors. It takes the password, length points, character points, sequence presence, repeat presence, common password status, and common word status as input. It returns the final score and rating as a string.

def calculating_rating(password, length_points, char_points, sequence, repeats, is_common, has_common_word, breach_count):
    strength = length_points + char_points

    if sequence:
        strength -= 1
    if repeats:
        strength -= 1
    if is_common or has_common_word:
        strength -= 2

    score = max(strength, 0)

    if is_common or len(password) < 8 or breach_count is not None and breach_count > 0:
        rating = "Weak"
    elif score <= 3: 
        rating = "Weak"
    elif score <= 5:
        rating = "Moderate"
    else:
        rating = "Strong"

    return score, rating





def hash_password(password):
        """SHA-1 the password, return (prefix, suffix) as 5 and 35 uppercase hex chars."""
        password_bytes = password.encode("utf-8")
        hex_digest = hashlib.sha1(password_bytes).hexdigest().upper()
        return hex_digest[:5], hex_digest[5:]

def fetch_breach_list(prefix):
    """Ask Have I been Pwned for every breached has starting with prefix. Return raw text"""
    url = "https://api.pwnedpasswords.com/range/" + prefix
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")
        
def check_breach(password):
    """How many times this password appeared in known breaches."""
    prefix, suffix = hash_password(password)
    try:
        text = fetch_breach_list(prefix)
    except Exception:
        return None

    for line in text.splitlines():
        line_suffix, count = line.split(":")
        if suffix == line_suffix:
            return int(count)

    return 0






## main function serves as the entry point of the program. It loads the common passwords, prompts the user to enter a password for testing, and displays the results of the password strength analysis. The user can continue testing passwords until they choose to quit by entering 'q'.


def main():
    common = load_common_passwords()
    print("PASSWORD STRENGTH TESTER\nStrength is rated on a scale of 0-7, with 7 being the strongest.")

    while True:
        password = input("Enter a password to test (or 'q' to quit): ")
        if password.lower() == "q":
            break
        if password == "":
          continue

        length_points = check_length(password)
        char_points, has_lower, has_upper, has_digit, has_special = check_characters(password)
        is_common, has_common_word = check_commmon(password, common)
        sequence = has_sequences(password)
        repeats = has_repeats(password)
        breach_count = check_breach(password)
        score, rating = calculating_rating(password, length_points, char_points, sequence, repeats, is_common, has_common_word, breach_count)

        print("=" * 50)
        print(f"Password: {password}")
        print(f"Length: {len(password)} characters")
        print("-" * 50)
        print("Lowercase letter .......)", "PASS" if has_lower else "FAIL")
        print("Uppercase letter .......", "PASS" if has_upper else "FAIL")
        print("Number ..................", "PASS" if has_digit else "FAIL")
        print("Special character .......", "PASS" if has_special else "FAIL")
        print("Not a common password ...", "PASS" if not is_common else "FAIL")
        print("No repeated characters .......", "PASS" if not repeats else "FAIL")
        print("No sequences .......", "PASS" if not sequence else "FAIL")
        print("No common words .......", "PASS" if not has_common_word else "FAIL")
        print("-" * 50)
        print(f"Password strength score: {score}/7")
        print(f"Password strength rating: {rating.upper()}")
        print("=" * 50)
        if breach_count is None:
            print("Breach check unavailable(No connection)")
        elif breach_count > 0:
            print("Password was present in breaches", breach_count ,"times")
        else:
            print("Not found in any known breach")









if __name__ == "__main__":

    main()





    

   