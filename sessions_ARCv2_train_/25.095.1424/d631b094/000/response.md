*   **Perception:** The task involves processing a 2D grid of numbers (integers). The input grids contain mostly zeros and one specific non-zero digit repeated multiple times. The output is a 1D sequence (represented as a space-separated string) containing only the non-zero digits from the input grid. The order of the digits in the output corresponds to the order they appear when reading the input grid row by row, from left to right.

*   **Facts:**
    
```yaml
    task_elements:
      - item: input_grid
        type: 2D list of integers
        properties:
          - contains mostly zeros
          - contains one type of non-zero integer
      - item: output_sequence
        type: string
        properties:
          - contains space-separated integers
          - consists only of the non-zero integer found in the input_grid
          - the count of the integer matches its count in the input_grid
    relationships:
      - relation: extraction
        from: input_grid
        to: output_sequence
        details: Non-zero elements are extracted from the input grid.
      - relation: ordering
        of: elements in output_sequence
        based_on: input_grid scan order
        details: Elements appear in the output in the order they are encountered when scanning the input grid row by row (top-to-bottom), then column by column (left-to-right).
    ```


*   **Natural Language Program:**
    1.  Initialize an empty list to store the non-zero numbers.
    2.  Iterate through each row of the input grid, from the top row to the bottom row.
    3.  Within each row, iterate through each element (number) from left to right.
    4.  If the current element is not zero, append it to the list of non-zero numbers.
    5.  After iterating through all elements in the grid, convert the numbers in the collected list to strings.
    6.  Join the string representations of the numbers with a single space delimiter to form the final output string.