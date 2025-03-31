
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 2 7 7 2 0 0 0
0 0 0 2 7 7 2 0 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 2 2 2 2 0 0 0
0 2 2 7 7 7 7 2 2 0
0 2 2 7 2 2 7 2 2 0
0 2 2 7 2 2 7 2 2 0
0 2 2 7 7 7 7 2 2 0
0 0 0 2 2 2 2 0 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 4 6 4 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 4 6 6 6 4 0 0 0
0 0 4 6 4 6 4 0 0 0
0 0 4 6 6 6 4 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 1 1 3 0 0 0 0
0 0 3 1 1 3 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 3 3 3 0 0 0 0
3 3 1 1 1 1 3 3 0 0
3 3 1 3 3 1 3 3 0 0
3 3 1 3 3 1 3 3 0 0
3 3 1 1 1 1 3 3 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception**

1.  **Input Structure:** Each input grid features a single, prominent, non-white object set against a uniform white background (color 0). This object consistently appears as a rectangular frame of one color (`outer_color`) surrounding a rectangular core region containing another color (`inner_color`).
2.  **Output Structure:** The output grid also contains a single, larger object against a white background. This output object incorporates the original input object at its center. The original object appears expanded outwards.
3.  **Transformation Pattern:** The transformation seems to involve projecting the original object's structure outwards by two "layers".
    *   The rows and columns occupied by the original object are extended outwards by two cells on each side (left, right, top, bottom).
    *   The cells immediately adjacent (1 cell away) to the original object along these extended rows/columns are filled with the original object's `inner_color`.
    *   The cells next further out (2 cells away) along these extended rows/columns are filled with the original object's `outer_color`.
    *   The original object remains unchanged in its initial position.
    *   Pixels outside these extended rows/columns remain white, creating a cross-like or plus-shaped expansion rather than a solid rectangular one.

**Facts**


