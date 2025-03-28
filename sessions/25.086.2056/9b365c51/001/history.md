
## train_1

**input:**
```
0 1 0 6 0 7 0 8 8 8 0 0 8 8 8
0 1 0 6 0 7 0 8 8 8 0 0 8 8 8
0 1 0 6 0 7 0 0 0 0 8 8 8 8 8
0 1 0 6 0 7 0 0 0 0 8 8 0 0 0
0 1 0 6 0 7 0 0 0 0 8 8 0 0 0
0 1 0 6 0 7 0 0 0 0 8 8 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 1 1 1 0 0 7 7 7
0 0 0 0 0 0 0 1 1 1 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 6 6 7 7 7
0 0 0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 6 6 0 0 0
```


## train_2

**input:**
```
0 4 0 3 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 3 0 2 0 0 8 8 8 8 0 0 0 8 8 8 8 0
0 4 0 3 0 2 0 0 8 8 8 8 0 0 0 8 8 8 8 0
0 4 0 3 0 2 0 0 8 8 8 8 8 8 0 8 8 8 8 0
0 4 0 3 0 2 0 0 8 8 8 8 8 8 0 8 8 8 8 0
0 4 0 3 0 2 0 0 0 0 0 0 8 8 0 0 0 0 0 0
0 4 0 3 0 2 0 0 0 0 0 0 8 8 0 0 0 0 0 0
0 4 0 3 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 4 4 4 4 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 4 4 4 4 3 3 0 2 2 2 2 0
0 0 0 0 0 0 0 0 4 4 4 4 3 3 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 3 0 2 0 4 0 7 0 8 8 0 0 0 8 8 0 0
0 3 0 2 0 4 0 7 0 8 8 8 8 0 8 8 0 0
0 3 0 2 0 4 0 7 0 0 0 8 8 0 8 8 0 0
0 3 0 2 0 4 0 7 0 0 0 8 8 0 8 8 8 8
0 3 0 2 0 4 0 7 0 0 0 0 0 0 8 8 8 8
0 3 0 2 0 4 0 7 0 0 0 0 0 0 0 0 8 8
0 3 0 2 0 4 0 7 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 3 3 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 3 3 2 2 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 0 4 4 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

**Perception:**

1.  **Input Grid Structure:** The input grids generally consist of three main parts:
    *   A white background (color 0).
    *   Several distinct vertical lines, each one pixel wide and extending the full height of the grid. Each line has a unique color (not white/0 and not azure/8). These lines appear on the left side, separated by white columns.
    *   One or more shapes made of azure pixels (color 8) located to the right of the vertical lines. These shapes can be complex and sometimes disconnected, but are treated based on the columns they occupy.
2.  **Output Grid Structure:** The output grids have the same dimensions as the input grids.
    *   The vertical color lines from the input are gone.
    *   The areas originally occupied by azure pixels are now colored, using the colors from the vertical lines.
    *   All other pixels, including the original positions of the vertical lines and the original white background, are white (color 0).
3.  **Transformation:**
    *   The vertical lines act as color palettes or instructions. Their horizontal order is crucial.
    *   The azure pixels act as targets for recoloring.
    *   The columns containing azure pixels are grouped into contiguous blocks. For instance, if azure appears in columns 7, 8, 9, 11, 12, the groups are {7, 8, 9} and {11, 12}.
    *   There's a one-to-one mapping between the ordered vertical color lines (left-to-right) and the ordered groups of azure columns (left-to-right).
    *   The first color line dictates the new color for all azure pixels within the first group of azure columns. The second line dictates the color for the second group, and so on.
    *   The position (row and column) of each azure pixel remains the same in the output grid, but its color changes according to the mapping rule.

**YAML Facts:**


```yaml
task_context:
  grid_dimensionality: 2D
  grid_size_constraints: 1x1 to 30x30
  color_palette_size: 10 (0-9)
  background_color: 0 (white)

input_elements:
  - type: background
    color: 0 (white)
    description: Fills empty space.
  - type: vertical_lines
    color: variable (not 0, not 8)
    properties:
      - single_column_width
      - full_grid_height
      - distinct_colors
      - located_on_left
      - separated_by_white_columns
    role: source_of_color_information
  - type: target_shapes
    color: 8 (azure)
    properties:
      - variable_shape_size
      - located_on_right
      - can_be_multiple_disconnected_shapes
    role: pixels_to_be_recolored

