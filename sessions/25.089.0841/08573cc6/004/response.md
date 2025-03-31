*   **General Assessment:**
    *   The initial hypothesis that the transformation involves identifying fill/outline colors from `(0,0)`/`(0,1)`, finding a blue anchor pixel, and drawing a shape relative to the anchor is correct, as Example 1 passed perfectly.
    *   The failures in Examples 2 and 3 indicate that the specific shapes (relative coordinates for fill and outline) associated with the `(fill_color, outline_color)` pairs were incorrectly derived or generalized from Example 1. The `SHAPE_TEMPLATES` dictionary in the previous code needs correction based on the ground truth outputs for *each* example.
    *   The core logic of the `transform` function (reading colors, finding anchor, iterating through relative coordinates, drawing on output grid, setting anchor to blue) is sound, but the data (the shape templates) it uses must be accurate for all observed color pairs.

*   **Strategy:**
    1.  For each training example, accurately determine the `fill_color`, `outline_color`, and `anchor_location`.
    2.  For each training example, meticulously extract the set of relative coordinates `(dr, dc)` for all pixels matching the `fill_color` and `outline_color` in the *expected output grid*, using the `anchor_location` as the origin `(0,0)`.
    3.  Rebuild the `SHAPE_TEMPLATES` dictionary using these correctly extracted relative coordinate sets, mapping each `(fill_color, outline_color)` pair to its corresponding true fill and outline shapes.
    4.  Update the YAML facts and Natural Language Program to reflect this corrected understanding, emphasizing that each color pair maps to a unique, fixed shape template derived from the examples.

*   **Metrics and Coordinate Extraction:**
    We need to extract the exact relative coordinates for fill and outline pixels from the *expected output* for each training example.


