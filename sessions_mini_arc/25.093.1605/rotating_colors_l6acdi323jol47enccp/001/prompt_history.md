
## train_1

**input:**
```
7 0 8 0 9
0 0 0 0 0
1 0 0 0 5
0 0 0 0 0
2 0 3 0 4
```


**output:**
```
8 0 9 0 5
0 0 0 0 0
7 0 0 0 4
0 0 0 0 0
1 0 2 0 3
```


## train_2

**input:**
```
0 0 0 0 0
0 4 5 1 0
0 6 0 2 0
0 7 8 9 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 5 1 2 0
0 4 0 9 0
0 6 7 8 0
0 0 0 0 0
```


## train_3

**input:**
```
0 3 0 6 0
5 0 0 0 8
0 0 0 0 0
2 0 0 0 7
0 1 0 9 0
```


**output:**
```
0 6 0 8 0
3 0 0 0 7
0 0 0 0 0
5 0 0 0 9
0 2 0 1 0
```


## train_4

**input:**
```
0 9 8 7 0
7 0 0 0 6
4 0 0 0 5
3 0 0 0 4
0 1 2 3 0
```


**output:**
```
0 8 7 6 0
9 0 0 0 5
7 0 0 0 4
4 0 0 0 3
0 3 1 2 0
```


## train_5

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 4 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 4 0 0
0 0 0 0 0
0 0 0 0 0
```

**Perception of Elements:**

1.  **Input/Output:** Both are 2D grids (matrices) of integers, specifically 5x5 in all examples.
2.  **Grid Contents:** The grids contain digits from 0 to 9. The digit '0' appears to represent empty space or background. Non-zero digits are the primary objects of interest.
3.  **Core Transformation:** The transformation involves rearranging the non-zero digits within the grid. The positions of the '0' digits remain fixed relative to the overall structure, although non-zero digits might move into or out of positions previously occupied by '0'.
4.  **Pattern of Movement:** The non-zero digits appear to move in a rotational manner. Observing the examples, particularly train_1 and train_2, suggests movement along concentric square paths or "layers" within the grid.
    *   The outermost layer consists of cells in row 0, column 0, row 4, and column 4.
    *   The next inner layer consists of cells in row 1, column 1, row 3, and column 3 (that are not part of the outer layer).
    *   The innermost layer is the single cell at (2, 2).
5.  **Direction of Movement:** Tracking individual numbers (e.g., 7 at (0,0) in train_1 moves to (2,0) in the output, while 8 at (0,2) moves to (0,0)) reveals a clockwise shift. However, it's not a simple rotation of all cells in the layer. Instead, each non-zero digit moves to the position previously occupied by the *previous* non-zero digit encountered when traversing the layer clockwise. Equivalently, each non-zero position in the output grid receives its value from the *next* non-zero position encountered clockwise in the input grid.
6.  **Handling of Zeroes:** Zeroes ('0') do not participate in the rotation; they remain stationary unless a non-zero digit moves into their position. The path of rotation effectively skips over the zero cells.
7.  **Consistency:** This layered clockwise rotation of non-zero elements holds for all examples. In train_5, the single non-zero element is at the center (layer 2), which has only one position. Rotating a single element results in no change, correctly matching the output.

**YAML Fact Document:**


```yaml
task_description: "Rotate non-zero digits clockwise within concentric layers of a 2D grid."
grid_properties:
  dimensionality: 2
  element_type: integer
  value_range: 0-9
  background_value: 0
  size: 5x5 (constant across examples)
objects:
  - name: grid_cell
    properties:
      - value: integer (0-9)
      - coordinate: (row, column)
  - name: non_zero_digit
    properties:
      - value: integer (1-9)
      - initial_coordinate: (row, column) in input grid
      - final_coordinate: (row, column) in output grid
  - name: concentric_layer
    properties:
      - layer_index: integer (0 for outermost, increasing inwards)
      - coordinates: list of (row, column) tuples defining the layer path clockwise
relationships:
  - type: containment
    subject: non_zero_digit
    object: concentric_layer
    description: Each non-zero digit belongs to a specific concentric layer based on its coordinates.
  - type: spatial
    subject: non_zero_digit
    object: non_zero_digit
    description: Non-zero digits within the same layer have a clockwise positional relationship.
actions:
  - name: identify_layers
    description: Determine the coordinates belonging to each concentric layer of the grid.
  - name: extract_non_zero_elements
    description: For each layer, identify the coordinates containing non-zero digits.
  - name: rotate_elements
    description: >
      For each layer, map each non-zero digit's value from its original position
      in the input grid to the position of the *previous* non-zero digit
      encountered clockwise within that layer in the output grid.
      Equivalently, determine the value for each non-zero position in the output
      grid by taking the value from the *next* non-zero position clockwise
      in the input grid.
  - name: preserve_zeroes
    description: Zero values remain in their original positions unless replaced by a rotated non-zero digit. (Implicit in the rotation logic focusing only on non-zero positions).
```


**Natural Language Program:**

1.  Create an output grid of the same dimensions as the input grid, initially copying the input grid.
2.  Determine the number of concentric layers based on the grid size (N=5). The layers are indexed from `l=0` (outermost) to `floor((N-1)/2)` (innermost).
3.  For each layer index `l`:
    a.  Generate a list of coordinates `layer_coords` that trace the perimeter of the layer in clockwise order, starting from the top-left corner `(l, l)`.
    b.  Create a list `non_zero_coords_in_layer` containing only those coordinates from `layer_coords` where the input grid has a non-zero value.
    c.  If the number of non-zero coordinates in the layer is greater than 1:
        i.  Iterate through `non_zero_coords_in_layer` using an index `k` from 0 to its length minus 1.
        ii. Identify the "target" coordinate `(tgt_r, tgt_c)` as the `k`-th coordinate in `non_zero_coords_in_layer`.
        iii. Determine the index of the "source" coordinate within `non_zero_coords_in_layer` by calculating `source_idx = (k + 1) % len(non_zero_coords_in_layer)` (this wraps around to get the *next* non-zero coordinate clockwise).
        iv. Identify the "source" coordinate `(src_r, src_c)` as the coordinate at `source_idx` in `non_zero_coords_in_layer`.
        v. Get the `value` from the input grid at the source coordinate: `value = input[src_r][src_c]`.
        vi. Place this `value` into the output grid at the target coordinate: `output[tgt_r][tgt_c] = value`.
4.  Return the final output grid.
