
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 8 7 7 7 7 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 0 0 0 4 4 8 0 0
0 7 7 7 7 7 7 0 0 0 4 4 4 0 0
0 7 7 7 8 7 7 0 0 0 4 4 4 0 0
0 7 7 7 7 7 7 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 6 6 6 6 6 0 0
8 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 8 0 0 6 8 6 6 6 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 0 0 0 4 4 4 0 0
0 7 7 7 7 7 7 0 0 0 4 4 4 0 0
0 7 7 7 7 7 7 0 0 0 4 4 4 0 0
0 7 7 7 7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 3 0 3
0 0 3 3 3 3 3 3 3 3 0 0 3 3 0
0 0 3 3 3 3 3 3 3 3 0 0 3 3 3
0 0 3 0 3 3 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 2 0 0
0 2 2 2 2 0 0 0 0 0 2 2 2 0 0
0 2 2 2 0 0 0 0 0 0 2 2 2 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 3 3 3 3 3 0 3 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3
0 0 3 3 3 3 3 3 3 3 0 0 3 3 3
0 0 3 3 3 3 3 3 3 3 0 0 3 3 3
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0 0
0 2 2 2 2 0 0 0 0 0 2 2 2 0 0
0 2 2 2 2 0 0 0 0 0 2 2 2 0 0
0 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 0
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception of Elements:**

*   **Input/Output Structure:** Both input and output are 2D grids of integers, representing pixels or cells with different colors. The dimensions of the input and output grids are identical for each example.
*   **Colors:** The grids use integers to represent colors. Color '0' appears to be the background color. Other colors like '2', '3', '4', '6', '7', and '8' form shapes or regions within the grid.
*   **Color '8':** In `train_1`, color '8' appears in various locations, sometimes within or adjacent to regions of other colors, and sometimes isolated. In the output of `train_1`, all instances of color '8' are replaced with color '0'. Color '8' is absent in `train_2`.
*   **Color Filling:** In `train_2`, some cells that are '0' in the input become non-zero ('2' or '3') in the output. This filling seems to occur when a '0' cell is surrounded by a sufficient number of cells of a particular color. For example:
    *   `input[0][13]` is 0, but its neighbors `input[0][12]`, `input[0][14]`, `input[1][13]` are 3, 3, 3 respectively. The output `output[0][13]` becomes 3.
    *   `input[5][12]` is 0. Its 8 neighbors in the input include five '2's (`[4][12]`, `[4][13]`, `[5][11]`, `[6][11]`, `[6][13]`). The output `output[5][12]` becomes 2.
    *   `input[3][11]` is 0. Its 8 neighbors in the input include one '3' and two '2's. The output `output[3][11]` remains 0. This suggests a threshold (likely 3 or more neighbors of the *same* color) is needed for filling.
*   **Order of Operations:** The examples suggest a two-step process might be occurring:
    1.  A "filling" operation where '0' cells adopt the color of their neighbors under certain conditions (neighbor count threshold, most frequent color, ignoring color '8'). This happens in `train_2`.
    2.  A "cleaning" operation where all cells with color '8' are set to '0'. This happens in `train_1`.
    Applying this logic to both examples:
    *   `train_1`: No '0' cells meet the filling condition (or perhaps filling doesn't apply if color 8 is present nearby?). Then, all '8's are removed. This matches the output.
    *   `train_2`: Certain '0' cells are filled based on their neighbors (ignoring '0' and hypothetical '8's). Then, the (non-existent) '8's are removed. This matches the output.
    This implies the filling happens based on the original input state, and the removal of '8's happens as a final step.

**Facts:**


```yaml
task_type: grid_transformation
grid_properties:
  dimensionality: 2D
  cell_type: integer (representing color)
  background_color: 0
objects:
  - type: regions
    properties:
      color: non-zero integer
      shape: contiguous or near-contiguous areas of the same color
special_colors:
  - color: 0
    role: background
  - color: 8
    role: noise/artifact to be removed
transformations:
  - step: 1
    action: fill_background_cells
    input: original input grid
    output: intermediate grid
    conditions:
      - target_cell_color: 0
      - neighbor_analysis:
          - connectivity: 8 neighbors (including diagonals)
          - considered_neighbor_colors: all colors except 0 and 8
          - rule: find the most frequent color (C) among considered neighbors
          - threshold: count of color C must be >= 3
    effect: change target cell color from 0 to C if conditions met
  - step: 2
    action: remove_noise_color
    input: intermediate grid from step 1
    output: final output grid
    conditions:
      - target_cell_color: 8
    effect: change target cell color from 8 to 0
relationships:
  - The filling decision for a cell depends on the colors and frequency of its neighbors in the original input grid.
  - The removal of color 8 is unconditional for any cell containing it after the filling step (if any).
order: The filling step (based on input) logically precedes the noise removal step.
```


**Natural Language Program:**

1.  Initialize an intermediate grid as a copy of the input grid.
2.  Iterate through each cell `(r, c)` of the input grid.
3.  If the color of the cell `input[r][c]` is 0:
    a.  Identify the colors of its 8 neighbors (N, S, E, W, NE, NW, SE, SW) in the *input* grid, ignoring neighbors outside the grid boundaries.
    b.  Create a list of neighbor colors, excluding any neighbors with color 0 or color 8.
    c.  If this list is not empty:
        i.  Determine the color that appears most frequently in the list (`majority_color`).
        ii. Count the occurrences of `majority_color` (`count`).
        iii. If `count` is 3 or greater, set the color of the cell `intermediate_grid[r][c]` to `majority_color`.
4.  Initialize the final output grid as a copy of the intermediate grid.
5.  Iterate through each cell `(r, c)` of the intermediate grid.
6.  If the color of the cell `intermediate_grid[r][c]` is 8, set the color of the corresponding cell `output_
