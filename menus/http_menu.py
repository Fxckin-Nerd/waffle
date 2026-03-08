"""HTTP mode selection menu."""


def choose_http_mode() -> str:
    print("\nSelect cURL HTTP mode:")
    print("1. http")
    print("2. http1.1")
    print("3. http2")
    print("4. no http (default)")

    options = {
        "1": "-0",
        "2": "--http1.1",
        "3": "--http2",
        "4": "",
    }

    while True:
        selection = input("Enter option number (1-4): ").strip()
        if selection in options:
            return options[selection]
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

