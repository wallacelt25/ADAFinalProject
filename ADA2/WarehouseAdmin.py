import pandas as pd
from WarehouseItem import WarehouseItem
from WarehouseLayout import WarehouseLayout

class WarehouseAdmin:
    def __init__(self):
        self.layout = WarehouseLayout()
        self.load_items_from_csv('C:/Users/walla/Downloads/ADA22/ADA2/Updated Warehouse Data.csv')

    def load_items_from_csv(self, file_path):
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            item = WarehouseItem(row['Product_ID'], row['Location'], row['Weight'], row['Priority'], row['Size'])
            self.layout.add_item(item)

    # Additional functionalities...
