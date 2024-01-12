import pandas as pd

class OrderProcessor:

    
    def get_orders_to_process(self, csv_path):
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_path)
        
        # Assuming that each row in the CSV is an item, group by 'Order_ID' to create orders
        orders = df.groupby('Order_ID').apply(lambda x: x.to_dict(orient='records')).to_dict()
        
        # Create a new list of orders where each order has an 'items' key
        orders_with_items = [{'Order_ID': order_id, 'items': items} for order_id, items in orders.items()]
        
        return orders_with_items


    def __init__(self, warehouse_layout):
        self.warehouse_layout = warehouse_layout
        self.current_strategy = "greedy"  # default strategy

    def process_order(self, order):
        # Choose a strategy based on current warehouse layout
         if self.current_strategy == "greedy":
             return self.process_using_greedy(order)
         elif self.current_strategy == "genetic":
             return self.process_using_genetic(order)
         else:
             raise ValueError("Unknown strategy")

    def process_using_greedy(self, order):
        # Example implementation of a greedy algorithm
        sorted_items = sorted(order['items'], key=lambda item: self.distance_to_entrance(item))
        return self.retrieve_items(sorted_items)
    
    def process_using_genetic(self, order):
        # Genetic logic: process the order based on a predetermined sequence from genetic optimization
        sequence = self.genetic_sequence(order)
        # This assumes the genetic_sequence method defines the picking sequence
        return self.retrieve_items(sequence)

    def distance_to_entrance(self, item):
        # Placeholder method to calculate distance of item from entrance or loading dock
        # You would replace this with actual logic
        return self.warehouse_layout.distance_from_entrance(item['Product_ID'])

    def genetic_sequence(self, order):
        # Placeholder method to determine the sequence of picking items based on genetic optimization
        # You would replace this with actual logic
        return order['items']

    def retrieve_items(self, sorted_items):
        # Assuming 'sorted_items' is a list of items sorted according to the chosen strategy
        picked_items = []
        for item in sorted_items:
            # Retrieve the item from the warehouse
            if self.warehouse_layout.pick_item(item['Product_ID']):
                picked_items.append(item)
        return picked_items

