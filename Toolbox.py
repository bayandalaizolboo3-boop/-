import os
import sys
import time
import random
import string
import secrets
import json
import shutil
import platform
import subprocess
import requests
import psutil

# ==========================================
#          PYTHON TOOLBOX
# ==========================================

GREEN = "\033[92m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"

EXPENSE_FILE = "expenses.json"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress ENTER to continue...")


def header():
    clear()
    print(GREEN + "=" * 48)
    print("             PYTHON TOOLBOX")
    print("          ALL-IN-ONE TOOLKIT")
    print("=" * 48 + RESET)


# ==========================================
# 01. NUMBER GUESSING GAME
# ==========================================

def guessing_game():
    header()

    secret = random.randint(1, 100)
    attempts = 0

    print("Guess a number between 1 and 100!")

    while True:
        try:
            guess = int(input("\nYour guess: "))
            attempts += 1

            if guess < secret:
                print("Too low!")
            elif guess > secret:
                print("Too high!")
            else:
                print(f"\nCorrect! The number was {secret}.")
                print(f"Total attempts: {attempts}")
                break

        except ValueError:
            print("Please enter a valid number.")

    pause()


# ==========================================
# 02. TIMER / ALARM
# ==========================================

def timer():
    header()

    try:
        minutes = float(input("Enter minutes: "))

        if minutes < 0:
            print("Please enter a positive number.")
            pause()
            return

        seconds = int(minutes * 60)

        print("\nTimer started!")

        while seconds > 0:
            mins, secs = divmod(seconds, 60)

            print(
                f"\rTime remaining: {mins:02d}:{secs:02d}",
                end="",
                flush=True
            )

            time.sleep(1)
            seconds -= 1

        print("\n\nTIME IS UP!")

    except ValueError:
        print("Invalid input.")

    except KeyboardInterrupt:
        print("\nTimer cancelled.")

    pause()


# ==========================================
# 03. FILE ORGANIZER
# ==========================================

def file_organizer():
    header()

    folder = input("Enter folder path: ").strip().strip('"')

    if not os.path.isdir(folder):
        print("Folder not found!")
        pause()
        return

    categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
        "Music": [".mp3", ".wav", ".flac"],
        "Archives": [".zip", ".rar", ".7z"]
    }

    moved = 0

    for filename in os.listdir(folder):
        source = os.path.join(folder, filename)

        if not os.path.isfile(source):
            continue

        extension = os.path.splitext(filename)[1].lower()

        for category, extensions in categories.items():
            if extension in extensions:

                destination_folder = os.path.join(
                    folder, category
                )

                os.makedirs(destination_folder, exist_ok=True)

                destination = os.path.join(
                    destination_folder, filename
                )

                # Avoid overwriting existing files
                if os.path.exists(destination):
                    print(f"Skipped: {filename}")
                    break

                shutil.move(source, destination)
                print(f"Moved: {filename} -> {category}")
                moved += 1
                break

    print(f"\nFinished! {moved} files organized.")
    pause()


# ==========================================
# 04. PASSWORD GENERATOR
# ==========================================

def password_generator():
    header()

    try:
        length = int(input("Password length: "))

        if length < 1 or length > 256:
            print("Choose a length between 1 and 256.")
            pause()
            return

        characters = (
            string.ascii_letters
            + string.digits
            + "!@#$%^&*()_+-="
        )

        password = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        print("\nGenerated Password:")
        print(GREEN + password + RESET)

    except ValueError:
        print("Invalid length.")

    pause()


# ==========================================
# 05. WEATHER CHECKER
# ==========================================

def weather_checker():
    header()

    city = input("Enter city name: ").strip()

    if not city:
        print("Please enter a city.")
        pause()
        return

    try:
        url = f"https://wttr.in/{city}?format=j1"

        response = requests.get(url, timeout=15)
        response.raise_for_status()

        data = response.json()
        current = data["current_condition"][0]

        print("\n========== WEATHER ==========")
        print("City:", city)
        print("Temperature:", current["temp_C"], "C")
        print("Feels like:", current["FeelsLikeC"], "C")
        print("Humidity:", current["humidity"], "%")
        print("Wind:", current["windspeedKmph"], "km/h")
        print(
            "Condition:",
            current["weatherDesc"][0]["value"]
        )

    except requests.RequestException:
        print("Could not connect to weather service.")

    except (KeyError, IndexError, ValueError):
        print("Could not read weather information.")

    pause()


# ==========================================
# 06. CALCULATOR
# ==========================================

def calculator():
    header()

    try:
        a = float(input("First number: "))
        operator = input("Operator (+ - * /): ")
        b = float(input("Second number: "))

        if operator == "+":
            result = a + b

        elif operator == "-":
            result = a - b

        elif operator == "*":
            result = a * b

        elif operator == "/":
            if b == 0:
                print("Cannot divide by zero!")
                pause()
                return

            result = a / b

        else:
            print("Invalid operator!")
            pause()
            return

        print(f"\nResult: {result}")

    except ValueError:
        print("Please enter valid numbers.")

    pause()


# ==========================================
# 07. EXPENSE TRACKER
# ==========================================