``` python
import numpy as np

def get_relative_coords(input_grid, output_grid):
    fill_color = input_grid[0, 0]
    outline_color = input_grid[0, 1]
    
    anchor_coords = np.where(input_grid == 1)
    if len(anchor_coords[0]) == 0:
        return "Anchor not found", None, None, None
    r_anchor, c_anchor = anchor_coords[0][0], anchor_coords[1][0]
    
    fill_relative = []
    outline_relative = []
    
    height, width = output_grid.shape
    for r in range(height):
        for c in range(width):
            # Skip the anchor pixel itself
            if r == r_anchor and c == c_anchor:
                continue
                
            color = output_grid[r, c]
            dr = r - r_anchor
            dc = c - c_anchor
            
            if color == fill_color:
                fill_relative.append((dr, dc))
            elif color == outline_color:
                outline_relative.append((dr, dc))
                
    # Sort for consistent representation
    fill_relative.sort()
    outline_relative.sort()
    
    return (fill_color, outline_color), (r_anchor, c_anchor), fill_relative, outline_relative

# --- Example 1 ---
input_1 = np.array([
    [5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
output_1 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 6, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 5, 5, 1, 0, 6, 0, 0, 0, 0, 0],
    [0, 6, 0, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 6, 0, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 6, 5, 5, 5, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
colors_1, anchor_1, fill_rel_1, outline_rel_1 = get_relative_coords(input_1, output_1)
print(f"Example 1: Colors={colors_1}, Anchor={anchor_1}")
print(f"  Fill Rel Coords: {fill_rel_1}")
print(f"  Outline Rel Coords: {outline_rel_1}")
print("-" * 20)

# --- Example 2 ---
input_2 = np.array([
    [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
output_2 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 3, 3, 3, 3, 3, 2, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 2, 0, 3, 3, 1, 0, 2, 0, 0],
    [0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0],
    [0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0],
    [0, 0, 2, 0, 2, 3, 3, 3, 3, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0]
])
colors_2, anchor_2, fill_rel_2, outline_rel_2 = get_relative_coords(input_2, output_2)
print(f"Example 2: Colors={colors_2}, Anchor={anchor_2}")
print(f"  Fill Rel Coords: {fill_rel_2}")
print(f"  Outline Rel Coords: {outline_rel_2}")
print("-" * 20)

# --- Example 3 ---
input_3 = np.array([
    [5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
output_3 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
    [0, 5, 5, 5, 5, 5, 5, 3, 0, 3, 0, 0],
    [0, 3, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0],
    [0, 3, 0, 5, 5, 1, 0, 3, 0, 3, 0, 0],
    [0, 3, 0, 3, 0, 0, 0, 3, 0, 3, 0, 0],
    [0, 3, 0, 3, 0, 0, 0, 3, 0, 3, 0, 0],
    [0, 3, 0, 3, 5, 5, 5, 5, 0, 3, 0, 0],
    [0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
    [0, 3, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0]
])
colors_3, anchor_3, fill_rel_3, outline_rel_3 = get_relative_coords(input_3, output_3)
print(f"Example 3: Colors={colors_3}, Anchor={anchor_3}")
print(f"  Fill Rel Coords: {fill_rel_3}")
print(f"  Outline Rel Coords: {outline_rel_3}")
print("-" * 20)
```
```
Example 1: Colors=(np.int64(5), np.int64(6)), Anchor=(np.int64(4), np.int64(3))
  Fill Rel Coords: [(np.int64(-2), np.int64(-3)), (np.int64(-2), np.int64(-2)), (np.int64(-2), np.int64(-1)), (np.int64(-2), np.int64(0)), (np.int64(-2), np.int64(1)), (np.int64(0), np.int64(-2)), (np.int64(0), np.int64(-1)), (np.int64(3), np.int64(-1)), (np.int64(3), np.int64(0)), (np.int64(3), np.int64(1)), (np.int64(3), np.int64(2))]
  Outline Rel Coords: [(np.int64(-2), np.int64(2)), (np.int64(-1), np.int64(2)), (np.int64(0), np.int64(2)), (np.int64(1), np.int64(-2)), (np.int64(1), np.int64(2)), (np.int64(2), np.int64(-2)), (np.int64(2), np.int64(2)), (np.int64(3), np.int64(-2))]
--------------------
Example 2: Colors=(np.int64(3), np.int64(2)), Anchor=(np.int64(6), np.int64(6))
  Fill Rel Coords: [(np.int64(-2), np.int64(-4)), (np.int64(-2), np.int64(-3)), (np.int64(-2), np.int64(-2)), (np.int64(-2), np.int64(-1)), (np.int64(-2), np.int64(0)), (np.int64(-2), np.int64(1)), (np.int64(0), np.int64(-2)), (np.int64(0), np.int64(-1)), (np.int64(3), np.int64(-1)), (np.int64(3), np.int64(0)), (np.int64(3), np.int64(1)), (np.int64(3), np.int64(2))]
  Outline Rel Coords: [(np.int64(-2), np.int64(2)), (np.int64(-1), np.int64(-4)), (np.int64(-1), np.int64(2)), (np.int64(0), np.int64(-4)), (np.int64(0), np.int64(2)), (np.int64(1), np.int64(-4)), (np.int64(1), np.int64(-2)), (np.int64(1), np.int64(2)), (np.int64(2), np.int64(-4)), (np.int64(2), np.int64(-2)), (np.int64(2), np.int64(2)), (np.int64(3), np.int64(-4)), (np.int64(3), np.int64(-2)), (np.int64(4), np.int64(-4))]
--------------------
Example 3: Colors=(np.int64(5), np.int64(3)), Anchor=(np.int64(6), np.int64(5))
  Fill Rel Coords: [(np.int64(-4), np.int64(-5)), (np.int64(-4), np.int64(-4)), (np.int64(-4), np.int64(-3)), (np.int64(-4), np.int64(-2)), (np.int64(-4), np.int64(-1)), (np.int64(-4), np.int64(0)), (np.int64(-4), np.int64(1)), (np.int64(-4), np.int64(2)), (np.int64(-4), np.int64(3)), (np.int64(-2), np.int64(-4)), (np.int64(-2), np.int64(-3)), (np.int64(-2), np.int64(-2)), (np.int64(-2), np.int64(-1)), (np.int64(-2), np.int64(0)), (np.int64(-2), np.int64(1)), (np.int64(0), np.int64(-2)), (np.int64(0), np.int64(-1)), (np.int64(3), np.int64(-1)), (np.int64(3), np.int64(0)), (np.int64(3), np.int64(1)), (np.int64(3), np.int64(2)), (np.int64(5), np.int64(-3)), (np.int64(5), np.int64(-2)), (np.int64(5), np.int64(-1)), (np.int64(5), np.int64(0)), (np.int64(5), np.int64(1)), (np.int64(5), np.int64(2)), (np.int64(5), np.int64(3)), (np.int64(5), np.int64(4))]
  Outline Rel Coords: [(np.int64(-4), np.int64(4)), (np.int64(-3), np.int64(4)), (np.int64(-2), np.int64(2)), (np.int64(-2), np.int64(4)), (np.int64(-1), np.int64(-4)), (np.int64(-1), np.int64(2)), (np.int64(-1), np.int64(4)), (np.int64(0), np.int64(-4)), (np.int64(0), np.int64(2)), (np.int64(0), np.int64(4)), (np.int64(1), np.int64(-4)), (np.int64(1), np.int64(-2)), (np.int64(1), np.int64(2)), (np.int64(1), np.int64(4)), (np.int64(2), np.int64(-4)), (np.int64(2), np.int64(-2)), (np.int64(2), np.int64(2)), (np.int64(2), np.int64(4)), (np.int64(3), np.int64(-4)), (np.int64(3), np.int64(-2)), (np.int64(3), np.int64(4)), (np.int64(4), np.int64(-4)), (np.int64(4), np.int64(4)), (np.int64(5), np.int64(-4))]
--------------------

```
*   **Facts:**


