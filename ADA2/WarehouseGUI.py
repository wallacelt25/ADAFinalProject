import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from WarehouseLayout import WarehouseLayout
from OrderProcessor import OrderProcessor
from PerformanceAnalyzer import PerformanceAnalyzer
import pandas as pd
from WarehouseItem import WarehouseItem


class WarehouseGUI:
    def __init__(self, warehouse_layout, order_processor, performance_analyzer):
        self.warehouse_layout = warehouse_layout
        self.order_processor = order_processor
        self.performance_analyzer = performance_analyzer
        self.root = tk.Tk()
        self.root.title("Warehouse Management System")

    def run(self):
        self.create_widgets()
        self.populate_items()  # Make sure this is called to populate the listbox
        self.root.mainloop()

    def create_widgets(self):
        # Create the algorithm comparison UI
        self.create_algorithm_comparison_tools()

        # Create the item management UI
        self.create_item_management_tools()

    def create_algorithm_comparison_tools(self):
        # Frame for the algorithm comparison
        comparison_frame = ttk.Frame(self.root)
        comparison_frame.pack(padx=10, pady=10, fill='x', expand=True)

        # Labels for the algorithms
        ttk.Label(comparison_frame, text="Greedy Algorithm").grid(row=0, column=0, sticky='w')
        ttk.Label(comparison_frame, text="Genetic Algorithm").grid(row=0, column=1, sticky='w')

        # Labels for the metrics
        ttk.Label(comparison_frame, text="Execution Time:").grid(row=1, column=0, sticky='e')
        ttk.Label(comparison_frame, text="Memory Usage:").grid(row=2, column=0, sticky='e')
        ttk.Label(comparison_frame, text="Effectiveness:").grid(row=3, column=0, sticky='e')

        # Variables to store metrics
        self.greedy_time = tk.StringVar(value="0")
        self.genetic_time = tk.StringVar(value="0")
        self.greedy_memory = tk.StringVar(value="0")
        self.genetic_memory = tk.StringVar(value="0")
        self.greedy_effectiveness = tk.StringVar(value="0")
        self.genetic_effectiveness = tk.StringVar(value="0")

        # Labels for displaying metrics
        ttk.Label(comparison_frame, textvariable=self.greedy_time).grid(row=1, column=1, sticky='w')
        ttk.Label(comparison_frame, textvariable=self.genetic_time).grid(row=1, column=2, sticky='w')
        ttk.Label(comparison_frame, textvariable=self.greedy_memory).grid(row=2, column=1, sticky='w')
        ttk.Label(comparison_frame, textvariable=self.genetic_memory).grid(row=2, column=2, sticky='w')
        ttk.Label(comparison_frame, textvariable=self.greedy_effectiveness).grid(row=3, column=1, sticky='w')
        ttk.Label(comparison_frame, textvariable=self.genetic_effectiveness).grid(row=3, column=2, sticky='w')

        # Button to initiate comparison
        compare_button = ttk.Button(comparison_frame, text="Compare Algorithms", command=self.compare_algorithms)
        compare_button.grid(row=4, columnspan=3, pady=5)
        pass

    def compare_algorithms(self):
        # Load orders to process
        orders_to_process = self.order_processor.get_orders_to_process("C:/Users/walla/Downloads/ADA22/ADA2/Updated Warehouse Data.csv")

        # Compare algorithms
        comparison_results = self.performance_analyzer.compare_algorithms(
            orders_to_process, 
            self.order_processor.process_using_greedy, 
            self.order_processor.process_using_genetic
        )

        # Update the GUI with the results
        self.greedy_time.set(f"{comparison_results['greedy']['execution_time']:.2f} seconds")
        self.genetic_time.set(f"{comparison_results['genetic']['execution_time']:.2f} seconds")
        self.greedy_memory.set(f"{comparison_results['greedy']['peak_memory_usage']:.2f} MB")
        self.genetic_memory.set(f"{comparison_results['genetic']['peak_memory_usage']:.2f} MB")
        self.greedy_effectiveness.set(f"{comparison_results['greedy']['effectiveness']} items processed")
        self.genetic_effectiveness.set(f"{comparison_results['genetic']['effectiveness']} items processed")

    def create_item_management_tools(self):
        # Frame for item management
        item_management_frame = ttk.LabelFrame(self.root, text="Item Management")
        item_management_frame.pack(fill="x", expand=True)

         # Define the entry_fields_frame here
        self.entry_fields_frame = ttk.Frame(item_management_frame)
        self.entry_fields_frame.pack(side="top", fill="x", expand=True)

        # Listbox to display items, with a scrollbar
        self.item_listbox = tk.Listbox(item_management_frame)
        self.item_listbox.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(item_management_frame, orient="vertical", command=self.item_listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.item_listbox.config(yscrollcommand=scrollbar.set)

        # Right side frame for entry fields, search, and buttons
        right_frame = ttk.Frame(item_management_frame)
        right_frame.pack(side="left", fill="both", expand=True)

        # Entry fields and labels for item details
        labels = ['Order_ID', 'Product_ID', 'Order_Quantity', 'Priority', 'Product_Type', 'Location', 'Weight', 'Size']
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(right_frame, text=label).grid(row=i, column=0, sticky='e')
            entry = ttk.Entry(right_frame)
            entry.grid(row=i, column=1, sticky='ew')
            self.entries[label] = entry

        # Search field and buttons
        ttk.Label(right_frame, text="Search by Product_ID:").grid(row=len(labels), column=0, sticky='e')
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(right_frame, textvariable=self.search_var)
        search_entry.grid(row=len(labels), column=1, sticky='ew')
        search_button = ttk.Button(right_frame, text="Search Item", command=self.search_items)
        search_button.grid(row=len(labels) + 1, column=0, sticky='ew')
        show_all_button = ttk.Button(right_frame, text="Show All Items", command=self.populate_items)
        show_all_button.grid(row=len(labels) + 1, column=1, sticky='ew')

        # Buttons for adding, saving, and deleting items
        add_item_button = ttk.Button(right_frame, text="Add Item", command=self.add_item)
        add_item_button.grid(row=len(labels) + 2, column=0, sticky='ew')
        save_item_button = ttk.Button(right_frame, text="Save Item", command=self.save_item)
        save_item_button.grid(row=len(labels) + 2, column=1, sticky='ew')
        delete_item_button = ttk.Button(right_frame, text="Delete Item", command=self.delete_item)
        delete_item_button.grid(row=len(labels) + 3, columnspan=2, sticky='ew')

        # Initially populate the list with all items from the CSV
        self.populate_items()

    def on_item_select(self, event):
        # Method to handle item selection from the listbox
        widget = event.widget
        index = int(widget.curselection()[0])
        item_key = widget.get(index)

        # Fetch item details and update entry fields
        item = self.warehouse_layout.get_item(item_key)
        for label, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, str(getattr(item, label.lower())))

    def update_item(self):
        # Method to update the selected item
        selected_index = self.item_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No item selected.")
            return
        item_key = self.item_listbox.get(selected_index[0])
        item_details = {label: entry.get() for label, entry in self.entries.items()}
        
        # Call the update_item method of the WarehouseLayout class
        self.warehouse_layout.update_item(item_key, item_details)
        
        # Provide feedback to the user
        messagebox.showinfo("Success", f"Item {item_key} updated successfully.")
        
        # Refresh the item list to show the updated details
        self.populate_items()

    def add_item(self):
        item_details = {label.lower(): entry.get() for label, entry in self.entries.items()}
    # Map the keys to the constructor parameter names, if they are different
        item_details = {
            'order_id': item_details.get('order_id'),
            'product_id': item_details.get('product_id'),
            'quantity': item_details.get('order_quantity'),
            'priority': item_details.get('priority'),
            'product_type': item_details.get('product_type'),
            'location': item_details.get('location'),
            'weight': float(item_details.get('weight', 0)),  # convert weight to float
            'size': item_details.get('size'),
        }
     # Create a new WarehouseItem instance
        new_item = WarehouseItem(**item_details)
    # Add the new item to the warehouse
        self.warehouse_layout.add_item(new_item)
    # Reflect the change in the GUI
        self.populate_items()
    # Clear the entry fields
        for entry in self.entries.values():
            entry.delete(0, tk.END)


    def save_item(self):
    # Get the selected item's key (Product_ID)
        selected_index = self.item_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No item selected.")
            return
        item_key = self.item_listbox.get(selected_index[0]).split(':')[0]  # Assuming the format is "Product_ID: details"

        # Collect updated details from the GUI fields
        updated_details = {label.lower(): entry.get() for label, entry in self.entries.items()}

        # Update the corresponding item in the WarehouseLayout class
        self.warehouse_layout.update_item(item_key, updated_details)

        # Save the updated items dictionary back to the CSV for persistence
        self.warehouse_layout.save_items_to_csv()

        # Provide feedback to the user
        messagebox.showinfo("Success", f"Item {item_key} saved successfully.")

        # Refresh the item list to reflect the changes
        self.populate_items()

    def delete_item(self):
        selected_index = self.item_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No item selected.")
            return
        # Get the product_id of the selected item
        item_key = self.item_listbox.get(selected_index[0]).split(':')[0]
        # Delete the item from the warehouse
        self.warehouse_layout.delete_item(item_key)
        # Reflect the change in the GUI
        self.populate_items()

    def search_items(self, event=None):
        search_queries = {label.lower(): entry.get().strip() for label, entry in self.entries.items() if entry.get().strip()}
        self.item_listbox.delete(0, tk.END)

        found_items = False
        for item in self.warehouse_layout.items.values():
            item_attributes = {k: str(v) for k, v in vars(item).items()}

            # Special handling for 'order_id' to match both padded and non-padded versions
            search_order_id = search_queries.get('order_id')
            if search_order_id is not None:
                item_order_id = item_attributes.get('order_id')
                # Remove leading zeros for the comparison
                if item_order_id.lstrip('0') != search_order_id.lstrip('0'):
                    continue

            # Check other attributes
            if any(item_attributes.get(key, '').lower() != value.lower() for key, value in search_queries.items() if key != 'order_id'):
                continue

            # If we reach here, it means all attributes have matched
            display_text = f"{item.order_id}: {item.product_id} - {item.product_type} - Qty: {item.quantity} - Priority: {item.priority} - Location: {item.location} - Weight: {item.weight} - Size: {item.size}"
            self.item_listbox.insert(tk.END, display_text)
            found_items = True

        if not found_items:
            self.item_listbox.insert(tk.END, "No items match your search.")

    def populate_items(self):
        self.item_listbox.delete(0, tk.END)  
        for product_id, item in self.warehouse_layout.items.items():
            display_text = f"{product_id}: {item.product_type} - Qty: {item.quantity}"
            print(display_text)  # For debugging
            self.item_listbox.insert(tk.END, display_text)

# Example usage
warehouse_layout = WarehouseLayout()  # You would pass the actual warehouse_layout instance here
order_processor = OrderProcessor(warehouse_layout)  # Pass the actual order_processor instance
performance_analyzer = PerformanceAnalyzer(warehouse_layout)  # Pass the actual performance_analyzer instance
app = WarehouseGUI(warehouse_layout, order_processor, performance_analyzer)
app.run()
