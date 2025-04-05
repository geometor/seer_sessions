
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 3 0 0 3
0 0 0 0 0 0 3 0 0 3
0 0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 4 0 0 4 0 0 0 0 0
0 4 0 0 4 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4
0 0 0 0 0 0 4 0 0 4
0 0 0 0 0 0 4 0 0 4
0 0 0 0 0 0 4 4 4 4
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0
0 1 0 1 0 6 6 6 6 6
0 1 1 1 0 6 0 0 0 6
0 0 0 0 0 6 0 0 0 6
0 0 0 0 0 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0
0 5 0 5 0 5 5 5 5 5
0 5 5 5 0 5 0 0 0 5
0 0 0 0 0 5 0 0 0 5
0 0 0 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 0 2 0 0 2 2 2 0
0 2 0 2 0 0 2 0 2 0
0 2 0 2 0 0 2 0 2 0
0 2 2 2 0 0 2 0 2 0
0 0 0 0 0 0 2 0 2 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 4 0 4 0 0 4 4 4 0
0 4 0 4 0 0 4 0 4 0
0 4 0 4 0 0 4 0 4 0
0 4 4 4 0 0 4 0 4 0
0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 7 7 7 7
0 8 0 8 0 0 7 0 0 7
0 8 0 8 0 0 7 0 0 7
0 8 0 8 0 0 7 0 0 7
0 8 0 8 0 0 7 0 0 7
0 8 0 8 0 0 7 0 0 7
0 8 8 8 0 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 5 5 5 5
0 5 0 5 0 0 5 0 0 5
0 5 0 5 0 0 5 0 0 5
0 5 0 5 0 0 5 0 0 5
0 5 0 5 0 0 5 0 0 5
0 5 0 5 0 0 5 0 0 5
0 5 5 5 0 0 5 5 5 5
0 0 0 0 0 0 0 0 0 0
```

## Perception

The input and output are 10x10 grids containing integer values. The value '0' represents the background color. The non-zero values represent foreground colors, forming distinct shapes or patterns within the grid.

Comparing the input and output grids reveals the following:
1.  **Structure Preservation:** The positions of the '0' (background) cells and the non-zero (foreground) cells remain unchanged between the input and output.
2.  **Color Transformation:** All non-zero cells in the input grid are uniformly replaced by a single, new non-zero color in the output grid.
3.  **Rule Dependency:** The specific color used for replacement in the output seems to depend on the variety of non-zero colors present in the input grid.
    *   In `train_1`, the input has only color '3', and the output color is '4'.
    *   In `train_2`, the input has colors '1' and '6', and the output color is '5'.
    *   In `train_3`, the input has only color '2', and the output color is '4'.
    *   In `train_4`, the input has colors '7' and '8', and the output color is '5'.
4.  **Pattern Identified:** The output color appears to be determined by the *count* of unique non-zero colors in the input grid. If there is one unique non-zero color, the output color is 4. If there are two unique non-zero colors, the output color is 5.

## Facts


```yaml
objects:
  - grid:
      description: A 2D array of integer values representing pixels or cells.
      properties:
        - dimensions: [10, 10]
        - cells: list of cell objects
  - cell:
      description: An individual element within the grid.
      properties:
        - position: [row, column]
        - value: integer (color)
  - color:
      description: The integer value of a cell.
      properties:
        - is_background: boolean (true if value is 0)
        - is_foreground: boolean (true if value is not 0)
relationships:
  - input_grid maps_to output_grid
  - output_grid preserves_structure_of input_grid (zero vs non-zero positions)
properties_of_transformation:
  - input_non_zero_colors: The set of unique non-zero values in the input grid.
  - unique_color_count: The number of elements in input_non_zero_colors.
  - output_color: A single integer value determined by unique_color_count.
actions:
  - identify_unique_non_zero_colors: Find all distinct non-zero values in the input grid.
  - count_unique_colors: Determine the size of the set of unique non-zero colors.
  - determine_output_color:
      if unique_color_count == 1: output_color = 4
      if unique_color_count == 2: output_color = 5
  - transform_grid: Create the output grid by replacing all cells in the input grid that have a non-zero value with the determined output_color. Cells with a value of 0 remain 0.
```


## Natural Language Program

1.  Examine the input grid and identify all unique non-zero integer values (colors).
2.  Count the number of unique non-zero colors found.
3.  Determine the target output color based on this count:
    *   If the count of unique non-zero colors is 1, set the target output color to 4.
    *   If the count of unique non-zero colors is 2, set the target output color to 5.
4.  Create the output grid, ensuring it has the same dimensions as the input grid.
5.  Iterate through each cell of the input grid:
    *   If the input cell's value is 0, set the corresponding output cell's value to 0.
    *   If the input cell's value is non-zero, set the corresponding output cell's value to the target output color determined in step 3.
6.  Return the completed output grid.
