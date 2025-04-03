
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 5 7 7 7 7 7 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 5 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 4 8 8 8 8 8 8 8 8 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 4 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 7 8 8 8 8 8 8 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 8 8 8 8 8 8 7 0 0 0 0 0 0 0 0
```

**Perception of Elements:**

The task involves transforming a one-dimensional input grid (represented as a row) into an output grid of the same dimensions. The grids consist primarily of white pixels (0) and contain a single contiguous horizontal segment of non-white pixels. This non-white segment is composed of at least two different colors. The transformation appears to operate solely on this non-white segment, leaving the surrounding white pixels unchanged. Specifically, the first and last pixels of the non-white segment seem to exchange positions.

**YAML Documentation:**


```yaml
task_description: Modify a 1D grid by swapping the first and last pixels of the contiguous non-white segment.
grid_properties:
  - dimensions: 1 row, variable columns (e.g., 1x23)
  - background_color: white (0)
objects:
  - object_type: segment
    description: A single contiguous horizontal sequence of non-white pixels.
    properties:
      - start_column: The column index of the first non-white pixel.
      - end_column: The column index of the last non-white pixel.
      - first_pixel_color: The color of the pixel at the start_column.
      - last_pixel_color: The color of the pixel at the end_column.
      - length: Greater than or equal to 2 pixels.
relationships:
  - The non-white segment is embedded within a background of white pixels.
actions:
  - identify: Locate the contiguous non-white segment within the input grid.
  - extract: Determine the start and end column indices and the colors of the first and last pixels of the segment.
  - swap: Exchange the positions of the first and last pixels within the identified segment.
  - reconstruct: Create the output grid by placing the modified segment back into its original position relative to the white background pixels.
```


**Natural Language Program:**

1.  Iterate through the input grid (which is a single row) to find the start and end column indices of the contiguous sequence of non-white pixels (pixels with values other than 0).
2.  If such a sequence is found and its length is at least 2 pixels:
    a.  Record the color of the pixel at the start index.
    b.  Record the color of the pixel at the end index.
    c.  Create a copy of the input grid for the output.
    d.  In the output grid, set the pixel at the start index to the color recorded from the end index of the input segment.
    e.  In the output grid, set the pixel at the end index to the color recorded from the start index of the input segment.
3.  If no non-white sequence is found, or if it contains only one pixel, the output grid is identical to the input grid.
4.  Return the modified grid as the output.
