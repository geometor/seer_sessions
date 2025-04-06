
## train_1

**input:**
```
0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 1 0 3 3 3 0 1 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves processing a 2D grid containing primarily 0s and a few 1s. The output grid modifies the input by adding a pattern of 3s. The core operation seems to be identifying the locations of the 1s and drawing a specific shape (a plus sign) centered at the midpoint between them using the value 3.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    input_elements:
      - element: grid
        properties:
          - type: 2D array of integers
          - size: 10x10 (based on examples)
          - values: contains 0s and 1s
      - element: marker_points
        properties:
          - value: 1
          - count: 2 (in examples)
          - role: define locations for transformation
    output_elements:
      - element: grid
        properties:
          - type: 2D array of integers
          - size: same as input grid
          - values: contains 0s, 1s, and 3s
      - element: added_shape
        properties:
          - value: 3
          - shape: plus sign (center + 4 orthogonal neighbors)
          - size: 5 cells
    transformation:
      action: identify_markers
        input: input_grid
        output: coordinates of cells with value 1
      action: calculate_midpoint
        input: coordinates of two marker points (r1, c1), (r2, c2)
        output: midpoint coordinates (mr, mc) = ( (r1+r2)/2, (c1+c2)/2 )
        constraints: midpoint coordinates must be integers (based on examples)
      action: draw_shape
        input: midpoint coordinates (mr, mc)
        target: output_grid
        details: set value to 3 at (mr, mc), (mr-1, mc), (mr+1, mc), (mr, mc-1), (mr, mc+1)
        preservation: original marker points (value 1) are preserved in the output.
    relationships:
      - The added shape (plus sign of 3s) is centered at the midpoint of the two marker points (1s).
      - The output grid is derived from the input grid by adding the shape.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as an identical copy of the input grid.
    2.  Scan the input grid to find the row and column coordinates of the two cells that contain the value 1. Let these coordinates be (r1, c1) and (r2, c2).
    3.  Calculate the integer midpoint coordinates (mr, mc) between these two points using the formula: `mr = (r1 + r2) // 2` and `mc = (c1 + c2) // 2`. (Using integer division assumes the midpoint falls exactly on a grid cell or halfway between cells, and we take the floor).
    4.  Identify the set of five coordinates representing the plus shape centered at the midpoint: the midpoint itself (mr, mc), and its four orthogonal neighbors: (mr-1, mc), (mr+1, mc), (mr, mc-1), (mr, mc+1).
    5.  For each coordinate in this set of five, update the corresponding cell in the output grid to the value 3, provided the cell is within the grid boundaries. (The examples suggest the original 1s are not overwritten, which is naturally handled if the midpoint and its neighbors don't coincide with the original 1s).
