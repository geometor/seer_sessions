## Perception of Elements

The input consists of a grid (matrix) of single-digit numbers, represented as space-separated values on multiple lines. The output is also a grid of single-digit numbers, similarly formatted. The key observation is that the output grid is larger than the input grid, specifically twice the height and twice the width. Each element (number) in the input grid appears to be expanded into a 2x2 block of identical elements in the corresponding position in the output grid.

## Documented Facts


```yaml
Task: Grid Element Expansion

Input:
  Type: Grid
  Format: Space-separated numbers per line
  Elements: Integers (appear to be single digits in examples)
  Properties:
    - rows: R
    - columns: C

Output:
  Type: Grid
  Format: Space-separated numbers per line
  Elements: Integers (same as input elements)
  Properties:
    - rows: 2 * R
    - columns: 2 * C
  Relationship_to_Input:
    - Each element `e` at input position `(r, c)` corresponds to a 2x2 block of element `e` in the output grid.
    - The top-left corner of this 2x2 block in the output is at position `(2*r, 2*c)`.
    - The four cells of the output block corresponding to input `(r, c)` are:
      - `(2*r, 2*c)`
      - `(2*r, 2*c + 1)`
      - `(2*r + 1, 2*c)`
      - `(2*r + 1, 2*c + 1)`
    - All four cells in this output block have the same value as the input element `e` at `(r, c)`.

Examples_Summary:
  - train_1: Input 2x2 -> Output 4x4
  - train_2: Input 3x3 -> Output 6x6
  - train_3: Input 4x4 -> Output 8x8
  - All examples follow the 2x2 expansion rule.
```


## Natural Language Program

1.  Read the input grid, determining its dimensions (R rows, C columns) and the value of each element at position `(r, c)`, where `r` is the row index (0 to R-1) and `c` is the column index (0 to C-1).
2.  Create a new output grid with dimensions (2*R rows, 2*C columns).
3.  Iterate through each element `e` at position `(r, c)` in the input grid.
4.  For each input element `e` at `(r, c)`, populate a 2x2 block in the output grid with the value `e`. The positions in the output grid to be filled are:
    *   `(2*r, 2*c)`
    *   `(2*r, 2*c + 1)`
    *   `(2*r + 1, 2*c)`
    *   `(2*r + 1, 2*c + 1)`
5.  Format the resulting output grid as space-separated numbers per line.