def expense_tracker():
    header()

    if os.path.exists(EXPENSE_FILE):
        try:
            with open(EXPENSE_FILE, "r") as file:
                expenses = json.load(file)
        except (json.JSONDecodeError, OSError):
            expenses = []
    else:
        expenses = []

    while True:
        print("\n========== EXPENSE TRACKER ==========")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Show total")
        print("4. Back to menu")

        choice = input("\nSelect: ")

        if choice == "1":
            name = input("Expense name: ")

            try:
                amount = float(input("Amount: "))

                if amount < 0:
                    print("Amount cannot be negative.")
                    continue

                expenses.append({
                    "name": name,
                    "amount": amount
                })

                with open(EXPENSE_FILE, "w") as file:
                    json.dump(expenses, file, indent=4)

                print("Expense saved!")

            except ValueError:
                print("Invalid amount.")

        elif choice == "2":
            print("\nYour expenses:")

            for item in expenses:
                print(
                    f"{item['name']}: "
                    f"{item['amount']:.2f}"
                )

        elif choice == "3":
            total = sum(
                item["amount"] for item in expenses
            )
            print(f"\nTotal expenses: {total:.2f}")

        elif choice == "4":
            break

        else:
            print("Invalid choice!")


# ==========================================
# 08. SIMPLE CHATBOT
# ==========================================

def chatbot():
    header()

    print("BOT: Hello! I am your assistant.")
    print("Type 'bye' to exit.\n")

    while True:
        message = input("YOU: ").lower().strip()

        if message in ["hi", "hello", "hey"]:
            print("BOT: Hello! How can I help you?")

        elif "how are you" in message:
            print("BOT: I'm doing great! Thanks.")

        elif "your name" in message:
            print("BOT: My name is Python Bot.")

        elif "time" in message:
            print("BOT:", time.strftime("%H:%M:%S"))

        elif "date" in message:
            print("BOT:", time.strftime("%Y-%m-%d"))

        elif "python" in message:
            print("BOT: Python is a powerful programming language.")

        elif message == "bye":
            print("BOT: Goodbye!")
            break

        else:
            print("BOT: Sorry, I don't understand.")

    pause()


# ==========================================
# 09. PC SYSTEM INFORMATION
# ==========================================

def system_info():
    header()

    print("========== OPERATING SYSTEM ==========")
    print("OS:", platform.system())
    print("Version:", platform.version())
    print("Release:", platform.release())
    print("Architecture:", platform.architecture()[0])

    print("\n========== CPU INFORMATION ==========")

    print("Processor:", platform.processor())
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Logical cores:", psutil.cpu_count(logical=True))
    print("CPU Usage:", psutil.cpu_percent(interval=1), "%")

    if platform.system() == "Windows":
        try:
            command = [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-CimInstance Win32_Processor).Name"
            ]

            cpu_name = subprocess.check_output(
                command,
                text=True,
                timeout=5
            ).strip()

            print("CPU Model:", cpu_name)

        except (subprocess.SubprocessError, OSError):
            print("Exact CPU model unavailable.")

    print("\n========== RAM INFORMATION ==========")

    ram = psutil.virtual_memory()

    print("Total:", round(ram.total / (1024 ** 3), 2), "GB")
    print("Used:", round(ram.used / (1024 ** 3), 2), "GB")
    print("Available:", round(ram.available / (1024 ** 3), 2), "GB")
    print("Usage:", ram.percent, "%")

    print("\n========== STORAGE INFORMATION ==========")

    drive = os.environ.get("SystemDrive", "C:") if os.name == "nt" else "/"

    disk = shutil.disk_usage(drive)

    print("Drive:", drive)
    print("Total:", round(disk.total / (1024 ** 3), 2), "GB")
    print("Used:", round(disk.used / (1024 ** 3), 2), "GB")
    print("Free:", round(disk.free / (1024 ** 3), 2), "GB")

    pause()


# ==========================================
# 10. MATRIX ANIMATION
# ==========================================

def matrix_animation():
    clear()

    columns = shutil.get_terminal_size().columns
    rows = shutil.get_terminal_size().lines

    chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*"

    drops = [
        random.randint(-rows, 0)
        for _ in range(columns)
    ]

    print("\033[?25l", end="")

    try:
        while True:
            print("\033[H", end="")

            for row in range(rows - 1):
                line = ""

                for col in range(columns):
                    if drops[col] == row:
                        line += "\033[92m" + random.choice(chars) + "\033[0m"
                    elif drops[col] > row and drops[col] - row < 5:
                        line += "\033[32m" + random.choice(chars) + "\033[0m"
                    else:
                        line += " "

                print(line)

            for col in range(columns):
                if drops[col] > rows or random.random() > 0.97:
                    drops[col] = random.randint(-10, 0)
                else:
                    drops[col] += 1

            time.sleep(0.07)

    except KeyboardInterrupt:
        pass

    finally:
        print("\033[0m\033[?25h")
        clear()
        print("Matrix animation stopped.")


# ==========================================
# MAIN MENU
# ==========================================

def main():

    while True:
        header()

        print("""
 [01] Number Guessing Game
 [02] Timer / Alarm
 [03] File Organizer
 [04] Password Generator
 [05] Weather Checker
 [06] Calculator
 [07] Expense Tracker
 [08] Simple Chatbot
 [09] PC System Information
 [10] Matrix Animation

 [00] Exit
        """)

        choice = input("Select a tool: ").strip()

        tools = {
            "1": guessing_game,
            "2": timer,
            "3": file_organizer,
            "4": password_generator,
            "5": weather_checker,
            "6": calculator,
            "7": expense_tracker,
            "8": chatbot,
            "9": system_info,
            "10": matrix_animation
        }

        if choice == "0":
            print("\nThank you for using Python Toolbox!")
            break

        elif choice in tools:
            try:
                tools[choice]()
            except KeyboardInterrupt:
                print("\n\nOperation cancelled.")
                pause()

        else:
            print("Invalid selection!")
            time.sleep(1)


if __name__ == "__main__":
    main()
