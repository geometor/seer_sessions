
## train_1

**input:**
```
8 8 8 8 8 8 8 7 8 8
8 8 8 8 8 8 8 8 8 8
1 6 8 8 8 8 8 8 8 7
8 8 8 8 8 8 8 8 8 8
8 8 8 8 6 1 8 8 8 7
8 8 6 8 8 8 6 8 8 8
8 8 1 8 8 8 1 8 8 8
8 8 8 8 8 8 8 6 8 8
8 8 8 8 8 8 8 1 8 8
8 8 7 8 8 8 7 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 7 8 8
8 8 8 8 8 8 8 8 8 8
1 6 8 8 8 8 8 8 8 7
8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 6 8 8 8 7
8 8 1 8 8 8 1 8 8 8
8 8 6 8 8 8 6 8 8 8
8 8 8 8 8 8 8 6 8 8
8 8 8 8 8 8 8 1 8 8
8 8 7 8 8 8 7 8 8 8
```


## train_2

**input:**
```
8 7 8 8 8 8 8 7
8 8 8 8 8 8 8 8
8 6 8 8 8 8 8 1
8 1 8 1 8 8 8 6
8 8 8 6 8 8 8 8
8 8 8 8 8 8 8 8
7 8 8 8 8 1 6 8
8 8 8 7 8 8 8 8
```


**output:**
```
8 7 8 8 8 8 8 7
8 8 8 8 8 8 8 8
8 6 8 8 8 8 8 6
8 1 8 1 8 8 8 1
8 8 8 6 8 8 8 8
8 8 8 8 8 8 8 8
7 8 8 8 8 6 1 8
8 8 8 7 8 8 8 8
```


## train_3

**input:**
```
7 8 8 8 8 8 8 8 8 8 8 8 7 8
8 8 1 6 8 8 8 8 8 8 8 8 8 7
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 6 1 8 8 8 7
8 8 8 8 8 8 8 8 1 6 8 8 8 7
8 8 8 8 1 8 8 8 8 8 8 8 6 8
8 8 8 8 6 8 8 8 8 8 8 8 1 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 1 6 8 8 8 8 7
8 8 8 8 8 8 8 8 8 8 8 8 8 8
1 8 8 8 8 8 8 8 8 8 8 8 8 8
6 8 8 8 7 8 8 8 8 8 8 8 8 8
```


**output:**
```
7 8 8 8 8 8 8 8 8 8 8 8 7 8
8 8 1 6 8 8 8 8 8 8 8 8 8 7
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 6 8 8 8 7
8 8 8 8 8 8 8 8 1 6 8 8 8 7
8 8 8 8 1 8 8 8 8 8 8 8 6 8
8 8 8 8 6 8 8 8 8 8 8 8 1 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 1 6 8 8 8 8 7
8 8 8 8 8 8 8 8 8 8 8 8 8 8
6 8 8 8 8 8 8 8 8 8 8 8 8 8
1 8 8 8 7 8 8 8 8 8 8 8 8 8
```

**Perception of Task Elements:**

The task involves modifying a grid based on the relative positions of specific colored pixels. The input grids primarily consist of an azure (8) background, with scattered pixels of other colors, notably blue (1), magenta (6), and orange (7). The transformation rule focuses specifically on the interaction between blue (1) and magenta (6) pixels when they are vertically adjacent. Orange (7) and azure (8) pixels appear unaffected and act as background or static elements. The core operation is a conditional positional swap between vertically adjacent magenta and blue pixels.

**YAML Facts:**


```yaml
task_elements:
  - grid_dimensions: Variable (e.g., 10x10, 8x8, 14x14)
  - background_color: azure (8)
  - relevant_colors:
      - blue (1)
      - magenta (6)
  - static_colors:
      - orange (7)
      - azure (8)
  - key_relationship: Vertical adjacency
  - condition: A magenta (6) pixel is located directly above a blue (1) pixel.
  - action: If the condition is met, swap the positions (colors) of the magenta (6) and blue (1) pixels.
  - constraints:
      - Only applies to vertical adjacency (not horizontal or diagonal).
      - Only applies when magenta (6) is above blue (1).
      - Swaps happen in pairs; isolated blue or magenta pixels are not affected unless they form the specific vertical pair.
      - Other colors (orange, azure) are unchanged.
```


**Natural Language Program:**

1.  Create a copy of the input grid to serve as the basis for the output grid.
2.  Iterate through each cell `(row, col)` of the input grid, excluding the last row.
3.  Check if the color of the cell at `(row, col)` is magenta (6).
4.  If it is magenta (6), check if the color of the cell directly below it, at `(row + 1, col)`, is blue (1).
5.  If both conditions are true (magenta at `(row, col)` and blue at `(row + 1, col)`), then modify the *output grid copy*:
    *   Set the color of the cell at `(row, col)` in the output grid to blue (1).
    *   Set the color of the cell at `(row + 1, col)` in the output grid to magenta (6).
6.  After checking all cells (excluding the last row), the modified output grid copy represents the final output.
