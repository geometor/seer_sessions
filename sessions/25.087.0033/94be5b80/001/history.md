
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 2 1 3 0 0 0
0 0 0 0 0 0 0 7 2 1 3 0 0 0
0 0 0 0 0 0 0 7 2 1 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 2 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 1 0 0 1 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 7 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0 0 0 0
0 0 0 2 0 0 2 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 1 0 0 1 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 3 0 0 3 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 1 6 0 0 0 0 0 0 0 0
0 0 4 1 6 0 0 0 0 0 0 0 0
0 0 4 1 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 0 0 0 0 0 0
0 0 0 1 0 0 1 0 0 0 0 0 0
0 1 1 1 0 0 1 1 1 0 0 0 0
0 0 1 1 0 0 1 1 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0 0 0
0 0 0 6 6 6 6 0 0 0 0 0 0
0 0 0 6 0 0 6 0 0 0 0 0 0
0 6 6 6 0 0 6 6 6 0 0 0 0
0 0 6 6 0 0 6 6 0 0 0 0 0
0 0 6 6 6 6 6 6 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 0 0 0 0 0 0
0 0 0 4 0 0 4 0 0 0 0 0 0
0 4 4 4 0 0 4 4 4 0 0 0 0
0 0 4 4 0 0 4 4 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0 0 0 0
0 0 0 1 1 1 1 0 0 0 0 0 0
0 0 0 1 0 0 1 0 0 0 0 0 0
0 1 1 1 0 0 1 1 1 0 0 0 0
0 0 1 1 0 0 1 1 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0 0 0
0 0 0 6 6 6 6 0 0 0 0 0 0
0 0 0 6 0 0 6 0 0 0 0 0 0
0 6 6 6 0 0 6 6 6 0 0 0 0
0 0 6 6 0 0 6 6 0 0 0 0 0
0 0 6 6 6 6 6 6 0 0 0 0 0
```

Okay, let's break down the task based on the provided examples.

## Perception

1.  **Input Structure:** The input grid contains two main types of non-white elements:
    *   A "Palette": A horizontal bar of distinct colors, typically 3 rows high, located near the top.
    *   "Template Shapes": Several instances of the same geometric shape (ignoring color), located elsewhere in the grid. In the examples, these are 'T' shapes of different sizes.
2.  **Output Structure:** The output grid contains only the template shapes, potentially including new ones not present in the input. The palette is removed.
3.  **Transformation:**
    *   The palette defines a sequence of colors based on their left-to-right order.
    *   The task identifies the common geometric structure of the template shapes.
    *   The output grid removes the palette.
    *   It then constructs a vertical stack of the template shape, using *all* the colors from the palette, ordered according to the palette's sequence.
    *   The original template shapes are essentially replaced by this new, complete stack.
    *   The vertical positioning of this stack is determined by aligning one of the shapes in the stack (specifically, the one whose color corresponds to the *top-most* original template shape in the input) with the original position of that top-most shape.
    *   The horizontal positioning (column) of the stack matches the horizontal position of the original template shapes.
    *   The shapes in the final stack are placed immediately adjacent vertically (no gap).

## Facts


```yaml
task_type: object_transformation_and_arrangement

elements:
  - type: palette
    description: A horizontal, multi-row bar of unique, non-white pixels near the top. Defines an ordered sequence of colors.
    properties:
      - colors: [orange, red, blue, green] in train_1
      - colors: [yellow, blue, magenta] in train_2
      - order: determined by left-to-right position
    action: removed_in_output

  - type: template_shapes
    description: Multiple instances of the same geometric shape structure, differing only in color, located elsewhere in the grid.
    properties:
      - shape_structure: unique geometric form (e.g., 'T' shape)
      - height: H pixels
      - width: W pixels
      - colors_present_in_input: a subset of palette colors
      - common_start_column: all instances share the same leftmost column index
      - minimum_start_row: the row index of the topmost instance

relationships:
  - type: color_mapping
    description: The set of all colors used for the final output shapes is exactly the set of colors present in the input palette.
  - type: order_dependence
    description: The vertical order of shapes in the output stack matches the left-to-right order of colors in the input palette.
  - type: spatial_alignment
    description:
      - horizontal: The output stack of shapes aligns horizontally (uses the same starting column) with the original template shapes.
      - vertical: The stack is positioned so that the shape corresponding to the color of the *top-most original* template shape appears at the *same row* where that top-most original shape started. Shapes in the stack are placed contiguously, with no vertical gap.

actions:
  - identify_palette_colors_and_order
  - identify_template_shape_structure_and_dimensions
  - identify_original_template_shapes_position_and_colors
  - determine_anchor_shape (the topmost original shape)
  - calculate_output_stack_start_position (based on anchor shape color, its index in palette, and its original row)
  - generate_output_grid:
      - remove palette
      - draw the complete stack of shapes (one for each palette color in order) at the calculated position.

derived_properties:
  - stack_height: number_of_palette_colors * template_shape_height
```


## Natural Language Program

1.  **Identify the Palette:** Scan the input grid to find a dense, horizontal rectangular region, typically 3 rows high and located near the top, composed of unique non-white colors. Extract the sequence of colors (`P`) from left to right within this region.
2.  **Identify the Template Shape:** Locate all other non-white objects in the grid. Verify that they share the same geometric shape. Define this common shape as the `Template`. Determine its height (`H`) and the common starting column (`colS`) of these initial instances.
3.  **Identify the Anchor:** Find the instance of the `Template` in the input grid that has the minimum starting row (`min_orig_row`). Record its color (`anchor_color`).
4.  **Find Anchor Index in Palette:** Determine the 0-based index (`k`) where `anchor_color` appears in the palette color sequence `P`.
5.  **Calculate Stack Start Row:** Compute the starting row (`R_start`) for the output stack using the formula: `R_start = min_orig_row - (k * H)`.
6.  **Generate Output:** Create a new grid with the same dimensions as the input, initially filled with the background color (white). For each color `ci` in the palette sequence `P` at index `i` (from 0 to n-1, where n is the number of colors in P):
    a.  Calculate the placement row for this shape: `current_row = R_start + (i * H)`.
    b.  Draw the `Template` shape using color `ci` onto the output grid, starting at position (`current_row`, `colS`).
7.  Return the generated output grid.
