from pygments.formatters import NullFormatter
from pygments import highlight
from pygments.lexers import guess_lexer
from PIL import Image
import traceback
import platform
import configparser
import pytesseract as pt
import autopep8
import os

config = configparser.ConfigParser()
config.read("settings.ini")
options = autopep8.parse_args(['--ignore=W191,E101,E111', '--aggressive', '--global-config', 'settings.ini', '-'])


def get_operating_system():
    system_name = platform.system()
    if system_name == "Windows":
        return "Windows"
    elif system_name == "Linux":
        return "Linux"
    elif system_name == "Darwin":
        return "macOS"
    else:
        return "Unknown"

def get_text_info(image):
    # Open the image
    img = Image.open(image)

    # Use pytesseract to extract data from the image
    data = pt.image_to_data(img, output_type=pt.Output.DICT, config=config['CDC']['recognized_config'])

    # Get coordinates for each line of text
    line_info = []
    current_line = []
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 0:  # Make sure there is non-zero confidence in text detection
            left, top, width, height = int(data['left'][i]), int(data['top'][i]), int(data['width'][i]), int(data['height'][i])
            text = data['text']
            current_line.append((left, top, width, height, text))
        else:
            if current_line:
                line_info.append(current_line[0])  # Take only the first coordinate of each line
                current_line = []

    # Create a list with information about each line
    result_list = []
    for i, entry in enumerate(line_info):
        left, top, _, _, text = entry
        line_info_dict = {
            'line_number': i + 1,
            'text': text,
            'coordinate_X': left,
        }
        result_list.append(line_info_dict)

    return result_list



class Code: 
    def __init__(self, img):
        try:
            # Set Tesseract path for Windows
            if config['CDC']['your_system'].lower() == 'windows':
                pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            else:
                pass

            # Extract text from the image and clean empty lines
            recognized_text = pt.image_to_string(Image.open(img), config=config['CDC']['recognized_config'])
            recognized_text = "\n".join(line for line in recognized_text.splitlines() if line.strip())
            recognized_text_with_line_numbers = [(i+1, line, '') for i, line in enumerate(recognized_text.split('\n'))]

            # Attempt to guess the language
            lexer = guess_lexer(recognized_text)

            # If the language is known, adjust the indentation
            if lexer.name:
                if lexer.name == 'Python':
                    info_list = get_text_info(img)
                    inaccuracy = int(config['CDC']['inaccuracy'])

                    # Deduplicate X-coordinates to handle indentation
                    unique_values = []
                    for entry in info_list:
                        value_found = False
                        for value in unique_values:
                            if abs(entry['coordinate_X'] - value) <= inaccuracy:
                                value_found = True
                                break
                        if not value_found:
                            unique_values.append(entry['coordinate_X'])
                    value_index_mapping = {value: index for index, value in enumerate(unique_values)}
                    for entry in info_list:
                        for value, index in value_index_mapping.items():
                            if abs(entry['coordinate_X'] - value) <= inaccuracy:
                                entry['coordinate_X'] = index

                    # Update 'coordinate_X' values in the first list
                    for i, (line_num, text, _) in enumerate(recognized_text_with_line_numbers):
                        matching_info = next((info for info in info_list if info['line_number'] == line_num), None)
                        if matching_info:
                            recognized_text_with_line_numbers[i] = (line_num, text, matching_info['coordinate_X'])
                        else:
                            # Handle case where 'line_num' is not found in info_list
                            recognized_text_with_line_numbers[i] = (line_num, text, 0)  # or another default value

                    # Output result
                    Code_list = recognized_text_with_line_numbers
                    for index, item in enumerate(Code_list):
                        Code_list[index] = '\t' * item[2] + item[1]

                    # Output result
                    recognized_text = '\n'.join(Code_list)

                # Highlight the code with Pygments
                code = highlight(recognized_text, lexer, NullFormatter())

                # Optionally, format the code with autopep8
                if config['CDC']['use_autopep8'] == 'True':
                    code = autopep8.fix_code(code, options=options)
                else:
                    pass

                # Save information about the detected language, filename, and formatted code
                self.detect_lang = lexer.name
                self.filename = lexer.filenames
                self.temp_save = code
            else:
                print('Error:\n', traceback.format_exc())
        except Exception as e:
            error_message = f'error: {e}\n'
            with open('log.txt', 'a') as error_file:
                error_file.write(error_message)

    # once_system_definer
    def once_system_definer():
        flag_file = "command_ran.flag"
        if not os.path.exists(flag_file):
            os_name = get_operating_system()
            config["CDC"]["your_system"] = os_name.lower()
            with open("settings.ini", "w") as config_file:
                config.write(config_file)
            with open(flag_file, "w") as flag:
                flag.write("Command executed")

    # Save the file
    @staticmethod
    def compile_and_save(code_text, output_file):
        with open(output_file, 'w') as f:
            f.write(code_text)


