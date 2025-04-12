**Perception**

The task involves transforming an input grid into an output grid. Key observations across the examples:
1.  The height of the grid remains unchanged in all examples.
2.  The width of the grid decreases.
3.  The transformation involves removing certain columns from the input grid.
4.  The columns removed appear to be those composed entirely of the background color (white '0').
5.  After removing the empty columns, the content (non-background pixels) from the remaining columns is placed into the new grid.
6.  The vertical position (row) of the pixels in the output grid is often different from their original row in the input grid. This vertical shift seems to be the most complex part of the transformation. It does not appear to be simple gravity, nor a consistent shift based solely on color or original column index. It might depend on the color of the pixel, or perhaps the structure/grouping of the remaining columns.

**Facts**


```yaml
task_context:
  grid_properties:
    - height_constant: True # Grid height remains the same between input and output.
    - width_variable: True # Grid width changes, specifically decreases.
    - background_color: 0 # White '0' is the background color.
  objects:
    - type: contiguous_pixels # Objects are formed by connected pixels of the same non-background color.
    - behavior: preserved_relative_shape # The internal shape of objects seems mostly preserved.
actions:
  - name: identify_empty_columns
    input: input_grid
    description: Find all columns in the input grid that consist entirely of the background color (0).
  - name: remove_columns
    input: input_grid, empty_column_indices
    output: intermediate_grid
    description: Create a new grid structure by excluding the identified empty columns. The width is reduced.
  - name: rearrange_pixels_vertically
    input: intermediate_grid_structure, original_pixel_data
    output: output_grid
    description: Place the non-background pixels from the original non-empty columns into the new grid structure. The final row position of each pixel is determined by a rule that shifts pixels vertically compared to their original row. The exact rule for this vertical shift is complex and not immediately obvious (potentially depending on color, original position, or column context).
relationships:
  - type: column_mapping
    description: A mapping exists between the indices of non-empty columns in the input and the column indices in the output grid.
  - type: vertical_shift
    description: Non-background pixels undergo a vertical shift (change in row index, possibly modulo the grid height) during the transformation. The magnitude and direction of the shift appear dependent on factors yet to be fully determined (e.g., color, column).
```


**Natural Language Program**

1.  Receive the input grid.
2.  Identify all columns in the input grid that contain only the background color (white '0'). Let these be the "empty columns".
3.  Determine the number of non-empty columns. This will be the width of the output grid. The height remains the same as the input grid.
4.  Create a mapping from the original index of each non-empty column to its corresponding index in the output grid (maintaining relative order).
5.  Create a new output grid of the calculated dimensions, initialized with the background color.
6.  Iterate through each pixel `(r, c)` of the input grid.
7.  If the pixel `Input[r, c]` is not the background color AND column `c` is not an empty column:
    a.  Determine the new column index `c_new` using the mapping created in step 4.
    b.  Determine the new row index `r_new`. This requires applying a vertical shift rule to the original row `r`. The shift rule appears complex: based on observations, it might depend on the pixel's color (e.g., in the examples with height 3, Red seems to have 0 shift, Magenta and Blue often -1 shift, Azure seems to shift differently). Calculate `r_new = (r + shift_amount) mod grid_height`.
    c.  Place the color `Input[r, c]` into the output grid at position `(r_new, c_new)`. Resolve potential overlaps if necessary (e.g., last pixel mapped wins).
8.  Return the populated output grid.

*(Self-correction note: The exact vertical shift rule (step 7b) is the main uncertainty. It needs further analysis or refinement based on more examples or insights. The current best guess involves a color-dependent shift, but it wasn't perfectly consistent across all examples and colors tested during analysis.)*