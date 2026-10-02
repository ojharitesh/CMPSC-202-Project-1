# Planning and Analysis - Group 2 (Katie, Abishek, Ritesh)

## Problem Formulation: 
The objective of the Processing Files Problem is to efficiently process and reorder the given files to help the user have a seamless experience while waiting.
We are provided with a list of n file sizes, denoted as F = [f1,f2,…,fn]. Calculating the time each file takes to process, our algorithm will find the best way
to handle the user’s input of files, and return the time taken to process. The constraints that we face is that our algorithm can only process one file at any
given time. Our goal for this issue is to design an algorithm that reorders the files to then process them as efficiently as possible so that the average time a
user spends waiting for their files to finish processing is at a minimum, no matter the given amount of files.

### Baseline Solutions:
For our baseline solution, we will be using a brute-force approach. Since the goal is to find the ordering of files that minimizes the average completion
time, the baseline algorithm generates every possible ordering of the files and calculates the average completion time for each one.

The algorithm keeps track of the lowest average completion time found so far and the ordering that produced it. After checking every possible permutation,

it returns the ordering with the minimum average completion time.

```text
Algorithm ProcessFilesBaseline(F):
    input: List of file sizes F of length n
    output: Order with minimum average completion time

    best_order = empty
    best_average = infinity

    for each permutation P of F:
        current_time = 0
        total_completion_time = 0
        for each file in P:
            current_time = current_time + file
            total_completion_time = total_completion_time + current_time
        average = total_completion_time / n

        if average < best_average:
            best_average = average
            best_order = P
    return best_order, best_average
```

For example, if:

`F = [8, 3, 6, 2]` the baseline checks all 4! = 24 possible orderings. After comparing their average completion times, it finds that `[2, 3, 6, 8]` gives the minimum average completion time of 9.25.

The brute-force approach guarantees an optimal solution because it checks every possible ordering. 
This becomes impractical as the number of files increases, motivating the need for a more efficient algorithm.

### Algorithmic Strategy: 

To improve on brute-force baseline, we can use a greedy approach based on Shortest Job First(shortest processing time): sorting files in ascending order then processing them in
that order. The reasoning behind this approach comes from how completion time to process depends on the size of the file which eventually gets accumulated in a single server queue.
This means larger files take more time to process and add more time to the queue for shorter jobs to starve. By placing the smallest files first, we ensure that the files with least
processing time are least responsible for delaying the rest of the queue. And, when it comes down to larger files, they will consume most of their own time without affecting the
rest of the queue. 

Furthermore, this greedy choice can be justified with an exchange argument. Suppose two adjacent files in some ordering are out of order, meaning a larger file is scheduled immediately
before a smaller one. Swapping these two files does not change the completion times of any other file in the queue, but it strictly decreases the combined completion time of the two
swapped files. Since any ordering that is not fully sorted by size must contain at least one such swappable pair, repeatedly applying this swap will always reduce (or never increase)
the total completion time until the list is fully sorted in ascending order. This shows that the sorted order is guaranteed to be optimal.

Here’s a pseudocode that strategizes improving on brute-force baseline solutions. Unlike baseline, we can just sort the files and find the optimal way to process the files and minimize the queue time. 

```text
Algorithm ProcessFilesGreedy(F):
    input: List of file sizes F of length n
    output: Order with minimum average completion time

    P = sort F in ascending order

    current_time = 0
    total_completion_time = 0
    for each file in P:
        current_time = current_time + file
        total_completion_time = total_completion_time + current_time
    average = total_completion_time / n

    return P, average
```

### Complexity Analysis:

Comparing the two algorithms above, we can see that the greedy algorithm is more efficient when compared to the brute force strategy we first designed. The shorter running time, which
is the main issue that we were faced with, is drastically decreased when the files are processed in the greedy algorithm. The naive baseline algorithm operates with a worst-case time
complexity as for n files, there are n! possible orderings, and for each ordering, the algorithm goes through all n files to calculate the average completion time. Therefore,
the overall running time is `O(n! × n)`. Our proposed greedy strategy is more efficient when compared to our brute-force algorithm, with the overall running time of `O(n * logn)`
as the algorithm's performance is dominated by the sorting step at the beginning. Which makes this approach more optimal than the proposed baseline’s running time, `O(n! ×  n)`.
