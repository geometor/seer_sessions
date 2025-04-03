## Perception of Task Elements

The input and output grids are single rows (1D arrays represented horizontally).
Each input grid contains a single horizontal line segment of a specific color (azure, orange, or blue) surrounded by white pixels (0).
The output grid shows the same colored line segment shifted horizontally to the right.
The length and color of the line segment remain unchanged.
The background remains white.
The amount of shift appears consistent across all examples.

Let's analyze the shift amount:
-   **Example 1 (train_1):** The azure (8) line starts at index 10 and ends at index 24 in the input. In the output, it starts at index 12 and ends at index 26. The shift is 2 positions to the right.
-   **Example 2 (train_2):** The orange (7) line starts at index 11 and ends at index 21 in the input. In the output, it starts at index 13 and ends at index 23. The shift is 2 positions to the right.
-   **Example 3 (train_3):** The blue (1) line starts at index 1 and ends at index 8 in the input. In the output, it starts at index 3 and ends at index 10. The shift is 2 positions to the right.

The consistent pattern is a horizontal shift of the colored line segment two positions to the right.

## YAML Facts


```yaml
task_type: transformation
grid_dimensionality: 1D (represented as a single row)
input_features:
  - element: background
    color: white (0)
  - element: object
    type: horizontal line segment
    count: 1
    color: variable (azure, orange, blue in examples)
    properties:
      - contiguous
      - non-white color
output_features:
  - element: background
    color: white (0)
  - element: object
    type: horizontal line segment
    count: 1
    color: same as input object color
    properties:
      - contiguous
      - non-white color
      - same length as input object
transformation:
  action: horizontal shift
  target: the colored line segment object
  direction: right
  magnitude: 2 positions
constraints:
  - The input grid contains exactly one contiguous non-white object (line segment).
  - The object's color and length are preserved.
  - The shift is always 2 positions to the right.
```


## Natural Language Program

1.  Identify the contiguous horizontal segment of non-white pixels in the input row.
2.  Determine the starting and ending column indices of this segment.
3.  Create a new output row of the same length as the input, initialized with white (0) pixels.
4.  Copy the identified colored segment into the output row, starting at the original starting index plus 2, and ending at the original ending index plus 2.