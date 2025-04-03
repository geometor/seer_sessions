**Perception:**

The task involves processing 1-dimensional arrays (or single-row grids) of colored pixels. Each input array contains one or more contiguous sequences of a single non-white color, embedded within a background of white pixels (color 0). The transformation focuses on modifying these non-white sequences. Specifically, for each sequence, only the first and the last pixel retain their original color, while all pixels *between* the first and the last are changed to white (color 0). Sequences of length 1 or 2 remain unchanged as there are no pixels strictly *between* the first and last. The white background pixels remain unaffected.

**YAML Facts:**


```yaml
task_type: array_transformation
dimensionality: 1D # (represented as 1xN grids)
background_color: 0 # white
objects:
  - type: contiguous_horizontal_sequence
    properties:
      color: non-zero (e.g., 7, 4, 5)
      minimum_length: 1
      surrounded_by: color 0 (white) or grid boundary
transformation:
  target: each identified non-zero color sequence
  action: conditional_pixel_replacement
  condition: sequence length > 2
  details:
    - Keep the color of the first pixel in the sequence.
    - Keep the color of the last pixel in the sequence.
    - Change the color of all pixels strictly between the first and last pixel to 0 (white).
  unchanged_elements:
    - Background pixels (color 0).
    - Sequences of length 1 or 2.
```


**Natural Language Program:**

1.  Iterate through the input array from left to right.
2.  Identify the start and end indices of each maximal contiguous sequence of non-white pixels (pixels with color > 0).
3.  For each identified sequence:
    a.  Determine its length.
    b.  If the length is greater than 2:
        i.  Keep the pixel at the start index unchanged.
        ii. Keep the pixel at the end index unchanged.
        iii. Change the color of all pixels located at indices between the start index and the end index to white (0).
    c.  If the length is 1 or 2, leave the sequence unchanged.
4.  Keep all original white pixels (color 0) unchanged.
5.  Construct the output array based on these modifications.