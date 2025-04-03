
## train_1

**input:**
```
0 5 5 5 5 5 0 0 0 0
```


**output:**
```
0 5 0 0 0 5 0 0 0 0
```


## train_2

**input:**
```
0 4 4 4 4 0 0 0 0 0
```


**output:**
```
0 4 0 0 4 0 0 0 0 0
```


## train_3

**input:**
```
5 5 5 5 5 5 0 0 0 0
```


**output:**
```
5 0 0 0 0 5 0 0 0 0
```

*   **Perception:**
    *   The input and output grids are always single rows (1xN).
    *   Each input grid contains a single contiguous horizontal segment of a non-white color (gray or yellow in the examples) against a white background (color 0).
    *   The output grid modifies this non-white segment. Specifically, it retains the first and last pixels of the segment but changes all the pixels *between* the first and last to white (0).
    *   Pixels outside the original non-white segment remain unchanged (they stay white).
    *   The length and starting position of the non-white segment vary between examples.

*   **Facts:**
    
```yaml
    examples:
      - description: Example 1 with a gray segment.
        input:
          grid: [[0, 5, 5, 5, 5, 5, 0, 0, 0, 0]]
          objects:
            - type: segment
              color: gray (5)
              location: row 0, columns 1 to 5
              length: 5
            - type: background
              color: white (0)
        output:
          grid: [[0, 5, 0, 0, 0, 5, 0, 0, 0, 0]]
          action: hollow_out_segment
          details: The interior pixels (columns 2, 3, 4) of the gray segment were changed to white.
      - description: Example 2 with a yellow segment.
        input:
          grid: [[0, 4, 4, 4, 4, 0, 0, 0, 0, 0]]
          objects:
            - type: segment
              color: yellow (4)
              location: row 0, columns 1 to 4
              length: 4
            - type: background
              color: white (0)
        output:
          grid: [[0, 4, 0, 0, 4, 0, 0, 0, 0, 0]]
          action: hollow_out_segment
          details: The interior pixels (columns 2, 3) of the yellow segment were changed to white.
      - description: Example 3 with a gray segment starting at the edge.
        input:
          grid: [[5, 5, 5, 5, 5, 5, 0, 0, 0, 0]]
          objects:
            - type: segment
              color: gray (5)
              location: row 0, columns 0 to 5
              length: 6
            - type: background
              color: white (0)
        output:
          grid: [[5, 0, 0, 0, 0, 5, 0, 0, 0, 0]]
          action: hollow_out_segment
          details: The interior pixels (columns 1, 2, 3, 4) of the gray segment were changed to white.

    commonalities:
      grid_dimensions: 1 row, variable columns (10 in examples)
      background_color: white (0)
      input_pattern: Contains exactly one contiguous horizontal segment of a single non-white color.
      transformation: Identifies the non-white segment, keeps its start and end pixels, and changes all pixels between them to white (0).
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Scan the single row of the input grid to find the first non-white pixel. Record its column index as `start_col` and its color.
    3.  Continue scanning from `start_col` to find the last contiguous pixel of the same non-white color. Record its column index as `end_col`.
    4.  Iterate through the columns from `start_col + 1` up to (but not including) `end_col`.
    5.  For each column index in this range, set the corresponding pixel in the output grid to white (0).
    6.  Return the modified output grid.
