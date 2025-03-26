
## train_1

**input:**
```
2 0 0 1 2 0 0 1 2 0 0 1
4 2 1 4 4 2 1 4 4 2 1 4
4 1 2 4 4 1 2 4 4 1 2 4
1 0 0 2 1 0 0 2 1 0 0 2
```


**output:**
```
2 0 0 1
4 2 1 4
4 1 2 4
1 0 0 2
```


## train_2

**input:**
```
4 5 1 1 5 4 4 5 1
5 5 5 5 5 5 5 5 5
1 5 4 4 5 1 1 5 4
```


**output:**
```
4 5 1
5 5 5
1 5 4
```


## train_3

**input:**
```
2 1 2 1 2 1
2 3 2 3 2 3
```


**output:**
```
2 1
2 3
```

*   **Perception:**
    *   Each input grid appears to be composed of a smaller grid pattern repeated horizontally multiple times.
    *   In all provided examples (train\_1, train\_2, train\_3), the input grid is exactly three times wider than the output grid.
    *   The height of the input grid is the same as the height of the output grid.
    *   The output grid corresponds precisely to the leftmost segment of the input grid, which represents the fundamental repeating unit.

*   **Facts:**
    
```yaml
    task_description: Extract the fundamental repeating horizontal pattern from the input grid.
    examples:
      train_1:
        input_grid:
          height: 4
          width: 12
          pattern: A 4x4 grid repeated horizontally 3 times.
        output_grid:
          height: 4
          width: 4
          content: The leftmost 4x4 section of the input grid.
        relationship: Output is the first horizontal repetition unit of the input.
      train_2:
        input_grid:
          height: 3
          width: 9
          pattern: A 3x3 grid repeated horizontally 3 times.
        output_grid:
          height: 3
          width: 3
          content: The leftmost 3x3 section of the input grid.
        relationship: Output is the first horizontal repetition unit of the input.
      train_3:
        input_grid:
          height: 2
          width: 6
          pattern: A 2x2 grid repeated horizontally 3 times.
        output_grid:
          height: 2
          width: 2
          content: The leftmost 2x2 section of the input grid.
        relationship: Output is the first horizontal repetition unit of the input.
    observations:
      - The input grid width is always a multiple of the output grid width (specifically, 3 times in these examples).
      - The input and output grid heights are identical.
      - The input grid content consists of the output grid pattern repeated horizontally.
    ```


*   **Natural Language Program:**
    1.  Determine the height (`H`) and width (`W`) of the input grid.
    2.  Assume the input grid is composed of a repeating pattern tiled horizontally exactly three times.
    3.  Calculate the width of the repeating pattern (`W_pattern`) by dividing the input width (`W`) by 3.
    4.  Create the output grid by extracting the leftmost section of the input grid with height `H` and width `W_pattern`.
