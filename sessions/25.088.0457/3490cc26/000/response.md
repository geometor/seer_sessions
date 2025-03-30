**Perception:**

The input grids contain a background of white pixels (0) and several distinct objects, primarily 2x2 squares of azure (8) and occasionally a single 2x2 square of red (2). The output grids are identical to the input grids, except for the addition of orange pixels (7).

The transformation involves identifying pairs of azure squares that are aligned either horizontally (sharing the same two rows) or vertically (sharing the same two columns). The rectangular area lying strictly *between* such aligned pairs is then filled with orange pixels. The red squares do not participate in this interaction and remain unchanged. The filling occurs regardless of the distance between the aligned azure squares, as long as they share the same rows or columns.

**Facts YAML:**


```yaml
elements:
  - object: background
    color: white
    value: 0
  - object: azure_square
    color: azure
    value: 8
    shape: 2x2 square
    count: multiple per grid
  - object: red_square
    color: red
    value: 2
    shape: 2x2 square
    count: zero or one per grid
  - object: filler
    color: orange
    value: 7
    role: added in output

interactions:
  - type: alignment_check
    subject: pairs of azure_square objects
    condition:
      - shares the same two rows (horizontal alignment)
      - OR shares the same two columns (vertical alignment)
  - type: fill_region
    action: fill with orange pixels (7)
    target: the rectangular region strictly between two aligned azure_square objects
    condition: the two azure_square objects must be aligned horizontally or vertically

constraints:
  - red_square objects are ignored and do not influence the transformation.
  - The original azure_square and red_square objects remain unchanged in the output.
  - Only the space *between* aligned azure squares is filled.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct 2x2 squares composed entirely of azure pixels (8) in the input grid. Record the top-left corner coordinates and dimensions (2x2) for each square.
3.  Iterate through all unique pairs of identified azure squares.
4.  For each pair of azure squares (Square A and Square B):
    a.  Check if they are horizontally aligned: Do they occupy the exact same two rows?
    b.  If horizontally aligned:
        i.  Determine the columns between them. Let Square A be at `(r, cA)` and Square B be at `(r, cB)`. Assume `cA < cB`.
        ii. The columns to fill are from `cA + 2` to `cB - 1`.
        iii.The rows to fill are `r` and `r + 1`.
        iv. Fill all pixels within this rectangular region (rows `r` to `r+1`, columns `cA+2` to `cB-1`) in the output grid with orange (7).
    c.  Check if they are vertically aligned: Do they occupy the exact same two columns?
    d.  If vertically aligned:
        i.  Determine the rows between them. Let Square A be at `(rA, c)` and Square B be at `(rB, c)`. Assume `rA < rB`.
        ii. The rows to fill are from `rA + 2` to `rB - 1`.
        iii.The columns to fill are `c` and `c + 1`.
        iv. Fill all pixels within this rectangular region (rows `rA+2` to `rB-1`, columns `c` to `c+1`) in the output grid with orange (7).
5.  Return the modified output grid.