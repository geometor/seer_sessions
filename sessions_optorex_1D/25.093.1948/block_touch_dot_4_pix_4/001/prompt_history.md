
## train_1

**input:**
```
0 0 0 0 0 2 3 3 3 3 3 3
```


**output:**
```
0 0 0 0 0 2 3 3 3 3 3 3
```


## train_2

**input:**
```
0 0 0 3 3 0 0 0 0 0 2 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 0 2 0
```


## train_3

**input:**
```
0 2 0 0 9 9 9 9 9 9 9 0
```


**output:**
```
0 2 9 9 9 9 9 9 9 0 0 0
```


## train_4

**input:**
```
0 4 4 4 4 0 2 0 0 0 0 0
```


**output:**
```
0 0 4 4 4 4 2 0 0 0 0 0
```


## train_5

**input:**
```
0 0 6 6 6 6 6 6 6 6 6 2
```


**output:**
```
0 0 6 6 6 6 6 6 6 6 6 2
```


## train_6

**input:**
```
0 0 6 6 6 0 0 0 0 0 2 0
```


**output:**
```
0 0 0 0 0 0 6 6 6 0 2 0
```


## train_7

**input:**
```
0 2 0 0 0 0 0 8 8 8 8 0
```


**output:**
```
0 2 0 8 8 8 8 0 0 0 0 0
```

Okay, let's break down the transformation.

**Perception of Elements:**

1.  **Input/Output:** The data consists of pairs of sequences (lists) of single-digit integers.
2.  **Key Marker:** The digit `2` appears in every example and seems to function as a crucial separator or pivot point in the sequence.
3.  **Main Objects:** Besides `0` and `2`, the most prominent features are contiguous blocks of identical non-zero digits (e.g., `3 3 3`, `9 9 9 9 9 9 9`, `4 4 4 4`, `6 6 6`, `8 8 8 8`). Usually, there's one such "main block" that undergoes movement.
4.  **Context:** The zeros (`0`) surrounding the main block and the marker `2` are relevant. Specifically, the zeros located *between* the main block and the `2` seem to participate in the transformation.
5.  **Action:** The core action appears to be a positional swap or shift involving the main block and the intervening zeros relative to the marker `2`. The direction of the shift depends on whether the block is initially to the left or right of `2`.

**YAML Facts:**


