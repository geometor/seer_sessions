
## train_1

**input:**
```
0 0 7 0 0 7 0 7 7 7 7 7 7 7 7 7 7 7 0 0 7 0 0 7 0 0 0 7 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 2 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 2 0 0 2 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 6 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0 0 0 6 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves processing 1D horizontal grids (represented as 1xN 2D arrays). Each input grid contains a background color (white, 0) and one other foreground color. The foreground color pixels are arranged in various horizontal segments, some contiguous and some isolated. The output grid retains only the single longest contiguous horizontal segment of the foreground color from the input, replacing all other pixels (including shorter foreground segments and isolated foreground pixels) with the background color. The dimensions of the output grid match the input grid.

*   **Facts:**
    
```yaml
    task_type: noise_reduction_1d
    grid_dimensionality: 1_row
    background_color: 0 (white)
    input_features:
      - contains_background_color: true
      - contains_single_foreground_color: true
      - foreground_pixels_form_horizontal_segments: true
      - segments_can_be_isolated_or_contiguous: true
    output_features:
      - retains_input_dimensions: true
      - contains_background_color: true
      - contains_single_foreground_color: true (same as input)
      - foreground_pixels_form_single_longest_contiguous_horizontal_segment: true
    transformation:
      - identify the foreground color
      - find all contiguous horizontal segments of the foreground color
      - determine the length of each segment
      - identify the segment with the maximum length
      - create output grid filled with background color
      - copy the longest segment to the output grid at its original position
    relationships:
      - output foreground color is identical to input foreground color
      - output grid size is identical to input grid size
      - position of the longest segment is preserved
    ```


*   **Natural Language Program:**
    1.  Identify the non-white foreground color present in the input grid.
    2.  Scan the input grid horizontally to locate all contiguous segments composed solely of the foreground color.
    3.  Calculate the length of each identified segment.
    4.  Find the segment with the greatest length. If there are multiple segments of the same maximum length, select the first one encountered (although the examples only show one clear longest segment).
    5.  Create a new grid with the same dimensions as the input grid, initializing all cells to the background color (white, 0).
    6.  Copy the pixels belonging to the identified longest foreground segment from their original positions in the input grid to the corresponding positions in the new output grid.
    7.  The resulting grid is the final output.
