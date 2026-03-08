"""Output and user agent selection menus."""

import random


def get_verbose_output() -> bool:
    """Prompt user for verbose output preference."""
    while True:
        response = input("Do you want verbose output? (y/N): ").strip().lower()
        if response == "y":
            return True
        elif response == "n" or response == "":
            return False
        print("Invalid choice. Please enter 'y' or 'N'.")

def choose_user_agent() -> str:
    """Prompt user to select a user agent string."""
    print("\nSelect User Agent:")
    print("1. Windows 10 x86 - Chrome")
    print("2. Windows 11 - Chrome")
    print("3. Apple Mac M1 - Safari")
    print("4. Apple Mac M2 - Safari")
    print("5. Linux x86 - Firefox")
    print("6. Random")
    print("7. Custom")
    print("8. Default (no user agent)")

    user_agents = {
        "1": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "2": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "3": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "4": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
        "5": "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
    }

    while True:
        selection = input("Enter option number (1-8): ").strip()
        if selection in user_agents:
            return user_agents[selection]
        elif selection == "6":
            # Random user agent from the predefined list
            return random.choice(list(user_agents.values()))
        elif selection == "7":
            # Custom user agent
            custom_ua = input("Enter custom user agent string: ").strip()
            return custom_ua
        elif selection == "8":
            return ""
        print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7, or 8.")

