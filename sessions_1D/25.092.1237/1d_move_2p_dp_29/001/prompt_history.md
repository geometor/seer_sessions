
## train_1

**input:**
```
0 2 2 2 2 2 0 0 3 0
```


**output:**
```
0 0 0 2 2 2 2 2 3 0
```


## train_2

**input:**
```
4 4 4 4 4 4 0 0 3 0
```


**output:**
```
0 0 4 4 4 4 4 4 3 0
```


## train_3

**input:**
```
8 8 8 8 0 0 3 0 0 0
```


**output:**
```
0 0 8 8 8 8 3 0 0 0
```

*   **Perception**: The task operates on a single row (1D grid). The transformation involves rearranging segments of the row based on the position of a specific 'marker' pixel, which is green (3). A contiguous block of non-white pixels located to the left of the green pixel is identified. All white pixels (0) also located to the left of the green pixel are collected. In the output, these collected white pixels are placed first, followed by the identified non-white block, then the green pixel, and finally any pixels that were originally to the right of the green pixel. The relative order and content of the segment to the right of the green pixel remain unchanged. The core operation is a conditional rearrangement of elements preceding the green pixel, consolidating white space at the beginning and pushing the main colored block rightward until it's adjacent to the green pixel.

*   **Facts YAML**:
    
```yaml
    task_type: rearrangement_1d
    grid_dimensionality: 1
    elements:
      - pixels:
          colors_present: [white(0), red(2), green(3), yellow(4), azure(8)] # Based on all examples
          marker_pixel: green(3)
      - blocks:
          definition: contiguous sequence of same-colored pixels
          types:
            - white_block: consists of white(0) pixels
            - colored_block: consists of non-white, non-green pixels
    marker_properties:
      - color: green(3)
      - function: partition_marker
        description: Divides the grid into a left part and a right part (including the marker itself). The transformation primarily affects the left part.
    transformation:
      scope: affects only the part of the grid to the left of the green(3) marker.
      input_left_part:
        - identify: largest contiguous block of non-white pixels (main_block)
        - identify: all white(0) pixels (whitespace_pixels)
      output_left_part_construction:
        - place: all identified whitespace_pixels at the beginning.
        - append: the identified main_block.
      output_grid_construction:
        - concatenate: [output_left_part, green(3)_marker, original_right_part]
    relationships:
      - adjacency: used to define blocks and relative positions.
      - partitioning: the green(3) pixel acts as a separator.
    invariants:
      - the green(3) pixel itself does not change color or relative position concerning the right part of the grid.
      - the sequence and colors of pixels to the right of the green(3) pixel remain unchanged.
      - the content (colors and count) of the main_block remains unchanged, only its position shifts.
      - the total count of white(0) pixels remains unchanged.
    ```


*   **Natural Language Program**:
    1.  Locate the green pixel (color 3) in the input row. If no green pixel exists, return the input unchanged (assumption based on observed pattern; needs confirmation if such cases exist).
    2.  Define the 'left part' of the row as all pixels strictly to the left of the green pixel.
    3.  Define the 'right part' of the row as all pixels strictly to the right of the green pixel.
    4.  Within the 'left part', identify the largest contiguous block of pixels that are not white (color 0). Call this the 'main block'. If there are multiple such blocks of the same largest size, select the rightmost one (based on examples). If no non-white block exists in the left part, the 'main block' is empty.
    5.  Count the total number of white pixels (color 0) present in the 'left part'.
    6.  Construct the output row:
        a.  Start with a sequence of white pixels (color 0) equal to the count obtained in step 5.
        b.  Append the 'main block' identified in step 4.
        c.  Append the green pixel (color 3).
        d.  Append the 'right part' identified in step 3, maintaining its original sequence of pixels.
