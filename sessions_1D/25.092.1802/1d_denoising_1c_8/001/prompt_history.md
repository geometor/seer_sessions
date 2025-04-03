
## train_1

**input:**
```
0 0 2 0 0 0 0 2 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0 0 2 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 2 0 0 0 0 2 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 2 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 6 0 0 0 0 6 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 0 0 6 0 0 0 6 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    The input consists of a single row of pixels, primarily white (0) with scattered segments of a single non-white color (red '2' in train\_1 and train\_2, magenta '6' in train\_3). These non-white segments vary in length. The output retains only the longest contiguous segment of the non-white color from the input, placed in the same position. All other pixels in the output grid, including those that were part of shorter non-white segments in the input, are white (0). The core transformation involves identifying contiguous blocks of non-white pixels, comparing their lengths, and preserving only the longest block while discarding the others.

*   **Facts:**
    
```yaml
    task_type: filtering
    input_dimensionality: 1D (presented as row)
    output_dimensionality: 1D (presented as row)
    background_color: white (0)
    objects:
      - type: contiguous_horizontal_segment
        properties:
          - color (non-white)
          - length (number of pixels)
          - position (start and end index)
    actions:
      - identify: find all contiguous horizontal segments of non-white pixels.
      - measure: determine the length of each segment.
      - compare: find the segment with the maximum length among all identified segments.
      - filter: keep only the single longest segment.
      - replace: set all pixels not belonging to the longest segment to the background color (white).
    relationships:
      - comparison_criterion: length of the segment.
      - preservation: the longest segment's color and position are preserved in the output.
      - removal: all segments shorter than the longest one are removed (pixels turned to white).
    constraints:
      - Input and output grids have the same dimensions.
      - Assumes a unique longest segment based on provided examples.
    ```


*   **Natural Language Program:**
    1.  Create a new grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
    2.  Scan the input grid horizontally to identify all contiguous segments of non-white pixels. Record the color, start index, end index, and length for each segment found.
    3.  Determine which of these identified segments has the greatest length.
    4.  Copy the pixels corresponding to this single longest segment from the input grid to the new grid at the identical position.
    5.  The new grid is the output.
