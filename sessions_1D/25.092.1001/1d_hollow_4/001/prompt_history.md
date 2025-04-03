
## train_1

**input:**
```
0 0 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0
```


**output:**
```
0 0 2 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 0 0
```


**output:**
```
0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 4 0 0
```


## train_3

**input:**
```
0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0
```


**output:**
```
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0
```

**Perception:**

The input grids are all single rows (1 dimension high). Each input contains a contiguous horizontal block (segment) of a single non-white color, surrounded by white pixels (color 0). The output grid retains the same dimensions as the input. The transformation involves modifying the colored segment: only the leftmost and rightmost pixels of the original segment retain their color, while all pixels *between* these two endpoints are changed to white (color 0). The surrounding white pixels remain unchanged. The specific color of the segment varies between examples (red, yellow, green) but the transformation logic is consistent.

**Facts:**


```yaml
task_type: object modification
grid_dimensions: 1 row, variable columns (observed: 18 columns)
objects:
  - type: segment
    description: A contiguous horizontal block of a single non-white color.
    properties:
      - color: The specific non-white color (e.g., red, yellow, green).
      - start_index: The column index of the leftmost pixel of the segment.
      - end_index: The column index of the rightmost pixel of the segment.
      - length: The number of pixels in the segment (end_index - start_index + 1).
  - type: background
    description: Pixels with the white color (0).
    properties:
      - color: 0 (white)
actions:
  - name: identify_segment
    description: Find the start and end indices of the non-white segment.
  - name: modify_segment
    description: >
      Keep the pixels at the start_index and end_index of the segment.
      Change all pixels between the start_index and end_index to the background color (white, 0).
relationships:
  - The output grid has the same dimensions as the input grid.
  - The positions of the background pixels outside the original segment remain unchanged.
  - The color and position of the start_index pixel in the output match the start_index pixel of the input segment.
  - The color and position of the end_index pixel in the output match the end_index pixel of the input segment.
  - If the segment length is 1 or 2, the segment remains unchanged in the output. (Inferred, not explicitly shown in examples, but consistent with the rule).
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions and content as the input grid.
2.  Iterate through the single row of the input grid to find the first non-white pixel. Record its column index as `start_index` and its color.
3.  Continue iterating from `start_index` to find the last consecutive pixel of the same color. Record its column index as `end_index`.
4.  If a non-white segment is found (i.e., `start_index` and `end_index` are determined):
    a.  Iterate through the columns from `start_index + 1` up to (but not including) `end_index`.
    b.  For each column in this range, set the corresponding pixel in the *output* grid to white (0).
5.  Return the modified output grid.
