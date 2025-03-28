import tkinter as tk
from tkinter.ttk import Label, Entry, Button, Combobox, Frame
from tkinter import Text
from datatools import en, get_employee_by_samaccountname, get_object_by_name


class SettingsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Einstellungen")
        self.geometry("300x200")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame = Frame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        for i in range(2):
            self.frame.rowconfigure(i, weight=1)
            self.frame.columnconfigure(i, weight=1)

        self.db_label = Label(self.frame, text="Datenbankadresse:")
        self.db_label.grid(row=0, column=0, sticky="ew")
        self.db_name_input = Entry(self.frame)
        self.db_name_input.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.settings_save_btn = Button(self.frame, text="Speichern", command=self.destroy)
        self.settings_save_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")


class FlowsterDB(tk.Tk):
    def __init__(self):
        super().__init__()

        # holt sich die tatsächliche Größe, und berechnet dann 60% davon.
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{int(screen_width * 0.6)}x{int(screen_height * 0.6)}")  # 60% der Bildschirmgröße
        self.settings_window = None # Kontrollvar. für das Einstellungsfenster

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Hauptcontainer 
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Config für die Zeilen / Spalten von 0 - 2
        for i in range(3):
            self.frame.rowconfigure(i, weight=1)
            self.frame.columnconfigure(i, weight=1)

        # Config für die letzte Zeile
        self.frame.rowconfigure(3, weight=1)

        self.label = Label(self.frame, text="Suche", font="16")
        self.label.grid(row=0, column=0, columnspan=3)

        self.search_field = Entry(self.frame)
        self.search_field.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.search_field.bind("<Return>", self.on_enter)

        self.category = Combobox(self.frame)
        self.category['values'] = ('Employees', 'Distributor', 'ProjectDataroom', 'SharedMailbox')
        self.category.current(0)
        self.category.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.confirm = Button(self.frame, text='Bestätigen', command=self.btn_search)
        self.confirm.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # Scrollbars
        self.x_scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.y_scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)

        # ScrolledText-Feld mit horizontaler und vertikaler Scrollbar
        self.result_field = Text(
            self.frame, wrap=tk.NONE, xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set
        )
        self.result_field.grid(row=3, column=0, columnspan=3, sticky="nsew")  # "nsew" sorgt für vollständige Skalierung

        # Scrollbars mit dem Textfeld verbinden
        self.x_scrollbar.config(command=self.result_field.xview)
        self.y_scrollbar.config(command=self.result_field.yview)

        # Scrollbars im Grid positionieren
        self.y_scrollbar.grid(row=3, column=3, sticky="ns")  # Rechte Seite (vertikal)
        self.x_scrollbar.grid(row=4, column=0, columnspan=3, sticky="ew")  # Unterhalb des Textfelds (horizontal)

        # Damit die X-Scrollbar mitwächst
        self.frame.rowconfigure(4, weight=0) 

        self.settings_btn = Button(self.frame, text='Einstellungen', command=self.open_settings)
        # Row 99 soll immer die letzte Zeile des Fensters symbolisieren. 
        self.settings_btn.grid(row=99, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

    def open_settings(self):
        """Öffnet das Einstellungsfenster, falls es nicht bereits existiert."""
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)

    def on_enter(self, event):
        self.btn_search()

    def btn_search(self):
        self.result_field.delete('1.0', tk.END)
        txt = self.search_field.get()
        category = self.category.get()

        if category == "Employees":
            result = get_employee_by_samaccountname(en, txt)
            if not result.empty:
                result = result[['SamAccountName', 'Givenname', 'Surname', 'EmployeeID', 'changed', 'isActive']]
        else:
            result = get_object_by_name(en, category, txt)
            if not result.empty:
                result = result[[category, 'isActive', 'changed']]

        if len(result) > 0:
            self.result_field.insert('1.0', result.to_string(index=False))
        else:
            self.result_field.insert('1.0', "Nichts gefunden!")        


if __name__ == "__main__":
    app = FlowsterDB()
    app.mainloop()