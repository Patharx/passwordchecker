import re
import string

# A list of the most common passwords hackers try first
# This is a tiny sample — real tools use lists of millions
COMMON_PASSWORDS = [
    "password", "123456", "password123", "admin", "letmein",
    "qwerty", "monkey", "1234567890", "iloveyou", "sunshine",
    "princess", "dragon", "master", "login", "welcome",
    "solo", "abc123", "password1", "superman", "batman"
]

# Gandalf's verdicts based on score
GANDALF_VERDICTS = {
    "very_weak": [
        "You shall not pass... because this password is absolutely terrible.",
        "Even a Took could crack this. And that is saying something.",
        "I have seen Orcs with more creativity than this password.",
    ],
    "weak": [
        "This password worries me greatly. Much work remains.",
        "A Nazgul would crack this before his horse could blink.",
        "You are like a candle in the wind — bright for a moment, easily extinguished.",
    ],
    "medium": [
        "A wizard sees potential here, but much work remains.",
        "Not quite worthy of the Fellowship, but not Orc-level either.",
        "You are on the right path, but the journey is not yet complete.",
    ],
    "strong": [
        "Now THAT is a password worthy of Rivendell!",
        "Sauron would need considerable effort to crack this. Well done.",
        "You have the makings of a true guardian of Middle-earth.",
    ],
    "very_strong": [
        "Even the Eye of Sauron could not crack this! Magnificent!",
        "By the Valar — this password could guard the One Ring itself!",
        "I am genuinely impressed. A password worthy of Gandalf the White!",
    ]
}

import random

def check_length(password):
    """
    Checks password length and returns a score.
    Length is the single most important factor in password strength.
    """
    length = len(password)
    if length >= 16:
        return 3, f"✅ Length: {length} characters (Excellent!)"
    elif length >= 12:
        return 2, f"✅ Length: {length} characters (Good)"
    elif length >= 8:
        return 1, f"⚠️  Length: {length} characters (Minimum — longer is better)"
    else:
        return 0, f"❌ Length: {length} characters (Too short — 8 minimum)"

def check_character_diversity(password):
    """
    Checks if the password uses a mix of character types.
    Each type adds complexity — hackers have to try more combinations.
    """
    score = 0
    feedback = []

    # Check for lowercase letters
    if re.search(r'[a-z]', password):
        score += 1
        feedback.append("✅ Contains lowercase letters")
    else:
        feedback.append("❌ No lowercase letters")

    # Check for uppercase letters
    if re.search(r'[A-Z]', password):
        score += 1
        feedback.append("✅ Contains uppercase letters")
    else:
        feedback.append("❌ No uppercase letters")

    # Check for numbers
    if re.search(r'[0-9]', password):
        score += 1
        feedback.append("✅ Contains numbers")
    else:
        feedback.append("❌ No numbers")

    # Check for special characters
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
        feedback.append("✅ Contains special characters")
    else:
        feedback.append("❌ No special characters (!@#$% etc)")

    return score, feedback

def check_common_passwords(password):
    """
    Checks against a list of commonly used passwords.
    Hackers always try these first — no matter how 'complex' they look.
    """
    if password.lower() in COMMON_PASSWORDS:
        return 0, "❌ This is one of the most commonly used passwords — avoid it!"
    return 1, "✅ Not a commonly known password"

def check_patterns(password):
    """
    Checks for repeated characters or sequential patterns.
    'aaaaaa' and '123456' are weak even if they meet length requirements.
    """
    # Check for repeated characters (e.g. 'aaaa')
    if re.search(r'(.)\1{2,}', password):
        return 0, "❌ Contains repeated characters (e.g. 'aaa')"

    # Check for sequential numbers (e.g. '1234')
    if re.search(r'(012|123|234|345|456|567|678|789)', password):
        return 0, "⚠️  Contains sequential numbers (e.g. '123')"

    # Check for sequential letters (e.g. 'abcd')
    if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm)', password.lower()):
        return 0, "⚠️  Contains sequential letters (e.g. 'abc')"

    return 1, "✅ No obvious patterns detected"

def get_strength_label(score, max_score):
    """
    Converts a numerical score into a strength category.
    """
    percentage = score / max_score

    if percentage >= 0.9:
        return "very_strong", "🟢 VERY STRONG"
    elif percentage >= 0.7:
        return "strong", "🟢 STRONG"
    elif percentage >= 0.5:
        return "medium", "🟡 MEDIUM"
    elif percentage >= 0.3:
        return "weak", "🔴 WEAK"
    else:
        return "very_weak", "🔴 VERY WEAK"

def check_password(password):
    """
    Main function — runs all checks and prints a full report.
    """
    print("\n" + "=" * 50)
    print("🔐 PASSWORD STRENGTH ANALYSIS")
    print("=" * 50)

    total_score = 0
    max_score = 9  # Maximum possible score across all checks

    # Run length check
    length_score, length_feedback = check_length(password)
    total_score += length_score
    print(f"\n📏 LENGTH (max 3 points)")
    print(f"   {length_feedback}")
    print(f"   Score: {length_score}/3")

    # Run character diversity check
    diversity_score, diversity_feedback = check_character_diversity(password)
    total_score += diversity_score
    print(f"\n🔤 CHARACTER DIVERSITY (max 4 points)")
    for line in diversity_feedback:
        print(f"   {line}")
    print(f"   Score: {diversity_score}/4")

    # Run common password check
    common_score, common_feedback = check_common_passwords(password)
    total_score += common_score
    print(f"\n📋 COMMON PASSWORDS (max 1 point)")
    print(f"   {common_feedback}")
    print(f"   Score: {common_score}/1")

    # Run pattern check
    pattern_score, pattern_feedback = check_patterns(password)
    total_score += pattern_score
    print(f"\n🔁 PATTERNS (max 1 point)")
    print(f"   {pattern_feedback}")
    print(f"   Score: {pattern_score}/1")

    # Calculate final strength
    strength_key, strength_label = get_strength_label(total_score, max_score)

    print("\n" + "-" * 50)
    print(f"📊 TOTAL SCORE: {total_score}/{max_score}")
    print(f"💪 STRENGTH: {strength_label}")
    print("-" * 50)

    # Gandalf's verdict
    verdict = random.choice(GANDALF_VERDICTS[strength_key])
    print(f"\n🧙 Gandalf says:")
    print(f'   "{verdict}"')
    print("=" * 50 + "\n")

# Main program
if __name__ == "__main__":
    print("🧙 GANDALF'S PASSWORD CHECKER")
    print("=" * 50)
    print("*adjusts hat and peers at you suspiciously*")
    print("Let us see how worthy your password truly is...\n")

    while True:
        password = input("Enter a password to check (or 'quit' to exit): ")

        if password.lower() == 'quit':
            print("\n🧙 'Farewell! May your passwords be ever strong!'")
            break

        check_password(password)