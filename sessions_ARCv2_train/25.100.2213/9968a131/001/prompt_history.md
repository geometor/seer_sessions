
## train_1

**input:**
```
7 3 8 7
7 8 3 7
7 3 8 7
7 8 3 7
```


**output:**
```
7 3 8 7
7 7 8 3
7 3 8 7
7 7 8 3
```


## train_2

**input:**
```
0 5 7 7 7 7
5 0 7 7 7 7
0 5 7 7 7 7
5 0 7 7 7 7
0 5 7 7 7 7
5 0 7 7 7 7
```


**output:**
```
0 5 7 7 7 7
7 5 0 7 7 7
0 5 7 7 7 7
7 5 0 7 7 7
0 5 7 7 7 7
7 5 0 7 7 7
```

## Perception of Task Elements

The task operates on a 2D grid of numbers. The transformation modifies specific rows of the input grid while leaving others unchanged. The core logic depends on the row's position (index) within the grid. Even-numbered rows (using 1-based indexing) undergo a specific modification, while odd-numbered rows are copied directly from the input to the output. The modification applied to the even-numbered rows is a right circular shift: the last element moves to the first position, and all other elements shift one position to the right. The dimensions of the output grid are identical to the input grid.

## YAML Fact Document

```yaml
task_elements:
  - object: input_grid
    description: A 2D array or list of lists containing numbers.
  - object: output_grid
    description: A 2D array derived from the input_grid, having the same dimensions.
  - object: row
    description: A 1D array or list representing a horizontal line of numbers within the grid.
    properties:
      - index: The 1-based position of the row within the grid (e.g., 1st row, 2nd row).
      - parity: Whether the index is odd or even.
  - object: element
    description: A single number within a row.
    properties:
      - value: The numerical value.
      - position: The index of the element within its row.

actions:
  - action: copy_row
    description: Transferring a row directly from the input_grid to the corresponding position in the output_grid without modification.
  - action: right_circular_shift
    description: Modifying a row by moving the last element to the first position and shifting all other elements one position to the right.

relationships:
  - relationship: row_modification_based_on_parity
    description: >
      The transformation applied to a row depends on its index parity.
      Odd-indexed rows (1st, 3rd, etc.) are processed using the `copy_row` action.
      Even-indexed rows (2nd, 4th, etc.) are processed using the `right_circular_shift` action.
  - relationship: grid_structure_preservation
    description: The output_grid maintains the same number of rows and columns as the input_grid.
```

## Natural Language Program

1.  Initialize an empty output grid with the same dimensions as the input grid.
2.  Iterate through each row of the input grid, keeping track of the row's 1-based index (position).
3.  For each row:
    a.  Check if the row's index is odd or even.
    b.  If the index is odd: Copy the row directly from the input grid to the corresponding row in the output grid.
    c.  If the index is even:
        i.  Perform a right circular shift on the elements of the row. (Take the last element and place it at the beginning of the row, shifting all other elements one position to the right).
        ii. Place the modified row into the corresponding row of the output grid.
4.  Return the completed output grid.
