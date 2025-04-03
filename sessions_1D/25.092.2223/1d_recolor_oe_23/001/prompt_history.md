
## train_1

**input:**
```
0 0 0 7 7 7 0 0 7 7 0 7 7 0 7 7 7 0 0
```


**output:**
```
0 0 0 2 2 2 0 0 6 6 0 6 6 0 2 2 2 0 0
```


## train_2

**input:**
```
0 0 7 7 7 7 7 0 7 7 7 7 0 0 0 7 7 7 7
```


**output:**
```
0 0 2 2 2 2 2 0 6 6 6 6 0 0 0 6 6 6 6
```


## train_3

**input:**
```
0 0 7 7 7 7 7 7 0 0 0 7 7 7 7 7 0 0 7
```


**output:**
```
0 0 6 6 6 6 6 6 0 0 0 2 2 2 2 2 0 0 2
```

## Perception

The input and output are one-dimensional arrays (or single-row grids) of pixels.
The input contains white (0) and orange (7) pixels.
The output contains white (0), red (2), and magenta (6) pixels.
The white pixels remain unchanged in the output.
The orange pixels change color based on the length of the contiguous horizontal segment they belong to.
Specifically, contiguous segments of three orange pixels change to red, and contiguous segments of two orange pixels change to magenta.

## Facts


```yaml
task_context:
  grid_dimensionality: 1D (or single row)
  colors_present_input: [white, orange]
  colors_present_output: [white, red, magenta]

objects:
  - type: pixel_segment
    description: Contiguous horizontal sequence of pixels of the same color.
    properties:
      - color: The color of the pixels in the segment (e.g., white, orange).
      - length: The number of pixels in the segment.

transformation:
  description: Changes the color of orange pixel segments based on their length.
  rules:
    - condition: Input pixel is white (0).
      action: Output pixel remains white (0).
    - condition: Input pixel is orange (7) and belongs to a segment of length 3.
      action: Output pixel becomes red (2).
    - condition: Input pixel is orange (7) and belongs to a segment of length 2.
      action: Output pixel becomes magenta (6).
  unchanged_elements: White background pixels.

relationships:
  - type: color_mapping
    input_color: orange (7)
    output_color_conditions:
      - condition: segment length == 3
        output_color: red (2)
      - condition: segment length == 2
        output_color: magenta (6)
```


## Natural Language Program

1.  Iterate through the input array/row to identify contiguous horizontal segments of orange (7) pixels.
2.  For each identified orange segment:
    *   Determine the length of the segment.
    *   If the length is 3, replace all orange pixels in that segment with red (2) pixels in the output.
    *   If the length is 2, replace all orange pixels in that segment with magenta (6) pixels in the output.
3.  Keep all white (0) pixels unchanged in their original positions in the output.
4.  Construct the output array/row based on these replacements and unchanged pixels.
