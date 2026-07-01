import sqlite3
import tkinter as tk
from tkinter import ttk

DB_FILE = "example.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS table_a (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS table_b (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def insert_into(table_name, value):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table_name} (value) VALUES (?)", (value,))
    conn.commit()
    conn.close()

def fetch_entire_db_text():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # List tables
    cur.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    tables = [row[0] for row in cur.fetchall()]

    out_lines = []
    for t in tables:
        out_lines.append(f"== {t} ==")
        cur.execute(f"SELECT * FROM {t}")
        rows = cur.fetchall()
        if not rows:
            out_lines.append("(empty)")
        else:
            for r in rows:
                out_lines.append(str(r))
        out_lines.append("")  # blank line

    conn.close()
    return "\n".join(out_lines).strip()

# -------- GUI --------
init_db()

root = tk.Tk()
root.title("SQLite + Tkinter Example")
root.geometry("720x420")

main = ttk.Frame(root, padding=12)
main.pack(fill="both", expand=True)

ttk.Label(main, text="Value to insert:").grid(row=0, column=0, sticky="w")

value_var = tk.StringVar()
entry = ttk.Entry(main, textvariable=value_var, width=40)
entry.grid(row=0, column=1, sticky="we", padx=(8, 8))

def refresh_db_view():
    db_text = fetch_entire_db_text()
    text_box.configure(state="normal")
    text_box.delete("1.0", "end")
    text_box.insert("1.0", db_text)
    text_box.configure(state="disabled")

def on_insert_a():
    v = value_var.get().strip()
    if not v:
        return
    insert_into("table_a", v)
    refresh_db_view()

def on_insert_b():
    v = value_var.get().strip()
    if not v:
        return
    insert_into("table_b", v)
    refresh_db_view()

btn_a = ttk.Button(main, text="INSERT into table_a", command=on_insert_a)
btn_a.grid(row=1, column=0, columnspan=2, sticky="we", pady=(10, 6))

btn_b = ttk.Button(main, text="INSERT into table_b", command=on_insert_b)
btn_b.grid(row=2, column=0, columnspan=2, sticky="we", pady=(0, 10))

# Text box showing entire DB
text_box = tk.Text(main, height=12, wrap="none")
text_box.grid(row=3, column=0, columnspan=2, sticky="nsew")

scroll_y = ttk.Scrollbar(main, orient="vertical", command=text_box.yview)
scroll_y.grid(row=3, column=2, sticky="ns")
text_box.configure(yscrollcommand=scroll_y.set)

scroll_x = ttk.Scrollbar(main, orient="horizontal", command=text_box.xview)
scroll_x.grid(row=4, column=0, columnspan=2, sticky="ew")
text_box.configure(xscrollcommand=scroll_x.set)

main.columnconfigure(1, weight=1)
main.rowconfigure(3, weight=1)

text_box.configure(state="disabled")
refresh_db_view()

root.mainloop()
