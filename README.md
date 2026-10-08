# 🔐 Secure Random Password Generator

A Python-based **Secure Random Password Generator** that creates customizable and strong passwords using Python's `secrets` module.

## 📌 Project Overview

This project generates random passwords based on the user's requirements. The user can choose the password length and decide whether to include:

* Uppercase letters
* Lowercase letters
* Numbers
* Special symbols

The program also provides predefined **Easy, Moderate, and Strong** password levels.

## ✨ Features

* 🔑 Secure random password generation
* 🔠 Uppercase and lowercase character support
* 🔢 Number support
* 🔣 Special symbol support
* 📏 Custom password length
* 💪 Password strength checking
* 🎯 Easy, Moderate, and Strong presets
* 🔄 Generate multiple passwords at once
* 💾 Save generated passwords to a text file
* ✅ Input validation and error handling

## 🛠️ Technologies Used

* **Python 3**
* `string` module
* `secrets` module

## 📂 Project Structure

```text
Password-Generator/
│
├── password_generator.py
├── generated_passwords.txt
└── README.md
```

> `generated_passwords.txt` is created automatically when the user chooses to save the generated passwords.

## 🚀 How to Run

### Step 1: Install Python

Make sure Python 3 is installed on your system.

### Step 2: Run the program

Open the terminal in the project folder and run:

```bash
python password_generator.py
```

## 🖥️ How It Works

The program provides two generation modes:

### 1. Custom Mode

The user can manually select:

```text
Password length
Uppercase letters
Lowercase letters
Numbers
Special symbols
```

The program then generates a password according to these choices.

### 2. Strength Level Mode

The user can directly select:

```text
Easy
Moderate
Strong
```

The program automatically applies the appropriate configuration.

## 🔐 Password Generation Process

The password is generated using the following process:

```text
User Input
    ↓
Build Character Pool
    ↓
Select Guaranteed Characters
    ↓
Generate Remaining Characters
    ↓
Securely Shuffle Characters
    ↓
Generate Password
    ↓
Check Password Strength
    ↓
Display / Save Password
```

## 💪 Password Strength

The program checks five factors:

1. Password length is at least 12 characters
2. Contains uppercase letters
3. Contains lowercase letters
4. Contains numbers
5. Contains special symbols

Based on these conditions:

| Score | Strength |
| ----- | -------- |
| 0–2   | Weak     |
| 3–4   | Moderate |
| 5     | Strong   |

## 🔒 Why `secrets` Module?

The project uses Python's `secrets` module instead of the normal `random` module because password generation requires stronger randomness.

The `secrets` module is designed for security-sensitive applications such as passwords and authentication tokens.

## 📁 Saving Passwords

The user can choose to save generated passwords.

The passwords are stored in:

```text
generated_passwords.txt
```

Each password is stored on a separate line.

## 🧩 Error Handling

The program handles invalid inputs such as:

* Non-numeric values when a number is expected
* Negative or zero values
* Invalid Yes/No responses
* Password length below the minimum requirement
* No character type being selected
* Invalid strength level

## 🎯 Objective

The main objective of this project is to develop a simple, secure, and user-friendly password generator that can create customizable passwords and evaluate their strength.

## 🔮 Future Enhancements

Possible future improvements include:

* Graphical User Interface (GUI)
* Password history
* Password copy-to-clipboard option
* Password entropy calculation
* Custom symbol selection
* Password generation using a web interface

## 👩‍💻 Author

**Bhumika Dandare**

CSE(AIML)
SB Jain College of Engineering

## 📜 License

This project is created for educational and academic purposes.

