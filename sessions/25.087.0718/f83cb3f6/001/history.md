
## train_1

**input:**
```
0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 5 0 0 0 0
5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
5 0 0 0 0 0 0 5 0 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 5 5 0 0 5
8 8 8 8 8 8 8 8 8 8
5 5 5 5 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 8 0 0 0 0 0 0 0 1
1 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 1 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 1 0 0 0 0 0
0 0 0 0 0 8 0 1 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 1 0 0 0
0 0 1 0 0 8 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 1 0
```


**output:**
```
0 0 0 0 0 8 1 0 0 0 0 0 0 0
0 0 0 0 1 8 0 0 0 0 0 0 0 0
0 0 0 0 0 8 1 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 8 1 0 0 0 0 0 0 0
0 0 0 0 0 8 1 0 0 0 0 0 0 0
0 0 0 0 0 8 1 0 0 0 0 0 0 0
0 0 0 0 1 8 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 2 0 0 2 0 0 0 0
2 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 2
0 0 2 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
8 8 8 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 2 0
0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 2 0 0 2 0 0 0 0
8 8 8 0 0 8 8 8 8 0
2 0 0 0 0 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception**

1.  **Input Structure:** Each input grid contains scattered single pixels of one color (gray '5' in train_1, blue '1' in train_2, red '2' in train_3) and a solid line (horizontal or vertical) of azure '8' pixels. The rest of the grid is white '0'.
2.  **Output Structure:** The output grid retains the azure '8' line in its original position. The scattered pixels from the input are either removed or relocated near the azure line. The background remains white '0'.
3.  **Transformation:** The azure '8' line acts as a barrier or separator. The transformation depends on the orientation of this line:
    *   **Horizontal Azure Line (train_1, train_3):** Pixels of the scattered color located *above* the azure line in the input are removed in the output. Pixels of the scattered color located *below* the azure line are moved vertically upwards, stacking against the row immediately *above* the azure line, maintaining their original columns. The lowest pixel in a column lands directly above the line, the next lowest lands above that, and so on.
    *   **Vertical Azure Line (train_2):** Pixels of the scattered color located *to the left* of the azure line in the input are removed in the output. Pixels of the scattered color located *to the right* of the azure line are moved horizontally leftwards, stacking against the column immediately *to the right* of the azure line, maintaining their original rows. The leftmost pixel in a row lands directly to the right of the line, the next leftmost lands to the right of that, and so on.
4.  **Key Colors:** The azure '8' color defines the static barrier. The other non-white color (5, 1, or 2) represents the mobile objects subject to the rule. White '0' is the background.

**Facts**


```yaml
elements:
  - object: barrier_line
    color: 8 (azure)
    shape: solid line (horizontal or vertical)
    property: static, acts as a separator/destination boundary
  - object: mobile_pixels
    color: variable (5, 1, or 2 in examples)
    shape: single pixels
    property: potentially mobile or removable based on position relative to barrier_line
  - object: background
    color: 0 (white)
    property: occupies empty space

relationships:
  - type: relative_position
    objects: [mobile_pixels, barrier_line]
    details: Each mobile pixel is either on one side of the barrier line or the other (e.g., above/below for horizontal line, left/right for vertical line).

actions:
  - action: identify_barrier
    input: input_grid
    output: location (row/column index) and orientation (horizontal/vertical) of the azure line
  - action: identify_mobile_color
    input: input_grid
    output: the color code of the non-zero, non-azure pixels
  - action: filter_and_remove
    condition: based on barrier orientation and mobile pixel position
    details: |
      If barrier is horizontal, remove mobile pixels above it.
      If barrier is vertical, remove mobile pixels to its left.
  - action: relocate_and_stack
    condition: based on barrier orientation and mobile pixel position
    details: |
      If barrier is horizontal, move mobile pixels from below the barrier upwards, stacking them vertically starting from the row just above the barrier, preserving their column.
      If barrier is vertical, move mobile pixels from the right of the barrier leftwards, stacking them horizontally starting from the column just to the right of the barrier, preserving their row.
  - action: preserve_barrier
    details: The barrier_line remains unchanged in the output grid.
  - action: initialize_output
    details: The output grid starts as all white (0).

transformation_goal: Relocate mobile pixels from one side of the barrier line to stack against the other side, removing mobile pixels from the starting side.
```


**Natural Language Program**

1.  Initialize the output grid with the same dimensions as the input grid, filled with white (0).
2.  Find the continuous line of azure (8) pixels in the input grid. Determine its orientation (horizontal or vertical) and its row or column index (`barrier_index`).
3.  Copy the azure (8) line from the input grid to the same location in the output grid.
4.  Identify the color of the mobile pixels (the single color present that is not white (0) or azure (8)). Let this be `mobile_color`.
5.  If the barrier line is horizontal (at `row = barrier_index`):
    *   For each column `c`:
        *   Find all mobile pixels (`mobile_color`) in that column `c` in the input grid located *below* the barrier line (`row > barrier_index`).
        *   Count how many such pixels were found (`count`).
        *   Place these `count` pixels in the output grid in column `c`, starting at row `barrier_index - 1` and moving upwards (i.e., rows `barrier_index - 1`, `barrier_index - 2`, ..., `barrier_index - count`). Fill these cells with `mobile_color`.
6.  If the barrier line is vertical (at `col = barrier_index`):
    *   For each row `r`:
        *   Find all mobile pixels (`mobile_color`) in that row `r` in the input grid located *to the right* of the barrier line (`col > barrier_index`).
        *   Count how many such pixels were found (`count`).
        *   Place these `count` pixels in the output grid in row `r`, starting at column `barrier_index + 1` and moving rightwards (i.e., columns `barrier_index + 1`, `barrier_index + 2`, ..., `barrier_index + count`). Fill these cells with `mobile_color`.
7.  Return the completed output grid.