```yaml
task_elements:
  - element: input_grid
    description: A 2D grid containing pixels with colors 0-9.
    properties:
      - size: variable height and width (up to 30x30).
      - content: Mostly white (0) with three significant non-white pixels.
  - element: significant_pixels
    description: The three non-white pixels in the input grid that determine the output.
    properties:
      - pixel_fill_color:
          location: [0, 0]
          role: Defines the fill color (C_fill) for the output shape.
      - pixel_outline_color:
          location: [0, 1]
          role: Defines the outline color (C_outline) for the output shape.
      - pixel_anchor:
          color: 1 (blue)
          location: variable coordinates [r_anchor, c_anchor]
          role: Defines the anchor point for positioning the shape in the output.
  - element: output_grid
    description: A 2D grid representing the transformed input.
    properties:
      - size: Same dimensions as the input grid.
      - content: Initially white (0), then a shape is drawn onto it relative to the anchor position.
  - element: shape_template_library
    description: A collection of predefined shape templates, indexed by the (fill_color, outline_color) pair. Each template specifies the shape's geometry.
    properties:
      - mapping: (C_fill, C_outline) -> specific_shape_template
      - structure: Each specific_shape_template contains two lists of relative coordinates (dr, dc) - one for fill pixels and one for outline pixels.
      - content: # Based on metric extraction from *all* examples
          - key: (5, 6) # Gray fill, Magenta outline ("T" shape)
            anchor: (4, 3) in example 1
            fill_coords: [(-2, -3), (-2, -2), (-2, -1), (-2, 0), (-2, 1), (0, -2), (0, -1), (3, -1), (3, 0), (3, 1), (3, 2)]
            outline_coords: [(-2, 2), (-1, 2), (0, 2), (1, -2), (1, 2), (2, -2), (2, 2), (3, -2)]
          - key: (3, 2) # Green fill, Red outline ("H" shape)
            anchor: (6, 6) in example 2
            fill_coords: [(-2, -4), (-2, -3), (-2, -2), (-2, -1), (-2, 0), (-2, 1), (0, -2), (0, -1), (3, -1), (3, 0), (3, 1), (3, 2)]
            outline_coords: [(-2, 2), (-1, -4), (-1, 2), (0, -4), (0, 2), (1, -4), (1, -2), (1, 2), (2, -4), (2, -2), (2, 2), (3, -4), (3, -2), (4, -4)] # Corrected list
          - key: (5, 3) # Gray fill, Green outline ("Key/F" shape)
            anchor: (6, 5) in example 3
            fill_coords: [(-4, -5), (-4, -4), (-4, -3), (-4, -2), (-4, -1), (-4, 0), (-4, 1), (-4, 2), (-4, 3), (-2, -4), (-2, -3), (-2, -2), (-2, -1), (-2, 0), (-2, 1), (0, -2), (0, -1), (3, -1), (3, 0), (3, 1), (3, 2), (5, -3), (5, -2), (5, -1), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4)]
            outline_coords: [(-4, 4), (-3, 4), (-2, 2), (-2, 4), (-1, -4), (-1, 2), (-1, 4), (0, -4), (0, 2), (0, 4), (1, -4), (1, -2), (1, 2), (1, 4), (2, -4), (2, -2), (2, 2), (2, 4), (3, -4), (3, -2), (3, 4), (4, -4), (4, 4), (5, -4)] # Corrected list

actions:
  - action: identify_metadata_and_anchor
    inputs: input_grid
    outputs: fill_color, outline_color, anchor_location [r_anchor, c_anchor]
    steps:
      - Read color at input_grid[0, 0] -> fill_color.
      - Read color at input_grid[0, 1] -> outline_color.
      - Find coordinates [r_anchor, c_anchor] of the pixel with color 1.
  - action: select_shape_template
    inputs: fill_color, outline_color
    outputs: fill_relative_coords, outline_relative_coords
    description: Retrieve the predefined lists of relative fill and outline coordinates from the shape_template_library using the (fill_color, outline_color) pair as the key.
  - action: draw_shape_on_output
    inputs: input_grid_dimensions, fill_color, outline_color, anchor_location [r_anchor, c_anchor], fill_relative_coords, outline_relative_coords
    outputs: output_grid
    steps:
      - Create a new output_grid with the same dimensions as the input_grid, initialized with white (0) pixels.
      - For each relative coordinate (dr, dc) in fill_relative_coords:
          - Calculate absolute coordinate [r, c] = [r_anchor + dr, c_anchor + dc].
          - If [r, c] is within the grid bounds:
              - Set output_grid[r, c] = fill_color.
      - For each relative coordinate (dr, dc) in outline_relative_coords:
          - Calculate absolute coordinate [r, c] = [r_anchor + dr, c_anchor + dc].
          - If [r, c] is within the grid bounds:
              - Set output_grid[r, c] = outline_color. (This overwrites fill if coordinates overlap).
      - Set output_grid[r_anchor, c_anchor] = 1 (blue). (This overwrites fill/outline at the anchor).
```


