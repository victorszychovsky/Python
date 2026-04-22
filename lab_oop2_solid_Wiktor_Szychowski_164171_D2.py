from abc import ABC, abstractmethod

# Wiktor_Szychowski 164171 D2
# 1. ZASADA POJEDYNCZEJ ODPOWIEDZIALNOŚCI (SRP)


class Invoice:
    def __init__(self, invoice_id: int, client: str, amount: float):
        self.invoice_id = invoice_id
        self.client = client
        self.amount = amount

class VATCalculator:
    def calculate(self, amount: float) -> float:
        return round(amount * 0.23, 2)

class InvoiceFormatter:
    def format(self, invoice: Invoice) -> str:
        return f"<div><h2>Faktura #{invoice.invoice_id}</h2><p>{invoice.client}: {invoice.amount} PLN</p></div>"

class InvoiceRepository:
    def save(self, invoice: Invoice, filename: str) -> bool:
        try:
            with open(filename, 'w') as f:
                f.write(f"{invoice.invoice_id}|{invoice.client}|{invoice.amount}")
            return True
        except Exception:
            return False


# 2. ZASADA OTWARTE/ZAMKNIĘTE (OCP) - STRATEGIE


class TaxStrategy(ABC):
    @abstractmethod
    def calculate(self, income: float) -> float:
        pass

class NoTax(TaxStrategy):
    def calculate(self, income: float) -> float:
        return 0.0

class FlatTax(TaxStrategy):
    def __init__(self, rate: float):
        self.rate = rate

    def calculate(self, income: float) -> float:
        return round(income * self.rate, 2)

class TaxCalculator:
    def __init__(self, strategy: TaxStrategy):
        self.strategy = strategy

    def net_income(self, gross: float) -> float:
        return gross - self.strategy.calculate(gross)


# Blok testowy
if __name__ == '__main__':
    print("--- ZADANIE 1 (SRP) ---")
    inv = Invoice(1, "Jan Kowalski", 1000.0)
    print(inv.invoice_id)  # Oczekiwane: 1
    print(inv.client)      # Oczekiwane: Jan Kowalski
    print(inv.amount)      # Oczekiwane: 1000.0

    calc = VATCalculator()
    print(calc.calculate(1000.0))  # Oczekiwane: 230.0
    print(calc.calculate(500.0))   # Oczekiwane: 115.0
    print(calc.calculate(199.99))  # Oczekiwane: 46.0

    formatter = InvoiceFormatter()
    html = formatter.format(inv)
    print(html)  # Oczekiwane: <div><h2>Faktura #1</h2><p>Jan Kowalski: 1000.0 PLN</p></div>

    repo = InvoiceRepository()
    result = repo.save(inv, "invoice.txt")
    print(result)  # True (jeśli zapis się powiódł)
    


    print("\n--- ZADANIE 2 (OCP) ---")
    n = NoTax()
    print(n.calculate(50000.0))  # Oczekiwane: 0.0

    flat = FlatTax(0.12)
    print(flat.calculate(10000.0))  # Oczekiwane: 1200.0
    print(flat.calculate(9.99))     # Oczekiwane: 1.2

    flat23 = FlatTax(0.23)
    print(flat23.calculate(9.99))   # Oczekiwane: 2.3

    calc_tax = TaxCalculator(FlatTax(0.12))
    print(calc_tax.net_income(10000.0))  # Oczekiwane: 8800.0

    calc2 = TaxCalculator(NoTax())
    print(calc2.net_income(10000.0))  # Oczekiwane: 10000.0

    calc3 = TaxCalculator(FlatTax(0.20))
    print(calc3.net_income(5000.0))  # Oczekiwane: 4000.0