Devices = []
General = []
Device_Names = set([])

def is_this_device(some_string):
    is_device = False
    if some_string.startswith("app/processor/devices/"):
        is_device = True
    elif some_string.startswith("tests/processor/") and \
        some_string.endswith("_processor_test.py"):
        is_device = True
    return is_device

def populate_device_names(some_string):
    if some_string.startswith("app/processor/devices/"):
        some_string = some_string[22:]
        if some_string.find("/") > 0:
            some_string = some_string[:some_string.find("/")]
            Device_Names.add(some_string)
    elif some_string.startswith("tests/processor/") and \
        some_string.endswith("_processor_test.py"):
        some_string = some_string[16:]
        if some_string.find("_processor_test.py") > 0:
            some_string = some_string[:some_string.find("_processor_test.py")]
            Device_Names.add(some_string)

with open("changed_files.txt") as fp:
    Lines = fp.readlines()
    for line in Lines:
        line_stripped = line.strip('\n')
        if is_this_device(line_stripped):
            Devices.append(line_stripped)
        else:
            General.append(line_stripped)

print(Devices)
print(General)

with open("run_tests.sh","w") as file:
    file.write("#!/bin/sh\n")
    if len(General) > 0:
        # file.write("pytest")
        file.write("echo 'General files changed'")
    else:
        for device in Devices:
            populate_device_names(device)
        for device in Device_Names:
            # file.write(f"pytest tests/processor/{device}_processor_test.py\n")
            file.write(f"echo '{device} files changed'\n")

print(Device_Names)