
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 1 2 0 0 2 1 1 0
0 1 1 2 0 0 2 1 1 0
0 2 2 0 0 0 0 2 2 0
0 1 1 0 0 0 0 1 1 0
0 1 1 0 0 0 0 1 1 0
0 2 2 0 0 0 0 2 2 0
0 1 1 2 1 1 2 1 1 0
0 1 1 2 1 1 2 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 1 2 1 1 2 1 1 0
0 1 1 2 1 1 2 1 1 0
0 2 2 0 0 0 0 2 2 0
0 1 1 0 0 0 0 1 1 0
0 1 1 0 0 0 0 1 1 0
0 2 2 0 0 0 0 2 2 0
0 1 1 2 1 1 2 1 1 0
0 1 1 2 1 1 2 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 2 6 6 6 6 2 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 2 6 6 0 0 2 0
```


**output:**
```
0 2 6 6 6 6 2 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 2 6 6 6 6 2 0
```

Okay, let's analyze the provided examples to understand the transformation logic.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are 2D grids (matrices) containing single digits (0-9).
2.  **Grid Size:** The grid dimensions remain unchanged between input and output in both examples (12x10 for Ex1, 6x8 for Ex2).
3.  **Content:** The grids contain a background of '0's and foreground patterns/shapes composed of non
