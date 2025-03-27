
## train_1

**input:**
```
7 7 8
7 7 8
8 8 8
```


**output:**
```
7 7 8 8 7 7
7 7 8 8 7 7
8 8 8 8 8 8
8 8 8 8 8 8
7 7 8 8 7 7
7 7 8 8 7 7
```


## train_2

**input:**
```
8 6
6 8
```


**output:**
```
8 6 6 8
6 8 8 6
6 8 8 6
8 6 6 8
```


## train_3

**input:**
```
6 9 9
6 4 4
6 4 4
```


**output:**
```
6 9 9 6 6 6
6 4 4 4 4 9
6 4 4 4 4 9
9 4 4 4 4 6
9 4 4 4 4 6
6 6 6 9 9 6
```

**Perception**

1.  **Input/Output Size:** The output grid is always twice the height and twice the width of the input grid. If the input is HxW, the output is 2Hx2W.
2.  **Grid Structure:** The output grid can be conceptually divided into four quadrants, each having the same dimensions as the input grid.
3.  **Transformation:** Each quadrant of the output grid is a rotated version of the entire input grid.
    *   The Top-Left (TL) quadrant is
