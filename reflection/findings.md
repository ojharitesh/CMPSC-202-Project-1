# Processing Files Problem

The Processing Files problem asks us to reorder a list of files so that the average completion time is minimized. Only one file can be processed at a time, so the order of the files affects how long each file waits before finishing. Our project compares a brute-force baseline with a more efficient greedy algorithm.

## Problem Formulation

We have a list of `n` files, written as `F = [f₁, f₂, ..., fₙ]`. Each file's size represents how long it takes to process. A file's completion time includes its own processing time and the time spent processing the files before it. Our goal is to arrange the files so that their average completion time is as small as possible.

For example, for the order `[8, 3, 6, 2]`, the completion times are $8$, $11$, $17$, and $19$, giving an average of $13.75$. Reordering the files to `[2, 3, 6, 8]` gives completion times $2$, $5$, $11$, and $19$, with an average of $9.25$.

## Baseline Solution

The baseline uses a brute-force approach. It generates every possible permutation of the files, calculates the average completion time for each permutation, and keeps the ordering with the smallest average.

```text
Algorithm ProcessFilesBaseline(F):
    best_order = F
    best_average = infinity

    for each permutation P of F:
        current_time = 0
        total_completion_time = 0

        for each file in P:
            current_time = current_time + file
            total_completion_time = total_completion_time + current_time

        average = total_completion_time / number of files

        if average < best_average:
            best_order = P
            best_average = average

    return best_order, best_average
```

The baseline guarantees an optimal result because it checks every possible ordering. However, it becomes impractical for large inputs. There are $n!$ possible permutations, and evaluating each permutation takes $O(n)$ time, so the overall time complexity is $O(n! \times n)$.

## Proposed Algorithmic Strategy

To efficiently find the ordering with the minimum average completion time, we propose a greedy algorithmic strategy that processes smaller files first. The core insight is that each file delays every file after it, so processing shorter files first reduces the total time that files spend waiting.

We begin by sorting the list of file sizes in ascending order. We then process the files in that order, keeping track of the elapsed processing time and the sum of all completion times. For each file, we add its size to the elapsed time, which gives that file's completion time. We add this completion time to the running total. After processing all files, we divide the total completion time by the number of files to find the average. If the list is empty, we return an empty ordering and an average of zero.

```text
Algorithm ProcessFilesGreedy(F):
    input: List of file sizes F of length n
    output: Optimal file ordering and minimum average completion time

    if n == 0:
        return [], 0

    order = Sort F in ascending order
    current_time = 0
    total_completion_time = 0

    for each file in order:
        // Calculate when this file finishes
        current_time = current_time + file
        total_completion_time = total_completion_time + current_time

    average = total_completion_time / n
    return order, average
```

### Step-by-Step Walkthrough

To understand how the greedy approach works, let's trace it with the example array of files `F = [8, 3, 6, 2]`.

- **Initialization:** Sort the files to get `[2, 3, 6, 8]`. Set `current_time = 0` and `total_completion_time = 0`.
- **Step 1:** Process the file of size 2. It finishes at time `0 + 2 = 2`. The total completion time is `2`.
- **Step 2:** Process the file of size 3. It finishes at time `2 + 3 = 5`. The total completion time is `2 + 5 = 7`.
- **Step 3:** Process the file of size 6. It finishes at time `5 + 6 = 11`. The total completion time is `7 + 11 = 18`.
- **Step 4:** Process the file of size 8. It finishes at time `11 + 8 = 19`. The total completion time is `18 + 19 = 37`.

Optimal ordering: `[2, 3, 6, 8]`. Minimum average completion time: `37 / 4 = 9.25`.

The correctness of this strategy and its time complexity are explained in the sections below.

## Correctness Analysis

### Baseline Algorithm

The baseline algorithm is correct because it checks every possible ordering of the files. For each ordering, it calculates the average completion time and compares it with the best result found so far. Since every possible ordering is evaluated, the algorithm cannot miss the ordering with the minimum average completion time. Therefore, the result returned by the baseline is optimal.

### Greedy Algorithm

The greedy algorithm processes files from smallest to largest. This ordering is optimal because a file affects not only its own completion time, but also the completion time of every file processed after it.

Consider two adjacent files where a larger file is processed before a smaller file. Let the two file sizes be $a$ and $b$, where $a > b$. If the order is $[a, b]$, their completion times are $t + a$ and $t + a + b$, where $t$ is the time before these files begin. Their combined completion time is:

