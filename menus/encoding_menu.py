"""Directory encoding selection menu."""


def choose_directory_mode() -> str:
    print("\nSelect directory handling mode:")
    print("1. standard command")
    print("2. asicii encoded directory")
    print("3. asicii double encoded directory")
    print("4. enclosed alphanumeric letters (ⓐⓓⓜⓘⓝ)")
    print("5. homoglyphs (аdmіn)")
    print("6. invisible characters (ad​min)")
    print("7. non-breaking characters (ad min)")
    print("8. control characters (null bytes)")
    print("9. fullwidth characters (ａｄｍｉｎ)")
    print("10. variable spacing (a d  m   i    n)")
    print("11. special symbols (@dm!n)")
    print("12. pictograph characters (🅰dℹn)")
    print("13. whitespace variants (various spaces)")
    print("14. combining characters (a̋d̋m̋i̋n̋)")
    print("15. path traversal (../../../admin)")
    print("16. Back")

    options = {
        "1": "standard",
        "2": "encoded",
        "3": "double-encoded",
        "4": "enclosed-alphanumeric",
        "5": "homoglyphs",
        "6": "invisible-characters",
        "7": "non-breaking-characters",
        "8": "control-characters",
        "9": "fullwidth-characters",
        "10": "variable-spacing",
        "11": "special-symbols",
        "12": "pictograph-characters",
        "13": "whitespace-variants",
        "14": "combining-characters",
        "15": "path-traversal",
    }

    while True:
        selection = input("Enter option number (1-16): ").strip()
        if selection == "16":
            return "back"
        elif selection in options:
            return options[selection]
        print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, or 16.")

