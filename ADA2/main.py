from WarehouseLayout import WarehouseLayout
from OrderProcessor import OrderProcessor
from PerformanceAnalyzer import PerformanceAnalyzer
from WarehouseGUI import WarehouseGUI

def main():
    # Initialize the warehouse layout and load items from the CSV
    warehouse_layout = WarehouseLayout()
    warehouse_layout.load_items_from_csv('C:/Users/walla/Downloads/ADA22/ADA2/Updated Warehouse Data.csv')

    # Initialize the order processor with the warehouse layout
    order_processor = OrderProcessor(warehouse_layout)
    
    # Initialize the performance analyzer with the warehouse layout
    performance_analyzer = PerformanceAnalyzer(warehouse_layout)
    
    # Initialize and run the GUI, passing in the warehouse layout, order processor, and performance analyzer
    gui = WarehouseGUI(warehouse_layout, order_processor, performance_analyzer) 
    gui.run()

if __name__ == "__main__":
    main()
