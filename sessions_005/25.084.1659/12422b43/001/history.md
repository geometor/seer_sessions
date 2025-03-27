
## train_1

**input:**
```
5 0 0 3 3 0
5 0 0 3 2 0
5 0 0 2 3 0
5 0 0 8 8 0
0 0 0 8 8 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
5 0 0 3 3 0
5 0 0 3 2 0
5 0 0 2 3 0
5 0 0 8 8 0
0 0 0 8 8 0
0 0 0 3 3 0
0 0 0 3 2 0
0 0 0 2 3 0
0 0 0 8 8 0
0 0 0 3 3 0
0 0 0 3 2 0
0 0 0 2 3 0
0 0 0 8 8 0
```


## train_2

**input:**
```
5 0 8 8 0 0 0
5 0 0 7 0 0 0
5 0 0 4 4 0 0
0 0 3 3 0 0 0
0 0 1 1 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
5 0 8 8 0 0 0
5 0 0 7 0 0 0
5 0 0 4 4 0 0
0 0 3 3 0 0 0
0 0 1 1 0 0 0
0 0 8 8 0 0 0
0 0 0 7 0 0 0
0 0 0 4 4 0 0
```


## train_3

**input:**
```
5 0 0 4 4 0 0
5 0 8 8 8 0 0
0 0 0 2 0 0 0
0 0 0 3 3 0 0
0 0 4 4 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
5 0 0 4 4 0 0
5 0 8 8 8 0 0
0 0 0 2 0 0 0
0 0 0 3 3 0 0
0 0 4 4 0 0 0
0 0 0 4 4 0 0
0 0 8 8 8 0 0
0 0 0 4 4 0 0
0 0 8 8 8 0 0
```


## train_4

**input:**
```
5 0 6 8 0 0
0 0 8 3 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
5 0 6 8 0 0
0 0 8 3 0 0
0 0 6 8 0 0
0 0 6 8 0 0
0 0 6 8 0 0
0 0 6 8 0 0
0 0 6 8 0 0
```


## train_5

**input:**
```
5 0 6 0 0
5 4 4 4 0
0 0 6 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
5 0 6 0 0
5 4 4 4 0
0 0 6 0 0
0 0 6 0 0
0 4 4 4 0
```

*   **Perception**: The task involves replicating patterns found in the upper portion of an input grid into the lower, initially empty portion. All examples feature a distinct vertical gray bar on the leftmost column, which seems to act as an anchor or selector. The objects to be replicated are colored shapes (non-white, non-gray) that are adjacent to this gray bar. The replication process involves copying the horizontal rows containing these selected objects downwards, repeating the pattern until the bottom of the grid is reached or filled. The original content, including the gray bar and the initial set of objects, remains in the output grid.

*   **Facts**:
    
```yaml
    elements:
      - item: grid
        properties:
          - background_color: white (0)
          - contains: objects
          - contains: vertical_bar
      - item: vertical_bar
        properties:
          - color: gray (5)
          - location: leftmost column (column 0)
          - role: anchor/selector
          - state: static (unchanged in output)
      - item: objects
        properties:
          - color: non-white (0), non-gray (5)
          - shape: variable (1x1, 1x2, 2x1, etc.)
          - location: initially in the upper part of the grid
      - item: selected_objects
        properties:
          - subtype_of: objects
          - condition: adjacent (including diagonally) to the gray vertical_bar
      - item: pattern_block
        properties:
          - composition: horizontal rows from the input grid
          - row_range: spans from the minimum row index to the maximum row index containing any part of any selected_object
          - column_range: excludes the leftmost column (column 0) containing the gray bar
      - item: empty_space
        properties:
          - location: lower part of the input grid, below the initial objects
          - color: white (0)
          - role: destination for replication
    actions:
      - action: identify
        actor: system
        target: gray vertical_bar
      - action: identify
        actor: system
        target: all colored objects
      - action: select
        actor: system
        input: all colored objects
        output: selected_objects
        condition: adjacency to gray vertical_bar
      - action: determine
        actor: system
        input: selected_objects
        output: row range (min_row_sel, max_row_sel)
      - action: define
        actor: system
        input: input grid, row range (min_row_sel, max_row_sel)
        output: pattern_block
      - action: determine
        actor: system
        input: input grid (excluding gray bar)
        output: maximum row index of any non-white pixel (max_row_orig)
      - action: replicate
        actor: system
        source: pattern_block
        destination: empty_space in the output grid, starting below max_row_orig
        details: The pattern_block is copied repeatedly downwards, filling the available white space vertically. Each copy starts immediately below the previous block (or the original objects for the first copy). Copying stops if the grid boundary is reached, potentially truncating the last copy.
    relationships:
      - type: adjacency
        from: selected_objects
        to: gray vertical_bar
        importance: defines which objects form the pattern
      - type: spatial
        item: pattern_block
        relation: located below original objects in the output
      - type: repetition
        item: pattern_block
        direction: vertical downwards
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify the gray (5) vertical bar in the first column (column 0).
    3.  Find all colored pixels (not white 0 and not gray 5) in the input grid. Group contiguous pixels of the same color into objects.
    4.  Select the objects that have at least one pixel adjacent (horizontally, vertically, or diagonally) to any pixel of the gray bar in column 0.
    5.  If no objects are selected, return the unchanged input grid.
    6.  Determine the minimum row index (`min_row_sel`) and the maximum row index (`max_row_sel`) occupied by any pixel belonging to any of the selected objects.
    7.  Define the "pattern block" as the rectangular region of the *input* grid spanning rows `min_row_sel` to `max_row_sel` and columns 1 to the last column.
    8.  Determine the maximum row index (`max_row_orig`) occupied by any non-white (0), non-gray (5) pixel in the entire input grid.
    9.  Set the starting row for the first copy, `current_dest_row`, to `max_row_orig + 1`.
    10. Calculate the height of the pattern block: `pattern_height = max_row_sel - min_row_sel + 1`.
    11. While `current_dest_row` is less than the total height of the grid:
        a.  Iterate through the rows of the pattern block, from `r_offset = 0` up to `pattern_height - 1`.
        b.  Calculate the source row index: `src_r = min_row_sel + r_offset`.
        c.  Calculate the destination row index: `dest_r = current_dest_row + r_offset`.
        d.  If `dest_r` is greater than or equal to the grid height, stop copying for this repetition (break the inner loop).
        e.  Copy the contents of the input grid row `src_r` from column 1 to the end, into the output grid row `dest_r` from column 1 to the end.
        f.  Increment `current_dest_row` by `pattern_height`.
    12. Return the modified output grid.
