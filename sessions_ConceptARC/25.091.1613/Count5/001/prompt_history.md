
## train_1

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 3 3 3 0 0 0
0 3 0 3 0 0 0
0 3 3 3 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0
```


## train_2

**input:**
```
0 0 0 0 0 0 0
0 3 3 3 3 0 0
0 3 0 0 3 0 0
0 3 0 0 3 0 0
0 3 3 3 3 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 3 3 3 3 3 0
0 3 0 0 0 3 0
0 3 0 0 0 3 0
0 3 3 3 3 3 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
```

*   **Perception:** The task involves transforming an input grid containing a single, hollow, green (3) object on a white (0) background into a single row output grid filled with white (0) pixels. The green object always appears to be a frame or border, exactly one pixel thick, enclosing a rectangular region of white pixels (the 'hole'). The background of the input grid is consistently white (0). The output grid is always a single row (1 pixel high) and its width varies across examples. The key challenge is determining the width of the output row based on the properties of the input green object.

*   **Facts:**
    
