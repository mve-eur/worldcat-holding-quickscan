import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
import time
import traceback
import subprocess
import sys
import threading
from pathlib import Path
import os

SCRIPT_DIR = Path(__file__).parent.resolve()
current_process = None

# --- Colors ---
PRIMARY = "#0c8066"
PRIMARY_LIGHT = "#d7f3ec"
BG_MAIN = "#ffffff"
BG_CARD = "#f7f7f7"
TEXT_MUTED = "#777"

# -------------------------
# FILE SELECT
# -------------------------
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        set_file(file_path)

def set_file(path):
    entry_var.set(path)
    drop_label.config(
        text=f"📄 {Path(path).name}",
        fg=PRIMARY,
        font=("Segoe UI", 11, "bold")
    )
    drop_frame.config(highlightbackground=PRIMARY)

# -------------------------
# DRAG AND DROP
# -------------------------
def drop_file(event):
    file_path = event.data.strip()

    if file_path.startswith("{") and file_path.endswith("}"):
        file_path = file_path[1:-1]

    set_file(file_path)

def on_drag_enter(event):
    drop_frame.config(bg=PRIMARY_LIGHT)
    drop_label.config(bg=PRIMARY_LIGHT)

def on_drag_leave(event):
    drop_frame.config(bg=BG_CARD)
    drop_label.config(bg=BG_CARD)

# -------------------------
# LOG
# -------------------------
def open_log():
    log_path = SCRIPT_DIR / "log.txt"
    if log_path.exists():
        os.startfile(log_path)
    else:
        messagebox.showinfo("Info", "Nog geen logbestand.")

# -------------------------
# FORMAT ETA
# -------------------------
def format_eta(seconds):
    seconds = int(seconds)

    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}s"
    else:
        return f"{s}s"

# -------------------------
# BUTTON FUNCTIONS
# -------------------------
def create_button(parent, text, command, primary=False, disabled=False):
    if primary:
        bg = PRIMARY
        fg = "white"
        active_bg = "#0a6b55"
    else:
        bg = "#eeeeee"
        fg = "#333"
        active_bg = "#dddddd"

    state = "disabled" if disabled else "normal"

    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=active_bg,
        relief="flat",
        bd=0,
        padx=12,
        pady=6,
        font=("Segoe UI", 9),
        state=state
    )

def update_button_states(running):
    if running:
        start_btn.config(
            state="disabled",
            bg="#e5e5e5",
            fg="#aaaaaa"
        )
        stop_btn.config(
            state="normal",
            bg=PRIMARY,
            fg="white"
        )
    else:
        start_btn.config(
            state="normal",
            bg=PRIMARY,
            fg="white"
        )
        stop_btn.config(
            state="disabled",
            bg="#eeeeee",
            fg="#888"
        )

