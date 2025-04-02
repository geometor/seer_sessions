
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 1 1 1 1 0
0 3 3 0 0 1 0 0 1 0
0 3 3 0 0 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0
0 0
0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 4 4 4 4 0
0 7 7 7 0 4 4 4 4 0
0 7 0 7 0 4 4 4 4 0
0 7 0 7 0 0 0 0 0 0
0 7 0 7 0 8 8 8 0 0
0 7 0 7 0 8 0 8 0 0
0 7 7 7 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```


## train_3

**input:**
```
0 6 6 6 6 6 0 8 8 8
0 6 0 0 0 6 0 8 0 8
0 6 6 6 6 6 0 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0
0 2 2 2 0 0 4 0 4 0
0 2 2 2 0 0 4 0 4 0
0 2 2 2 0 0 4 4 4 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
```


**output:**
```
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```

**Perception**

1.  **Input Structure:** The input is a grid containing a white background (color 0) and several distinct "objects". Each object is a contiguous block of pixels of the same non-white color.
2.  **Output Structure:** The output is always a grid filled entirely with white pixels (color 0). The size (height and width) of the output grid varies between examples.
3.  **Transformation Goal:** The task is to determine the correct dimensions (height and width) for the output grid based on the properties of the objects found in the input grid.
4.  **Object Properties:** The key properties of the objects seem to be their bounding box dimensions (height and width). Color itself doesn't directly determine the output grid's content (which is always white) or necessarily its size, but it helps distinguish objects.
5.  **Identifying the Rule:**
    *   First, all distinct non-white objects need to be identified.
    *   For each object, its height and width (based on its bounding box) must be calculated.
    *   From the set of all object dimensions, four values are crucial: the overall maximum height (MaxH), the overall minimum width (MinW), the overall maximum width (MaxW), and potentially the overall minimum height (MinH), although MinH wasn't needed in the final rule.
    *   A comparison between MaxH and MaxW determines how the output dimensions are calculated.
    *   If the maximum height found among all objects is strictly greater than the maximum width found among all objects (MaxH > MaxW), then the output grid's dimensions are MaxW x MaxW.
    *   Otherwise (if MaxH <= MaxW), the output grid's dimensions are MaxH x MinW.
    *   The output grid is then created with these calculated dimensions and filled with white (0).

**Facts**


