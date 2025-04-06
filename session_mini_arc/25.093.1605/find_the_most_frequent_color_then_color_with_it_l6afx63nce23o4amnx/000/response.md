## Perception of Task Elements

The task involves transforming a 2D grid of numbers based on the frequency of the non-zero numbers present in the input grid. The core elements are:

1.  **Input Grid:** A 2D array of integers.
2.  **Output Grid:** A 2D array of integers derived from the input grid.
3.  **Cells:** Individual positions within the grid containing integer values.
4.  **Numbers:** The integer values within the cells. These can be zero or non-zero.
5.  **Frequency:** The count of occurrences of each distinct non-zero number within the input grid.
6.  **Most Frequent Non-Zero Number:** The non-zero integer that appears most often in the input grid.
7.  **Transformation Rule:** A procedure that modifies the input grid to produce the output grid. In this task, the rule involves identifying the most frequent non-zero number and using it to replace all other non-zero numbers.

## Documented Facts


```yaml
task_type: grid_transformation
components:
  - type: grid
    properties:
      - dimensionality: 2D
      - cell_content: integers
      - size: variable (observed as 5x5 in examples)
objects:
  - name: input_grid
    type: grid
  - name: output_grid
    type: grid
  - name: non_zero_numbers
    description: The set of unique integers greater than 0 present in the input grid.
  - name: frequency_map
    description: A mapping from each non_zero_number to its count of occurrences in the input_grid.
  - name: target_number
    description: The non_zero_number with the highest frequency in the frequency_map. If there's a tie, the examples don't explicitly cover this, but the logic implies any one of the tied most frequent numbers could be chosen (though the examples provided don't have ties).
relationships:
  - type: derived_from
    source: output_grid
    target: input_grid
actions:
  - name: count_frequency
    input: input_grid
    output: frequency_map
    description: Count the occurrences of each distinct non-zero number in the input grid.
  - name: find_most_frequent
    input: frequency_map
    output: target_number
    description: Identify the non-zero number with the highest count.
  - name: replace_non_zeros
    input:
      - input_grid
      - target_number
    output: output_grid
    description: Create the output grid by iterating through the input grid. If a cell contains a non-zero number, replace it with the target_number. If a cell contains zero, keep it as zero.
```


## Natural Language Program

1.  Receive the input grid.
2.  Identify all unique non-zero numbers present in the input grid.
3.  Count the frequency (number of occurrences) of each unique non-zero number within the entire input grid.
4.  Determine which non-zero number has the highest frequency. This number is the "target number".
5.  Create a new grid (the output grid) with the same dimensions as the input grid.
6.  Iterate through each cell of the input grid:
    *   If the value in the current cell is zero, place zero in the corresponding cell of the output grid.
    *   If the value in the current cell is non-zero, place the "target number" (the most frequent non-zero number found in step 4) in the corresponding cell of the output grid.
7.  Return the completed output grid.