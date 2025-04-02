
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0
```


## train_2

**input:**
```
5 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0
```


**output:**
```
0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 0 0
```

**Perception of Task Elements:**

The task involves modifying rows in a grid based on the presence and arrangement of non-white pixels within those rows. Specifically, it identifies rows containing exactly two pixels of the same non-white color. The transformation then fills the horizontal space between these two pixels with the same color. Rows that do not meet this specific condition (e.g., have zero, one, or more than two pixels of the same non-white color, or pairs of different colors) remain unchanged. The background color is consistently white (0) in the examples, and this is the color that gets replaced during the filling process. The grid dimensions stay the same.

**YAML Facts:**


```yaml
task_context:
  grid_properties:
    - dimensions_preserved: True
    - background_color: white (0)
  transformation_type: row_based_filling
objects:
  - type: pixel
    properties:
      - color: non-white (1-9) or white (0)
      - position: (row_index, column_index)
  - type: row
    properties:
      - content: sequence of pixels
      - identified_features: pairs of identical non-white pixels
relationships:
  - type: horizontal_adjacency
    description: Pixels located within the same row.
  - type: betweenness
    description: Pixels located horizontally between two specific pixels in the same row.
actions:
  - name: identify_pairs
    inputs: row
    outputs: list of pairs, where each pair consists of [color, index1, index2] for rows with exactly two identical non-white pixels.
    condition: A row must contain exactly two pixels of the same non-white color.
  - name: fill_between
    inputs: row, identified_pair [color, index1, index2]
    outputs: modified_row
    description: Change the color of pixels from index1 + 1 to index2 - 1 (exclusive) to the identified color.
    condition: Operates only on rows where a valid pair was identified.
    target_pixels: white (0) pixels between the pair.
  - name: copy_row
    inputs: row
    outputs: identical_row
    condition: Row does not meet the criteria for identify_pairs.
transformation_flow:
  - step: Iterate through each row of the input grid.
  - step: For each row, apply the identify_pairs action.
  - step: If a pair is identified, apply the fill_between action to that row using the pair's information.
  - step: If no pair is identified, apply the copy_row action.
  - step: Collect the resulting rows (modified or copied) to form the output grid.

```


**Natural Language Program:**

1.  Initialize an empty output grid with the same dimensions as the input grid.
2.  Process the input grid one row at a time.
3.  For each row:
    a.  Find all non-white pixels, noting their color and column index.
    b.  Group these pixels by color.
    c.  Check if there is exactly one color group that contains exactly two pixels.
    d.  **If** such a group exists (let the color be C and the column indices be col1 and col2, assuming col1 < col2):
        i.  Copy the row from the input to the corresponding row in the output.
        ii. Fill the segment of the output row between col1 and col2 (i.e., from column index col1 + 1 up to col2 - 1) with color C.
    e.  **Else** (if the row contains zero non-white pixels, one non-white pixel, more than two pixels of the same color, or pairs of different colors):
        i.  Copy the row directly from the input to the corresponding row in the output without modification.
4.  Return the completed output grid.
