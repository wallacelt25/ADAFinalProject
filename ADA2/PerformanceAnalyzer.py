import time
import tracemalloc

class PerformanceAnalyzer:
    def __init__(self, warehouse_layout):
        self.warehouse_layout = warehouse_layout

    def analyze_performance(self, algorithm_function, *args, **kwargs):
        # Start tracking time and memory usage
        start_time = time.time()
        tracemalloc.start()

        # Run the algorithm functioan
        result = algorithm_function(*args, **kwargs)

        # Stop tracking memory and calculate usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time = time.time()

        # Compile performance data
        performance_data = {
            'execution_time': end_time - start_time,
            'peak_memory_usage': peak / 10**6,  # Convert to MB
            'result': result
        }
        return performance_data

    def compare_algorithms(self, orders, greedy_function, genetic_function):
        greedy_results_total = {
            'execution_time': 0,
            'peak_memory_usage': 0,
            'effectiveness': 0
        }
        genetic_results_total = {
            'execution_time': 0,
            'peak_memory_usage': 0,
            'effectiveness': 0
        }

        # Iterate over each order
        for order in orders:
            greedy_results = self.analyze_performance(greedy_function, order)
            genetic_results = self.analyze_performance(genetic_function, order)

            greedy_results_total['execution_time'] += greedy_results['execution_time']
            greedy_results_total['peak_memory_usage'] += greedy_results['peak_memory_usage']
            greedy_results_total['effectiveness'] += len(greedy_results['result'])

            genetic_results_total['execution_time'] += genetic_results['execution_time']
            genetic_results_total['peak_memory_usage'] += genetic_results['peak_memory_usage']
            genetic_results_total['effectiveness'] += len(genetic_results['result'])

        # Compile comparative analysis
        comparative_analysis = {
            'greedy': greedy_results_total,
            'genetic': genetic_results_total
        }

        print("Greedy results:", greedy_results_total)  # Debug print
        print("Genetic results:", genetic_results_total)  # Debug print

        comparative_analysis = {
            'greedy': greedy_results_total,
            'genetic': genetic_results_total
        }

        return comparative_analysis
