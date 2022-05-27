import os


General = []
All_Devices = []
Device_Names = set([])

def is_in_app_processor_devices(some_string):
    return some_string.startswith("app/processor/devices/")

def is_in_tests(some_string):
    return some_string.startswith("tests/processor/") and \
        some_string.endswith("_processor_test.py")

def is_in_examples(some_string):
    return some_string.startswith("examples/")

def is_this_device(some_string):
    return is_in_app_processor_devices(some_string) or \
            is_in_tests(some_string) or \
            is_in_examples(some_string)

def populate_device_names(some_string):
    if is_in_app_processor_devices(some_string):
        some_string = some_string[22:]
        if some_string.find("/") > 0:
            some_string = some_string[:some_string.find("/")]
            Device_Names.add(some_string)
    elif is_in_tests(some_string):
        some_string = some_string[16:]
        if some_string.find("_processor_test.py") > 0:
            some_string = some_string[:some_string.find("_processor_test.py")]
            Device_Names.add(some_string)

path_to_all_devices = 'tests/processor'
for path_to_all_devices, dirs, files in os.walk(path_to_all_devices):
    for file in files:
        if file.endswith("_processor_test.py"):
            file = file.replace("_processor_test.py", "")
            All_Devices.append(file)
    break

with open("changed_files.txt") as file:
    Lines = file.readlines()
    for line in Lines:
        line_stripped = line.strip('\n')
        if is_this_device(line_stripped):
            populate_device_names(line_stripped)
        else:
            General.append(line_stripped)

with open("run_tests.sh","w") as file:
    file.write("#!/bin/sh\n")
    if len(General) > 0:
        file.write("echo 'Changed files could affect entire program'\n")
        for device in All_Devices:
            file.write(f"echo 'Changed files could affect {device} part of the program'\n")
    else:
        for device in Device_Names:
            file.write(f"echo 'Changed files could affect {device} part of the program'\n")
