import pandas as pd
import random
import csv
from WarehouseItem import WarehouseItem


class WarehouseLayout:
    def __init__(self, grid_size=10, population_size=50, number_of_generations=100):
        self.items = {}  # key: Product_ID, value: WarehouseItem
        self.grid_size = grid_size
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.population_size = population_size
        self.number_of_generations = number_of_generations

    def load_items_from_csv(self, csv_path):
        try:
            data = pd.read_csv(csv_path)
            if data.empty:
                print(f"The file at {csv_path} is empty.")
                return
            
            # Clear existing items before loading new ones
            self.items.clear()

            for _, row in data.iterrows():
                item = WarehouseItem(
                    order_id=str(row['Order_ID']),
                    product_id=row['Product_ID'],
                    quantity=row['Order_Quantity'],
                    priority=row['Priority'],
                    product_type=row['Product_Type'],
                    location=row['Location'],
                    weight=row['Weight'],
                    size=row['Size']
                )
                self.items[row['Product_ID']] = item

            print(f"Loaded {len(self.items)} items.")
            # Print first 5 items as a sample (for debugging purposes)
            for product_id, item in list(self.items.items())[:5]:
                print(f"{product_id}: {item}")

        except FileNotFoundError:
            print(f"Error: The file at {csv_path} was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    def add_item(self, item):
        if not isinstance(item, WarehouseItem):
            raise ValueError("item must be an instance of WarehouseItem")
        self.items[item.product_id] = item
        self.save_items_to_csv()

    def update_item(self, product_id, updated_details):
        self.items[product_id].update(updated_details)
        self.save_items_to_csv('C:/Users/walla/Downloads/ADA22/ADA2/Updated Warehouse Data.csv')  # Provide the correct path to your CSV file

    def delete_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
            self.save_items_to_csv('C:/Users/walla/Downloads/ADA22/ADA2/Updated Warehouse Data.csv')

    def pick_item(self, product_id):
        """
        Handles the logic when an item is picked from the warehouse.
        This is a placeholder implementation.
        """
        if product_id in self.items:
            item = self.items[product_id]
            # Placeholder: Update item status or perform other necessary actions
            print(f"Item {product_id} picked from location {item.location}.")
            return True
        else:
            print(f"Item {product_id} not found in the warehouse.")
            return False


    def save_items_to_csv(self, csv_path='C:/Users/walla/Downloads/ADA22/ADA2/Updated Warehouse Data.csv'):
        # Make sure to replace '/path/to/your/csvfile.csv' with the actual path to your CSV file
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['order_id', 'product_id', 'quantity', 'priority', 'product_type', 'location', 'weight', 'size'])
            writer.writeheader()
            for item in self.items.values():
                writer.writerow({
                    'order_id': item.order_id,
                    'product_id': item.product_id,
                    'quantity': item.quantity,
                    'priority': item.priority,
                    'product_type': item.product_type,
                    'location': item.location,
                    'weight': item.weight,
                    'size': item.size
                })

    def update_item(self, product_id, updated_details):
        if product_id in self.items:
            # Update item details
            item = self.items[product_id]
            for detail_key, detail_value in updated_details.items():
                setattr(item, detail_key, detail_value)  # Update attributes
            self.save_items_to_csv()  # Save changes to CSV
            print(f"Item {product_id} updated with {updated_details}")
        else:
            print(f"Item {product_id} not found in the warehouse.")

    
    def optimize_layout_greedy(self):
        """
        Reorganizes items based on predefined optimization criteria using a Greedy Algorithm.
        """
        # Sort items based on a criterion, e.g., size or weight
        sorted_items = sorted(self.items.values(), key=lambda item: item.size)
        # Arrange items in the warehouse based on sorted order
        # This is a simplified example; actual implementation will depend on your warehouse's specifics
        for item in sorted_items:
            self.place_item_in_warehouse(item)

    def optimize_layout_genetic(self):
        # Initialize a population of layouts based on the greedy algorithm's output
        population = self.initialize_population()
        for generation in range(self.number_of_generations):
            # Evaluate fitness of each layout
            fitness_scores = self.evaluate_fitness(population)
            # Select, crossover, and mutate to create a new generation
            new_generation = self.genetic_operations(population, fitness_scores)
            population = new_generation
        # Choose the best layout from the final generation
        best_layout = self.select_best_layout(population)
        self.apply_layout(best_layout)

    def find_nearest_items(self, product_id):
        """
        Finds and returns items nearest to a given product ID.
        Placeholder logic: return items with similar weights.
        """
        target_item = self.items.get(product_id)
        if not target_item:
            return []
        similar_items = [item for item in self.items.values() if abs(item.weight - target_item.weight) < 5]
        return similar_items

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            layout = self.grid.copy()
            random.shuffle(layout)  # Shuffle the layout to generate diversity
            population.append(layout)
        return population

    def evaluate_fitness(self, population):
        fitness_scores = []
        for layout in population:
            # Example fitness function: Count how many items are 'properly' placed
            score = sum(1 for row in layout for item_id in row if item_id)
            fitness_scores.append(score)
        return fitness_scores

    def genetic_operations(self, population, fitness_scores):
        # Select the best-performing layouts
        sorted_population = [layout for _, layout in sorted(zip(fitness_scores, population), reverse=True)]
        # Crossover and mutation to create a new generation
        new_population = []
        for _ in range(len(population)):
            parent1, parent2 = random.sample(sorted_population[:self.population_size // 2], 2)
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)
        return new_population

    def crossover(self, parent1, parent2):
        # Combine two layouts to create a new one
        child = []
        for row1, row2 in zip(parent1, parent2):
            if random.random() < 0.5:
                child.append(row1)
            else:
                child.append(row2)
        return child

    def mutate(self, layout):
        # Randomly swap two items in the layout
        row_idx1, col_idx1, row_idx2, col_idx2 = random.sample(range(10), 4)
        layout[row_idx1][col_idx1], layout[row_idx2][col_idx2] = layout[row_idx2][col_idx2], layout[row_idx1][col_idx1]
        return layout

    def select_best_layout(self, population):
        # Simply return the layout with the most items for this example
        return max(population, key=lambda layout: sum(1 for row in layout for item_id in row if item_id))

    def apply_layout(self, best_layout):
        # Apply the best layout to the warehouse
        self.grid = best_layout

    def distance_from_entrance(self, product_id):
        """
        Calculates the distance of a product from the warehouse entrance.
        This is a placeholder implementation assuming grid coordinates.
        """
        item = self.items.get(product_id)
        if not item:
            return float('inf')  # Return a high distance for items not found

        # Assuming 'location' is stored as grid coordinates like 'A-5'
        # and entrance is at 'A-1'
        col, row = item.location.split('-')
        col_distance = ord(col.upper()) - ord('A')
        row_distance = int(row) - 1
        return col_distance + row_distance  # Simple distance calculation

# Example usage
warehouse_layout = WarehouseLayout()
# Assuming `items` are loaded with product details from the table
best_layout = warehouse_layout.select_best_layout(warehouse_layout.initialize_population())
warehouse_layout.apply_layout(best_layout)


