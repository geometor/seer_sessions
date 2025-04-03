**Perception:**

The input is always a single row (1D grid). It contains a contiguous horizontal segment of a single non-white color, surrounded by white pixels (color 0). The output grid has the same dimensions as the input. The transformation rule seems to isolate the endpoints of the colored segment. Specifically, it keeps the first and the last pixel of the colored segment and changes all the pixels *between* these endpoints to white (color 0). The pixels outside the original colored segment remain white. The color of the endpoints in the output matches the color of the segment in the input.

**Facts:**


```yaml
task_type: Grid Transformation
grid_dimensionality: 1D (single row)
input_composition:
  - background: white (0) pixels
  - object:
      type: contiguous horizontal segment
      count: 1
      color: non-white (magenta, green, yellow in examples)
      properties:
        - start_index
        - end_index
        - color_value
output_composition:
  - background: white (0) pixels
  - objects:
      type: individual pixels
      count: 2 (unless the segment length is 1)
      color: same as the input segment color
      location:
        - at the start_index of the input segment
        - at the end_index of the input segment
transformation:
  - Identify the single contiguous non-white segment in the input row.
  - Determine its color, start index, and end index.
  - Create an output row of the same size, initialized to white (0).
  - Place the segment's color at the start index in the output row.
  - Place the segment's color at the end index in the output row.
  - All other pixels in the output row remain white (0).
relationships:
  - The output grid size is identical to the input grid size.
  - The color of the output pixels is determined by the color of the input segment.
  - The positions of the output pixels correspond to the start and end positions of the input segment.
```


**Natural Language Program:**

1.  Identify the contiguous block of non-white pixels in the input row. Note its color, the index of its first pixel (start index), and the index of its last pixel (end index).
2.  Create a new output row with the same length as the input row, filled entirely with white (0) pixels.
3.  Set the pixel at the start index in the output row to the color identified in step 1.
4.  Set the pixel at the end index in the output row to the color identified in step 1.
5.  Return the modified output row.