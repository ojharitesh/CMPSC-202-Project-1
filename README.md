# Project 2 Overview - Ritesh, Katie, Abishek

This project focuses on solving the Processing Files problem. A web server receives a queue of files from users and can process only one file at a time. Since processing time
increases with file size, the order in which files are processed affects how long users have to wait.

The goal of this project is to find an ordering of the files that minimizes the average completion time. We first use a brute-force baseline that checks every possible ordering
to find the optimal solution. We then develop a more efficient greedy algorithm that processes files from smallest to largest and compare the correctness and running time of
both approaches.
