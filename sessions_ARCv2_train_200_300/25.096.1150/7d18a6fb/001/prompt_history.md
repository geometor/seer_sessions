
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 2 0 0 0 0 0 1 2 1 1 1 4 1
0 0 2 2 2 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 2 2 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 1 6 1 1 1 3 1
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 2 0 0 4 0
2 2 2 0 4 4 4
0 2 2 0 0 4 4
0 0 0 0 0 0 0
6 0 6 0 3 3 0
0 6 0 0 3 0 3
6 6 6 0 0 3 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 2 0 2 0 0 0
0 0 0 4 0 0 0 0 2 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0
1 4 1 1 1 8 1 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 8 0 0
1 1 1 1 1 1 1 0 0 8 0 8 0
1 1 1 1 1 1 1 0 0 0 8 0 0
1 3 1 1 1 2 1 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0
```


**output:**
```
0 4 0 0 0 8 0
4 4 4 0 8 0 8
0 4 0 0 0 8 0
0 0 0 0 0 0 0
3 0 3 0 2 2 0
3 3 0 0 2 0 2
0 3 0 0 0 2 0
```


## train_3

**input:**
```
1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 5 1 1 1 4 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 4 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 4 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 4 4 4 0 0 0 0
1 2 1 1 1 3 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 2 0 0 0 0 6 0 0
0 0 3 0 3 0 0 0 2 0 2 0 0 0 0 0 0
0 0 0 3 3 0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0 0 0 0 0 0
0 0 5 0 0 0 0 0 8 8 8 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 0 0 0 0 4
5 5 0 0 0 4 0
0 0 5 0 4 4 4
0 0 0 0 0 0 0
0 2 0 0 3 0 3
2 0 2 0 0 3 3
2 2 2 0 0 0 3
```

## Perception of Task Elements

1.  **Input:** The input is a 2D grid containing integers. Zeroes represent the background. Non-zero integers form distinct "objects" or connected components.
2.  **Objects:** Objects are contiguous blocks of the same non-zero digit.
3.  **Special Objects:** Objects made of the digit '1' often form boundaries or enclosures around other objects.
4.  **Filtering:** Objects enclosed within the largest '1' boundary are irrelevant to the output. The '1' objects themselves are also irrelevant.
5.  **Target Objects:** Typically, four non-'1' objects exist outside the '1' boundary in each input. These are the objects of interest.
6.  **Subgrid Extraction:** Each target object fits within or corresponds to a 3x3 subgrid in the input.
7.  **Output:** The output is a fixed-size 7x7 grid.
8.  **Composition:** The output grid is constructed by arranging the four 3x3 subgrids (extracted from the target objects) into four quadrants of the 7x7 grid, separated by a central row and column of zeros.
9.  **Mapping:** The placement of each 3x3 subgrid into the output quadrants (Top-Left, Top-Right, Bottom-Left, Bottom-Right) depends on the relative spatial position of the corresponding target object in the input grid compared to the other three target objects. Specifically, it's determined by which quadrant the object's center lies in relative to the geometric center of all four target objects.

## Facts about the Transformation


