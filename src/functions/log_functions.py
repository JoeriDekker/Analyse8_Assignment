from datetime import datetime

from functions.encrypt_functions import EncryptFunc

import os

class LogFunc:
    def append_to_file(username, activity, additional_info, suspicious):

        if os.path.exists('log.txt'):
            EncryptFunc.decrypt_file()

        with open("log.txt", 'a+') as file:
            file.seek(0)
            if not file.readline().startswith('No.'):
                file.write('No., Date, Time, Username, Description of activity, Additional Information, Suspicious\n')
            no = len(file.readlines()) + 1
            date = datetime.now().strftime('%Y-%m-%d')
            time = datetime.now().strftime('%H:%M:%S')
            log_entry = f"{no}, {date}, {time}, {username}, {activity}, {additional_info}, {suspicious}\n"
            file.write(log_entry)
        
        EncryptFunc.encrypt_file()
        return

    def text_wrapper(text, width):
        lines = []
        while len(text) > width:
            space_index = text.rfind(' ', 0, width)
            if space_index == -1: 
                space_index = width
            lines.append(text[:space_index])
            text = text[space_index:].strip()
        lines.append(text)
        return lines

    def read_log():
        EncryptFunc.decrypt_file()
        if not os.path.exists('log.txt'):
            print("Log file not found.")
            return
        
        with open("log.txt", 'r') as file:
            lines = file.readlines()
            # Define the headers manually
            widths = [5, 12, 10, 15, 30, 30, 10]
            for line in lines:
                fields = line.strip().split(', ')
                wrapped_fields = [LogFunc.text_wrapper(field, width) for field, width in zip(fields, widths)]
                
                # Find the maximum number of lines for the current row
                max_lines = max(len(field) for field in wrapped_fields)
                
                # Print each line of the wrapped text
                for i in range(max_lines):
                    row = []
                    for field in wrapped_fields:
                        if i < len(field):
                            row.append(field[i])
                        else:
                            row.append('')
                    print("| {:<5} | {:<12} | {:<10} | {:<15} | {:<30} | {:<30} | {:<10} |".format(*row))
                print("-"*134)
        EncryptFunc.encrypt_file()