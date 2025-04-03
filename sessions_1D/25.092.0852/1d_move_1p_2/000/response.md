**Perception:**

The input grids are all single rows (1x30). Each input contains a horizontal segment of a single non-white color (magenta, blue, or gray) surrounded by white pixels. The output grids are identical to the inputs, except that the colored segment has been shifted one position horizontally to the right. The pixel that was originally the leftmost pixel of the colored segment becomes white, and the white pixel immediately to the right of the original segment takes on the color of the segment.

**Facts:**


```yaml
task_type: object_transformation
grid_dimensions:
  input: 1x30
  output: 1x30
objects:
  - type: horizontal_segment
    color: non-white (varies per example: magenta, blue, gray)
    properties:
      - contiguous
      - surrounded by white pixels
transformation:
  action: horizontal_shift
  direction: right
  distance: 1 pixel
relationships:
  - The colored segment maintains its color and length.
  - The position of the segment changes relative to the grid boundaries.
invariance:
  - Grid dimensions remain the same.
  - The color of the segment remains the same.
  - The length of the segment remains the same.
  - The background color (white) remains the same, except where affected by the shift.
```


**Natural Language Program:**

1.  Identify the contiguous horizontal segment of non-white pixels in the input row.
2.  Determine the color and the start and end column indices of this segment.
3.  Create an output row of the same dimensions, initially filled with white pixels.
4.  Copy the identified segment into the output row, shifting its starting column index one position to the right. Ensure the segment retains its original color and length.