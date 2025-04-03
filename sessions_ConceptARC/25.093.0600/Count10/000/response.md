Okay, let's break down this task.

## Perception

1.  **Input Data:** The input is always a 2D grid (matrix) of non-negative integers. The grids have varying dimensions. Within each grid, there are background cells (value 0) and foreground cells (value > 0). The non-zero values form distinct shapes or patterns. The specific non-zero value (e.g., 2, 3, 4) differs between examples but seems consistent within a single input grid's pattern.
2.  **Output Data:** The output is always a 1D array (a single row) containing only the integer 0. The length of this output row varies between examples.
3.  **Transformation:** The core task appears to be determining the *length* of the output row based on some property of the input grid's non-zero elements. The *content* of the output row is constant (all zeros). The specific values (2, 3, 4) and the exact shapes they form seem less important than their locations (which rows and columns they occupy). The transformation involves analyzing the spatial distribution of the non-zero elements.

## Facts


```yaml
task_description: Determine the length of a zero-filled output row based on the spatial distribution of non-zero elements in an input grid.

input_features:
  - name: input_grid
    type: 2D list of integers
    description: A grid containing non-negative integers, with 0 representing background and non-zero values representing foreground patterns.

output_features:
  - name: output_row
    type: 1D list of integers
    description: A single row grid containing only the value 0. Its length is derived from the input grid.

derived_properties:
  - name: non_zero_row_indices
    description: The set of unique row indices in the input_grid that contain at least one non-zero value.
  - name: count_non_zero_rows
    description: The number of unique rows containing non-zero values.
  - name: non_zero_col_indices
    description: The set of unique column indices in the input_grid that contain at least one non-zero value.
  - name: count_non_zero_cols
    description: The number of unique columns containing non-zero values.
  - name: derived_output_length
    description: The minimum value between count_non_zero_rows and count_non_zero_cols.

relationships:
  - property: output_row.length
    equals: derived_output_length
  - property: output_row.elements
    value: All elements are 0.

actions:
  - Identify all row indices containing non-zero elements.
  - Count the number of unique identified row indices (count_non_zero_rows).
  - Identify all column indices containing non-zero elements.
  - Count the number of unique identified column indices (count_non_zero_cols).
  - Calculate the minimum of count_non_zero_rows and count_non_zero_cols to determine the derived_output_length.
  - Construct the output_row as a list of zeros with the calculated derived_output_length.
```


## Natural Language Program

1.  Receive the input 2D grid.
2.  Initialize an empty set to store the indices of rows containing non-zero values (`non_zero_rows`).
3.  Initialize an empty set to store the indices of columns containing non-zero values (`non_zero_cols`).
4.  Iterate through each cell `(row_index, col_index)` of the input grid.
5.  If the value of the cell is not zero:
    a.  Add the `row_index` to the `non_zero_rows` set.
    b.  Add the `col_index` to the `non_zero_cols` set.
6.  Calculate the number of unique rows found: `num_active_rows = size of non_zero_rows set`.
7.  Calculate the number of unique columns found: `num_active_cols = size of non_zero_cols set`.
8.  Determine the target length for the output: `output_length = minimum(num_active_rows, num_active_cols)`.
9.  Create a new 1D list (row) of size `output_length`.
10. Fill this new list entirely with the integer value 0.
11. Return the created list as the output.