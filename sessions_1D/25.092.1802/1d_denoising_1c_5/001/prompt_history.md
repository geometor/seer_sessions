
## train_1

**input:**
```
0 0 0 4 0 0 0 0 4 0 0 0 0 4 0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0
```


## train_2

**input:**
```
0 0 2 0 0 2 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 2 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
```


## train_3

**input:**
```
0 0 4 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 4 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception**

The input grids contain scattered pixels of a single foreground color (yellow in `train_1`, red in `train_2`, yellow in `train_3`) on a white background. The output grids retain only one specific horizontal line segment from the input grid, turning all other pixels white. The core task appears to be identifying and isolating the "most important" horizontal line segment according to some criteria.

Observing the examples:
1.  In `train_1`, the input has various yellow pixels, but the longest contiguous horizontal segment is the full row of yellow at the bottom (row index 4). The output keeps only this line.
2.  In `train_2`, the input has two full horizontal lines of red pixels (row indices 3 and 4) and a few other scattered red pixels. Both lines have the same maximum length (5). The output keeps only the bottom-most of these two lines (row index 4).
3.  In `train_3`, the input has yellow pixels forming various shapes, including horizontal segments of length 3 (row index 1), length 5 (row index 2), and length 3 (row index 3). The longest segment is the one in row index 2. The output keeps only this line.

From these observations, the rule seems to involve finding the longest horizontal contiguous segment of non-white pixels. If there's a tie for the longest segment, the one in the lowest row (highest row index) is chosen. The final output grid consists of only this selected segment against a white background.

**Facts**


```yaml
task_context:
  grid_properties:
    - dimensions: Input and output grids have the same dimensions (5x5 in examples).
    - background_color: Consistently white (0).
    - foreground_colors: A single non-white color per example (yellow/4, red/2).
  elements:
    - type: Pixel
      properties:
        - color
        - position (row, column)
    - type: Horizontal Segment
      definition: A contiguous sequence of one or more pixels of the same non-white color within the same row.
      properties:
        - color
        - length (number of pixels)
        - row_index
        - start_column
        - end_column
  transformation: Filtering based on segment properties.

selection_criteria:
  primary:
    - property: length
    - rule: Select the Horizontal Segment(s) with the maximum length.
  secondary (tie-breaker):
    - condition: More than one segment has the maximum length.
    - property: row_index
    - rule: Select the segment with the highest row index (i.e., the lowest one visually).

output_generation:
  - Create an output grid of the same dimensions as the input, initialized with the background color (white).
  - Place the selected Horizontal Segment into the output grid at its original position.
  - All other pixels remain the background color.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid, but with all pixels set to the background color (white, 0).
2.  Identify all contiguous horizontal segments of non-white pixels in the input grid. For each segment, record its color, length, and row index.
3.  Find the maximum length among all identified segments.
4.  Filter the segments to keep only those that have this maximum length.
5.  If only one segment remains after filtering, select this segment.
6.  If multiple segments remain (i.e., there was a tie for the maximum length), select the segment among them that has the highest row index (is lowest on the grid).
7.  Copy the pixels corresponding to the single selected segment from the input grid to the output grid at their original positions.
8.  The resulting output grid is the final answer.
