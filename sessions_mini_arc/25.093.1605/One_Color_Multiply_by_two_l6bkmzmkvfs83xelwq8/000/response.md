**Perception:**

The task involves transforming a 5x5 input grid of binary digits (0s and 1s) into a 5x5 output grid. The transformation appears to operate on a row-by-row basis, where specific rows from the input grid are selected and potentially duplicated to form the rows of the output grid. The relative positions of the 0s and 1s within the selected rows are preserved. The key is to identify which input rows are used to construct which output rows.

Observing the examples:
- The first row (index 0) of the input seems to consistently map directly to the first row (index 0) of the output.
- The fourth row (index 3) of the input seems to be copied to both the second and third rows (indices 1 and 2) of the output.
- The fifth row (index 4) of the input seems to be copied to both the fourth and fifth rows (indices 3 and 4) of the output.

**Facts:**


```yaml
task_elements:
  - object: grid
    properties:
      - type: input
      - type: output
      - dimensions: 5x5
      - cell_values: [0, 1]
  - object: row
    properties:
      - part_of: grid
      - index: 0 to 4
      - content: sequence of 5 cell values
relationships:
  - type: mapping
    source: input_grid rows
    target: output_grid rows
    details:
      - output_row[0] is a copy of input_row[0]
      - output_row[1] is a copy of input_row[3]
      - output_row[2] is a copy of input_row[3]
      - output_row[3] is a copy of input_row[4]
      - output_row[4] is a copy of input_row[4]
actions:
  - name: copy_row
    source: specific row from input_grid
    destination: specific row(s) in output_grid
```


**Natural Language Program:**

1.  Initialize an empty 5x5 output grid.
2.  Copy the content of the first row (index 0) from the input grid to the first row (index 0) of the output grid.
3.  Copy the content of the fourth row (index 3) from the input grid to the second row (index 1) of the output grid.
4.  Copy the content of the fourth row (index 3) from the input grid to the third row (index 2) of the output grid.
5.  Copy the content of the fifth row (index 4) from the input grid to the fourth row (index 3) of the output grid.
6.  Copy the content of the fifth row (index 4) from the input grid to the fifth row (index 4) of the output grid.
7.  Return the completed output grid.