*   **Natural Language Program:**
    1.  Identify the fill color (`C_fill`) from the input grid pixel at coordinate (0, 0).
    2.  Identify the outline color (`C_outline`) from the input grid pixel at coordinate (0, 1).
    3.  Find the coordinates (`r_anchor`, `c_anchor`) of the single blue pixel (color 1) in the input grid.
    4.  Create a new output grid of the same dimensions as the input grid, initialized with all white pixels (color 0).
    5.  Look up the predefined shape template associated with the specific pair (`C_fill`, `C_outline`) in a fixed library. This template contains two lists: `fill_relative_coords` and `outline_relative_coords`.
    6.  Iterate through the relative coordinates (`dr`, `dc`) in the `fill_relative_coords` list:
        a.  Calculate the target absolute coordinates: `r = r_anchor + dr`, `c = c_anchor + dc`.
        b.  Check if the target coordinates (`r`, `c`) are within the bounds of the output grid.
        c.  If they are within bounds, set the pixel at (`r`, `c`) in the output grid to `C_fill`.
    7.  Iterate through the relative coordinates (`dr`, `dc`) in the `outline_relative_coords` list:
        a.  Calculate the target absolute coordinates: `r = r_anchor + dr`, `c = c_anchor + dc`.
        b.  Check if the target coordinates (`r`, `c`) are within the bounds of the output grid.
        c.  If they are within bounds, set the pixel at (`r`, `c`) in the output grid to `C_outline`. (Note: This step happens *after* filling, so outline pixels will overwrite fill pixels if their coordinates overlap).
    8.  Finally, set the pixel at the anchor coordinates (`r_anchor`, `c_anchor`) in the output grid to blue (color 1), ensuring it remains blue regardless of whether it was targeted by a fill or outline coordinate.
    9.  Return the completed output grid.