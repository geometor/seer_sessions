
## train_1

**input:**
```
0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0
```


## train_3

**input:**
```
0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task operates on single-row grids (1D arrays). Each input contains a single contiguous block of a non-white color surrounded by white pixels. The transformation involves shifting this colored block one position to the right within the row. The size and color of the block remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_type: grid_manipulation
    grid_dimensionality: 1D # Effectively 1 row
    input_features:
      - name: background
        color: white (0)
        property: fills space not occupied by the object
      - name: object
        property: single contiguous block of non-white pixels
        attributes:
          - color: varies (green, gray, blue in examples)
          - shape: horizontal line segment
          - size: varies
          - position: varies
    transformation:
      - action: identify
        target: non-white object
        details: find start index, end index, and color
      - action: shift
        target: non-white object
        direction: right
        distance: 1 pixel
      - action: maintain
        target: size and color of the object
      - action: fill
        details: position vacated by the left end of the object becomes white
    output_features:
      - name: background
        color: white (0)
      - name: object
        property: same as input object but shifted right by 1
    relationship: The output grid is the input grid with the single non-white object shifted horizontally one position to the right.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous segment of non-white pixels within the input row. Determine its color, its starting column index, and its ending column index.
    2.  Create a new output row with the same length as the input row, initially filled with white pixels (0).
    3.  Copy the identified non-white segment into the output row, placing it starting at (input starting column index + 1) and ending at (input ending column index + 1). Ensure the color is preserved.
    4.  Return the newly created output row.
