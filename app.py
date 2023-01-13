import tkinter as tk
from tkinter import filedialog, messagebox, OptionMenu
import os
import serial.tools.list_ports
import re
import shutil

path_to_arduino=''

def generate_makefile(arduino_path, ino_file, elf_file):
    global arduino_cores
    arduino_cores = os.path.join(arduino_path, "hardware", "arduino", "avr", "cores", "arduino")
    arduino_variants = os.path.join(arduino_path, "hardware", "arduino", "avr", "standard")
    core_path = os.path.join(arduino_cores, "core.a")

    with open("Makefile", "w") as makefile:
        makefile.write("ARDUINO_PATH = {}\n".format(arduino_path))
        makefile.write("ARDUINO_CORES = {}\n".format(arduino_cores))
        makefile.write("ARDUINO_VARIANTS = {}\n".format(arduino_variants))
        makefile.write("ARDUINO_CORE = {}\n".format(core_path))
        makefile.write("INO_FILE = {}\n".format(ino_file))
        makefile.write("ELF_FILE = {}\n\n".format(elf_file))
        makefile.write("all: $(ELF_FILE)\n\n")
        makefile.write("$(ELF_FILE): $(INO_FILE)\n")
        makefile.write("\tavr-g++ -mmcu=atmega328p -DARDUINO=105 -DF_CPU=16000000L")
        makefile.write(" -I$(ARDUINO_CORES) -I$(ARDUINO_VARIANTS) -Os -fno-exceptions")
        makefile.write(" -ffunction-sections -fdata-sections -Wl,--gc-sections -g -Wall -Wextra")
        makefile.write(" -x c++ -include Arduino.h $(INO_FILE) -x none $(ARDUINO_CORE) -lm -o $(ELF_FILE)\n\n")
        makefile.write(".PHONY: clean\n")
        makefile.write("clean:\n")
        makefile.write("\trm -f $(ELF_FILE)\n")

def ino_to_cpp(ino_file):
    arduino_header = "#include <Arduino.h>\n"
    function_prototypes = ""
    cpp_file = ""

    with open(ino_file, "r") as file:
        contents = file.read()

    cpp_file += arduino_header

    # Forward declarations
    functions = re.findall(r"void\s+\w+\s*\(.*\)\s*{", contents)
    for function in functions:
        if "setup" not in function and "loop" not in function:
            function_prototypes += function + ";\n"

    cpp_file += function_prototypes
    cpp_file += contents
    with open(ino_file.replace(".ino", ".cpp"), "w") as file:
        file.write(cpp_file)

def generate_code():
    # read the sketch file
    with open(sketch_file, "r") as f:
        sketch_lines = f.readlines()
    check= False

    # replace the parameter values in the sketch
    for i, line in enumerate(sketch_lines):
        if variable_type.get()+" "+parameter_name.get() in line:
            sketch_lines[i] = f"{variable_type.get()} {parameter_name.get()} = {parameter_value.get()}\n"
            check = True

    # write the modified sketch to a new file
    with open("modified_sketch.ino", "w") as f:
        f.writelines(sketch_lines)
    
    #check if successful
    if check:
        messagebox.showinfo("Success!", f"{parameter_name.get()} has been changed to {parameter_value.get()}")
        ino_to_cpp("modified_sketch.ino")
        generate_makefile(path_to_arduino, "modified_sketch.ino", "modified_sketch.elf")
        main_cpp = os.path.join(arduino_cores, "main.cpp")
        with open("modified_sketch.ino", "ab") as f:
            with open(main_cpp, "rb") as main_f:
                 shutil.copyfileobj(main_f, f)
    else:
        messagebox.showinfo("Warning!", "No such variable with the specified type, please retry!")

def change_ino_file():
    global sketch_file
    sketch_file = filedialog.askopenfilename(title="Select Arduino sketch")

def select_arduino_path():
    global path_to_arduino
    path_to_arduino = filedialog.askdirectory(title = "Select Arduino Installation Folder")

root = tk.Tk()
root.title("Arduino Code Generator")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

options_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Change .ino file", command=change_ino_file)
options_menu.add_command(label="Change Arduino folder path", command=select_arduino_path)

variable_type_label = tk.Label(root, text="Variable Type:")
variable_type_label.pack()

variable_type = tk.StringVar()
variable_type_options = ["int", "float", "double", "char"]
variable_type_dropdown = OptionMenu(root, variable_type, *variable_type_options)
variable_type.set("int")
variable_type_dropdown.pack()

com_port_label = tk.Label(root, text="COM Port:")
com_port_label.pack()

com_port_options = [port.device for port in serial.tools.list_ports.comports()]
com_port_var = tk.StringVar()
com_port_dropdown = OptionMenu(root, com_port_var, *com_port_options)
com_port_var.set(com_port_options[0])
com_port_dropdown.pack()
if com_port_var.get() != "Select a COM port":
    com_port = com_port_var.get()
else:
    messagebox.showerror("Error", "No COM port selected.")

parameter_name_label = tk.Label(root, text="Parameter Name:")
parameter_name_label.pack()

parameter_name = tk.StringVar()
parameter_name_entry = tk.Entry(root, textvariable=parameter_name)
parameter_name_entry.pack()

parameter_value_label = tk.Label(root, text="Parameter Value:")
parameter_value_label.pack()

parameter_value = tk.StringVar()
parameter_value_entry = tk.Entry(root, textvariable=parameter_value)
parameter_value_entry.pack()

generate_code_button = tk.Button(root, text="Generate Code", command=generate_code)
generate_code_button.pack()

root.mainloop()


