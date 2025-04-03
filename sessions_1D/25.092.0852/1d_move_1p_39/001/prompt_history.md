
## train_1

**input:**
```
0 6 6 6 6 6 6 6 0 0 0 0
```


**output:**
```
0 0 6 6 6 6 6 6 6 0 0 0
```


## train_2

**input:**
```
2 2 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
6 6 6 6 6 6 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 6 6 6 0 0 0 0 0
```

*   **Perception:** The input consists of a single row (a 1D array) containing mostly white pixels (0) and a single contiguous block of non-white pixels of a specific color (magenta or red in the examples). The output is a row of the same size where the non-white block has been shifted one position to the right. The background remains white.

*   **YAML Facts:**
    
```yaml
    task_type: array_transformation
    dimensionality: 1D
    input_characteristics:
      - type: array
      - contains:
          - background_color: white (0)
          - object:
              type: contiguous_block
              color: non-white (variable, e.g., magenta (6), red (2))
              count: 1
    output_characteristics:
      - type: array
      - size: same as input
      - contains:
          - background_color: white (0)
          - object:
              type: contiguous_block
              color: same as input object
              count: 1
              position: shifted one unit right relative to input position
    transformation:
      action: shift
      target: non-white_contiguous_block
      direction: right
      distance: 1 unit
      background_handling: maintain background color (white) in vacated/new positions
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of non-white pixels in the input array. Note its color, starting index, and ending index.
    2.  Create a new output array of the same size as the input array, initially filled entirely with white pixels (0).
    3.  Determine the new starting index for the block by adding 1 to the original starting index.
    4.  Copy the sequence of non-white pixels from the identified block in the input array into the output array, starting at the new calculated index.