# -------------------------
# PROCESS
# -------------------------
def run_process(input_file, output_file):
    global current_process

    script_path = SCRIPT_DIR / "holding_quickscan.py"
    log_path = SCRIPT_DIR / "log.txt"

    try:
        if not log_path.exists():
            log_path.touch()

        with open(log_path, "w", encoding="utf-8") as logfile:
            current_process = subprocess.Popen(
                [sys.executable, str(script_path), input_file, output_file],
                stdout=logfile,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

        last_pos = 0
        start_time = time.time()

        while current_process and current_process.poll() is None:
            if log_path.exists():
                with open(log_path, "r", encoding="utf-8") as f:
                    f.seek(last_pos)
                    data = f.read()
                    last_pos = f.tell()

                    current_row = 0
                    total_rows = 0
                    percent = 0

                    for line in data.splitlines():
                        if "PROGRESS:" in line:
                            try:
                                percent = int(line.split("PROGRESS:")[1])
                                progress["value"] = percent
                            except:
                                pass

                        if "ROW:" in line:
                            try:
                                row_info = line.split("ROW:")[1]
                                current_row, total_rows = map(int, row_info.split("/"))
                            except:
                                pass

                    if current_row > 0:
                        elapsed = time.time() - start_time
                        time_per_row = elapsed / current_row
                        remaining = total_rows - current_row
                        eta_seconds = round(time_per_row * remaining)
                        eta_text = format_eta(eta_seconds)

                        progress_label.config(
                            text=f"{current_row}/{total_rows} ({percent}%) • {eta_text} remaining"
                        )

            root.update_idletasks()

        if current_process:
            current_process.wait()

        if current_process and current_process.returncode != 0:
            raise Exception("Fout tijdens verwerking")

        messagebox.showinfo(
            "Voltooid",
            f"✅ Scan succesvol voltooid\n\nOutput:\n{output_file}"
        )

        drop_label.config(
            text="✅ Scan complete",
            fg=PRIMARY,
            bg=BG_CARD,
            font=("Segoe UI", 11, "bold")
        )
        
        root.update_idletasks()
        time.sleep(1)

    except Exception as e:
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("\n[ERROR]\n")
            f.write(traceback.format_exc())

        messagebox.showerror("Error", str(e))

    finally:
        # reset process
        current_process = None

        # reset progress UI
        progress.pack_forget()
        progress_label.pack_forget()
        
        # reset buttons
        update_button_states(False)

        #reset drop UI
        entry_var.set("")
        drop_frame.config(bg=BG_CARD, highlightbackground="#dcdcdc")
        drop_label.config(
            text="Drop Excel file or click to browse",
            fg=TEXT_MUTED,
            bg=BG_CARD,
            font=("Segoe UI", 11)
        )

        root.update_idletasks()

# -------------------------
# CANCEL
# ------------------------
def cancel_process():
    global current_process

    if not current_process or current_process.poll() is not None:
        messagebox.showinfo("Info", "Er draait geen proces.")
        return

    confirm = messagebox.askyesno(
        "Bevestigen",
        "Weet je zeker dat je de scan wilt stoppen?\nVerwerkte data wordt niet opgeslagen."
    )

    if not confirm:
        return

    try:
        current_process.terminate()
    except Exception:
        pass

    messagebox.showinfo("Gestopt", "Verwerking is afgebroken.")

    progress.pack_forget()
    progress_label.pack_forget()

    update_button_states(False)

# -------------------------
# START
# -------------------------
def run_script():
    input_file = entry_var.get()

    if not input_file:
        selected = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx")]
        )

        if not selected:
            return

        input_file = selected
        set_file(input_file)

    input_path = Path(input_file).resolve()

    if not input_path.exists():
        messagebox.showerror("Fout", "Bestand bestaat niet.")
        return

    output_file = input_path.with_name(input_path.stem + "-qs.xlsx")

    progress.pack(pady=10)
    progress_label.pack()

    progress["value"] = 0
    progress_label.config(text="Starting...")

    update_button_states(True)

    thread = threading.Thread(
        target=run_process,
        args=(str(input_path), str(output_file))
    )
    thread.start()

# -------------------------
# EXIT
# -------------------------
def exit_app():
    root.destroy()

# -------------------------
# UI
# -------------------------
root = TkinterDnD.Tk()
root.title("WorldCat Holding Quickscan")
try:
    root.iconbitmap(SCRIPT_DIR / "icon.ico")
except Exception:
    pass
root.geometry("540x340")
root.resizable(False, False)
root.configure(bg=BG_MAIN)

# Top bar
top_frame = tk.Frame(root, bg="#ffffff")
top_frame.pack(fill="x", pady=5, padx=10)

log_btn = create_button(
    top_frame,
    "📄 Log",
    open_log
)
log_btn.pack(side="right")

# State store
entry_var = tk.StringVar()

# Drop card
drop_frame = tk.Frame(
    root,
    bg=BG_CARD,
    highlightthickness=2,
    highlightbackground="#dcdcdc"
)
drop_frame.pack(pady=25, padx=25, fill="x")

drop_label = tk.Label(
    drop_frame,
    text="Drop Excel file or click to browse",
    bg=BG_CARD,
    fg=TEXT_MUTED,
    font=("Segoe UI", 11),
    pady=25
)
drop_label.pack(fill="both")

# Events
drop_label.bind("<Button-1>", lambda e: select_file())
drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind("<<Drop>>", drop_file)
drop_label.dnd_bind("<<DragEnter>>", on_drag_enter)
drop_label.dnd_bind("<<DragLeave>>", on_drag_leave)

# Progress
style = ttk.Style(root)
style.theme_use("default")
style.configure(
    "green.Horizontal.TProgressbar",
    troughcolor="#eeeeee",
    background=PRIMARY,
    thickness=8
)

progress = ttk.Progressbar(
    root, 
    mode="determinate", 
    length=350,
    style="green.Horizontal.TProgressbar"
    )

progress_label = tk.Label(
    root, 
    text="", 
    bg=BG_MAIN, 
    font=("Segoe UI", 10)
    )

# Buttons
bottom_frame = tk.Frame(root, bg=BG_MAIN)
bottom_frame.pack(side="bottom", fill="x", pady=15, padx=10)

start_btn = create_button(
    bottom_frame,
    "▶ Start",
    run_script,
    primary=True
)
start_btn.pack(side="left")

stop_btn = create_button(
    bottom_frame,
    "⛔ Stop",
    cancel_process,
    disabled=True
)
stop_btn.pack(side="left", padx=10)

close_btn = create_button(
    bottom_frame,
    "✖ Close",
    exit_app
)
close_btn.pack(side="right")

root.mainloop()