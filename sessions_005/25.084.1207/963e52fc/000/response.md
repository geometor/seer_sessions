**Perception:**

Each example pair shows an input grid and a corresponding output grid.
1.  The output grid consistently has the same height as the input grid.
2.  The output grid consistently has exactly double the width of the input grid.
3.  Visually, the output grid appears to be formed by placing two copies of the input grid side-by-side horizontally.
4.  This duplication applies to all rows, whether they contain patterns (non-white pixels) or are entirely white.

**Facts:**


```yaml
task_description: Horizontally duplicate the input grid to create the output grid.
grid_transformation:
  - operation: duplication
    direction: horizontal
    factor: 2
details:
  - input_grid: Represents the source data structure.
  - output_grid:
      height: Same as input_grid height.
      width: Double the input_grid width.
      content: Each row in the output_grid is formed by concatenating the corresponding row from the input_grid with itself.
```


**Natural Language Program:**

1.  Given an input grid.
2.  Create a new output grid with the same number of rows as the input grid and twice the number of columns.
3.  For each row in the input grid:
    a.  Copy the entire row.
    b.  Append the copied row to its own end, effectively concatenating the row with itself.
    c.  Place this new, doubled row into the corresponding row position in the output grid.
4.  Return the completed output grid.