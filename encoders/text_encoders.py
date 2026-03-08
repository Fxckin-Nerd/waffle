"""Text encoding functions for WAF bypass testing."""


def enclosed_alphanumeric(value: str) -> str:
    """Convert alphanumeric characters to enclosed/circled Unicode variants."""
    result = []
    for ch in value:
        if 'a' <= ch <= 'z':
            # Circled lowercase letters: ⓐ-ⓩ (U+24D0 to U+24E9)
            result.append(chr(0x24D0 + (ord(ch) - ord('a'))))
        elif 'A' <= ch <= 'Z':
            # Circled uppercase letters: Ⓐ-Ⓩ (U+24B6 to U+24CF)
            result.append(chr(0x24B6 + (ord(ch) - ord('A'))))
        elif '0' <= ch <= '9':
            # Circled digits: ⓪①②③④⑤⑥⑦⑧⑨
            if ch == '0':
                result.append(chr(0x24EA))  # ⓪
            else:
                result.append(chr(0x2460 + (ord(ch) - ord('1'))))  # ①-⑨
        else:
            # Keep other characters unchanged
            result.append(ch)
    return "".join(result)


def homoglyphs(value: str) -> str:
    """Replace characters with visually similar characters from other Unicode blocks."""
    # Map of Latin characters to homoglyphs (Cyrillic, Greek, etc.)
    homoglyph_map = {
        'a': 'а', 'c': 'с', 'e': 'е', 'i': 'і', 'j': 'ј', 'o': 'о', 'p': 'р', 's': 'ѕ', 'x': 'х', 'y': 'у',
        'A': 'А', 'B': 'В', 'C': 'С', 'E': 'Е', 'H': 'Н', 'I': 'І', 'J': 'Ј', 'K': 'К', 'M': 'М', 'O': 'О',
        'P': 'Р', 'S': 'Ѕ', 'T': 'Т', 'X': 'Х', 'Y': 'Υ',
    }
    return "".join(homoglyph_map.get(ch, ch) for ch in value)


def invisible_characters(value: str) -> str:
    """Insert zero-width invisible characters between regular characters."""
    zwsp = '\u200B'  # Zero-width space
    result = []
    for ch in value:
        result.append(ch)
        result.append(zwsp)
    if result:
        result.pop()
    return "".join(result)


def non_breaking_characters(value: str) -> str:
    """Insert non-breaking spaces between regular characters."""
    nbsp = '\u00A0'  # Non-breaking space
    result = []
    for ch in value:
        result.append(ch)
        result.append(nbsp)
    if result:
        result.pop()
    return "".join(result)


def control_characters(value: str) -> str:
    """Insert control characters (null bytes as %00) between regular characters."""
    result = []
    for ch in value:
        result.append(ch)
        result.append('%00')
    if result:
        result.pop()
    return "".join(result)


def fullwidth_characters(value: str) -> str:
    """Convert ASCII characters to fullwidth Unicode characters."""
    result = []
    for ch in value:
        if 0x21 <= ord(ch) <= 0x7E:
            result.append(chr(ord(ch) + 0xFEE0))
        elif ch == ' ':
            result.append('\u3000')
        else:
            result.append(ch)
    return "".join(result)


def variable_spacing(value: str) -> str:
    """Insert variable spacing (alternating space types) between characters."""
    spaces = [' ', '\u2000', '\u2001', '\u2002', '\u2003', '\u2009']
    result = []
    for i, ch in enumerate(value):
        result.append(ch)
        if i < len(value) - 1:
            result.append(spaces[i % len(spaces)])
    return "".join(result)


def special_symbols(value: str) -> str:
    """Replace characters with special symbols and punctuation (leetspeak-style)."""
    symbol_map = {
        'a': '@', 'A': '@', 'e': '3', 'E': '3', 'i': '!', 'I': '!', 'o': '0', 'O': '0',
        's': '$', 'S': '$', 't': '7', 'T': '7', 'l': '1', 'L': '1', 'g': '9', 'G': '9',
        'b': '8', 'B': '8',
    }
    return "".join(symbol_map.get(ch, ch) for ch in value)


def pictograph_characters(value: str) -> str:
    """Replace characters with Unicode symbols and pictographs."""
    pictograph_map = {
        'a': '🅰', 'A': '🅰', 'b': '🅱', 'B': '🅱', 'o': '⭕', 'O': '⭕',
        'p': '🅿', 'P': '🅿', 'i': 'ℹ', 'I': 'ℹ', 'm': 'Ⓜ', 'M': 'Ⓜ',
        'x': '❌', 'X': '❌', 's': '💲', 'S': '💲', '!': '❗', '?': '❓',
    }
    return "".join(pictograph_map.get(ch, ch) for ch in value)


def whitespace_variants(value: str) -> str:
    """Insert various Unicode whitespace variants between characters."""
    whitespaces = [
        '\u0020', '\u00A0', '\u1680', '\u2000', '\u2001', '\u2002', '\u2003',
        '\u2004', '\u2005', '\u2006', '\u2007', '\u2008', '\u2009', '\u200A',
    ]
    result = []
    for i, ch in enumerate(value):
        result.append(ch)
        if i < len(value) - 1:
            result.append(whitespaces[i % len(whitespaces)])
    return "".join(result)


def combining_characters(value: str) -> str:
    """Add combining diacritical marks to characters."""
    combining_marks = ['\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0308', '\u030A', '\u0327']
    result = []
    for i, ch in enumerate(value):
        result.append(ch)
        if ch.isalnum():
            result.append(combining_marks[i % len(combining_marks)])
    return "".join(result)


def path_traversal(value: str) -> str:
    """Add path traversal sequences before the directory."""
    return "../../../" + value