output_elements:
  - type: background
    color: 0 (white)
    description: Fills all space except recolored target shapes.
  - type: recolored_shapes
    color: variable (derived from input vertical_lines)
    properties:
      - occupy_same_pixels_as_input_target_shapes
    role: result_of_transformation

transformation_rules:
  - action: identify_vertical_lines
    inputs: input_grid
    outputs: list_of_colors, list_of_column_indices
    description: Find columns composed entirely of a single non-white, non-azure color. Store their color and column index.
  - action: sort_vertical_lines
    inputs: list_of_colors, list_of_column_indices
    outputs: sorted_list_of_colors
    description: Sort the identified vertical lines based on their column index (left-to-right).
  - action: identify_azure_columns
    inputs: input_grid
    outputs: set_of_azure_column_indices
    description: Find all unique column indices that contain at least one azure (8) pixel.
  - action: group_azure_columns
    inputs: set_of_azure_column_indices
    outputs: list_of_column_groups
    description: Group the azure column indices into contiguous sets (e.g., {7,8,9}, {11,12}).
  - action: sort_azure_column_groups
    inputs: list_of_column_groups
    outputs: sorted_list_of_column_groups
    description: Sort the groups based on the minimum column index within each group (left-to-right).
  - action: map_colors_to_groups
    inputs: sorted_list_of_colors, sorted_list_of_column_groups
    outputs: mapping_dictionary (group -> color)
    description: Create a mapping where the i-th color corresponds to the i-th column group. Assumes the number of lines equals the number of groups.
  - action: generate_output_grid
    inputs: input_grid, mapping_dictionary
    outputs: output_grid
    description: Create an output grid of the same size, initialized to white. For each azure pixel in the input at (r, c), find its column group, get the corresponding color from the mapping, and place that color at (r, c) in the output grid.

relationships:
  - type: spatial_ordering
    entity1: vertical_lines
    entity2: azure_column_groups
    description: The left-to-right order of vertical lines corresponds directly to the left-to-right order of azure column groups.
  - type: color_assignment
    entity1: vertical_line_color
    entity2: azure_pixels_in_corresponding_group
    description: The color of a vertical line determines the output color of the azure pixels belonging to its corresponding column group.

assumptions:
  - The number of vertical color lines equals the number of contiguous groups of azure columns.
  - Vertical lines span the full height of the grid.
  - Vertical lines are always 1 pixel wide.
  - Azure (8) is exclusively used for the target shapes to be recolored.
  - All non-azure, non-line pixels in the input are white (0).
```


**Natural Language Program:**

1.  Create a new grid, the `output_grid`, with the same dimensions as the `input_grid`, and fill it entirely with white (0).
2.  Identify all vertical "color lines" in the `input_grid`. A color line is a column `j` where every cell `input_grid[row][j]` contains the same color `C`, and `C` is not white (0) and not azure (8). Store these as pairs of `(color, column_index)`.
3.  Sort these color line pairs based on their `column_index` in ascending order. Let the sorted colors be `C1, C2, ..., CN`.
4.  Identify all unique column indices in the `input_grid` that contain at least one azure (8) pixel.
5.  Group these azure column indices into contiguous sets. For example, if azure pixels are in columns 7, 8, 10, 11, 12, the groups are `{7, 8}` and `{10, 11, 12}`.
6.  Sort these groups based on their minimum column index in ascending order. Let the sorted groups be `G1, G2, ..., GN`.
7.  Iterate through each cell `(row, col)` of the `input_grid`.
8.  If the cell `input_grid[row][col]` contains the azure color (8):
    a.  Determine which group `Gi` the `col` belongs to (where `Gi` is one of the sorted groups `G1` to `GN`).
    b.  Find the index `i` of that group (e.g., if `col` is in `G2`, then `i` is 2).
    c.  Get the corresponding color `Ci` from the sorted list of color line colors (e.g., if `i` is 2, use color `C2`).
    d.  Set the cell `output_grid[row][col]` to this color `Ci`.
9.  Return the `output_grid`.
