#!/usr/bin/env python3
"""
Password Generator
A secure password generator with strength analysis.
Author: Jay Singh (iamjaysingh)
"""

import random
import string
import math


def calculate_entropy(password):
    """Calculate password entropy in bits."""
    charset_size = 0
    if any(c in string.ascii_lowercase for c in password):
        charset_size += 26
    if any(c in string.ascii_uppercase for c in password):
        charset_size += 26
    if any(c in string.digits for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += 32
    if charset_size == 0:
        return 0
    return len(password) * math.log2(charset_size)


def strength_label(entropy):
    """Get strength label based on entropy."""
    if entropy < 28:
        return "🔴 Very Weak"
    elif entropy < 36:
        return "🟠 Weak"
    elif entropy < 60:
        return "🟡 Moderate"
    elif entropy < 80:
        return "🟢 Strong"
    else:
        return "💪 Very Strong"


def generate_password(length=16, use_upper=True, use_digits=True, use_symbols=True, exclude=""):
    """Generate a secure password with given constraints."""
    chars = string.ascii_lowercase
    required = [random.choice(string.ascii_lowercase)]

    if use_upper:
        chars += string.ascii_uppercase
        required.append(random.choice(string.ascii_uppercase))
    if use_digits:
        chars += string.digits
        required.append(random.choice(string.digits))
    if use_symbols:
        chars += string.punctuation
        required.append(random.choice(string.punctuation))

    # Remove excluded characters
    for c in exclude:
        chars = chars.replace(c, "")

    # Fill remaining length
    remaining = length - len(required)
    if remaining > 0:
        required.extend(random.choices(chars, k=remaining))

    # Shuffle to randomize positions
    random.shuffle(required)
    return "".join(required)


def generate_passphrase(num_words=4):
    """Generate a memorable passphrase."""
    words = [
        "tiger", "cloud", "river", "flame", "stone", "maple", "storm",
        "eagle", "frost", "piano", "ocean", "crystal", "forest", "breeze",
        "lunar", "solar", "comet", "blaze", "spark", "thunder", "meadow",
        "harbor", "valley", "summit", "canyon", "glacier", "phoenix",
        "dragon", "falcon", "panther", "viper", "cobra", "wolf",
    ]
    selected = random.sample(words, min(num_words, len(words)))
    separator = random.choice(["-", "_", ".", "+"])
    # Capitalize random words and add numbers
    result = []
    for w in selected:
        if random.random() > 0.5:
            w = w.capitalize()
        result.append(w)
    result.append(str(random.randint(10, 99)))
    return separator.join(result)


def main():
    print("=" * 50)
    print("  🔐 Secure Password Generator")
    print("=" * 50)

    while True:
        print("\n  Options:")
        print("  1. Generate password")
        print("  2. Generate passphrase")
        print("  3. Check password strength")
        print("  4. Generate batch (5 passwords)")
        print("  5. Exit")

        choice = input("\n  Select: ").strip()

        if choice == "1":
            try:
                length = int(input("  Length (default 16): ").strip() or "16")
            except ValueError:
                length = 16
            password = generate_password(length)
            entropy = calculate_entropy(password)
            print(f"\n  🔑 Password: {password}")
            print(f"  📊 Entropy:  {entropy:.1f} bits")
            print(f"  💪 Strength: {strength_label(entropy)}")

        elif choice == "2":
            passphrase = generate_passphrase()
            entropy = calculate_entropy(passphrase)
            print(f"\n  🔑 Passphrase: {passphrase}")
            print(f"  📊 Entropy:    {entropy:.1f} bits")
            print(f"  💪 Strength:   {strength_label(entropy)}")

        elif choice == "3":
            pwd = input("  Enter password: ").strip()
            entropy = calculate_entropy(pwd)
            print(f"  📊 Entropy:  {entropy:.1f} bits")
            print(f"  💪 Strength: {strength_label(entropy)}")
            print(f"  📏 Length:   {len(pwd)} characters")

        elif choice == "4":
            print("\n  🔑 Generated passwords:")
            for i in range(5):
                pwd = generate_password(random.randint(12, 20))
                ent = calculate_entropy(pwd)
                print(f"    {i+1}. {pwd}  ({ent:.0f} bits)")

        elif choice == "5":
            print("\n  👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
