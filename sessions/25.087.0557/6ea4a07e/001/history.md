
## train_1

**input:**
```
8 0 0
0 8 0
0 0 0
```


**output:**
```
0 2 2
2 0 2
2 2 2
```


## train_2

**input:**
```
0 0 3
0 3 0
3 0 0
```


**output:**
```
1 1 0
1 0 1
0 1 1
```


## train_3

**input:**
```
5 0 0
5 5 0
5 0 0
```


**output:**
```
0 4 4
0 0 4
0 4 4
```


## train_4

**input:**
```
5 5 5
0 0 5
0 0 0
```


**output:**
```
0 0 0
4 4 0
4 4 4
```


## train_5

**input:**
```
0 8 0
0 8 0
8 0 0
```


**output:**
```
2 0 2
2 0 2
0 2 2
```


## train_6

**input:**
```
8 0 8
0 8 0
0 8 0
```


**output:**
```
0 2 0
2 0 2
2 0 2
```

Okay, let's analyze the provided examples for this task.

**Perception**

1.  **Grid Size:** All input and output grids are 3x3.
2.  **Input Colors:** Each input grid contains white (0) and exactly one other color (azure-8, green-3, or gray-5).
3.  **Output Colors:** Each output grid contains white (0) and exactly one other color (red-2, blue-1, or yellow-4).
4.  **Color Transformation:** There appears to be a consistent mapping between the non-white input color and the non-white output color:
    *   Azure (8) in the input maps to Red (2) in the output.
    *   Green (3) in the input maps to Blue (1) in the output.
    *   Gray (5) in the input maps to Yellow (4) in the output.
5.  **Pattern Transformation:** The positions of the non-white color in the output grid are the *inverse* of the positions of the non-white color in the input grid. Where the input had its specific color, the output has white (0). Where the input had white (0), the output has the mapped color.

**Facts**


```yaml
task_context:
  grid_size: fixed (3x3 for all examples)
  input_composition: contains white (0) and one unique non-white color
  output_composition: contains white (0) and one unique non-white color

transformations:
  - type: color_mapping
    input_color: 8 (azure)
    output_color: 2 (red)
  - type: color_mapping
    input_color: 3 (green)
    output_color: 1 (blue)
  - type: color_mapping
    input_color: 5 (gray)
    output_color: 4 (yellow)
  - type: pattern_inversion
    description: >
      The spatial pattern of the non-white color is inverted.
      Cells that were white in the input become the output color.
      Cells that held the unique input color become white in the output.

objects:
  - object: input_pattern
    description: The set of cells containing the unique non-white color in the input grid.
    properties:
      - color: varies (8, 3, or 5 in examples)
  - object: output_pattern
    description: The set of cells containing the unique non-white color in the output grid.
    properties:
      - color: determined by mapping from input_pattern color (2, 1, or 4 in examples)
  - object: background
    description: The set of cells containing white (0).
    properties:
      - color: 0 (white)

relationships:
  - relation: inverse_position
    object1: input_pattern
    object2: output_pattern
    description: The positions occupied by the output_pattern are precisely those *not* occupied by the input_pattern within the grid boundaries.
  - relation: color_correspondence
    object1: input_pattern
    object2: output_pattern
    description: The color of the output_pattern is determined by a fixed mapping based on the color of the input_pattern.
```


**Natural Language Program**

1.  Identify the unique non-white color present in the input grid; let this be `input_color`.
2.  Determine the corresponding `output_color` based on the following mapping: if `input_color` is 8, `output_color` is 2; if `input_color` is 3, `output_color` is 1; if `input_color` is 5, `output_color` is 4.
3.  Create a new output grid with the same dimensions as the input grid.
4.  Iterate through each cell (row `r`, column `c`) of the input grid.
5.  If the color of the input cell at (`r`, `c`) is white (0), set the color of the output grid cell at (`r`, `c`) to `output_color`.
6.  If the color of the input cell at (`r`, `c`) is `input_color`, set the color of the output grid cell at (`r`, `c`) to white (0).
7.  Return the completed output grid.
