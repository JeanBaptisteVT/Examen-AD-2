import random
import csv
from Code_lectures_2526.examens.exvorigjaar.examenvorigjaar import Product
# https://dodona.be/nl/activities/71750927/

class Inventory_Manager:
    def __init__(self):
        # Dictionary met product_name als key en Product-object als value
        self.products = {}

    # --------------------------------------------------------
    # Voeg een nieuw product toe
    # --------------------------------------------------------
    def add_product(self, product_name, holding_cost, stockout_penalty):
        """
        Voeg een nieuw product toe aan de voorraad.
        Als het product al bestaat, print een waarschuwing.
        """
        if product_name in self.products:
            print(f"Product [{product_name}] already exists.")
        else:
            # We gaan ervan uit dat je Product-class is:
            # Product(product_name, holding_cost, stockout_penalty)
            self.products[product_name] = Product(product_name, holding_cost, stockout_penalty)

    # --------------------------------------------------------
    # Voorraad aanvullen: batch toevoegen aan een product
    # --------------------------------------------------------
    def restock_product(self, product_name, quantity, cost_per_unit):
        """
        Voeg een nieuwe batch toe aan een bestaand product.
        Als het product niet bestaat, print een foutmelding.
        """
        if product_name not in self.products:
            print(f"Product [{product_name}] not found")
        else:
            product = self.products[product_name]
            product.add_batch(quantity, cost_per_unit)

    # --------------------------------------------------------
    # Willekeurige vraag simuleren voor elk product
    # --------------------------------------------------------
    def simulate_demand(self, min_demand=0, max_demand=20):
        """
        Genereer een willekeurige vraag voor elk product.
        Returnt een dictionary: {product_name: demand}.
        """
        demand_dict = {}
        for name in self.products:
            demand = random.randint(min_demand, max_demand)
            demand_dict[name] = demand
        return demand_dict

    # --------------------------------------------------------
    # Simuleer een dag: vraag -> fulfill_demand -> costs
    # --------------------------------------------------------
    def simulate_day(self, demand):
        totale_aandhoudingskosten = 0
        totale_stockoutkosten = 0

        # loop tegelijk over (naam, product) via .items()
        for naam, product in self.products.items():
            # vraag voor dit product (0 als het niet in demand staat)
            qty = demand.get(naam, 0)

            # eerst vraag vervullen → geeft stockoutkosten
            totale_stockoutkosten += product.fulfill_demand(qty)

            # dan holding cost van de resterende voorraad
            totale_aandhoudingskosten += product.calculate_holding_cost()

        return totale_aandhoudingskosten, totale_stockoutkosten
    # --------------------------------------------------------
    # Voorraad wegschrijven naar CSV
    # --------------------------------------------------------
    def save_to_csv(self, filename):
        """
        Sla de voorraad op in een CSV-bestand.
        Elke rij:
        [product_name],[batch_quantity],[batch_cost_per_unit]
        """
        with open(filename, mode="w", newline="") as f:
            writer = csv.writer(f)
            for name, product in self.products.items():
                for batch in product.batches:
                    writer.writerow([name, batch.quantity, batch.cost_per_unit])

    # --------------------------------------------------------
    # Voorraad laden uit CSV
    # --------------------------------------------------------
    def load_from_csv(self, filename):
        """
        Laad voorraad uit CSV.
        Als het product nog niet bestaat, maak het aan
        (holding_cost en stockout_penalty zetten we hier bv. op 0).
        """
        with open(filename, mode="r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue  # lege lijn overslaan
                product_name = row[0]
                quantity = int(row[1])
                cost_per_unit = float(row[2])

                # Als product nog niet bestaat → nieuw Product aanmaken met default kosten
                if product_name not in self.products:
                    self.products[product_name] = Product(product_name, holding_cost=0, stockout_penalty=0)

                # Batch toevoegen
                self.products[product_name].add_batch(quantity, cost_per_unit)

    # --------------------------------------------------------
    # Print huidige voorraad
    # --------------------------------------------------------
    def print_inventory(self):
        """
        Print de volledige voorraad voor elk product.
        Gebruikt de __str__ van Product.
        """
        print("Current Inventory:")
        for product in self.products.values():
            print(product)
            print()  # lege lijn tussen producten


# ------------------------------------------------------------
# MAIN: test de code
def main():
    # Inventory manager aanmaken
    manager = Inventory_Manager()

    # Twee producten toevoegen
    manager.add_product("Widget", holding_cost=0.5, stockout_penalty=10)
    manager.add_product("Gadget", holding_cost=0.3, stockout_penalty=8)

    # Voor elk product minstens 2 batches toevoegen
    manager.restock_product("Widget", quantity=100, cost_per_unit=2.5)
    manager.restock_product("Widget", quantity=50, cost_per_unit=2.0)

    manager.restock_product("Gadget", quantity=70, cost_per_unit=3.0)
    manager.restock_product("Gadget", quantity=40, cost_per_unit=2.8)

    # Voorraad tonen
    manager.print_inventory()

    # Vraag simuleren
    demand = manager.simulate_demand(min_demand=0, max_demand=20)
    print("Simulated demand:", demand)

    # Dag simuleren
    total_holding, total_stockout = manager.simulate_day(demand)
    print(f"Total holding cost: {total_holding}")
    print(f"Total stockout cost: {total_stockout}")

    # Voorraad wegschrijven naar CSV
    manager.save_to_csv("inventory.csv")
    print("Inventory saved to inventory.csv")
