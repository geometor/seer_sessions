
## train_1

**input:**
```
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 9 7 7 7 7 7 7
9 9 9 7 7 2 2 2
8 8 8 8 8 8 8 8
```


**output:**
```
7 7 7 7 7 7 7 7
7 9 7 7 7 7 7 7
9 9 9 7 7 7 7 7
7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
8 8 8 8 8 8 8 8
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 9 7 7 7 7
7 2 7 9 7 7 7 3
7 2 7 9 7 1 7 3
8 8 8 8 8 8 8 8
```


**output:**
```
7 7 7 7 7 7 7 7
7 7 7 9 7 7 7 7
7 7 7 9 7 7 7 7
7 2 7 9 7 7 7 3
7 2 7 7 7 7 7 3
7 7 7 7 7 1 7 7
7 7 7 7 7 7 7 7
8 8 8 8 8 8 8 8
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 4
1 1 7 7 7 3 7 4
1 1 1 7 3 3 7 4
8 8 8 8 8 8 8 8
```


**output:**
```
1 1 7 7 7 7 7 7
1 1 1 7 7 7 7 4
7 7 7 7 7 3 7 4
7 7 7 7 3 3 7 4
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
8 8 8 8 8 8 8 8
```

Okay, let's analyze the provided examples.

**Perception**

1.  **Grid Structure:** The task operates on 8x8 grids.
2.  **Background & Border:** There's a consistent background color, Orange (7), and a solid border color, Azure (8), along the bottom edge (row 7). These appear static in the transformation.
3.  **Objects:** Each input grid contains several distinct objects composed of contiguous pixels of colors other than Orange (7) or Azure (8). These objects vary in shape, color, and size (pixel count).
4.  **Transformation:** The core transformation involves moving these objects vertically upwards. The background and border remain unchanged.
5.  **Movement Rule:** The amount each object shifts upwards seems directly related to the size of the object itself. Specifically, after analyzing the examples, the vertical shift distance (in rows) for each object is equal to the number of pixels that make up that object. Objects retain their shape and color during the shift. No horizontal movement occurs.

**Facts**


```yaml
task_context:
  grid_size: [8, 8]
  static_elements:
    - element_type: background
      color: 7 # Orange
      location: all cells not occupied by border or objects
    - element_type: border
      color: 8 # Azure
      location: all cells in the last row (row index 7)
  dynamic_elements:
    - element_type: object
      description: Contiguous blocks of pixels with colors other than 7 (Orange) or 8 (Azure).
      properties:
        - color: Varies (e.g., 9, 2, 3, 1, 4)
        - shape: Varies (e.g., L-shape, bar, block, single pixel)
        - size: Measured by the number of pixels (P)
        - position: Defined by the set of coordinates (row, column) for its pixels.
      actions:
        - action_type: vertical_shift
          direction: upwards
          magnitude_determinant: size (number of pixels P)
          rule: shift_amount = P
relationships:
  - Each object's transformation is independent of other objects' initial positions but depends solely on its own size.
  - Objects maintain their internal structure (shape) and color during the shift.
  - The final position of an object is its initial position shifted upwards by P rows.
```


**Natural Language Program**

1.  Initialize the output grid as an exact copy of the input grid. This preserves the background (Orange, 7) and the bottom border (Azure, 8).
2.  Identify all distinct contiguous objects in the input grid. An object consists of one or more connected pixels (sharing a side or corner) that are neither the background color (Orange, 7) nor the border color (Azure, 8).
3.  For each identified object:
    a.  Determine the set of coordinates `(r, c)` for all pixels belonging to this object in the input grid.
    b.  Count the total number of pixels `P` in this object.
    c.  Calculate the upward shift amount `S = P`.
    d.  For every pixel `(r, c)` belonging to this object in the input grid:
        i.  Temporarily set the color of the corresponding pixel `(r, c)` in the *output* grid to the background color (Orange, 7). This effectively erases the object from its original position in the output grid copy.
4.  For each identified object again:
    a.  Retrieve its original color and the set of its original coordinates `(r, c)`.
    b.  Retrieve its calculated shift amount `S`.
    c.  For every original pixel coordinate `(r, c)` of the object:
        i.  Calculate the new coordinate `(r', c')` where `r' = r - S` and `c' = c`.
        ii. Set the color of the pixel at the new coordinate `(r', c')` in the output grid to the object's original color.
