## Perception

The input and output grids in all examples are the same size (30x30).
The grids display a background pattern consisting of alternating rows:
1.  Rows composed entirely of blue pixels (1).
2.  Rows containing a repeating sequence of colors, starting with blue (1).

In the input grids, some areas of this underlying pattern are obscured by patches of white pixels (0).
The output grids restore the original background pattern by replacing the white pixels (0) with the color that should be present at that location according to the repeating sequence of the row it belongs to. The solid blue rows remain unchanged as they don't contain white pixels in the examples.

The specific repeating sequence in the non-blue rows varies between examples:
*   Example 1: `1, 4, 2, 5, 3` (blue, yellow, red, gray, green) - Length 5
*   Example 2: `1, 4` (blue, yellow) - Length 2
*   Example 3: `1, 4, 7, 3, 6, 2, 5` (blue, yellow, orange, green, magenta, red, gray) - Length 7

The core task is pattern completion or restoration where white pixels act as "missing data" markers.

## Facts


```yaml
elements:
  - object: grid
    properties:
      - height: 30
      - width: 30
  - object: pattern
    properties:
      - type: background
      - structure: alternating_rows
      - row_type_1: solid_color
        - color: blue (1)
      - row_type_2: repeating_sequence
        - sequence: varies per example, determined by the first non-solid-blue row without white pixels
        - examples:
          - [1, 4, 2, 5, 3]
          - [1, 4]
          - [1, 4, 7, 3, 6, 2, 5]
  - object: obscuration
    properties:
      - color: white (0)
      - shape: patches or blocks
      - location: overlaid on the background pattern in input grids

actions:
  - action: identify_pattern
    actor: system
    input: input_grid
    output: repeating_sequence (for non-solid-blue rows)
    condition: Find the first row that is not entirely blue and contains no white pixels. Use this row to define the sequence.
  - action: restore_pattern
    actor: system
    input: input_grid, repeating_sequence
    output: output_grid
    process: Iterate through each pixel of the input grid. If a pixel is white (0), replace it with the color from the identified repeating sequence corresponding to its column index modulo the sequence length. Otherwise, keep the original pixel color.

relationships:
  - white pixels (0) in the input grid indicate positions where the underlying pattern needs to be restored.
  - the output grid is a restored version of the input grid's pattern, with white pixels replaced.
  - the color used for replacement depends on the column position and the specific repeating sequence of that row type.
```


## Natural Language Program

1.  Examine the input grid to identify the two types of rows: rows consisting entirely of blue pixels (1) and rows containing a sequence of colors.
2.  Find the first row that is not entirely blue and does not contain any white pixels (0). Record the sequence of colors in this row. This is the "reference sequence" for all non-solid-blue rows. Let the length of this sequence be L.
3.  Create a copy of the input grid to serve as the basis for the output grid.
4.  Iterate through each row (`r`) and column (`c`) of the input grid.
5.  Check the color of the pixel at `input[r, c]`.
6.  If the color is white (0):
    a.  Determine the replacement color by taking the color from the reference sequence at index `c % L`.
    b.  Update the corresponding pixel in the output grid copy with this replacement color.
7.  If the color is not white (0), keep the pixel in the output grid copy as it is (it already matches the underlying pattern).
8.  After iterating through all pixels, the modified grid copy is the final output grid.