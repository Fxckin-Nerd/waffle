#!/usr/bin/env python3
"""Interactive WAF bypass testing tool - WAFFLE.

Modular structure:
- utils/: URL and encoding utilities
- encoders/: Text encoding functions
- menus/: User interaction menus
- commands/: Command building (future)
"""

import subprocess
import sys
import time
import os

# Import utilities
from utils import normalize_target_url, extract_hostname, apply_directory_encoding, split_request_into_chunks

# Import menu functions
from menus import (
    choose_http_mode, choose_request_type, choose_raw_format, choose_slow_send,
    choose_tls_tool, choose_header_test_type, choose_wget_mode, choose_webdav_method,
    get_single_header, get_multi_headers, get_timeout_duration, get_sleep_duration,
    choose_directory_mode, get_verbose_output, choose_user_agent
)


def main() -> int:
    # Display ASCII art banner
    print("""
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░ ░▒▓█▓▒░      ░▒▓██████▓▒░   
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░        
 ░▒▓█████████████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓████████▓▒░▒▓████████▓▒░ 
                                                                                       
""")
    print("WAF Directory Check Tool")
    print("------------------------")

    website_url = input("Enter website URL (example: https://www.mysite.com): ").strip()
    directory = input("Enter directory to test (example: admin): ").strip()

    try:
        # Menu navigation loop
        while True:
            http_mode = choose_http_mode()
            
            # Request type menu
            while True:
                request_type = choose_request_type()
                if request_type == "back":
                    break  # Go back to HTTP mode selection
                
                port = None
                webdav_method = None
                raw_format = None
                custom_headers = None
                header_test_type = None
                wget_mode = None
                wget_headers = None
                
                # Handle raw request type - get port and format
                if request_type == "raw":
                    while True:
                        port_input = input("Enter port number (example: 443): ").strip()
                        if port_input.isdigit():
                            port = int(port_input)
                            break
                        print("Invalid port. Please enter a number.")
                    
                    # Choose format after port
                    while True:
                        raw_format = choose_raw_format()
                        if raw_format == "back":
                            break  # Go back to port input
                        else:
                            break  # Valid format selected, proceed
                    
                    if raw_format == "back":
                        continue  # Stay in request type loop
                    
                    # Choose slow send after format
                    while True:
                        slow_send = choose_slow_send()
                        if slow_send == "back":
                            break  # Go back to format selection
                        else:
                            break  # Valid selection, proceed
                    
                    if slow_send == "back":
                        continue  # Stay in format selection loop
                    
                    # Get timeout and sleep duration if slow send is enabled
                    timeout_duration = None
                    sleep_duration = None
                    if slow_send == "yes":
                        timeout_duration = get_timeout_duration()
                        sleep_duration = get_sleep_duration()
                
                # Handle TLS fingerprint modification
                elif request_type == "tls":
                    while True:
                        tls_tool = choose_tls_tool()
                        if tls_tool == "back":
                            break  # Go back to request type selection
                        else:
                            break  # Valid tool selected, proceed
                    
                    if tls_tool == "back":
                        continue  # Stay in request type loop
                
                # Handle WebDAV request type - get method
                elif request_type == "webdav":
                    while True:
                        webdav_method = choose_webdav_method()
                        if webdav_method == "back":
                            break  # Go back to request type selection
                        else:
                            break  # Valid method selected, proceed
                    
                    if webdav_method == "back":
                        continue  # Stay in request type loop
                
                # Handle Header test request type
                elif request_type == "header":
                    while True:
                        header_test_type = choose_header_test_type()
                        if header_test_type == "back":
                            break  # Go back to request type selection
                        else:
                            break  # Valid type selected, proceed
                    
                    if header_test_type == "back":
                        continue  # Stay in request type loop
                    
                    # Get headers based on test type
                    if header_test_type == "single":
                        custom_headers = get_single_header()
                    else:  # multi
                        custom_headers = get_multi_headers()
                
                # Handle wget request type
                elif request_type == "wget":
                    while True:
                        wget_mode = choose_wget_mode()
                        if wget_mode == "back":
                            break  # Go back to request type selection
                        else:
                            break  # Valid mode selected, proceed
                    
                    if wget_mode == "back":
                        continue  # Stay in request type loop
                    
                    # Get headers if wget with headers mode
                    if wget_mode == "headers":
                        print("\nHow many headers?")
                        print("1. Single header")
                        print("2. Multiple headers")
                        choice = input("Enter option (1 or 2): ").strip()
                        if choice == "1":
                            wget_headers = get_single_header()
                        else:
                            wget_headers = get_multi_headers()
                
                # Directory mode menu
                return_to_http_mode = False
                while True:
                    directory_mode = choose_directory_mode()
                    if directory_mode == "back":
                        break  # Go back to request type selection
                    else:
                        # All selections complete, build and run command
                        try:
                            normalized_directory = directory.strip().strip("/")
                            final_directory = apply_directory_encoding(normalized_directory, directory_mode)
                            target_url = normalize_target_url(website_url, final_directory)
                        except ValueError as exc:
                            print(f"Error: {exc}")
                            return 1

                        # Ask for verbose output preference
                        verbose = get_verbose_output()
                        
                        # Ask for user agent preference
                        user_agent = choose_user_agent()
                        
                        # Build command based on request type
                        if request_type == "raw":
                            # Extract hostname for Host header
                            hostname = extract_hostname(website_url)
                            # Build raw HTTP request
                            http_version = {"--http1.1": "HTTP/1.1", "--http2": "HTTP/2", "-0": "HTTP/1.0"}.get(http_mode, "HTTP/1.1")
                            # Add User-Agent header if specified
                            ua_header = f"User-Agent: {user_agent}\\r\\n" if user_agent else ""
                            
                            if raw_format == "extra-spaces":
                                raw_request = f"GET  /{final_directory}  {http_version}\\r\\nHost: {hostname}\\r\\n{ua_header}\\r\\n"
                            elif raw_format == "tab-separated":
                                raw_request = f"GET\\t/{final_directory}\\t{http_version}\\r\\nHost: {hostname}\\r\\n{ua_header}\\r\\n"
                            else:  # standard
                                raw_request = f"GET /{final_directory} {http_version}\\r\\nHost: {hostname}\\r\\n{ua_header}\\r\\n"
                            
                            # Handle slow send
                            if slow_send == "yes":
                                # Build request line and headers separately
                                if raw_format ==  "extra-spaces":
                                    request_line = f"GET  /{final_directory}  {http_version}\\r\\n"
                                elif raw_format == "tab-separated":
                                    request_line = f"GET\\t/{final_directory}\\t{http_version}\\r\\n"
                                else:  # standard
                                    request_line = f"GET /{final_directory} {http_version}\\r\\n"
                                
                                host_header = f"Host: {hostname}\\r\\n{ua_header}\\r\\n"
                                
                                # Split request line into chunks, keep host header whole
                                request_chunks = split_request_into_chunks(request_line, 2)
                                commands = []
                                for chunk in request_chunks:
                                    commands.append(["bash", "-c", f"echo -e \"{chunk}\" | timeout {timeout_duration} nc {hostname} {port}"])
                                # Add final host header as complete chunk
                                commands.append(["bash", "-c", f"echo -e \"{host_header}\" | timeout {timeout_duration} nc {hostname} {port}"])
                                command = commands
                                command.append(("sleep", sleep_duration))  # Attach sleep duration
                            else:
                                command = [["bash", "-c", f"echo -e \"{raw_request}\" | nc {hostname} {port}"]]  # Wrap in list for consistency
                        elif request_type == "tls":
                            hostname = extract_hostname(website_url)
                            cipher = "ECDHE-RSA-AES128-GCM-SHA256"  # Default cipher suite
                            
                            if tls_tool == "curl":
                                curl_cmd = ["curl", "--tls-max", "1.2", "--ciphers", cipher]
                                if http_mode:
                                    curl_cmd.append(http_mode)
                                if user_agent:
                                    curl_cmd.extend(["--user-agent", user_agent])
                                if verbose:
                                    curl_cmd.append("-v")
                                curl_cmd.append(target_url)
                                command = [curl_cmd]
                            else:  # openssl
                                ua_line = f"User-Agent: {user_agent}\\n" if user_agent else ""
                                http_request = f"GET /{final_directory} HTTP/1.1\\nHost: {hostname}\\n{ua_line}\\n"
                                debug_flag = " -debug" if verbose else ""
                                command = [["bash", "-c", f"openssl s_client -connect {hostname}:443 -servername {hostname} -cipher '{cipher}'{debug_flag} <<< \"{http_request}\""]]
                        elif request_type == "header":
                            curl_cmd = ["curl"]
                            if http_mode:
                                curl_cmd.append(http_mode)
                            # Add custom headers
                            for header_name, header_value in custom_headers:
                                curl_cmd.extend(["-H", f"{header_name}: {header_value}"])
                            curl_cmd.append("-I")
                            if user_agent:
                                curl_cmd.extend(["--user-agent", user_agent])
                            if verbose:
                                curl_cmd.append("-v")
                            curl_cmd.append(target_url)
                            command = [curl_cmd]
                        elif request_type == "wget":
                            if wget_mode == "simple":
                                # Simple wget with no-check-certificate and spider
                                wget_cmd = "wget --no-check-certificate --spider"
                                if user_agent:
                                    wget_cmd += f" --user-agent \"{user_agent}\""
                                wget_cmd += f" {target_url} 2>&1 | head -5"
                                command = [["bash", "-c", wget_cmd]]
                            else:  # headers
                                # wget with headers
                                wget_cmd_parts = ["wget", "--no-check-certificate", "--spider"]
                                if user_agent:
                                    wget_cmd_parts.append(f"--user-agent \"{user_agent}\"")
                                for header_name, header_value in wget_headers:
                                    wget_cmd_parts.append(f'--header="{header_name}: {header_value}"')
                                wget_cmd_parts.append(target_url)
                                wget_cmd = " ".join(wget_cmd_parts) + " 2>&1"
                                command = [["bash", "-c", wget_cmd]]
                        elif request_type == "webdav":
                            curl_cmd = ["curl"]
                            if http_mode:
                                curl_cmd.append(http_mode)
                            curl_cmd.extend(["-X", webdav_method])
                            if user_agent:
                                curl_cmd.extend(["--user-agent", user_agent])
                            if verbose:
                                curl_cmd.append("-v")
                            curl_cmd.append(target_url)
                            command = [curl_cmd]
                        else:  # standard
                            curl_cmd = ["curl"]
                            if http_mode:
                                curl_cmd.append(http_mode)
                            curl_cmd.append("-I")
                            if user_agent:
                                curl_cmd.extend(["--user-agent", user_agent])
                            if verbose:
                                curl_cmd.append("-v")
                            curl_cmd.append(target_url)
                            command = [curl_cmd]

                        print("\nRunning command:")
                        if request_type == "raw":
                            # Show the actual command that will be executed
                            hostname = extract_hostname(website_url)
                            http_version = {"--http1.1": "HTTP/1.1", "--http2": "HTTP/2", "-0": "HTTP/1.0"}.get(http_mode, "HTTP/1.1")
                            # Add User-Agent header if specified
                            ua_header = f"User-Agent: {user_agent}\\r\\n" if user_agent else ""
                            
                            if raw_format == "extra-spaces":
                                raw_request = f"GET  /{final_directory}  {http_version}\\r\\nHost: {hostname}\\r\\n{ua_header}\\r\\n"
                            elif raw_format == "tab-separated":
                                raw_request = f"GET\\t/{final_directory}\\t{http_version}\\r\\nHost: {hostname}\\r\\n{ua_header}\\r\\n"
                            else:  # standard
                                raw_request = f"GET /{final_directory} {http_version}\\r\\nHost: {hostname}\\r\\n{ua_header}\\r\\n"
                            
                            if slow_send == "yes":
                                # Build request line and headers separately for chunking
                                if raw_format == "extra-spaces":
                                    request_line = f"GET  /{final_directory}  {http_version}\\r\\n"
                                elif raw_format == "tab-separated":
                                    request_line = f"GET\\t/{final_directory}\\t{http_version}\\r\\n"
                                else:  # standard
                                    request_line = f"GET /{final_directory} {http_version}\\r\\n"
                                
                                host_header = f"Host: {hostname}\\r\\n{ua_header}\\r\\n"
                                request_chunks = split_request_into_chunks(request_line, 2)
                                for i, chunk in enumerate(request_chunks, 1):
                                    print(f"[{i}/{len(request_chunks) + 1}] echo -e \"{chunk}\" | timeout {timeout_duration} nc {hostname} {port}")
                                print(f"[{len(request_chunks) + 1}/{len(request_chunks) + 1}] echo -e \"{host_header}\" | timeout {timeout_duration} nc {hostname} {port}")
                            else:
                                print(f"echo -e \"{raw_request}\" | nc {hostname} {port}")
                        elif request_type == "tls":
                            hostname = extract_hostname(website_url)
                            cipher = "ECDHE-RSA-AES128-GCM-SHA256"
                            if tls_tool == "curl":
                                http_flag = f" {http_mode}" if http_mode else ""
                                ua_flag = f" --user-agent \"{user_agent}\"" if user_agent else ""
                                verbose_flag = " -v" if verbose else ""
                                print(f"curl --tls-max 1.2 --ciphers '{cipher}'{http_flag}{ua_flag}{verbose_flag} {target_url}")
                            else:  # openssl
                                ua_line = f"User-Agent: {user_agent}\\n" if user_agent else ""
                                verbose_flag = " -debug" if verbose else ""
                                print(f"openssl s_client -connect {hostname}:443 -servername {hostname} -cipher '{cipher}'{verbose_flag} <<< \"GET /{final_directory} HTTP/1.1\\nHost: {hostname}\\n{ua_line}\\n\"")
                        elif request_type == "wget":
                            if wget_mode == "simple":
                                ua_flag = f" --user-agent \"{user_agent}\"" if user_agent else ""
                                print(f"wget --no-check-certificate --spider{ua_flag} {target_url} 2>&1 | head -5")
                            else:  # headers
                                ua_flag = f" --user-agent \"{user_agent}\"" if user_agent else ""
                                header_flags = " ".join([f'--header="{h[0]}: {h[1]}"' for h in wget_headers])
                                print(f"wget --no-check-certificate --spider{ua_flag} {header_flags} {target_url} 2>&1")
                        else:
                            if isinstance(command[0], list):
                                print(" ".join(command[0]))
                            else:
                                print(" ".join(command))
                        print()

                        try:
                            # Handle multiple commands for slow send
                            if isinstance(command[0], list) and len(command) > 1:
                                # Extract sleep duration if attached
                                sleep_time = 0
                                if command[-1] == ("sleep", sleep_duration) or (isinstance(command[-1], tuple) and command[-1][0] == "sleep"):
                                    sleep_time = command[-1][1]
                                    command = command[:-1]  # Remove the sleep tuple
                                
                                # Execute each command with sleep between them
                                for i, cmd in enumerate(command):
                                    completed = subprocess.run(cmd, check=False)
                                    if i < len(command) - 1 and sleep_time > 0:  # Sleep between commands, not after last
                                        time.sleep(sleep_time)
                                return_to_http_mode = True
                                break
                            else:
                                cmd = command[0] if isinstance(command[0], list) else command
                                completed = subprocess.run(cmd, check=False)
                            return_to_http_mode = True
                            break
                        except KeyboardInterrupt:
                            print("\n\nExiting gracefully... (￣3￣)╭")
                            return 0
                        except FileNotFoundError:
                            if request_type == "raw":
                                print("Error: nc (netcat) is not installed or not found in PATH.")
                            elif request_type == "tls" and tls_tool == "openssl":
                                print("Error: openssl is not installed or not found in PATH.")
                            elif request_type == "wget":
                                print("Error: wget is not installed or not found in PATH.")
                            else:
                                print("Error: curl is not installed or not found in PATH.")
                            return_to_http_mode = True
                            break

                if return_to_http_mode:
                    break  # Go back to HTTP mode selection after command execution
                
                # If we reach here, user went back from directory mode
                break  # Go back to HTTP mode
    except KeyboardInterrupt:
        print("\n\nExiting gracefully... (￣3￣)╭")
        return 0


if __name__ == "__main__":
    # Check for --help flag
    if "--help" in sys.argv or "-h" in sys.argv:
        try:
            # Get the directory where waffle.py is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            readme_path = os.path.join(script_dir, "README.md")
            
            with open(readme_path, "r") as f:
                print(f.read())
            sys.exit(0)
        except FileNotFoundError:
            print("Error: README.md not found.")
            print("\nUsage: python3 waffle.py")
            print("Interactive WAF bypass testing tool.")
            sys.exit(1)
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nExiting gracefully... (￣3￣)╭")
        sys.exit(0)
