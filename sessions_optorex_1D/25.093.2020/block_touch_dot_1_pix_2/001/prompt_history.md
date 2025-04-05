
## train_1

**input:**
```
0 0 0 0 0 6 6 0 0 0 2 0
```


**output:**
```
0 0 0 0 0 0 6 6 0 0 2 0
```


## train_2

**input:**
```
6 6 6 6 0 0 0 0 0 2 0 0
```


**output:**
```
0 6 6 6 6 0 0 0 0 2 0 0
```


## train_3

**input:**
```
2 0 3 3 3 3 3 3 3 3 3 0
```


**output:**
```
2 3 3 3 3 3 3 3 3 3 0 0
```


## train_4

**input:**
```
0 2 0 7 7 7 7 7 7 7 0 0
```


**output:**
```
0 2 7 7 7 7 7 7 7 0 0 0
```


## train_5

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 2
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 2
```


## train_6

**input:**
```
0 2 0 0 0 0 0 5 0 0 0 0
```


**output:**
```
0 2 0 0 0 0 5 0 0 0 0 0
```


## train_7

**input:**
```
0 0 2 1 1 1 1 1 1 1 0 0
```


**output:**
```
0 0 2 1 1 1 1 1 1 1 0 0
```

Okay, here are my observations and the natural language program for the task.

## Perception of Elements

1.  **Input/Output Format:** Both input and output are sequences (lists) of single-digit non-negative integers. The length of the sequence appears constant (12 elements in all examples).
2.  **Key Element:** The number `2` seems to act as a crucial marker or pivot point within the sequence. Its presence and position influence the transformation.
3.  **Role of Zero (`0`):** Zeros appear to interact with adjacent non-zero numbers, triggering shifts.
4.  **Transformation Type:** The transformation involves rearranging elements within a specific sub-sequence (segment). The rearrangement resembles a cyclic shift (either left or right).
5.  **Transformation Trigger & Location:**
    *   A transformation seems to occur if there's a zero adjacent to a block of non-zero numbers, either immediately before or immediately after the position of the `2`.
    *   If the pattern `[non-zero block, 0]` occurs *before* the `2`, a *right* cyclic shift happens involving the block and the zero.
    *   If the pattern `[0, non-zero block]` occurs *after* the `2`, a *left* cyclic shift happens involving the zero and the block.
6.  **Segment Identification:** The segment involved in the shift consists of the triggering zero and the adjacent contiguous block of non-zero numbers.
7.  **Priority:** The examples suggest only one shift occurs per sequence. The logic seems to prioritize checking for the condition before the `2` first, and only if that doesn't trigger a shift, it checks for the condition after the `2`.
8.  **No Change Condition:** If the number `2` is absent, or if neither the "before `2`" nor the "after `2`" conditions for a shift are met, the input
