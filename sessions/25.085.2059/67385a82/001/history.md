
## train_1

**input:**
```
3 3 0 3
3 3 0 0
3 0 0 3
0 0 3 3
```


**output:**
```
8 8 0 3
8 8 0 0
8 0 0 8
0 0 8 8
```


## train_2

**input:**
```
0 3 0 0 0 3
0 3 3 3 0 0
0 0 0 0 3 0
0 3 0 0 0 0
```


**output:**
```
0 8 0 0 0 3
0 8 8 8 0 0
0 0 0 0 3 0
0 3 0 0 0 0
```


## train_3

**input:**
```
3 3 0 0 0 0
0 3 0 0 3 0
3 0 0 0 0 0
0 3 3 0 0 0
0 3 3 0 0 3
```


**output:**
```
8 8 0 0 0 0
0 8 0 0 3 0
3 0 0 0 0 0
0 8 8 0 0 0
0 8 8 0 0 3
```


## train_4

**input:**
```
3 3 0
0 3 0
3 0 3
```


**output:**
```
8 8 0
0 8 0
3 0 3
```

Okay, let's break down this task.

**Perception of Elements:**

1.  **Grid Structure:** Both input and output are 2D grids of pixels. The grid dimensions vary across examples.
2.  **Colors Involved:** The primary colors in the input grids are green (3) and white (0). The output grids introduce azure (8) while retaining green (3) and white (0).
3.  **Transformation Focus:** The core transformation involves changing *some* green (3) pixels to azure (8) pixels. White (0) pixels always remain white (0). Some green (3) pixels also remain green (3).
4.  **Spatial Relationship:** The decision to change a green pixel seems dependent on its immediate surroundings. Looking at the examples, green pixels that are part of a larger group or cluster (connected orthogonally) tend to change to azure, while isolated green pixels or those only touching other green pixels diagonally often remain green.
5.  **Rule Identification:** By comparing input and output green pixels:
    *   A green pixel changes to azure if it has at least one **orthogonally adjacent** neighbor that is also green.
    *   A green pixel remains green if it has **no orthogonally adjacent** green neighbors.

**Facts (YAML):**


```yaml
task_description: Change the color of certain green pixels based on their neighbors.
elements:
  - type: grid
    properties:
      - Contains pixels with colors.
      - Colors present: green(3), white(0) in input; green(3), white(0), azure(8) in output.
  - type: pixel
    properties:
      - color: integer (0-9)
      - position: (row, column)
      - neighbors: orthogonal (up, down, left, right) and diagonal.
objects:
  - name: green_pixel
    is_a: pixel
    properties:
      - color: 3
  - name: azure_pixel
    is_a: pixel
    properties:
      - color: 8
  - name: white_pixel
    is_a: pixel
    properties:
      - color: 0
relationships:
  - type: adjacency
    applies_to: [pixel, pixel]
    properties:
      - orthogonal
      - diagonal
actions:
  - name: change_color
    input: green_pixel
    output: azure_pixel
    condition: The input green_pixel has at least one orthogonally adjacent neighbor that is also a green_pixel.
  - name: keep_color
    input: pixel
    output: pixel (same color)
    condition: Applies to white_pixels and green_pixels that do not meet the change_color condition.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Examine every pixel in the input grid.
3.  For each pixel located at `(row, col)`:
    a.  If the pixel's color is green (3):
        i.  Check its four orthogonal neighbors: `(row-1, col)`, `(row+1, col)`, `(row, col-1)`, `(row, col+1)`, ensuring they are within the grid boundaries.
        ii. Determine if any of these orthogonal neighbors in the *input* grid have the color green (3).
        iii. If at least one orthogonal neighbor is green (3), change the color of the pixel at `(row, col)` in the *output* grid to azure (8).
        iv. If none of the orthogonal neighbors are green (3), the pixel at `(row, col)` in the *output* grid retains its original green (3) color (no change needed).
    b.  If the pixel's color is not green (3), the pixel at `(row, col)` in the *output* grid retains its original color (no change needed).
4.  Return the final output grid.
