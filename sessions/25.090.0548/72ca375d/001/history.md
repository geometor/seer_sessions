
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0
0 0 4 4 0 0 8 8 8 0
0 0 0 0 0 0 8 0 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4
4 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 2 2 2 0 0 7 7 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 6
0 6 6 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 3 0 0 5 0 0 5 0
0 0 3 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
8 8 8 8 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 0 0 5
5 5 5 5
```

Okay, let's analyze the task based on the provided examples.

### Perception of Task Elements

1.  **Input Structure**: The input is a grid (10x10 in all examples) containing a white background (color 0) and several distinct "objects".
2.  **Objects**: Objects are contiguous areas of pixels sharing the same non-white color. In each example, there are exactly three such objects, each with a different color.
3.  **Output Structure**: The output is a smaller grid. It appears to be a rectangular subgrid (crop) extracted from the input grid.
4.  **Transformation**: The core task is to identify which object from the input determines the output grid, and then extract the content within that object's bounding box.
5.  **Key Features**: The relevant features seem to be the objects themselves, their colors, their bounding boxes, and the areas of these bounding boxes.

### YAML Facts


