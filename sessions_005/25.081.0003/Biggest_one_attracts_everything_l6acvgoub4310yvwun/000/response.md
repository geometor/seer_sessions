
**Perception of Elements:**

The task involves 2D grids of single-digit integers (0-9), representing colors. The transformation seems to involve a rearrangement of rows, specifically a rotation or vertical shifting of rows with certain contents. Empty rows (all zeros) seem to be added or removed in the process.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      - rows: list of rows
      - values: integers 0-9 (representing colors)
  - type: row
    properties:
       - contents : integers 0-9
       - is_empty: boolean # True if all elements are 0

actions:
  - shift_rows:
      description: Moves non-empty rows upwards, potentially inserting empty rows at the bottom.

relationships:
  - row-to-grid: Rows are contained within the grid.
  - row-emptiness : affects row position after transformation
```


**Natural Language Program:**

1.  **Identify Non-Empty Rows:** Examine each row in the input grid. A row is considered "non-empty" if it contains any digit other than 0.
2.  **Shift Non-Empty Rows Upwards:** Arrange all non-empty rows sequentially at the top of the output grid, maintaining their relative order from the input.
3. **Fill Remaining with empty rows:** insert empty (all 0) rows to bottom of the grid until the input and output grid have the same height.

In essence, the transformation "compacts" the non-zero rows to the top of the grid, and all empty rows are sent to the bottom.
