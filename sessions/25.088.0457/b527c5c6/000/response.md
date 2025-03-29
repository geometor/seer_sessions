Okay, let's analyze the provided examples to understand the transformation logic.

**Perception of Elements:**

1.  **Grid Composition:** The grids primarily consist of a white background (0) and green objects (3). Each green object contains exactly one red pixel (2).
2.  **Objects:** The core objects are contiguous blocks of green pixels, each marked by a single red pixel. These objects can be lines (horizontal or vertical) or potentially more complex shapes connected orthogonally.
3.  **Red Pixel Role:** The red pixel acts as a focal point or a "seed" within its connected green object.
4.  **Transformation Trigger:** The relationship between the red pixel and its immediate green neighbors determines the primary direction of action.
5.  **Action - Expansion/Filling:** The transformation involves expanding the colors (red and green) of the object into adjacent white space. The expansion follows a specific direction determined by the object's structure around the red pixel.
6.  **Expansion Direction Logic:**
    *   If the green pixels immediately adjacent to the red pixel are only horizontal (left/right), the expansion direction is vertical (either up or down).
    *   If the green pixels immediately adjacent to the red pixel are only vertical (up/down), the expansion direction is horizontal (either left or right).
    *   The specific direction (up vs. down, or left vs. right) is determined by checking the orthogonal direction from the red pixel *not* occupied by an adjacent green pixel. The expansion occurs towards the direction that initially points to a white cell.
7.  **Expansion Process:** Once the direction is determined for an object, *every* pixel (red or green) belonging to that connected object expands its own color in that direction, filling contiguous white cells along that line until a non-white cell or the grid boundary is encountered.

**YAML Facts:**


```yaml
task_description: Fill adjacent empty space based on the orientation of a colored shape relative to a unique marker pixel within it.

elements:
  - element: background
    color: white (0)
  - element: object
    description: Contiguous shape made of green pixels.
    color: green (3)
    contains:
      - element: marker
        color: red (2)
        count_per_object: 1
        role: Determines expansion characteristics.

properties:
  - object: marker (red pixel)
    property: adjacent_green_pixels
    value: Location of green pixels orthogonally touching the red pixel.
  - object: marker (red pixel)
    property: local_orientation
    value: Derived from adjacent_green_pixels (Horizontal or Vertical).
  - object: marker (red pixel)
    property: expansion_direction
    value: Derived from local_orientation and the color of the orthogonal neighbor not part of the adjacent_green_pixels (Up, Down, Left, or Right).

actions:
  - action: identify_objects
    inputs: [input_grid]
    outputs: [list_of_objects]
    description: Find all connected components of green and red pixels containing exactly one red pixel.
  - action: determine_expansion_direction
    inputs: [object, red_pixel_location]
    outputs: [direction]
    description: Based on the red pixel's immediate green neighbors and the color of the neighbor in the orthogonal direction. If horizontal green neighbors, check up/down for white; if vertical green neighbors, check left/right for white.
  - action: expand_object
    inputs: [object, direction, output_grid]
    outputs: [modified_output_grid]
    description: For each pixel in the object, fill white space in the specified direction with the pixel's color.

relationships:
  - type: containment
    from: object (green shape)
    to: marker (red pixel)
  - type: adjacency
    from: marker (red pixel)
    to: green pixels
    relation: Determines local_orientation.
  - type: adjacency
    from: marker (red pixel)
    to: white pixel (in non-green adjacent direction)
    relation: Determines specific expansion_direction (e.g., up vs down).
  - type: causation
    event: expansion
    cause: object properties (local_orientation, expansion_direction)
    effect: White pixels adjacent to the object in the expansion direction are recolored.

transformation_goal: For each object identified by a red marker, determine its expansion direction and fill the adjacent white space accordingly in the output grid.
```


**Natural Language Program:**

1.  Initialize the `output_grid` as a copy of the `input_grid`.
2.  Find all coordinates `(r, c)` where the pixel value is red (2) in the `input_grid`.
3.  For each found red pixel coordinate `(red_r, red_c)`:
    a.  Identify the full connected object containing `(red_r, red_c)`, consisting of the red pixel and all orthogonally connected green (3) pixels. Use a search algorithm (like BFS or DFS) starting from `(red_r, red_c)` and only traversing onto red (2) or green (3) pixels. Store all coordinates `(path_r, path_c)` belonging to this object.
    b.  Determine the primary orientation of green neighbors relative to the red pixel `(red_r, red_c)`:
        i.  Check if green pixels exist at `(red_r, red_c-1)` or `(red_r, red_c+1)`. If yes, the orientation is `horizontal`.
        ii. Check if green pixels exist at `(red_r-1, red_c)` or `(red_r+1, red_c)`. If yes, the orientation is `vertical`. (Assume only one orientation exists per object based on examples).
    c.  Determine the expansion direction based on the orientation and adjacent white space:
        i.  If orientation is `horizontal`:
            *   Check the pixel at `(red_r-1, red_c)`. If it is within grid bounds and is white (0) in the `input_grid`, the expansion direction is `Up`.
            *   Otherwise, check the pixel at `(red_r+1, red_c)`. If it is within grid bounds and is white (0), the expansion direction is `Down`.
        ii. If orientation is `vertical`:
            *   Check the pixel at `(red_r, red_c-1)`. If it is within grid bounds and is white (0) in the `input_grid`, the expansion direction is `Left`.
            *   Otherwise, check the pixel at `(red_r, red_c+1)`. If it is within grid bounds and is white (0), the expansion direction is `Right`.
    d.  Expand the object in the determined direction:
        i.  For each coordinate `(path_r, path_c)` in the identified object:
            *   Get the `original_color` (either 2 or 3) from the `input_grid` at `(path_r, path_c)`.
            *   Initialize `(curr_r, curr_c)` to the first cell adjacent to `(path_r, path_c)` in the expansion direction (e.g., `(path_r-1, path_c)` if direction is `Up`).
            *   While `(curr_r, curr_c)` is within the grid bounds AND the pixel at `(curr_r, curr_c)` in the `output_grid` is white (0):
                *   Set the pixel at `(curr_r, curr_c)` in the `output_grid` to `original_color`.
                *   Update `(curr_r, curr_c)` to the next cell in the expansion direction.
4.  Return the final `output_grid`.