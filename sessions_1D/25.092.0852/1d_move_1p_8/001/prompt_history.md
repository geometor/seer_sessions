
## train_1

**input:**
```
0 2 2 2 2 0 0 0 0
```


**output:**
```
0 0 2 2 2 2 0 0 0
```


## train_2

**input:**
```
0 0 8 8 8 0 0 0 0
```


**output:**
```
0 0 0 8 8 8 0 0 0
```


## train_3

**input:**
```
8 8 8 8 8 0 0 0 0
```


**output:**
```
0 8 8 8 8 8 0 0 0
```

**Perception:**

The task involves transforming a 1-dimensional grid (or a 1xN grid) containing a single contiguous block of a non-white color surrounded by white pixels. The transformation consists of shifting this entire block one position to the right, while maintaining its color and size. The grid dimensions remain unchanged.

**Facts:**


```yaml
task_type: object_transformation
grid_dimensionality: 1D
objects:
  - type: contiguous_block
    color: non-white (varies per example, e.g., red, azure)
    quantity: 1
    properties:
      - size (length): varies per example
      - position: varies per example
background_color: white (0)
transformation:
  - type: translation
    direction: right
    distance: 1 unit
    target: the single non-white block
properties_preserved:
  - grid_size
  - object_color
  - object_size (length)
```


**Natural Language Program:**

1.  Identify the contiguous block of non-white pixels in the input grid. Note its color, starting position, and length.
2.  Create a new grid of the same dimensions as the input grid, filled entirely with white pixels.
3.  Place the identified block (with its original color and length) into the new grid, starting at the position one unit to the right of its original starting position.
4.  The resulting grid is the output.
