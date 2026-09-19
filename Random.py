import string
import secrets
class PasswordGenerator:
    """Encapsulates all logic related to generating and evaluating passwords."""
    def __init__(self, length=12, use_upper=True, use_lower=True,
                 use_digits=True, use_symbols=True):
        self.length = length
        self.use_upper = use_upper
        self.use_lower = use_lower
        self.use_digits = use_digits
        self.use_symbols = use_symbols
    def _build_character_pool(self):
        """Builds the pool of characters to choose from, based on user options."""
        pool = ""
        if self.use_upper:
            pool += string.ascii_uppercase
        if self.use_lower:
            pool += string.ascii_lowercase
        if self.use_digits:
            pool += string.digits
        if self.use_symbols:
            pool += string.punctuation
        if not pool:
            raise ValueError("At least one character type must be selected.")
        return pool
    def _guaranteed_characters(self):
        """Ensures at least one character from each selected category is included."""
        guaranteed = []
        if self.use_upper:
            guaranteed.append(secrets.choice(string.ascii_uppercase))
        if self.use_lower:
            guaranteed.append(secrets.choice(string.ascii_lowercase))
        if self.use_digits:
            guaranteed.append(secrets.choice(string.digits))
        if self.use_symbols:
            guaranteed.append(secrets.choice(string.punctuation))
        return guaranteed
    def generate(self):
        """Generates a single secure password meeting all constraints."""
        if self.length < 4:
            raise ValueError("Password length should be at least 4 for security.")
        pool = self._build_character_pool()
        guaranteed = self._guaranteed_characters()
        remaining_length = self.length - len(guaranteed)
        remaining_chars = [secrets.choice(pool) for _ in range(remaining_length)]
        password_chars = guaranteed + remaining_chars
        # Shuffle securely so guaranteed characters aren't always at the start
        for i in range(len(password_chars) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_chars[i], password_chars[j] = password_chars[j], password_chars[i]
        return "".join(password_chars)
    @staticmethod
    def check_strength(password):
        """Returns a simple strength rating: Weak, Moderate, or Strong."""
        length_score = len(password) >= 12
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in string.punctuation for c in password)
        score = sum([length_score, has_upper, has_lower, has_digit, has_symbol])

        if score >= 5:
            return "Strong"
        elif score >= 3:
            return "Moderate"
        else:
            return "Weak"
    # Preset configurations that reliably produce each strength level
    STRENGTH_PRESETS = {
        "easy": {"length": 6, "use_upper": False, "use_lower": True,
                  "use_digits": True, "use_symbols": False},
        "moderate": {"length": 10, "use_upper": True, "use_lower": True,
                     "use_digits": True, "use_symbols": False},
        "strong": {"length": 14, "use_upper": True, "use_lower": True,
                   "use_digits": True, "use_symbols": True},
    }
    @classmethod
    def generate_by_strength(cls, level):
        """
        Generates a password that matches a user-chosen strength level
        ('easy', 'moderate', or 'strong'), instead of the caller having
        to manually pick length/character options.
        """
        level = level.strip().lower()
        if level not in cls.STRENGTH_PRESETS:
            raise ValueError("Strength level must be 'easy', 'moderate', or 'strong'.")

        preset = cls.STRENGTH_PRESETS[level]
        generator = cls(**preset)

        # Generate and re-check; presets are tuned to match on the first try,
        # but this loop guards against edge cases so the result always
        # matches what the user asked for.
        target = {"easy": "Weak", "moderate": "Moderate", "strong": "Strong"}[level]
        for _ in range(20):
            password = generator.generate()
            if cls.check_strength(password) == target:
                return password
        return password  # fallback after 20 tries (extremely unlikely to be needed)


def get_positive_int(prompt):
    """Safely gets a positive integer from the user, re-prompting on bad input."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_yes_no(prompt):
    """Safely gets a yes/no answer from the user."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "yes"):
            return True
        elif choice in ("n", "no"):
            return False
        print("Please answer with 'y' or 'n'.")
def main():
    print("=" * 50)
    print("        RANDOM PASSWORD GENERATOR")
    print("=" * 50)
    try:
        print("\nHow would you like to generate your password?")
        print("  1. Custom (you choose length & character types)")
        print("  2. By strength level (Easy / Moderate / Strong)")
        mode = input("Enter choice (1 or 2): ").strip()
        count = get_positive_int("How many passwords do you want to generate? ")
        passwords = []
        if mode == "2":
            while True:
                level = input("Choose strength (easy/moderate/strong): ").strip().lower()
                if level in PasswordGenerator.STRENGTH_PRESETS:
                    break
                print("Please type 'easy', 'moderate', or 'strong'.")

            print("\nGenerated Password(s):")
            print("-" * 50)
            for i in range(count):
                pwd = PasswordGenerator.generate_by_strength(level)
                passwords.append(pwd)
                print(f"{i + 1}. {pwd}   [Requested strength: {level.capitalize()}]")
        else:
            length = get_positive_int("Enter desired password length (min 4): ")
            use_upper = get_yes_no("Include uppercase letters? (y/n): ")
            use_lower = get_yes_no("Include lowercase letters? (y/n): ")
            use_digits = get_yes_no("Include numbers? (y/n): ")
            use_symbols = get_yes_no("Include special symbols? (y/n): ")
            generator = PasswordGenerator(
                length=length,
                use_upper=use_upper,
                use_lower=use_lower,
                use_digits=use_digits,
                use_symbols=use_symbols,
            )
            print("\nGenerated Password(s):")
            print("-" * 50)
            for i in range(count):
                pwd = generator.generate()
                strength = PasswordGenerator.check_strength(pwd)
                passwords.append(pwd)
                print(f"{i + 1}. {pwd}   [Strength: {strength}]")

        if get_yes_no("\nSave these passwords to a file? (y/n): "):
            filename = "generated_passwords.txt"
            with open(filename, "w") as f:
                for pwd in passwords:
                    f.write(pwd + "\n")
            print(f"Passwords saved to '{filename}'.")

    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting safely.")


if __name__ == "__main__":
    main()