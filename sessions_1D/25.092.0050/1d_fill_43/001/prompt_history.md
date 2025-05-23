
## train_1

**input:**
```
0 0 2 0 0 0 0 2 0 0 0
```


**output:**
```
0 0 2 2 2 2 2 2 0 0 0
```


## train_2

**input:**
```
0 0 0 0 3 0 0 0 3 0 0
```


**output:**
```
0 0 0 0 3 3 3 3 3 0 0
```


## train_3

**input:**
```
2 0 0 0 0 0 2 0 0 0 0
```


**output:**
```
2 2 2 2 2 2 2 0 0 0 0
```

*   **Perception:**
    *   The inputs and outputs are single-row grids (or 1D arrays).
    *   Each input grid contains exactly two pixels of a single non-white color (red or green in the examples), with the rest being white.
    *   The output grid is generated by filling the white pixels *between* the two non-white pixels in the input with that same non-white color.
    *   The positions of the original non-white pixels remain unchanged.
    *   The transformation identifies the span defined by the two non-white pixels and fills that span.

*   **Facts:**
    
```yaml
    task_type: fill_interval
    grid_dimensionality: 1D
    input_elements:
      - type: background
        color: white (0)
        count: variable
      - type: marker
        color: non-white (2 or 3 in examples)
        count: 2
        properties: defines the start and end of a segment
    actions:
      - identify_markers:
          input: input grid
          output: color and indices of the two non-white pixels
      - fill_segment:
          input: start_index, end_index, fill_color
          target: white pixels between start_index and end_index
          output: modified grid with the segment filled
    relationships:
      - spatial: The transformation acts on the segment *between* the first and last non-white pixels.
    output_elements:
      - type: background
        color: white (0)
        count: variable (potentially fewer than input)
      - type: filled_segment
        color: same as input marker color
        count: variable (original 2 markers + filled pixels)
        properties: forms a contiguous block from the first marker to the last marker
    ```


*   **Natural Language Program:**
    1.  Identify the non-white color present in the input grid.
    2.  Find the index (position) of the first occurrence of this non-white color.
    3.  Find the index (position) of the last occurrence of this non-white color.
    4.  Iterate through the grid cells from the index immediately following the first occurrence up to (but not including) the index of the last occurrence.
    5.  Change the color of each cell visited in the previous step to the identified non-white color.
    6.  Leave all other cells (the original non-white pixels and the white pixels outside the identified range) unchanged.
    7.  The resulting grid is the output.
