
## train_1

**input:**
```
0 0 0 3 3
0 0 0 0 3
8 0 4 0 0
8 0 0 0 0
8 8 8 0 0
```


**output:**
```
0 0 0 3 3
0 0 0 0 3
4 0 8 0 0
4 0 0 0 0
4 4 4 0 0
```


## train_2

**input:**
```
6 6 6 0 0
6 0 0 0 0
6 0 7 0 0
0 0 0 0 5
0 0 0 5 5
```


**output:**
```
7 7 7 0 0
7 0 0 0 0
7 0 6 0 0
0 0 0 0 5
0 0 0 5 5
```


## train_3

**input:**
```
0 0 0 7 7
0 0 0 0 7
0 0 8 0 9
0 0 0 0 9
0 0 9 9 9
```


**output:**
```
0 0 0 7 7
0 0 0 0 7
0 0 9 0 8
0 0 0 0 8
0 0 8 8 8
```

Okay, analyzing the provided examples to understand the transformation rule.

**Perception of Task Elements:**

*   **Input/Output:** Both are grids (2D arrays) of integers, likely representing colors or states.
*   **Grid Size:** All examples use 5x5 grids.
*   **Content:** The grids contain integers from 0 to 9. '0' seems to act as a background color. Non-zero integers form patterns or shapes.
*   **Transformation:** The core transformation involves swapping two specific non-zero colors throughout the grid, while leaving all other colors (including the background '0') unchanged.
*   **Color Selection:** The key challenge is determining *which* two colors to swap based on the input grid's properties. Analyzing the examples reveals a pattern:
    *   In Example 1, colors 8 and 4 are swapped. Color 4 appears once, color 8 is the most frequent non-zero color (5 times).
    *   In Example 2, colors 6 and 7 are swapped. Color 7 appears once, color 6 is the most frequent non-zero color (5 times).
    *   In Example 3, colors 8 and 9 are swapped. Color 8 appears once, color 9 is the most frequent non-zero color (5 times).
*   **Rule:** The transformation identifies the unique color that appears exactly once (excluding 0) and the most frequent non-zero color. These two colors are then swapped everywhere in the grid.

**YAML Fact Document:**


```yaml
task_description: Swap two specific colors in a grid based on frequency counts.
grid_properties:
  type: 2D array of integers
  element_range: 0-9 (observed)
  background_color: 0
objects:
  - object: color_cell
    properties:
      - value: integer (0-9)
      - position: (row, column)
      - frequency: count of occurrences in the grid
relationships:
  - relationship: color_frequency
    description: The number of times each non-zero color appears in the input grid.
  - relationship: unique_color
    description: The non-zero color that appears exactly once in the input grid.
    property: frequency == 1
  - relationship: most_frequent_color
    description: The non-zero color that appears most often in the input grid.
    property: maximum frequency among non-zero colors
actions:
  - action: identify_swap_colors
    inputs: input_grid
    outputs: [color_1, color_2]
    steps:
      - Calculate frequency of each non-zero color.
      - Find color_1 where frequency is 1.
      - Find color_2 with the maximum frequency (must be non-zero).
  - action: perform_swap
    inputs: [input_grid, color_1, color_2]
    outputs: output_grid
    steps:
      - Iterate through each cell of the input_grid.
      - If cell value == color_1, set output cell value to color_2.
      - Else if cell value == color_2, set output cell value to color_1.
      - Else, set output cell value to the input cell value.
transformation_goal: Create an output grid where color_1 and color_2 from the input grid have been swapped, and all other colors remain the same.
```


**Natural Language Program:**

1.  **Analyze Frequencies:** Examine the input grid and count the occurrences of each non-zero integer (color).
2.  **Identify Unique Color:** Find the color (`color_1`) that appears exactly one time in the grid.
3.  **Identify Most Frequent Color:** Find the non-zero color (`color_2`) that appears most frequently in the grid.
4.  **Generate Output Grid:** Create a new grid with the same dimensions as the input grid.
5.  **Swap Colors:** Iterate through each cell (`input_cell`) of the input grid at position (row, col):
    *   If the value of `input_cell` is `color_1`, set the corresponding cell in the output grid (`output_cell`) to `color_2`.
    *   Else if the value of `input_cell` is `color_2`, set `output_cell` to `color_1`.
    *   Else (if the value is neither `color_1` nor `color_2`), set `output_cell` to the same value as `input_cell`.
6.  **Return:** The completed output grid is the result of the transformation.
