SEQUENCES = ["abcdefghijklmnopqrstuvwxyz", "0123456789", "qwertyuiop", "asdfghjkl", "zxcvbnm"]
LEET = { "@": "a", "4": "a", "3": "e", "1": "i", "!": "i", "0": "o", "$": "s", "5": "s", "+": "t", "7": "t" }



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


def load_common_passwords():
    common = set()
    with open("common_passwords.txt") as f:
        for line in f:
            word = line.strip()
            if word:
                common.add(word)
    return common


def undo_leet(password):
    result = ""
    for c in password.lower():
        if c in LEET:
            result += LEET[c]
            
        else:
            result += c
            
    return result

def check_common(password, common):
    is_common = password.lower() in common

    normalized = undo_leet(password)
    has_common_word = False
    for word in common:
       if len(word) >= 4 and word in normalized:
           has_common_word = True
           

    return is_common, has_common_word


def has_sequences(password):
    lower = password.lower()
    for seq in SEQUENCES:
        for s in [seq, seq[::-1]]:
            for i in range(len(s) - 3):
                window = s[i:i+4]
                if window in lower:
                    return True
    return False

def has_repeats(password):
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            return True
    return False


def calculating_rating(password, length_points, char_points, sequence, repeats, is_common, has_common_word):
    strength = length_points + char_points

    if sequence:
        strength -= 1
    if repeats:
        strength -= 1
    if is_common or has_common_word:
        strength -= 2

    score = max(strength, 0)

    if is_common or len(password) < 8:
        rating = "Weak"
    elif score <= 3: 
        rating = "Weak"
    elif score <= 5:
        rating = "Moderate"
    else:
        rating = "Strong"

    return score, rating

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
        is_common, has_common_word = check_common(password, common)
        sequence = has_sequences(password)
        repeats = has_repeats(password)
        score, rating = calculating_rating(password, length_points, char_points, sequence, repeats, is_common, has_common_word)

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

if __name__ == "__main__":

    main()