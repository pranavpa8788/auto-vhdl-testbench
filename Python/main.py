import os
import re
import typing

# os.path.isfile() does not check for case sensitivity, probably because file systems are case insensitive in general
# TODO
# Fix middle port regex
# Fix return values

file_extensions = [".vhd", ".vhdl"]

def create_testbench(entity_name: str):
    entity_file = check_entity(entity_name)
    port_list = find_ports(entity_file)
    for port in port_list:
        print(f"Ports found are: '{port}'")

def find_ports(entity_file: str) -> typing.List[str]:
    with open(entity_file, "r") as file:
        file_data = file.readlines()
    for line_count, line in enumerate(file_data):
        file_data[line_count] = line.replace('\n', '')

    within_entity_declaration = False
    within_port_declaration = False
    first_port_found = False
    last_port_found = False

    entity_declaration_pattern = r"^entity"
    port_declaration_pattern = r"port\("
    first_port_declaration_pattern = r"(\()([^;]*)?"
    middle_port_declaration_pattern = r"((?:(?!\s{1,}))[^;]*)?((?:(?<!\)));)x"
    last_port_declaration_pattern = r"((?:(?!\s{1,}))[^;]*)?(\);)"

    port_list = []

    for line_count, line in enumerate(file_data):
        if (
            within_entity_declaration is False and 
            within_port_declaration is False and
            first_port_found is False and
            last_port_found is False
            ):

            entity_match = re.search(entity_declaration_pattern, line)
            if bool(entity_match) is True:
                within_entity_declaration = True

        if (
            within_entity_declaration is True and 
            within_port_declaration is False and
            first_port_found is False and
            last_port_found is False
            ):

            port_match = re.search(port_declaration_pattern, line)
            if bool(port_match) is True:
                within_port_declaration = True

        if (
            within_entity_declaration is True and 
            within_port_declaration is True and
            first_port_found is False and
            last_port_found is False
            ):

            first_port_match = re.findall(first_port_declaration_pattern, line)
            if len(first_port_match) > 0:
                first_port_content = first_port_match[0][1]
                first_port_found = True
                if bool(first_port_content.strip()) is True:
                    port_list.append(first_port_content)

            last_port_match = re.findall(last_port_declaration_pattern, line)
            if len(last_port_match) > 0:
                last_port_content = last_port_match[0][0]
                last_port_found = True
                if bool(last_port_content.strip()) is True:
                    port_list.append(last_port_content)

                middle_port_match = re.findall(middle_port_declaration_pattern, line)
                if len(middle_port_match) > 0:
                    for port_match in middle_port_match[0]:
                        port_list.append(port_match)
                return port_list

        if (
            within_port_declaration is True and
            within_port_declaration is True and
            first_port_found is True and
            last_port_found is False
            ):

            last_port_match = re.findall(last_port_declaration_pattern, line)
            if len(last_port_match) > 0:
                last_port_content = last_port_match[0][0]
                last_port_found = True
                if bool(last_port_content.strip()) is True:
                    port_list.append(last_port_content)
                return port_list

            middle_port_match = re.findall(middle_port_declaration_pattern, line)
            if len(middle_port_match) > 0:
                for port_match in middle_port_match:
                    for port in port_match:
                        if port != ";" and bool(port.strip()) is True:
                            port_list.append(port)

def check_entity(entity_name: str) -> str:
    """Checks different extension files for the given entity"""

    for extension in file_extensions:
        entity_file = entity_name + extension

        if os.path.isfile(entity_file) is True:
            return entity_file

    raise Exception(f"FileNotFoundError: The {entity_name} entity source file could not be found")

if __name__ == "__main__":
    create_testbench("test")