$$
(t + a) + (t + a + b) = 2t + 2a + b
$$

If we swap them to `[b, a]`, their combined completion time becomes:

$$
(t + b) + (t + b + a) = 2t + 2b + a
$$

Because $b < a$, the swapped order has a smaller combined completion time. The completion times of all files after this pair do not change because both files still take the same total time to process. Therefore, swapping any larger file that appears before a smaller file reduces the total completion time. Repeatedly applying this swap produces ascending order, proving that the greedy algorithm returns an optimal ordering.

## Complexity Analysis

### Baseline Algorithm

For $n$ files, the baseline examines $n!$ possible permutations. Calculating the average completion time for one permutation requires processing all $n$ files, which takes $O(n)$ time. Therefore, the total time complexity is:

$$
O(n! \times n)
$$

The baseline also stores a copy of the best ordering, which requires $O(n)$ space. The permutation generator may use additional space while producing each ordering, but the dominant practical limitation is its factorial running time.

### Greedy Algorithm

The greedy algorithm first sorts the $n$ file sizes, which takes $O(n \log n)$ time. It then makes one pass through the sorted files to calculate completion times, which takes $O(n)$ time. The total time complexity is therefore:

$$
O(n \log n) + O(n) = O(n \log n)
$$

The sorted list and the returned ordering require $O(n)$ space. Compared with the baseline's factorial running time, the greedy algorithm is practical for much larger inputs.


## Empirical Synthesis

### Implementation

We implemented two algorithms (`methods.py`) to solve the Processing Files problem: a brute-force baseline and a proposed greedy algorithm. Unit testing (`tests.py`) confirms that both algorithms produce the same optimal ordering and minimum average completion time for various inputs, including empty lists, duplicate file sizes, and already sorted lists.

### Results

We compared the performance of both algorithms using randomly generated arrays of file sizes between 1 and 100 (`benchmark.py`). The benchmark tested different input sizes, ranging from small arrays to 50,000 files, with each algorithm executed five times per tested input size. Because of its factorial time complexity, the baseline was restricted to inputs of at most 10 files, while the greedy algorithm was tested on all input sizes.

The plots below illustrate the differences in execution time. The first plot shows the results on a linear scale, while the second uses a logarithmic scale to better display the large differences between the two algorithms.

| ![Benchmark Plot (Linear Scale)](../assets/benchmark_plot.png) | ![Benchmark Plot (Logarithmic Scale)](../assets/benchmark_plot_log.png) |
| -------------------------------------------------------------- | ----------------------------------------------------------------------- |

The following graph focuses specifically on the brute-force baseline, illustrating how its execution time increases as the number of files grows.

![Benchmark Plot (Baseline Only)](../assets/benchmark_baseline.png)

Our empirical results are consistent with our theoretical complexity analysis:

- **Baseline Factorial Scaling:** The baseline algorithm has a theoretical time complexity of $O(n \times n!)$ because it examines every possible ordering of the files. At 10 files, the baseline took approximately **1.034 seconds** on average. This demonstrates how quickly the brute-force approach becomes impractical as input sizes increase.

- **Proposed Algorithm Efficiency:** The greedy algorithm operates at $O(n \log n)$ because it sorts the files before calculating their average completion time. At 10 files, the greedy algorithm took approximately **0.000000733 seconds**, compared to the baseline's 1.034 seconds. Even when processing 50,000 files, the greedy algorithm took only approximately **0.00352 seconds**, demonstrating its scalability.

- **Runtime Observations:** The linear-scale graph shows a sharp increase in baseline execution time, while the greedy algorithm appears nearly flat because its runtimes are significantly smaller. The logarithmic-scale graph makes these differences easier to observe. Although greedy runtimes generally increased with input size, minor fluctuations occurred, potentially due to system activity or measurement overhead.

Overall, our findings support the theoretical efficiency of the greedy algorithm. While both algorithms produce the same optimal results, the greedy approach requires significantly less computation. However, because the baseline was only benchmarked on smaller inputs, our measurements provide limited direct evidence of its full factorial growth.

**The Real-World Impact:** The performance difference between these algorithms has important practical implications. A web server processing a large queue of files must determine an efficient processing order without introducing unnecessary delays. Using the greedy algorithm allows the server to calculate an optimal ordering much more efficiently than the brute-force approach. This demonstrates how choosing an efficient algorithm can improve scalability while minimizing computational overhead.
