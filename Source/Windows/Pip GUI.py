import os
os.system("python -m pip install tk")
os.system("python -m pip install pypisearch")
import tkinter as tk
from tkinter import ttk
import subprocess



def execute_pip_command(command):
    try:
        result = subprocess.check_output(f"py -m pip {command}", stderr=subprocess.STDOUT, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        result = e.output
    output_text.configure(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    output_text.configure(state='disabled')

def search():
    name = package_entry.get()
    try:
        result = subprocess.check_output(f"py -m pypisearch {name}", stderr=subprocess.STDOUT, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        result = e.output
    output_text.configure(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    output_text.configure(state='disabled')
    global show_term_out
    show_term_out=True
    toggleTerminal()


def install_package():
    package_name = package_entry.get()
    execute_pip_command(f"install {package_name}")

def copy_text():
    root.clipboard_clear()
    root.clipboard_append(output_text.get("sel.first", "sel.last"))

def paste_text():
    text = root.clipboard_get()
    package_entry.insert(tk.INSERT, text)

def uninstall_package():
    package_name = package_entry.get()
    execute_pip_command(f"uninstall -y {package_name}")
    
def list_packages():
    execute_pip_command("list")
    global show_term_out
    show_term_out=True
    toggleTerminal()

def open_about():
    about_window = tk.Toplevel(root)
    about_window.title("About Pip GUI")
    title_widget = ttk.Label(about_window, text="About Pip GUI\n", font=("Arial", 18))
    about_text = ttk.Label(about_window, text="Pip GUI is a graphical interface for using pip.")
    label3 = ttk.Label(about_window, text=" Pip GUI was made using Python, Pip, Tkinter, and Pypisearch.", justify="center")
    label4 = ttk.Label(about_window, text="Useful for novice users and anyone who wants a graphical to interact with pip.")
    title_widget.pack()
    about_text.pack()
    label4.pack()
    label3.pack()
    label2.pack()
    


show_term_out = False

def toggleTerminal():
    global show_term_out
    show_term_out = not show_term_out
    if show_term_out:
        output_text.grid_remove()
        showTerminal.config(text="Show terminal output ↓")
    else:
        output_text.grid(column=0, row=3, columnspan=5, padx=5, pady=5)
        showTerminal.config(text="Hide terminal output ↑")


root = tk.Tk()
root.title("Pip GUI")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

package_label = ttk.Label(mainframe, text="Package:")
package_label.grid(column=0, row=0, padx=5, pady=5)

package_entry = ttk.Entry(mainframe)
package_entry.grid(column=1, row=0, padx=5, pady=5)

install_button = ttk.Button(mainframe, text="Install", command=install_package)
install_button.grid(column=2, row=0, padx=5, pady=5)

uninstall_button = ttk.Button(mainframe, text="Uninstall", command=uninstall_package)
uninstall_button.grid(column=3, row=0, padx=5, pady=5)

list_button = ttk.Button(mainframe, text="List", command=list_packages)
list_button.grid(column=4, row=0, padx=5, pady=5)

search_button = ttk.Button(mainframe, text="Search", command=search)
search_button.grid(column=5, row=0, padx=5, pady=5)

output_text = tk.Text(mainframe, wrap=tk.WORD, width=80, height=20, state="disabled")
output_text.focus()

showTerminal = ttk.Button(mainframe, text="", command=toggleTerminal)
showTerminal.grid(column=0, row=1, columnspan=5, padx=5, pady=5)
toggleTerminal()

menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar)
menubar.add_cascade(label="Package", menu=file_menu)
file_menu.add_command(label="Install package", command=install_package)
file_menu.add_command(label="Uninstall package", command=uninstall_package)
file_menu.add_command(label="List installed packages", command=list_packages)

edit_menu = tk.Menu(menubar)
menubar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)

help_menu = tk.Menu(menubar)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=open_about)


scrollbar = ttk.Scrollbar(mainframe, orient="vertical", command=output_text.yview)
scrollbar.grid(column=5, row=1, padx=(0, 5), pady=5, sticky=(tk.N, tk.S))
output_text["yscrollcommand"] = scrollbar.set

root.mainloop()
