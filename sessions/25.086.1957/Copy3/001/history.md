
## train_1

**input:**
```
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 1 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
```


**output:**
```
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0
0 0 1 0 1 0 1 0 0 1 0 1 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 3 3 3 3 3 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0
0 0 4 4 4 0 0 0 0 4 4 4 0 0 0 0
```


## train_2

**input:**
```
6 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 6 6 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 0 0 7 0 0 0 0
4 0 0 0 0 0 0 0 7 0 0 0 0
0 4 0 0 0 0 0 0 7 0 0 0 0
0 0 6 6 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 6 6 0 0 0 0 0
3 0 7 0 0 0 0 0 0 0 0 0 0
3 4 7 0 0 0 3 0 7 0 0 0 0
4 0 0 0 0 0 3 4 7 0 0 0 0
0 4 0 0 0 0 3 0 7 0 0 0 0
0 0 6 6 0 0 3 4 7 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

**Perception**

1.  **Input/Output Grids:** Both examples maintain the grid dimensions from input to output. The background color (white, 0) remains largely unchanged, except where new objects are placed.
2.  **Conditional Behavior:** The transformation logic appears to depend on the presence or absence of magenta (6) pixels in the input grid.
3.  **Example 1 (No Magenta):**
    *   The input grid has several distinct objects (yellow, blue, green) primarily located in the left half.
    *   The output grid retains these original objects and adds copies of them to the right half.
    *   The copies appear to be shifted horizontally to the right. The shift amount seems related to the grid width. Specifically, objects starting in column `c` are copied starting in column `c + width // 2 - 1`. Let's verify: width = 16. `16 // 2 - 1 = 7`. An object at (0, 2) is copied to (0, 2+7) = (0, 9). This matches the output. All objects fully contained within the left half (columns 0 to `width // 2 - 1` = 0 to 7) are copied.
4.  **Example 2 (Magenta Present):**
    *   The input grid contains magenta (6) blocks, a complex object made of green/yellow/orange, and some isolated orange pixels.
    *   The output grid shows that only the complex green/yellow/orange object has been copied. The original object and all other elements (magenta blocks, isolated orange pixels) remain untouched.
    *   The copy is shifted both horizontally and vertically.
    *   Identifying the largest non-white object: The complex object seems visually largest. Let's assume it is. Its top-left corner is at (2, 0).
    *   Identifying the magenta blocks: There are four 2-pixel magenta blocks. Let's find their top-left coordinates: (0,0), (3,6), (8,2), (11,8).
    *   Sorting these coordinates (row first, then column): (0,0), (3,6), (8,2), (11,8).
    *   The copy of the largest object starts at (5, 6) in the output.
    *   The shift vector is (delta_row, delta_col) = (5-2, 6-0) = (3, 6).
    *   This shift vector (3, 6) matches the coordinates of the *second* magenta block in the sorted list.
5.  **General Pattern:** The task involves conditionally copying objects. If magenta is absent, copy all objects from the left half with a specific horizontal shift `(0, width // 2 - 1)`. If magenta is present, copy only the largest object with a shift determined by the coordinates of the second magenta block (when sorted by position).

**Facts**


```yaml
task_type: object_copying_conditional
grid_properties:
  - dimensions_preserved: True
  - background_color: white (0) # Generally preserved
objects:
  - type: contiguous_pixels # Non-white pixels adjacent (including diagonals) form objects
  - properties:
      - color: Any non-white color (1-9)
      - size: Number of pixels in the object
      - position: Coordinates of pixels, often represented by top-left corner or bounding box
      - location_constraint: In one condition, objects must be within the left half (columns 0 to width // 2 - 1)
  - key_object_color: magenta (6) # Presence acts as a condition switch
actions:
  - action: identify_objects # Find all contiguous non-white pixel groups
  - action: check_condition # Check if magenta (6) pixels exist in the input
  - action: filter_objects # Based on condition (location or size)
  - action: calculate_shift_vector
      - if_magenta_absent: shift = (0, grid_width // 2 - 1)
      - if_magenta_present:
          - find_magenta_blocks
          - sort_magenta_blocks_by_position # Top-left corner, row then column
          - select_second_magenta_block
          - shift = top_left_coordinates_of_second_block
  - action: copy_object(s) # Apply shift vector to selected object(s) pixels
  - action: draw_copy # Place copied pixels onto the output grid, overwriting existing pixels
relationships:
  - if_magenta_absent: Shift depends on grid_width. Applies to objects in the left half.
  - if_magenta_present: Shift depends on the position of the second magenta block. Applies only to the largest object.
```


**Natural Language Program**

1.  Receive the input grid. Create an output grid initialized as a copy of the input grid.
2.  Determine the width (`W`) of the grid.
3.  Check if any pixel in the input grid has the color magenta (6).
4.  **If no magenta pixels are found:**
    a.  Calculate the horizontal shift amount: `shift_col = W // 2 - 1`. The vertical shift `shift_row` is 0.
    b.  Identify all distinct non-white objects in the input grid.
    c.  For each identified object:
        i.  Check if all pixels of the object are located within the left half of the grid (column index < `W // 2`).
        ii. If the object is entirely within the left half, calculate the new position for each pixel `(r, c)` of the object as `(r + shift_row, c + shift_col) = (r, c + shift_col)`.
        iii. Draw the object's pixels (using their original colors) at these new positions onto the output grid, overwriting any existing pixels at those locations.
5.  **If magenta pixels are found:**
    a.  Identify all distinct non-white objects in the input grid.
    b.  Find the object with the largest number of pixels (the largest object). If there's a tie in size, the choice might need further clarification (e.g., first one found, topmost, leftmost), but based on the example, assume there's a unique largest or the specific choice doesn't matter. Let the top-left pixel of the largest object be at `(obj_r, obj_c)`.
    c.  Identify all distinct magenta (6) objects (blocks).
    d.  Determine the top-left coordinate `(r_tl, c_tl)` for each magenta block.
    e.  Create a list of these top-left coordinates.
    f.  Sort the list of coordinates, first by row (`r_tl`) and then by column (`c_tl`).
    g.  Select the coordinates of the *second* item in the sorted list. Let these be `(shift_row, shift_col)`.
    h.  For each pixel `(r, c)` belonging to the largest object identified in step 5b:
        i.  Calculate its new position as `(r + shift_row, c + shift_col)`.
        ii. Draw the pixel (using its original color) at this new position onto the output grid, overwriting any existing pixels at that location.
6.  Return the modified output grid.
