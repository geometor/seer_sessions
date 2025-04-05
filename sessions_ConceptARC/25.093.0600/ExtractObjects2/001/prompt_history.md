
## train_1

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 3 0 0 0 0 0 0 0 0
1 1 1 1 3 1 3 1 1 1 1 1 1 1
0 0 0 3 0 0 0 3 0 0 0 0 0 0
1 1 3 1 1 1 1 1 3 1 1 1 1 1
0 0 0 3 0 0 0 3 0 0 0 0 0 0
1 1 1 1 3 1 3 1 1 1 1 1 1 1
0 0 0 0 0 3 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 3 0 0 0
0 0 3 0 3 0 0
0 3 0 0 0 3 0
3 0 0 0 0 0 3
0 3 0 0 0 3 0
0 0 3 0 3 0 0
0 0 0 3 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 0 9 9 9 9 9 0 0 0 0 0 0 0 0
4 0 4 9 4 0 4 9 4 0 4 0 4 0 4 0
0 4 0 9 0 4 0 9 0 4 0 4 0 4 0 4
0 0 0 9 0 0 0 9 0 0 0 0 0 0 0 0
6 0 6 9 9 9 9 9 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 8 0 8 0 8 0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0 8 0 8 0 8 0 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0
0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
9 9 9 9 9
9 0 0 0 9
9 0 0 0 9
9 0 0 0 9
9 9 9 9 9
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 4 0 0 0 4 0 0
0 4 0 4 0 4 0 4 0 4 0
0 0 4 0 0 0 4 0 0 0 4
4 0 0 6 6 6 0 0 4 0 0
0 4 0 4 0 6 0 4 0 4 0
0 0 4 0 0 6 4 0 0 0 4
4 0 0 6 6 6 0 0 0 0 0
0 4 0 4 0 4 0 0 0 4 0
0 0 4 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 4 0 0 0
```


**output:**
```
6 6 6
0 0 6
0 0 6
6 6 6
```

*   **Perception:** The task involves processing 2D grids of integers. The input grids contain background zeros and various non-zero integers forming different patterns and shapes. The output grid is always a subgrid of the input grid. The transformation seems to involve identifying a specific connected region of identical non-zero numbers within the input and extracting the rectangular bounding box surrounding that region.
*   **Logic:** The core logic appears to be:
    1.  Identify all connected components (regions where adjacent cells have the same non-zero value). Connectivity can be considered 4-way (up, down, left, right).
    2.  Determine the "most significant" component. Based on the examples, this seems to be the connected component containing the largest number of cells, irrespective of the actual number value.
    3.  Find the minimal bounding box (smallest rectangle) that encloses all cells of this largest component.
    4.  Extract the subgrid corresponding to this bounding box from the input grid.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    input_elements:
      - type: grid
        description: 2D grid of integers.
        properties:
          - contains_zeros: True (likely background)
          - contains_non_zeros: True (form patterns/objects)
    output_elements:
      - type: grid
        description: A subgrid extracted from the input.
    transformation:
      action: extract_subgrid
      target_object:
        type: connected_component
        properties:
          - composed_of_single_non_zero_value: True
          - criteria_for_selection: largest_area (maximum number of cells)
      subgrid_definition:
        type: bounding_box
        description: Minimal rectangular area enclosing the target connected component.
    relationships:
      - output is a sub-section of the input grid.
      - the content of the output grid directly corresponds to the content of the input grid within the identified bounding box.
    ```


*   **Natural Language Program:**
    1.  Receive the input grid.
    2.  Initialize variables to track the largest connected component found so far (e.g., `max_component_size = 0`, `largest_component_cells = None`).
    3.  Create a `visited` grid of the same dimensions as the input, initialized to `False`.
    4.  Iterate through each cell (`r`, `c`) of the input grid.
    5.  If the current cell `(r, c)` contains a non-zero value and has not been `visited`:
        a.  Initiate a search (e.g., Breadth-First Search or Depth-First Search) starting from `(r, c)` to find all connected cells with the same non-zero value. Mark each visited cell as `True` in the `visited` grid.
        b.  Store the coordinates of all cells belonging to this newly found component.
        c.  Count the number of cells (`current_component_size`) in this component.
        d.  If `current_component_size` is greater than `max_component_size`:
            i.  Update `max_component_size` to `current_component_size`.
            ii. Store the list of cell coordinates for this component in `largest_component_cells`.
    6.  After iterating through all cells, determine the minimum and maximum row (`min_r`, `max_r`) and column (`min_c`, `max_c`) indices from the coordinates stored in `largest_component_cells`. This defines the bounding box.
    7.  Create a new output grid by extracting the subgrid from the input grid ranging from `min_r` to `max_r` (inclusive) and `min_c` to `max_c` (inclusive).
    8.  Return the extracted output grid.
