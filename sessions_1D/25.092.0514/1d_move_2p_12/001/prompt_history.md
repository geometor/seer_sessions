
## train_1

**input:**
```
0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
```


## train_3

**input:**
```
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
```

**Perception**

1.  **Input Structure:** Each input is a single row (1D array) of pixels.
2.  **Objects:** The primary object in each input is a contiguous horizontal line (or segment) of a single non-white color (green, gray, or blue). The rest of the row consists of white pixels (color 0).
3.  **Transformation:** The transformation involves shifting the colored line segment horizontally to the right.
4.  **Shift Magnitude:** In all examples, the colored line segment shifts exactly two positions to the right.
5.  **Consistency:** The color, length, and integrity of the colored line segment are preserved during the shift. The white pixels effectively fill the space vacated by the line segment on the left and are pushed out on the right, maintaining the overall row length.
6.  **Background:** The background is uniformly white (color 0).

**YAML Facts**


```yaml
task_description: Horizontally shift a contiguous block of non-white pixels within a single row grid.
grid_properties:
  - dimensions: All examples are 1x25 grids.
  - background_color: white (0)
objects:
  - object_type: horizontal_line_segment
    properties:
      - color: non-white (varies per example: green (3), gray (5), blue (1))
      - contiguity: The pixels forming the line are adjacent horizontally.
      - uniqueness: There is only one such segment per input grid.
    actions:
      - type: shift
        direction: right
        magnitude: 2 positions
relationships:
  - The non-white line segment is embedded within a background of white pixels.
transformation_rule:
  - Identify the contiguous segment of non-white pixels.
  - Translate this segment 2 positions to the right.
  - Ensure the grid dimensions remain the same, padding with the background color (white) as needed.
invariants:
  - Grid dimensions.
  - Color of the line segment.
  - Length of the line segment.
  - Background color.
```


**Natural Language Program**

1.  Identify the single contiguous horizontal segment of non-white pixels within the input row.
2.  Determine the starting and ending indices of this segment.
3.  Create a new output row of the same dimensions as the input row, initially filled with the background color (white, 0).
4.  Copy the identified non-white segment from the input row into the output row, but shifted 2 positions to the right (i.e., starting at index `start_index + 2` and ending at index `end_index + 2`).
