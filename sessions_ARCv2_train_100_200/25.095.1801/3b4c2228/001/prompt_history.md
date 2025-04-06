
## train_1

**input:**
```
0 3 3 0 0
0 3 3 0 0
0 0 0 0 0
2 2 0 0 2
2 2 0 0 0
0 0 0 2 2
0 0 0 2 2
```


**output:**
```
1 0 0
0 0 0
0 0 0
```


## train_2

**input:**
```
0 3 3 0 0 0 3
0 3 3 0 0 0 0
0 0 0 0 2 0 0
3 0 0 0 3 3 0
0 0 3 0 3 3 0
```


**output:**
```
1 0 0
0 1 0
0 0 0
```


## train_3

**input:**
```
0 0 0 2 2
3 3 0 2 2
3 3 0 0 0
0 0 2 2 0
3 0 2 2 0
```


**output:**
```
1 0 0
0 0 0
0 0 0
```


## train_4

**input:**
```
0 0 3 3 0 0 0
2 0 3 3 0 3 0
0 0 0 0 0 0 0
3 3 0 0 2 2 0
3 3 0 0 2 2 0
0 0 3 3 0 0 0
0 0 3 3 0 0 0
```


**output:**
```
1 0 0
0 1 0
0 0 1
```


## train_5

**input:**
```
2 2 0 3 0 0 3
2 2 0 2 2 0 0
0 0 0 2 2 0 0
2 3 3 0 0 2 2
0 3 3 0 0 2 2
0 0 0 0 3 3 0
3 0 2 0 3 3 0
```


**output:**
```
1 0 0
0 1 0
0 0 0
```

## Perception of Task Elements

The input is a rectangular grid of integers, specifically 0, 2, and 3. The output is always a 3x3 grid containing only 0s and 1s. The task involves identifying specific patterns within the input grid and summarizing their presence and potentially their order or location in the fixed-size output grid. The number '0' appears to function as a background color. The numbers '2' and '3' seem to represent different kinds of objects or patterns within the grid. The transformation specifically focuses on identifying contiguous 2x2 blocks composed entirely of the number '3'. The number '2' appears to be irrelevant to the final output. The position of the '1's in the 3x3 output grid correlates with the order in which these 2x2 blocks of '3's are found when scanning the input grid from top-to-bottom, left-to-right.

## YAML Fact Document


```yaml
task_type: pattern_detection_and_mapping
input_domain:
  data_type: 2D_grid
  element_type: integer
  possible_values: [0, 2, 3]
  value_semantics:
    0: background
    2: irrelevant_object_color
    3: target_object_color
output_domain:
  data_type: 2D_grid
  element_type: integer
  possible_values: [0, 1]
  grid_size: [3, 3]
  value_semantics:
    0: pattern_absent_at_position
    1: pattern_present_at_position
identified_objects:
  - name: target_pattern
    shape: square
    size: [2, 2]
    composition: uniform_color
    color_value: 3
relationships:
  - type: spatial_scan_order
    description: Input grid is scanned top-to-bottom, then left-to-right to find instances of the target pattern.
  - type: mapping_order
    description: The detected target patterns are mapped to specific locations in the output grid based on their discovery order.
    mapping_rules:
      - order: 1st_found -> output_coord: [0, 0]
      - order: 2nd_found -> output_coord: [1, 1]
      - order: 3rd_found -> output_coord: [2, 2]
actions:
  - action: find_pattern
    target: target_pattern
    input: input_grid
    result: list_of_top_left_coordinates
  - action: sort_coordinates
    input: list_of_top_left_coordinates
    criteria: row_index_ascending, then_column_index_ascending
    result: sorted_list_of_coordinates
  - action: map_to_output
    input: sorted_list_of_coordinates
    output: 3x3_output_grid
    logic: Place '1' at diagonal positions corresponding to the order of the first three found patterns.
constraints:
  - Only the first three detected patterns (in scan order) influence the output.
  - The output grid size is fixed at 3x3.
```


## Natural Language Program

1.  Initialize a 3x3 output grid, filling it entirely with the value 0.
2.  Create an empty list to store the row and column indices (coordinates) of the top-left corner of each identified target pattern.
3.  Iterate through each cell `(r, c)` of the input grid, considering it as a potential top-left corner for a 2x2 square. Stop the iteration early enough so that a 2x2 square fits entirely within the grid boundaries (i.e., iterate `r` from 0 to `height - 2` and `c` from 0 to `width - 2`).
4.  For each potential top-left corner `(r, c)`, check if the cell at `(r, c)`, `(r+1, c)`, `(r, c+1)`, and `(r+1, c+1)` in the input grid all contain the value 3.
5.  If all four cells contain the value 3, add the coordinate `(r, c)` to the list of found patterns.
6.  After scanning the entire input grid, sort the list of found coordinates based primarily on the row index (ascending) and secondarily on the column index (ascending).
7.  Examine the sorted list of coordinates:
    a.  If the list contains at least one coordinate, set the value of the output grid at position `(0, 0)` to 1.
    b.  If the list contains at least two coordinates, set the value of the output grid at position `(1, 1)` to 1.
    c.  If the list contains at least three coordinates, set the value of the output grid at position `(2, 2)` to 1.
8.  Return the final 3x3 output grid.
