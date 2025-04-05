
## train_1

**input:**
```
9 2 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
9 2 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 3 0 0 0 0 0 0 0 2 0
```


**output:**
```
0 0 0 0 3 0 0 0 0 0 2 0
```


## train_3

**input:**
```
4 4 4 4 4 4 4 4 0 0 2 0
```


**output:**
```
0 0 4 4 4 4 4 4 4 4 2 0
```


## train_4

**input:**
```
0 0 9 0 0 0 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 9 0 0 0 2 0 0 0
```


## train_5

**input:**
```
0 0 0 1 1 0 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 0 1 1 0 2 0 0 0
```


## train_6

**input:**
```
0 2 4 4 4 4 0 0 0 0 0 0
```


**output:**
```
0 2 4 4 4 4 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 2 0 0 7
```


**output:**
```
0 0 0 0 0 0 0 0 2 7 0 0
```

Okay, let's analyze the input-output pairs to understand the transformation.

**1. Perception of Task Elements**

*   The input and output are sequences of integers, always 12 elements long in the examples.
*   The sequences contain single-digit non-negative integers, with '0' being common.
*   The number '2' appears exactly once in every input sequence and seems to play a pivotal role. Its position remains unchanged in the output.
*   Other non-zero numbers sometimes change position relative to the '2'.
*   Numbers *before* the '2' tend to shift *rightwards* towards the '2'.
*   Numbers *after* the '2' tend to shift *leftwards* towards the '2'.
*   The shift seems to happen only when there are exactly two consecutive '0's between the number and the position it moves to. The number effectively "jumps" over these two zeros.
*   Numbers adjacent to '2' (either immediately before or after) do not move.
*   If multiple numbers are eligible to move (e.g., a block like '4 4 4 4'), they maintain their relative order after the shift.
*   The processing order matters: processing elements *before* the '2' from right-to-left and elements *after* the '2' from left-to-right ensures correct placement when blocks of numbers are shifted.

**2. Facts (YAML)**


