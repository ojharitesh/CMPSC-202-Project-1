# Findings

## Empirical Synthesis

Our empirical results show a significant difference in efficiency compared to the brute-force baseline and our proposed greedy algorithm. The baseline has a theoretical time complexity of **O(n × n!)** as it attempts all possible arrangements of the files. However, the greedy algorithm takes **O(n log n)** time since it sorts the files before determining the average completion time. Our benchmarking results are consistent with these theoretical expectations and show that the greedy approach is significantly more efficient as the number of files gets larger.

For an input size of 10 files, the brute-force algorithm took on average approximately **1.84 seconds**, while the greedy algorithm ran for approximately **0.00000314 seconds**. This difference demonstrates how fast the factorial complexity of the baseline becomes impractical. Hence the baseline benchmarks were restricted to smaller input sizes while the greedy algorithm was tested with up to 50,000 files. Even at this largest input size the greedy algorithm took **0.00528 seconds**, roughly.

We can also see from our visualizations how the algorithms differ. The baseline's runtime increases rapidly on the linear-scale graph, while the greedy algorithm appears almost flat as its running times are significantly smaller. The logarithmic-scale graph shows the runtime differences for the input sizes tested more effectively. In general, the running times of the greedy algorithm increased with input size. It did have some minor swings though, which could be due to system activity.

Overall, our empirical results support our theoretical analysis and show that the greedy algorithm is a much more scalable approach to the Processing Files problem. The greedy algorithm requires far less computation, but still gives the same optimal result as the baseline, which checks all possible orderings. One limitation of our evaluation is that the baseline was only measured at small input sizes so our benchmarks may offer limited direct evidence of its factorial growth.

![Execution Time Comparison (Linear Scale)](../assets/benchmark_plot.png)

![Execution Time Comparison (Logarithmic Scale)](../assets/benchmark_plot_log.png)

![Execution Time Comparison (Baseline Only)](../assets/benchmark_baseline.png)

## Baseline Comparison

## Reflection
