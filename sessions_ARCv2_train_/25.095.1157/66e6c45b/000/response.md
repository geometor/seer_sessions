## Perception of Elements

The input and output are both 4x4 grids containing single-digit integers. The input grid features a central 2x2 block of non-zero digits, surrounded by zeros. The output grid consists mostly of zeros, with the non-zero digits from the input's central block relocated to the four corner positions of the grid.

## Factual Documentation


```yaml
Task: Relocate central 2x2 block elements to grid corners.

Input:
  Type: Grid
  Properties:
    - Size: 4x4
    - Cells: Contain single-digit integers.
    - Pattern: Zeros dominate, except for a 2x2 subgrid located at rows 1-2 and columns 1-2 (0-indexed) which contains non-zero digits.
  Objects:
    - Grid: The overall 4x4 structure.
    - Cells: Individual elements within the grid.
    - Central Block: The 2x2 subgrid containing non-zero values at (1,1), (1,2), (2,1), (2,2).

Output:
  Type: Grid
  Properties:
    - Size: 4x4
    - Cells: Contain single-digit integers.
    - Pattern: Zeros dominate, except for the four corner cells.
  Objects:
    - Grid: The overall 4x4 structure.
    - Cells: Individual elements within the grid.
    - Corner Cells: Positions (0,0), (0,3), (3,0), (3,3).

Transformation:
  Action: Move and Map
  Details:
    - The four non-zero digits from the input's central 2x2 block are moved to the output grid's corner positions.
    - The mapping preserves relative positions:
      - Input (1,1) -> Output (0,0) (Top-Left)
      - Input (1,2) -> Output (0,3) (Top-Right)
      - Input (2,1) -> Output (3,0) (Bottom-Left)
      - Input (2,2) -> Output (3,3) (Bottom-Right)
    - All other positions in the output grid are set to 0.
  Relationship:
    - The output grid's corner values are directly sourced from the input grid's central 2x2 block values.
    - The dimensions of the input and output grids are identical (4x4).
```


## Natural Language Program

1.  Create a new 4x4 grid initialized with all zeros; this will be the output grid.
2.  Copy the value from the input grid at position (row 1, column 1) to the output grid at position (row 0, column 0).
3.  Copy the value from the input grid at position (row 1, column 2) to the output grid at position (row 0, column 3).
4.  Copy the value from the input grid at position (row 2, column 1) to the output grid at position (row 3, column 0).
5.  Copy the value from the input grid at position (row 2, column 2) to the output grid at position (row 3, column 3).
6.  Return the modified output grid.