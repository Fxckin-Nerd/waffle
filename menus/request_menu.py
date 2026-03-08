"""Request type selection menus."""


def choose_request_type() -> str:
    print("\nSelect request type:")
    print("1. Standard (curl)")
    print("2. WebDAV method (curl -X)")
    print("3. Raw request line format (echo | nc)")
    print("4. TLS fingerprint modification (curl/openssl)")
    print("5. Header test (curl -H)")
    print("6. wget mode")
    print("7. Back")

    while True:
        selection = input("Enter option number (1-7): ").strip()
        if selection == "1":
            return "standard"
        elif selection == "2":
            return "webdav"
        elif selection == "3":
            return "raw"
        elif selection == "4":
            return "tls"
        elif selection == "5":
            return "header"
        elif selection == "6":
            return "wget"
        elif selection == "7":
            return "back"
        print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, or 7.")

def choose_raw_format() -> str:
    print("\nSelect raw request format:")
    print("1. Standard spacing (GET /admin HTTP/1.1)")
    print("2. Extra spaces (GET  /admin  HTTP/1.1)")
    print("3. Tab separated (GET\\t/admin\\tHTTP/1.1)")
    print("4. Back")

    while True:
        selection = input("Enter option number (1-4): ").strip()
        if selection == "1":
            return "standard"
        elif selection == "2":
            return "extra-spaces"
        elif selection == "3":
            return "tab-separated"
        elif selection == "4":
            return "back"
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

def choose_slow_send() -> str:
    print("\nDo you want to use slow send (send request in small chunks)?")
    print("1. No")
    print("2. Yes")
    print("3. Back")

    while True:
        selection = input("Enter option number (1-3): ").strip()
        if selection == "1":
            return "no"
        elif selection == "2":
            return "yes"
        elif selection == "3":
            return "back"
        print("Invalid choice. Please enter 1, 2, or 3.")

def choose_tls_tool() -> str:
    print("\nSelect TLS tool:")
    print("1. curl (with --tls-max and --ciphers)")
    print("2. openssl (with s_client)")
    print("3. Back")

    while True:
        selection = input("Enter option number (1-3): ").strip()
        if selection == "1":
            return "curl"
        elif selection == "2":
            return "openssl"
        elif selection == "3":
            return "back"
        print("Invalid choice. Please enter 1, 2, or 3.")

def choose_header_test_type() -> str:
    print("\nSelect header test type:")
    print("1. Single header test")
    print("2. Multi header test")
    print("3. Back")

    while True:
        selection = input("Enter option number (1-3): ").strip()
        if selection == "1":
            return "single"
        elif selection == "2":
            return "multi"
        elif selection == "3":
            return "back"
        print("Invalid choice. Please enter 1, 2, or 3.")

def choose_wget_mode() -> str:
    print("\nSelect wget mode:")
    print("1. Simple wget")
    print("2. wget with headers")
    print("3. Back")

    while True:
        selection = input("Enter option number (1-3): ").strip()
        if selection == "1":
            return "simple"
        elif selection == "2":
            return "headers"
        elif selection == "3":
            return "back"
        print("Invalid choice. Please enter 1, 2, or 3.")

def choose_webdav_method() -> str:
    print("\nSelect WebDAV method:")
    print("1. PROPFIND")
    print("2. LOCK")
    print("3. UNLOCK")
    print("4. TRACK")
    print("5. TRACE")
    print("6. OPTIONS")
    print("7. GET")
    print("8. Back")

    options = {
        "1": "PROPFIND",
        "2": "LOCK",
        "3": "UNLOCK",
        "4": "TRACK",
        "5": "TRACE",
        "6": "OPTIONS",
        "7": "GET",
    }

    while True:
        selection = input("Enter option number (1-8): ").strip()
        if selection == "8":
            return "back"
        elif selection in options:
            return options[selection]
        print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7, or 8.")

def get_single_header():
    """Get a single header name and value from user."""
    print("\nEnter custom header (example: X-Forwarded-For)")
    header_name = input("Header name: ").strip()
    header_value = input("Header value: ").strip()
    return [(header_name, header_value)]

def get_multi_headers():
    """Get multiple headers from user."""
    headers = []
    print("\nEnter custom headers (type 'done' when finished)")
    while True:
        header_name = input("Header name (or 'done' to finish): ").strip()
        if header_name.lower() == "done":
            if not headers:
                print("Please add at least one header.")
                continue
            break
        header_value = input("Header value: ").strip()
        headers.append((header_name, header_value))
        print(f"Added: {header_name}: {header_value}")
    return headers

def get_timeout_duration() -> int:
    """Get timeout duration in seconds for slow send requests."""
    while True:
        timeout_input = input("Enter timeout duration in seconds (default: 2): ").strip()
        if timeout_input == "":
            return 2  # Default
        if timeout_input.isdigit() and int(timeout_input) > 0:
            return int(timeout_input)
        print("Invalid timeout. Please enter a positive number.")

def get_sleep_duration() -> float:
    """Get sleep duration in seconds between slow send requests."""
    while True:
        sleep_input = input("Enter sleep duration between requests in seconds (default: 0): ").strip()
        if sleep_input == "":
            return 0  # Default
        try:
            sleep_value = float(sleep_input)
            if sleep_value >= 0:
                return sleep_value
            print("Sleep duration must be non-negative.")
        except ValueError:
            print("Invalid sleep duration. Please enter a number.")

