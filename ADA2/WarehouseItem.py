class WarehouseItem:
    def __init__(self, order_id, product_id, quantity, priority, product_type, location, weight, size):
        # Ensure the order_id is a string and maintain its length
        self.order_id = str(order_id)
        self.product_id = product_id
        self.quantity = quantity
        self.priority = priority
        self.product_type = product_type
        self.location = location
        self.weight = weight
        self.size = size

    def __getitem__(self, key):
        return getattr(self, key)
        
    def __repr__(self):
        return f"WarehouseItem(order_id={self.order_id}, product_id={self.product_id}, " \
               f"quantity={self.quantity}, priority={self.priority}, product_type={self.product_type}, " \
               f"location={self.location}, weight={self.weight}, size={self.size})"

    def map_priority(self, priority_str):
        priority_mapping = {'High': 3, 'Medium': 2, 'Low': 1}
        return priority_mapping.get(priority_str.strip(), 0)  # Changed default to 0 for non-matching priority

    def to_dict(self):
        # Convert all attributes to a dictionary
        return {
            'Order_ID': self.order_id,
            'Product_ID': self.product_id,
            'Order_Quantity': self.quantity,
            'Priority': self.priority,
            'Product_Type': self.product_type,
            'Location': self.location,
            'Weight': self.weight,
            'Size': self.size
        }

    # Additional methods as needed
