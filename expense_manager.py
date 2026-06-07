import json
import datetime


class ExpenseManager:
    def __init__(self, path="expenses.json"):
        self.path = path
        self.expenses = []
        self.load()

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.expenses = json.load(f)
        except FileNotFoundError:
            self.expenses = []
        except json.JSONDecodeError:
            self.expenses = []
        # Normalizuje daty w formacie ISO do bardziej czytelnego: DD.MM.YYYY HH:MM:SS
        for e in self.expenses:
            d = e.get("date")
            if isinstance(d, str) and "T" in d:
                try:
                    parsed = datetime.datetime.fromisoformat(d)
                    e["date"] = parsed.strftime("%d.%m.%Y %H:%M:%S")
                except Exception:
                    # pozostawiam bez zmian, jeśli parsowanie się nie powiedzie
                    pass

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=2)

    def add_expense(self, amount, category="", note=""):
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise ValueError("Nieprawidłowa kwota")
        expense = {
            "amount": amount,
            "category": category,
            "note": note,
            "date": datetime.datetime.now().strftime(
                "%d.%m.%Y %H:%M:%S"
            ),  # zapisuję datę w formacie: DD.MM.RRRR GG:MM:SS
        }
        self.expenses.append(expense)
        self.save()
        return expense

    def list_expenses(self):
        return list(self.expenses)

    def filter_by_category(self, category):
        """Zwraca listę wydatków z podanej kategorii (porównanie nieczułe na wielkość liter)."""
        if not category:
            return self.list_expenses()
        cat = str(category).strip().lower()
        return [e for e in self.expenses if str(e.get('category', '')).strip().lower() == cat]

    def get_categories(self):
        """Zwraca posortowaną listę unikalnych kategorii."""
        cats = {str(e.get('category', '')).strip() for e in self.expenses if e.get('category')}
        return sorted(cats)

    def total(self):
        return sum(e.get("amount", 0) for e in self.expenses)

    def remove(self, index):
        if index < 0 or index >= len(self.expenses):
            raise IndexError("Indeks poza zakresem")
        e = self.expenses.pop(index)
        self.save()
        return e
