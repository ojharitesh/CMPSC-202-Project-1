# Empirically measures the execution time of the file ordering algorithms.

import os
from time import perf_counter
import random
import pandas as pd
from methods import ProcessFilesBaseline, ProcessFilesGreedy

def generate_test_data(size, max_L):
    """Generates an array of random file sizes."""
    return [random.randint(1, max_L) for _ in range(size)]

def benchmark_algo_multi(algo, test_cases, repeat=1):
    times = []
    for i in test_cases:
        for _ in range(repeat):
            start = perf_counter()
            algo(i)
            end = perf_counter()
            times.append((len(i), end - start))
    return times

def run_benchmarks():
    # Identical input sizes shared by both algorithms
    input_sizes = [10, 50, 100, 500, 1000, 5000, 10000, 20000, 30000, 40000, 50000]
    L = 100
    
    # Generate one master set of test cases so inputs are identical
    test_cases = [generate_test_data(size, L) for size in input_sizes]

    # Filter test cases for Baseline to only keep sizes <= 10 items (needed as to prevent freezing because the baseline algorithm is O(n^2) and will take too long for larger sizes)
    baseline_test_cases = [case for case in test_cases if len(case) <= 10]
    
    print("Running Baseline algorithm (Filtered to safe sizes)...")
    baseline_times = benchmark_algo_multi(lambda files: ProcessFilesBaseline(files), baseline_test_cases, repeat=5)
    
    print("Running Greedy algorithm (All sizes)...")
    greedy_times = benchmark_algo_multi(lambda files: ProcessFilesGreedy(files), test_cases, repeat=5)
    
    # Structure data into DataFrames
    df_baseline = pd.DataFrame(baseline_times, columns=['Files', 'Time(seconds)'])
    df_baseline['Algorithm'] = 'Baseline'
    
    df_greedy = pd.DataFrame(greedy_times, columns=['Files', 'Time(seconds)'])
    df_greedy['Algorithm'] = 'Greedy'

    # Combine dataframes
    df_all = pd.concat([df_baseline, df_greedy], ignore_index=True)
    
    # Ensure directory exists and save file safely
    target_path = "./assests/empirical_results.csv"
    output_dir = os.path.dirname(target_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    df_all.to_csv(target_path, index=False)
    
    print("\nAll Recorded Times:")
    print(df_all)

if __name__ == '__main__':
    run_benchmarks()
