"""Encoding utility functions."""

from encoders import (
    enclosed_alphanumeric, homoglyphs, invisible_characters, non_breaking_characters,
    control_characters, fullwidth_characters, variable_spacing, special_symbols,
    pictograph_characters, whitespace_variants, combining_characters, path_traversal
)


def ascii_hex_percent_encode(value: str) -> str:
    """Encode every character as %HH using its ASCII code."""
    return "".join(f"%{ord(ch):02X}" for ch in value)


def apply_directory_encoding(directory: str, mode: str) -> str:
    """Apply the selected directory encoding mode."""
    encoders_map = {
        "standard": lambda x: x,
        "encoded": ascii_hex_percent_encode,
        "double-encoded": lambda x: ascii_hex_percent_encode(ascii_hex_percent_encode(x)),
        "enclosed-alphanumeric": enclosed_alphanumeric,
        "homoglyphs": homoglyphs,
        "invisible-characters": invisible_characters,
        "non-breaking-characters": non_breaking_characters,
        "control-characters": control_characters,
        "fullwidth-characters": fullwidth_characters,
        "variable-spacing": variable_spacing,
        "special-symbols": special_symbols,
        "pictograph-characters": pictograph_characters,
        "whitespace-variants": whitespace_variants,
        "combining-characters": combining_characters,
        "path-traversal": path_traversal,
    }
    
    if mode not in encoders_map:
        raise ValueError("Unknown encoding mode.")
    
    return encoders_map[mode](directory)


def split_request_into_chunks(request: str, chunk_size: int = 2) -> list:
    """Split HTTP request into small chunks for slow send attacks."""
    chunks = []
    i = 0
    while i < len(request):
        chunks.append(request[i:i + chunk_size])
        i += chunk_size
    return chunks
