# linux
# #!/bin/bash
# # Script to find and delete all .php files in the current directory and subdirectories

# log_deleted_files() {
#     local file="$1"
#     echo "$file" >> deleted_files.log
# }

# total_files=0
# total_size=0

# while IFS= read -r -d '' file
# do
#     file_size=$(stat -c%s "$file")
#     total_files=$((total_files + 1))
#     total_size=$((total_size + file_size))
#     log_deleted_files "$file"
#     rm -f "$file"
# done < <(find . -type f -name "*.php" -print0)

# echo "Total files deleted: $total_files"
# echo "Total size freed: $total_size bytes"



# windows
# @echo off
# REM Script to find and delete all .php files in the current directory and subdirectories

# setlocal enabledelayedexpansion
# set "log_file=deleted_files.log"
# echo. > "%log_file%"

# set /a total_files=0
# set /a total_size=0

# for /r %%f in (*.php) do (
#     set /a total_files+=1
#     for %%A in (%%f) do set /a total_size+=%%~zA
#     echo %%f >> "%log_file%"
#     del "%%f"
# )

# echo Total files deleted: %total_files%
# echo Total size freed: %total_size% bytes
# 
# 
# 
# 
# 
import os
import shutil
from tkinter import Tk, filedialog, StringVar, messagebox, Entry
from tkinter.ttk import Button, Label, Style

deleted_files_log = []
total_files = 0
total_size = 0

def select_folder():
    folder = filedialog.askdirectory()
    folder_path.set(folder)

def delete_files():
    global total_files, total_size
    ext = extension.get()
    name = file_name.get()
    if not ext.startswith('.'):
        ext = '.' + ext
    folder = folder_path.get()
    log_file_path = os.path.join(folder, "deleted_files.log")
    
    total_files = 0
    total_size = 0
    deleted_files_log.clear()
    
    for root, _, files in os.walk(folder):
        for file in files:
            if (file.endswith(ext) and name in file) or (ext == "." and name == file):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                total_size += file_size
                total_files += 1
                deleted_files_log.append(file_path)
    
    if total_files == 0:
        messagebox.showinfo("Нет файлов", "Нет файлов для удаления.")
        return
    
    # Confirm deletion
    if not messagebox.askyesno("Подтверждение", f"Будет удалено {total_files} файлов, освободится {total_size} байт. Продолжить?"):
        return
    
    # Delete files and save log
    with open(log_file_path, "w") as log_file:
        for path in deleted_files_log:
            try:
                os.remove(path)
                log_file.write(f"{path}\n")
            except Exception as e:
                print(f"Не удалось удалить {path}: {e}")
    
    messagebox.showinfo("Завершено", f"Удалено {total_files} файлов, освобождено {total_size} байт. Лог сохранён в {log_file_path}.")
    restore_button.config(state="normal")
    update_status()

def restore_files():
    for file_path in deleted_files_log:
        try:
            shutil.copy(file_path + ".bak", file_path)
            os.remove(file_path + ".bak")
        except Exception as e:
            print(f"Не удалось восстановить {file_path}: {e}")
    messagebox.showinfo("Восстановлено", "Файлы восстановлены.")
    update_status()

def update_status():
    status_label.config(text=f"Файлы: {total_files} | Объём: {total_size} байт")

# GUI setup
root = Tk()
root.title("Удаление файлов")
root.configure(bg="#2e2e2e")

folder_path = StringVar()
extension = StringVar()
file_name = StringVar()

style = Style()
style.theme_use('alt')
style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
style.configure("TButton", background="#444444", foreground="#ffffff", padding=6, relief="flat")
style.map("TButton", background=[("active", "#555555")])

Label(root, text="Выберите папку:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
Entry(root, textvariable=folder_path, width=50, bg="#444444", fg="#ffffff").grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Обзор", command=select_folder).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="Расширение файлов:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
Entry(root, textvariable=extension, width=10, bg="#444444", fg="#ffffff").grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Имя файла:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
Entry(root, textvariable=file_name, width=50, bg="#444444", fg="#ffffff").grid(row=2, column=1, padx=10, pady=10)

delete_button = Button(root, text="Удалить", command=delete_files)
delete_button.grid(row=3, column=1, pady=20)
style.configure("Red.TButton", background="#c05050", foreground="#ffffff")
delete_button.config(style="Red.TButton")

restore_button = Button(root, text="Восстановить", command=restore_files, state="disabled")
restore_button.grid(row=4, column=1, pady=20)
style.configure("Green.TButton", background="#50c050", foreground="#ffffff")
restore_button.config(style="Green.TButton")

status_label = Label(root, text="")
status_label.grid(row=5, column=0, columnspan=3, sticky="w", padx=10, pady=5)

update_status()
root.mainloop()
