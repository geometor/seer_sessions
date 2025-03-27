## Perception

1.  **Input Grids:** The input grids consist of a block of one or more contiguous rows containing non-white pixels (colors like red, azure, green) located at the very top. Below this block, the rest of the grid is filled with white pixels (0).
2.  **Output Grids:** The output grids have the same dimensions as their corresponding input grids. They retain the original block of non-white rows at the top. Additionally, a vertically flipped (mirrored) copy of this top block is placed at the very bottom of the grid, replacing the white pixels that were originally there. The rows between the original top block and the new bottom block remain white.
3.  **Transformation:** The core transformation involves identifying the non-white rows at the top of the input, creating a vertically mirrored copy of these rows, and appending this mirrored copy to the bottom of the grid.

## Facts


```yaml
task_type: object_manipulation
grid_properties:
  - input_dimensions: variable (e.g., 10x5, 10x3)
  - output_dimensions: same as input
  - background_color: white (0)
objects:
  - type: block
    description: A contiguous group of rows starting from the top row (row 0) containing non-white pixels.
    properties:
      - location: top of the input grid
      - colors: variable (e.g., red, azure, green)
      - height: variable (number of rows in the block)
      - width: same as grid width
actions:
  - identify: Locate the block of non-white rows at the top of the input grid. Determine its height (number of rows).
  - copy: Create a copy of this identified block.
  - transform: Vertically flip the copied block (reverse the order of its rows).
  - place: Position the flipped block at the bottom of the output grid, starting from the last row and going upwards, occupying the same number of rows as the original block's height.
relationships:
  - The output grid contains the original top block unchanged.
  - The output grid contains a vertically reflected version of the top block placed at the bottom.
  - The number of rows in the reflected block at the bottom equals the number of rows in the original block at the top.
  - The rows between the top block and the bottom reflected block in the output are white.
```


## Natural Language Program

1.  Receive the input grid.
2.  Determine the dimensions (height `H`, width `W`) of the input grid.
3.  Identify the block of contiguous rows starting from the top (row 0) that contain at least one non-white pixel. Let the number of rows in this block be `N`.
4.  Create a new output grid with the same dimensions (`H` x `W`) as the input grid, initially filled with the same contents as the input grid.
5.  Extract the identified top block of `N` rows (from row 0 to row `N-1`).
6.  Create a vertically flipped version of this extracted block by reversing the order of its rows.
7.  Place this flipped block into the output grid, starting at row `H-N` and ending at row `H-1` (the bottom `N` rows). Overwrite any existing pixels in these rows.
8.  Return the modified output grid.