
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 2 0 2 0 2 0 2 0
2 2 2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 0 2 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 0 2 0 2 0 2 0 2 0 2 0
2 2 2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 0 2 0 2 0 2 0
2 0 2 0 2 0 2 0 2 0 2 0
2 2 2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 0 2 0 2 0 2 0
2 0 2 0 2 0 2 0 2 0 2 0
2 2 2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 0 2 0 2 0 2 0
2 0 2 0 2 0 2 0 2 0 2 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```

Okay, let's analyze the provided examples.

## Perception

1.  **Input Grid Analysis:** Both input examples consist primarily of a background color (white, 0). Within each input grid, there is a distinct, horizontally oriented pattern made of a single non-background color (red (2) in the first example, azure (8) in the second). This pattern spans the full width of a sub-region of the grid and has a height of 3 rows. The pattern itself is composed of three unique rows:
    *   Example 1 (Red): Alternating red/white, Solid red, Alternating red/white.
    *   Example 2 (Azure): Sparse azure, Solid azure, Different sparse azure.
    The rest of the input grid is filled with the background color (white).

2.  **Output Grid Analysis:** The output grids have the same dimensions as their corresponding input grids. The entire output grid is filled by vertically repeating the 3-row pattern identified in the input. The repetition starts from the top row (row 0) and continues downwards, wrapping around if the grid height is not a multiple of the pattern height (3). The background color from the input grid is effectively ignored or overwritten in the output.

3.  **Transformation:** The core transformation involves identifying the non-background colored pattern within the input, extracting this pattern (specifically, the rows containing any non-background color), and then using this extracted pattern as a repeating vertical tile to construct the output grid.

## Facts


```yaml
Task: Vertical Tiling

Input:
  - type: grid
  - properties:
      - contains a background color (white, 0)
      - contains a single foreground color (e.g., red, azure)
      - foreground pixels form a contiguous block when considering only rows containing them
      - this block represents a repeating "motif" or pattern
  - motif_properties:
      - spans a subset of rows
      - spans the full width of the grid within those rows (or a sub-width in other cases, here it's full width)
      - extracted by finding the bounding box of all non-background pixels

Output:
  - type: grid
  - properties:
      - same dimensions as the input grid
      - filled entirely by vertically tiling the extracted motif
  - relationships:
      - output_row[r] = motif_row[r % motif_height] for all rows r
      - output grid color palette is determined solely by the motif colors

Derived_elements:
  - motif:
      - description: The smallest subgrid containing all non-background pixels from the input.
      - identified_by: Bounding box of non-background pixels.
      - role: Acts as the tile for the output grid.
  - background_color:
      - description: The most frequent color in the input grid, typically white (0).
      - role: Used to identify the foreground pattern/motif. Ignored in the output construction.
  - foreground_color:
      - description: The color(s) making up the motif.
      - role: Defines the content of the motif and thus the output.

Transformation:
  - name: Extract and Tile Vertically
  - steps:
      1. Identify non-background pixels in the input grid.
      2. Determine the minimum and maximum row and column indices containing these pixels (bounding box).
      3. Extract the subgrid defined by these row and column indices (the motif).
      4. Create a new grid with the same dimensions as the input grid.
      5. For each row `r` from 0 to output_height - 1:
         - Determine the corresponding source row index in the motif: `motif_r = r % motif_height`.
         - Copy the `motif_r`-th row of the motif to the `r`-th row of the output grid.
```


## Natural Language Program

1.  Identify all pixels in the input grid that are not the background color (white, 0).
2.  Find the minimum and maximum row indices (`min_row`, `max_row`) that contain any non-background pixels.
3.  Extract the horizontal slice of the input grid from `min_row` to `max_row` inclusive. This slice is the "motif". Let its height be `motif_height = max_row - min_row + 1`.
4.  Create a new output grid with the same height and width as the input grid.
5.  For each row index `r` from 0 up to (but not including) the height of the output grid:
    a.  Calculate the corresponding row index within the motif using the modulo operator: `source_row_index = r % motif_height`.
    b.  Copy the row content from the `source_row_index`-th row of the motif to the `r`-th row of the output grid.
6.  The resulting grid is the final output.
