## Initial Perception

The input and output are grids of the same dimensions (12x12). The grids contain numerical digits (0, 1, 2, 3 in the input; 0, 1, 3 in the output). A border composed of the digit '3' surrounds both grids and remains unchanged. The core transformation seems to involve swapping specific digits within the grid's interior. Specifically, the digit '2' in the input is replaced by '0' in the output, and the digit '0' in the input is replaced by '1' in the output. The digit '1' appears to remain '1', and the digit '3' remains '3'.

## Observed Facts

```yaml
task_elements:
  - grid:
      type: object
      description: A 2D array of digits.
      properties:
        - dimensions: [12, 12]
        - unique_values_input: [0, 1, 2, 3]
        - unique_values_output: [0, 1, 3]
  - border:
      type: object
      description: A frame composed of a single digit ('3') surrounding the grid's content.
      properties:
        - value: 3
        - thickness: 1 cell
      relationships:
        - unchanged: between input and output
  - digits:
      type: object
      description: Individual numerical values within the grid cells.
      properties:
        - value_map:
            input_2: output_0
            input_0: output_1
            input_1: output_1
            input_3: output_3
      actions:
        - substitution: based on the value_map
relationships:
  - identity: The grid dimensions remain constant.
  - identity: The border ('3') remains constant.
  - transformation: Internal grid values are substituted based on a specific mapping rule (2->0, 0->1, 1->1, 3->3).
```

## Natural Language Program

1.  Iterate through each cell of the input grid.
2.  For each cell, check the digit value:
    *   If the value is '2', change it to '0' in the corresponding output cell.
    *   If the value is '0', change it to '1' in the corresponding output cell.
    *   If the value is '1', keep it as '1' in the corresponding output cell.
    *   If the value is '3', keep it as '3' in the corresponding output cell.
3.  Construct the output grid with these modified cell values.