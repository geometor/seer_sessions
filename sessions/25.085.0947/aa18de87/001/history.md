
## train_1

**input:**
```
0 8 0 0 0 0 0 0 0 8 0 0
8 0 8 0 0 0 0 0 8 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8
0 0 0 0 8 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
```


**output:**
```
0 8 2 2 2 2 2 2 2 8 0 0
8 2 8 2 2 2 2 2 8 2 8 0
0 0 0 8 2 2 2 8 2 2 2 8
0 0 0 0 8 2 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
```


## train_2

**input:**
```
0 4 0 0 0 4 0 0
0 0 4 0 4 0 0 0
0 0 0 4 0 0 0 0
```


**output:**
```
0 4 2 2 2 4 0 0
0 0 4 2 4 0 0 0
0 0 0 4 0 0 0 0
```


## train_3

**input:**
```
1 0 0 0 0 0 0 0
0 1 0 0 0 0 0 1
0 0 1 0 0 0 1 0
0 0 0 1 0 1 0 0
0 0 0 0 1 0 0 0
```


**output:**
```
1 0 0 0 0 0 0 0
0 1 2 2 2 2 2 1
0 0 1 2 2 2 1 0
0 0 0 1 2 1 0 0
0 0 0 0 1 0 0 0
```


## train_4

**input:**
```
0 0 0 3 0 0 0 0
0 0 3 0 3 0 0 0
0 3 0 0 0 3 0 0
3 0 0 0 0 0 3 0
```


**output:**
```
0 0 0 3 0 0 0 0
0 0 3 2 3 0 0 0
0 3 2 2 2 3 0 0
3 2 2 2 2 2 3 0
```

**Perception**

The input grids consist of a white background (0) and scattered pixels of a single other color, which varies between examples (azure=8, yellow=4, blue=1, green=3). Let's call this the "marker color".

The output grids are identical to the input grids, except that some white pixels (0) have been changed to red (2).

The red pixels appear exclusively *between* pairs of marker-colored pixels that reside within the same row. Specifically, if two marker pixels exist in a row, and all the pixels horizontally situated strictly between them are white, then those white pixels are changed to red in the output. If there are more than two marker pixels in a row, this filling process applies to every consecutive pair of marker pixels in that row. Pixels outside these horizontal segments, including the marker pixels themselves, remain unchanged.

**Facts**


```yaml
task_description: Fill horizontal segments between pairs of marker pixels in each row with red.
elements:
  - type: grid
    properties:
      - background_color: white (0)
      - contains: pixels
  - type: pixel
    properties:
      - color: integer (0-9)
      - position: (row, column)
  - type: marker_pixel
    description: A pixel whose color is the single non-white color present in the input grid.
    properties:
      - color: Varies per example (8, 4, 1, 3)
      - is_non_white: true
  - type: white_pixel
    description: A pixel with color 0.
  - type: red_pixel
    description: A pixel with color 2, appearing only in the output.
  - type: row
    description: A horizontal line of pixels in the grid.

relationships:
  - type: horizontal_adjacency
    description: Pixels located next to each other in the same row.
  - type: horizontal_segment
    description: A sequence of pixels within a single row, located strictly between two marker pixels.

actions:
  - name: identify_marker_color
    description: Determine the single non-white color present in the input grid.
  - name: find_marker_pairs_in_row
    description: For each row, locate all pairs of marker pixels. If more than two exist, consider consecutive pairs (1st-2nd, 2nd-3rd, etc.).
  - name: check_segment_pixels
    description: For a given pair of marker pixels in a row, examine all pixels horizontally between them.
  - name: fill_segment
    description: If all pixels within a horizontal segment between two marker pixels are white (0), change their color to red (2).

transformation:
  - input: grid
  - steps:
    - Identify the marker color (the single non-white color in the input).
    - Create a copy of the input grid to serve as the output grid.
    - For each row in the input grid:
      - Find the column indices of all pixels with the marker color.
      - If there are two or more marker pixels in the row:
        - Iterate through consecutive pairs of these marker pixel indices (index_A, index_B).
        - Check if all pixels in the row between column index_A + 1 and index_B - 1 (inclusive) are white (0).
        - If they are all white, change the color of these pixels in the output grid (from column index_A + 1 to index_B - 1) to red (2).
  - output: modified grid
```


**Natural Language Program**

1.  Create a copy of the input grid; this will become the output grid.
2.  Identify the single non-white color present in the input grid. Call this the `marker_color`.
3.  Iterate through each `row` of the grid, from top to bottom.
4.  Within each `row`, find the column indices of all pixels that have the `marker_color`. Store these indices in a list, sorted in ascending order.
5.  If the list of indices for the current `row` contains fewer than two indices, proceed to the next row.
6.  If the list contains two or more indices, iterate through consecutive pairs of indices `(col1, col2)` from the list (e.g., the 1st and 2nd index, then the 2nd and 3rd index, and so on).
7.  For each pair `(col1, col2)`:
    a.  Check if all pixels in the current `row` located at column indices strictly between `col1` and `col2` (i.e., from `col1 + 1` to `col2 - 1`) have the color white (0).
    b.  If all these intervening pixels are white (0), then change the color of these pixels (from column `col1 + 1` to `col2 - 1`) in the output grid to red (2).
8.  After processing all rows, return the modified output grid.
