#!/usr/bin/env python3
"""Script to refactor waffle.py into modules."""

import re
import os

# Read the original file
with open('waffle.py', 'r') as f:
    content = f.read()

# Extract function definitions with their content
def extract_function(content, func_name):
    """Extract a complete function definition from content."""
    pattern = rf'(def {func_name}\([^)]*\)[^:]*:.*?)(?=\ndef |\nif __name__|$)'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).rstrip() + '\n\n' if match else None

# HTTP mode menu
http_menu_content = '''"""HTTP mode selection menu."""


''' + extract_function(content, 'choose_http_mode')

with open('menus/http_menu.py', 'w') as f:
    f.write(http_menu_content)

# Request type menus
request_funcs = [
    'choose_request_type',
    'choose_raw_format',
    'choose_slow_send',
    'choose_tls_tool',
    'choose_header_test_type',
    'choose_wget_mode',
    'choose_webdav_method',
    'get_single_header',
    'get_multi_headers',
    'get_timeout_duration',
    'get_sleep_duration',
]

request_menu_content = '''"""Request type selection menus."""


'''
for func in request_funcs:
    func_content = extract_function(content, func)
    if func_content:
        request_menu_content += func_content

with open('menus/request_menu.py', 'w') as f:
    f.write(request_menu_content)

# Encoding menu
encoding_menu_content = '''"""Directory encoding selection menu."""


''' + extract_function(content, 'choose_directory_mode')

with open('menus/encoding_menu.py', 'w') as f:
    f.write(encoding_menu_content)

# Output menus (verbose and user agent)
output_menu_content = '''"""Output and user agent selection menus."""

import random


''' + extract_function(content, 'get_verbose_output') + extract_function(content, 'choose_user_agent')

with open('menus/output_menu.py', 'w') as f:
    f.write(output_menu_content)

print("Menu modules created successfully!")
print("- menus/http_menu.py")
print("- menus/request_menu.py")
print("- menus/encoding_menu.py")
print("- menus/output_menu.py")
