from expense_manager import ExpenseManager

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
except Exception:
    tk = None


def run_gui():
    if tk is None:
        print("Tkinter nie jest dostępny w tym środowisku.")
        return

    manager = ExpenseManager()

    root = tk.Tk()
    root.title("Expense Manager")
    # Ustaw rozmiar okna:
    root.update_idletasks()
    # Pobierz bieżące wymiary (po uaktualnieniu rozmieszczenia)
    cur_w = root.winfo_width()
    cur_h = root.winfo_height()
    # Jeśli nie uda się odczytać sensownych wymiarów, zastosuj rozsądne domyślne
    if cur_w < 100:
        cur_w = 800
    if cur_h < 100:
        cur_h = 600
    # trzy razy szersze niż domyślna szerokość, wyśrodkowane na ekranie
    new_w = cur_w * 3
    # Zwiększ wysokość okna o 1.5 raza
    new_h = int(cur_h * 2)
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w // 2) - (new_w // 2)
    y = (screen_h // 2) - (new_h // 2)
    root.geometry(f"{new_w}x{new_h}+{x}+{y}")
    # Blokuję możliwość zmiany rozmiaru okna przez użytkownika
    root.resizable(False, False)

    # Tworzę ramkę danych wejściowych
    frm = tk.Frame(root, padx=10, pady=10)  # Ustawiam odstęp wokół ramki
    frm.pack(fill=tk.X)  # Rozciągam poziomo

    tk.Label(frm, text="Kwota:").grid(row=0, column=0, sticky=tk.W)
    amount_entry = tk.Entry(frm)
    amount_entry.grid(row=0, column=1, sticky=tk.EW)

    tk.Label(frm, text="Kategoria:").grid(row=1, column=0, sticky=tk.W)
    category_entry = tk.Entry(frm)
    category_entry.grid(row=1, column=1, sticky=tk.EW)

    tk.Label(frm, text="Notatka:").grid(row=2, column=0, sticky=tk.W)
    note_entry = tk.Entry(frm)
    note_entry.grid(row=2, column=1, sticky=tk.EW)

    frm.columnconfigure(1, weight=1)

    # Tworzę przyciski
    btn_frame = tk.Frame(root, padx=10, pady=5)
    btn_frame.pack(fill=tk.X)

    def refresh_list(items=None):
        """Odśwież listę. Jeśli items podane, użyj ich, inaczej pobierz wszystkie wydatki."""
        listbox.delete(0, tk.END)
        source = items if items is not None else manager.list_expenses()
        for i, e in enumerate(source):
            date = e.get("date", "")
            cat = e.get("category", "")
            amt = e.get("amount", 0)
            note = e.get("note", "")
            summary = f"{i}: {amt} zł — {cat} {note} ({date})"
            listbox.insert(tk.END, summary)

    def on_add():
        amt = amount_entry.get().strip()
        cat = category_entry.get().strip()
        note = note_entry.get().strip()
        try:
            manager.add_expense(amt or 0, cat, note)
            amount_entry.delete(0, tk.END)
            category_entry.delete(0, tk.END)
            note_entry.delete(0, tk.END)
            refresh_list()
        except ValueError as ex:
            messagebox.showerror("Błąd", str(ex))

    def on_remove():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Wybierz wydatek do usunięcia")
            return
        idx = sel[0]
        try:
            manager.remove(idx)
            refresh_list()
            # Po usunięciu odświeżam listę kategorii w comboboxie
            try:
                category_filter_cb["values"] = manager.get_categories()
            except Exception:
                pass
        except IndexError as ex:
            messagebox.showerror("Błąd", str(ex))

    def on_total():
        total = manager.total()
        messagebox.showinfo("Suma wydatków", f"Suma: {total} zł")

    add_btn = tk.Button(btn_frame, text="Dodaj", command=on_add)
    add_btn.pack(side=tk.LEFT)
    remove_btn = tk.Button(btn_frame, text="Usuń", command=on_remove)
    remove_btn.pack(side=tk.LEFT, padx=5)
    total_btn = tk.Button(btn_frame, text="Pokaż sumę", command=on_total)
    total_btn.pack(side=tk.LEFT, padx=5)

    # Tworzę kontrolki filtrowania po kategorii
    filter_frame = tk.Frame(root, padx=10, pady=5)
    filter_frame.pack(fill=tk.X)

    tk.Label(filter_frame, text="Filtruj kategorię:").pack(side=tk.LEFT)
    category_filter_cb = ttk.Combobox(filter_frame, values=manager.get_categories())
    category_filter_cb.pack(side=tk.LEFT, padx=5)

    def on_filter():
        cat = category_filter_cb.get().strip()
        if not cat:
            messagebox.showinfo("Info", "Wybierz kategorię do filtrowania")
            return
        items = manager.filter_by_category(cat)
        refresh_list(items)

    def on_show_all():
        # Odświeżam combobox z kategoriami i pokazuję wszystkie
        try:
            category_filter_cb["values"] = manager.get_categories()
        except Exception:
            pass
        refresh_list()

    filter_btn = tk.Button(filter_frame, text="Filtruj po kategorii", command=on_filter)
    filter_btn.pack(side=tk.LEFT, padx=5)
    show_all_btn = tk.Button(filter_frame, text="Odfiltruj", command=on_show_all)
    show_all_btn.pack(side=tk.LEFT, padx=5)

    # Tworzę ramkę listy
    list_frame = tk.Frame(root, padx=10, pady=5)
    list_frame.pack(fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
    listbox.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    refresh_list()

    root.mainloop()


if __name__ == "__main__":
    run_gui()
