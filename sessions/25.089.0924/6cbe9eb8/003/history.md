
## train_1

**input:**
```
0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1
1 8 8 8 8 8 8 8 8 8 8 8 1 2 3 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 4 4 4 4 4 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 4 4 4 4 4 4 3 0 6 6 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 6 6 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 2 3 0 1 2
0 8 8 8 8 8 8 8 8 8 8 8 0 1 2 3 0 1 2 3 0 1
1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```


## train_2

**input:**
```
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 4 4 1 2 0 1
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 8 8 4 4 2 0 1 2
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
0 1 2 0 1 3 3 3 3 3 3 3 3 3 8 6 6 6 8 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 8 8 8 8 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 3 3 3 3 3 3 3 3 3 3 3 0 1 2 0 1 2
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1
```


**output:**
```
3 3 3 3 3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 8 6 6 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3
```


## train_3

**input:**
```
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 3 3 3 3 3 3 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 4 4 4 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 3 3 3 3 3 3 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
```


**output:**
```
3 3 3 3 3 3 3 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 3 3 3 3 3 3 3
```

Okay, let's break down this task.

**Perception**

1.  **Input Structure:** The input grids are relatively large and contain a mix of elements:
    *   A repetitive background pattern using low-numbered colors (0, 1, 2, 3). This pattern fills most of the grid.
    *   A prominent, single-colored, hollow rectangular frame (thickness 1) embedded within the background. The frame color varies between examples (azure 8, green 3).
    *   Various smaller shapes or "objects" made of other distinct colors (yellow 4, gray 5, magenta 6, azure 8) located *inside* the rectangular frame. Some background pattern elements might also exist inside the frame.
2.  **Output Structure:** The output grid is smaller than the input. It consists of:
    *   A border matching the color of the frame identified in the input.
    *   An interior region corresponding to the area inside the input frame.
3.  **Transformation:** The core transformation involves:
    *   **Identifying the Frame:** Locating the single-colored rectangular frame in the input.
    *   **Extracting Content:** Focusing on the region *inside* this frame.
    *   **Filtering/Cleaning:** Replacing the pixels corresponding to the input's background pattern with white (0) within the extracted region.
    *   **Preserving Objects:** Keeping the pixels corresponding to the distinct shapes/objects found inside the input frame.
    *   **Constructing Output:** Building a new grid with the identified frame color as the border and the filtered/preserved content inside.

**YAML Facts**


```yaml
elements:
  - element: background_pattern
    description: A repeating pattern of low-value colors (e.g., white, blue, red, green) covering large areas of the input grid, primarily outside the main frame.
    properties:
      - repetitive
      - composed of low_value_colors (0, 1, 2, 3 in examples)
      - covers area outside the main frame
      - may also appear inside the main frame initially
  - element: frame
    description: A hollow rectangle, one pixel thick, made of a single non-white color. It encloses other objects and potentially some background pattern elements.
    properties:
      - rectangular_shape
      - hollow (interior exists)
      - thickness: 1 pixel
      - single_color (varies: azure, green in examples)
      - non_white
      - encloses_other_elements
  - element: inner_objects
    description: Contiguous shapes or blocks of pixels located spatially inside the 'frame'. Their colors are distinct from the frame color and typically distinct from the background pattern colors.
    properties:
      - located_inside_frame
      - colors_distinct_from_frame
      - colors_often_distinct_from_background (e.g., yellow, gray, magenta, azure)
      - contiguous

actions:
  - action: identify_frame
    description: Find the single-colored, non-white, 1-pixel thick, rectangular frame in the input grid. Determine its color and the bounding box of the area it encloses.
  - action: identify_background_colors
    description: Determine the set of colors present in the input grid region *outside* the identified frame's outer boundary. Include white (0) in this set.
  - action: extract_inner_content
    description: Select the portion of the input grid located strictly inside the identified frame.
  - action: filter_background
    description: Within the extracted inner content, replace any pixel whose color belongs to the identified background_colors set with white (0).
  - action: construct_output
    description: Create a new grid. Set its border (1 pixel thick) to the frame's color. Place the filtered inner content into the center of this new grid.

relationships:
  - relationship: containment
    description: The 'frame' contains the 'inner_objects' and some initial 'background_pattern' elements.
  - relationship: separation
    description: The 'frame' separates the inner content from the outer 'background_pattern'.
  - relationship: color_mapping
    description: Pixels inside the input frame are mapped to the output grid. Background pattern colors become white (0), while other object colors are preserved. The frame color defines the output border color.
```


**Natural Language Program**

1.  **Scan** the input grid to locate a rectangular, hollow frame that is exactly one pixel thick and composed of a single, non-white color. Let the color of this frame be `frame_color`. Identify the rectangular region strictly *inside* this frame.
2.  **Identify** the set of all unique pixel colors present in the input grid *outside* the bounding box of the found frame. Add white (0) to this set. Call this set `background_colors`.
3.  **Create** a new output grid whose dimensions are 2 plus the height and 2 plus the width of the inner region identified in step 1.
4.  **Draw** a border, one pixel thick, around the edge of the output grid using the `frame_color`.
5.  **Iterate** through each pixel `(r, c)` within the inner region of the input grid (identified in step 1). Let the color of this input pixel be `P`.
6.  **Determine** the corresponding position `(r_out, c_out)` in the output grid's interior (offset by +1 row, +1 column from the relative position within the inner region).
7.  **Check** if the input pixel color `P` is present in the `background_colors` set (identified in step 2).
8.  **If** `P` is in `background_colors`, set the pixel at `(r_out, c_out)` in the output grid to white (0).
9.  **Else** (if `P` is *not* in `background_colors`), set the pixel at `(r_out, c_out)` in the output grid to `P`.
10. **Output** the completed grid.
```python
import numpy as np
from typing import List, Tuple, Set, Optional

"""
Transformation Rule:

1. Identify a rectangular, hollow frame in the input grid that is exactly one pixel thick and composed of a single, non-white color. Record the frame's color and the bounding box of the region strictly inside it.
2. Determine the set of unique colors present in the input grid *outside* the identified frame's bounding box (including the frame pixels themselves). Add white (0) to this set; these are the 'background colors'.
3. Create a new output grid whose dimensions are sized to fit the inner region identified in step 1, plus a one-pixel border on all sides.
4. Fill the one-pixel border of the output grid with the frame's color identified in step 1.
5. Iterate through each pixel within the inner region of the input grid.
6. For each pixel, check if its color is in the set of 'background colors' identified in step 2.
7. If the pixel's color is a background color, place a white (0) pixel in the corresponding position within the output grid's interior.
8. Otherwise (if the pixel's color is not a background color), copy the pixel's original color to the corresponding position within the output grid's interior.
9. Return the constructed output grid.
"""

def find_frame(grid: np.ndarray) -> Optional[Tuple[int, int, int, int, int]]:
    """
    Finds a 1-pixel thick, single-color, non-white, hollow rectangular frame.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple (frame_color, inner_min_r, inner_min_c, inner_max_r, inner_max_c)
        representing the frame's color and the bounding box of the inner area,
        or None if no such frame is found.
    """
    rows, cols = grid.shape
    for color in range(1, 10):  # Iterate through possible frame colors (1-9)
        coords = np.argwhere(grid == color)
        if coords.size == 0:
            continue

        min_r, min_c = coords.min(axis=0)
        max_r, max_c = coords.max(axis=0)

        # Check if potential frame is at least 3x3 to be hollow
        if max_r - min_r < 2 or max_c - min_c < 2:
            continue

        is_frame = True
        # Check top and bottom border
        for c in range(min_c, max_c + 1):
            if grid[min_r, c] != color or grid[max_r, c] != color:
                is_frame = False
                break
            # Check thickness (inner)
            if grid[min_r + 1, c] == color or grid[max_r - 1, c] == color:
                 # Allow corners of inner objects to touch frame corners
                 if not ((c == min_c or c == max_c) and (grid[min_r+1, c] != color and grid[max_r-1, c] != color)):
                     # Check specifically if the inner adjacent pixel *is* the frame color
                     if grid[min_r + 1, c] == color or grid[max_r - 1, c] == color:
                         is_frame = False
                         break
            # Check thickness (outer) - if not on grid edge
            if min_r > 0 and grid[min_r - 1, c] == color:
                 is_frame = False; break
            if max_r < rows - 1 and grid[max_r + 1, c] == color:
                 is_frame = False; break
        if not is_frame: continue

        # Check left and right border (excluding corners already checked)
        for r in range(min_r + 1, max_r):
            if grid[r, min_c] != color or grid[r, max_c] != color:
                is_frame = False
                break
            # Check thickness (inner)
            if grid[r, min_c + 1] == color or grid[r, max_c - 1] == color:
                # Allow corners of inner objects to touch frame corners
                if not ((r == min_r or r == max_r) and (grid[r, min_c+1] != color and grid[r, max_c-1] != color)):
                     # Check specifically if the inner adjacent pixel *is* the frame color
                     if grid[r, min_c + 1] == color or grid[r, max_c - 1] == color:
                        is_frame = False
                        break
            # Check thickness (outer) - if not on grid edge
            if min_c > 0 and grid[r, min_c - 1] == color:
                 is_frame = False; break
            if max_c < cols - 1 and grid[r, max_c + 1] == color:
                 is_frame = False; break
        if not is_frame: continue

        # Final check: Ensure *no* pixels of frame_color exist *inside* the inner box
        inner_slice = grid[min_r + 1 : max_r, min_c + 1 : max_c]
        if np.any(inner_slice == color):
             # Check if the only interior pixels are due to objects touching corners
             interior_color_coords = np.argwhere(inner_slice == color)
             true_interior_pixels = False
             for r_in, c_in in interior_color_coords:
                 # Check if this pixel is truly interior or just a corner contact
                 # A corner contact would mean its neighbours inside the frame are NOT the frame color
                 is_corner_contact = False
                 # Check neighbours relative to the inner slice boundary
                 # Example: pixel at (min_r+1, min_c+1)
                 # check grid[min_r+1, min_c+2] and grid[min_r+2, min_c+1] etc.
                 # This check seems overly complex and might be wrong. Let's simplify:
                 # Assume if ANY frame color is inside, it's not a valid hollow frame for this problem's pattern.
                 is_frame = False # Simpler: If any frame color inside, reject.
                 break
        if not is_frame: continue


        # If all checks pass, we found our frame
        inner_min_r = min_r + 1
        inner_min_c = min_c + 1
        inner_max_r = max_r - 1
        inner_max_c = max_c - 1
        return color, inner_min_r, inner_min_c, inner_max_r, inner_max_c

    return None # No frame found


def get_background_colors(grid: np.ndarray, frame_min_r: int, frame_min_c: int, frame_max_r: int, frame_max_c: int) -> Set[int]:
    """
    Identifies colors outside the frame's bounding box.

    Args:
        grid: The input grid as a numpy array.
        frame_min_r, frame_min_c, frame_max_r, frame_max_c: Coordinates defining
            the outer bounding box of the frame itself.

    Returns:
        A set containing all unique colors found outside the frame, plus 0 (white).
    """
    rows, cols = grid.shape
    background_colors = set([0]) # Always include white

    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is outside the frame's outer bounding box
            if r < frame_min_r or r > frame_max_r or c < frame_min_c or c > frame_max_c:
                background_colors.add(grid[r, c])
    return background_colors

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
        Returns an empty list or raises an error if the frame cannot be found.
    """
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # 1. Scan to locate the frame and its inner region
    frame_info = find_frame(grid_np)
    if frame_info is None:
        # Handle error: No suitable frame found. Depending on ARC requirements,
        # maybe return input, empty grid, or raise error. Let's return input for now.
        print("Error: Could not find a valid frame.")
        return input_grid # Or potentially raise ValueError("No frame found")

    frame_color, inner_min_r, inner_min_c, inner_max_r, inner_max_c = frame_info
    frame_outer_min_r, frame_outer_min_c = inner_min_r - 1, inner_min_c - 1
    frame_outer_max_r, frame_outer_max_c = inner_max_r + 1, inner_max_c + 1


    # 2. Identify background colors (outside the frame)
    background_colors = get_background_colors(grid_np, frame_outer_min_r, frame_outer_min_c, frame_outer_max_r, frame_outer_max_c)

    # 3. Create the output grid
    inner_height = inner_max_r - inner_min_r + 1
    inner_width = inner_max_c - inner_min_c + 1
    output_height = inner_height + 2
    output_width = inner_width + 2
    # Initialize with white (0) - border will be overwritten
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    # 4. Draw the border with frame_color
    output_grid_np[0, :] = frame_color          # Top row
    output_grid_np[-1, :] = frame_color         # Bottom row
    output_grid_np[:, 0] = frame_color          # Left column
    output_grid_np[:, -1] = frame_color         # Right column

    # 5-9. Iterate through the inner region, filter, and place in output
    for r_in in range(inner_min_r, inner_max_r + 1):
        for c_in in range(inner_min_c, inner_max_c + 1):
            input_pixel_color = grid_np[r_in, c_in]

            # Calculate corresponding output coordinates (offset by 1 for the border)
            r_out = r_in - inner_min_r + 1
            c_out = c_in - inner_min_c + 1

            # Check if the input color is a background color
            if input_pixel_color in background_colors:
                output_grid_np[r_out, c_out] = 0 # Set to white
            else:
                output_grid_np[r_out, c_out] = input_pixel_color # Copy original color

    # 10. Return the completed grid as a list of lists
    return output_grid_np.tolist()
```

Previous Code:
```python
import numpy as np
from typing import List, Tuple, Set, Optional

"""
Transformation Rule:

1. Identify a rectangular, hollow frame in the input grid that is exactly one pixel thick and composed of a single, non-white color. Record the frame's color and the bounding box of the region strictly inside it.
2. Determine the set of unique colors present in the input grid *outside* the identified frame's bounding box (including the frame pixels themselves). Add white (0) to this set; these are the 'background colors'.
3. Create a new output grid whose dimensions are sized to fit the inner region identified in step 1, plus a one-pixel border on all sides.
4. Fill the one-pixel border of the output grid with the frame's color identified in step 1.
5. Iterate through each pixel within the inner region of the input grid.
6. For each pixel, check if its color is in the set of 'background colors' identified in step 2.
7. If the pixel's color is a background color, place a white (0) pixel in the corresponding position within the output grid's interior.
8. Otherwise (if the pixel's color is not a background color), copy the pixel's original color to the corresponding position within the output grid's interior.
9. Return the constructed output grid.
"""

def find_frame(grid: np.ndarray) -> Optional[Tuple[int, int, int, int, int]]:
    """
    Finds a 1-pixel thick, single-color, non-white, hollow rectangular frame.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple (frame_color, inner_min_r, inner_min_c, inner_max_r, inner_max_c)
        representing the frame's color and the bounding box of the inner area,
        or None if no such frame is found.
    """
    rows, cols = grid.shape
    for color in range(1, 10):  # Iterate through possible frame colors (1-9)
        coords = np.argwhere(grid == color)
        if coords.size == 0:
            continue

        min_r, min_c = coords.min(axis=0)
        max_r, max_c = coords.max(axis=0)

        # Check if potential frame is at least 3x3 to be hollow
        if max_r - min_r < 2 or max_c - min_c < 2:
            continue

        is_frame = True
        # Check top and bottom border
        for c in range(min_c, max_c + 1):
            if grid[min_r, c] != color or grid[max_r, c] != color:
                is_frame = False
                break
            # Check thickness (inner)
            if grid[min_r + 1, c] == color or grid[max_r - 1, c] == color:
                 # Allow corners of inner objects to touch frame corners
                 if not ((c == min_c or c == max_c) and (grid[min_r+1, c] != color and grid[max_r-1, c] != color)):
                     # Check specifically if the inner adjacent pixel *is* the frame color
                     if grid[min_r + 1, c] == color or grid[max_r - 1, c] == color:
                         is_frame = False
                         break
            # Check thickness (outer) - if not on grid edge
            if min_r > 0 and grid[min_r - 1, c] == color:
                 is_frame = False; break
            if max_r < rows - 1 and grid[max_r + 1, c] == color:
                 is_frame = False; break
        if not is_frame: continue

        # Check left and right border (excluding corners already checked)
        for r in range(min_r + 1, max_r):
            if grid[r, min_c] != color or grid[r, max_c] != color:
                is_frame = False
                break
            # Check thickness (inner)
            if grid[r, min_c + 1] == color or grid[r, max_c - 1] == color:
                # Allow corners of inner objects to touch frame corners
                if not ((r == min_r or r == max_r) and (grid[r, min_c+1] != color and grid[r, max_c-1] != color)):
                     # Check specifically if the inner adjacent pixel *is* the frame color
                     if grid[r, min_c + 1] == color or grid[r, max_c - 1] == color:
                        is_frame = False
                        break
            # Check thickness (outer) - if not on grid edge
            if min_c > 0 and grid[r, min_c - 1] == color:
                 is_frame = False; break
            if max_c < cols - 1 and grid[r, max_c + 1] == color:
                 is_frame = False; break
        if not is_frame: continue

        # Final check: Ensure *no* pixels of frame_color exist *inside* the inner box
        inner_slice = grid[min_r + 1 : max_r, min_c + 1 : max_c]
        if np.any(inner_slice == color):
             # Check if the only interior pixels are due to objects touching corners
             interior_color_coords = np.argwhere(inner_slice == color)
             true_interior_pixels = False
             for r_in, c_in in interior_color_coords:
                 # Check if this pixel is truly interior or just a corner contact
                 # A corner contact would mean its neighbours inside the frame are NOT the frame color
                 is_corner_contact = False
                 # Check neighbours relative to the inner slice boundary
                 # Example: pixel at (min_r+1, min_c+1)
                 # check grid[min_r+1, min_c+2] and grid[min_r+2, min_c+1] etc.
                 # This check seems overly complex and might be wrong. Let's simplify:
                 # Assume if ANY frame color is inside, it's not a valid hollow frame for this problem's pattern.
                 is_frame = False # Simpler: If any frame color inside, reject.
                 break
        if not is_frame: continue


        # If all checks pass, we found our frame
        inner_min_r = min_r + 1
        inner_min_c = min_c + 1
        inner_max_r = max_r - 1
        inner_max_c = max_c - 1
        return color, inner_min_r, inner_min_c, inner_max_r, inner_max_c

    return None # No frame found


def get_background_colors(grid: np.ndarray, frame_min_r: int, frame_min_c: int, frame_max_r: int, frame_max_c: int) -> Set[int]:
    """
    Identifies colors outside the frame's bounding box.

    Args:
        grid: The input grid as a numpy array.
        frame_min_r, frame_min_c, frame_max_r, frame_max_c: Coordinates defining
            the outer bounding box of the frame itself.

    Returns:
        A set containing all unique colors found outside the frame, plus 0 (white).
    """
    rows, cols = grid.shape
    background_colors = set([0]) # Always include white

    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is outside the frame's outer bounding box
            if r < frame_min_r or r > frame_max_r or c < frame_min_c or c > frame_max_c:
                background_colors.add(grid[r, c])
    return background_colors

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
        Returns an empty list or raises an error if the frame cannot be found.
    """
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # 1. Scan to locate the frame and its inner region
    frame_info = find_frame(grid_np)
    if frame_info is None:
        # Handle error: No suitable frame found. Depending on ARC requirements,
        # maybe return input, empty grid, or raise error. Let's return input for now.
        print("Error: Could not find a valid frame.")
        return input_grid # Or potentially raise ValueError("No frame found")

    frame_color, inner_min_r, inner_min_c, inner_max_r, inner_max_c = frame_info
    frame_outer_min_r, frame_outer_min_c = inner_min_r - 1, inner_min_c - 1
    frame_outer_max_r, frame_outer_max_c = inner_max_r + 1, inner_max_c + 1


    # 2. Identify background colors (outside the frame)
    background_colors = get_background_colors(grid_np, frame_outer_min_r, frame_outer_min_c, frame_outer_max_r, frame_outer_max_c)

    # 3. Create the output grid
    inner_height = inner_max_r - inner_min_r + 1
    inner_width = inner_max_c - inner_min_c + 1
    output_height = inner_height + 2
    output_width = inner_width + 2
    # Initialize with white (0) - border will be overwritten
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    # 4. Draw the border with frame_color
    output_grid_np[0, :] = frame_color          # Top row
    output_grid_np[-1, :] = frame_color         # Bottom row
    output_grid_np[:, 0] = frame_color          # Left column
    output_grid_np[:, -1] = frame_color         # Right column

    # 5-9. Iterate through the inner region, filter, and place in output
    for r_in in range(inner_min_r, inner_max_r + 1):
        for c_in in range(inner_min_c, inner_max_c + 1):
            input_pixel_color = grid_np[r_in, c_in]

            # Calculate corresponding output coordinates (offset by 1 for the border)
            r_out = r_in - inner_min_r + 1
            c_out = c_in - inner_min_c + 1

            # Check if the input color is a background color
            if input_pixel_color in background_colors:
                output_grid_np[r_out, c_out] = 0 # Set to white
            else:
                output_grid_np[r_out, c_out] = input_pixel_color # Copy original color

    # 10. Return the completed grid as a list of lists
    return output_grid_np.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1
1 8 8 8 8 8 8 8 8 8 8 8 1 2 3 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 4 4 4 4 4 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 4 4 4 4 4 4 3 0 6 6 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 6 6 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 2 3 0 1 2
0 8 8 8 8 8 8 8 8 8 8 8 0 1 2 3 0 1 2 3 0 1
1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1
1 8 8 8 8 8 8 8 8 8 8 8 1 2 3 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 4 4 4 4 4 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 4 4 4 4 4 4 3 0 6 6 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 6 6 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 2 3 0 1 2
0 8 8 8 8 8 8 8 8 8 8 8 0 1 2 3 0 1 2 3 0 1
1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: False
Color Count Correct: False
Score: None

## Example 2:
Input:
```
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 4 4 1 2 0 1
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 8 8 4 4 2 0 1 2
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
0 1 2 0 1 3 3 3 3 3 3 3 3 3 8 6 6 6 8 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 8 8 8 8 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 3 3 3 3 3 3 3 3 3 3 3 0 1 2 0 1 2
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 8 6 6 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 4 4 1 2 0 1
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 8 8 4 4 2 0 1 2
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
0 1 2 0 1 3 3 3 3 3 3 3 3 3 8 6 6 6 8 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 8 8 8 8 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 3 3 3 3 3 3 3 3 3 3 3 0 1 2 0 1 2
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: False
Color Count Correct: False
Score: None

## Example 3:
Input:
```
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 3 3 3 3 3 3 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 4 4 4 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 3 3 3 3 3 3 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
```
Expected Output:
```
3 3 3 3 3 3 3 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 3 3 3 3 3 3 3
```
Transformed Output:
```
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 3 3 3 3 3 3 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 4 4 4 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 3 3 3 3 3 3 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: False
Color Count Correct: False
Score: None
**General Assessment**

The previous code consistently failed because the `find_frame` function did not correctly identify the target rectangular frame in any of the training examples. It returned the original input grid as a fallback, indicating the core frame detection logic was flawed. The primary issues likely stem from overly strict checks for frame thickness (ensuring no adjacent pixels inside or outside share the frame color) and potentially misinterpreting how objects inside the frame might touch or interact with the frame boundary, or how the frame color itself might appear inside the frame as part of the initial background pattern.

The strategy is to:
1.  Relax or refine the frame detection logic (`find_frame`) to correctly identify the 1-pixel thick, single-colored rectangular boundary, even if objects touch it or if the frame color appears elsewhere in the grid initially.
2.  Ensure the background color identification logic correctly samples only from *outside* the identified frame.
3.  Verify the filtering process correctly removes background colors from the extracted inner region.

**Metrics and Analysis**

Let's re-examine the examples to refine assumptions, focusing on frame details and background colors.

*   **Example 1:**
    *   Input Shape: 14x22
    *   Output Shape: 12x11
    *   Expected Frame Color: 8 (azure)
    *   Expected Frame Outer Bounds (min_r, min_c, max_r, max_c): (1, 1, 12, 11)
    *   Expected Inner Bounds (min_r, min_c, max_r, max_c): (2, 2, 11, 10)
    *   Colors Strictly *Outside* Frame Bounds (r<1, r>12, c<1, c>11): {0, 1, 2, 3} -> `background_colors` = {0, 1, 2, 3}
    *   Colors *Inside* Inner Bounds (before filtering): {0, 1, 2, 3, 4, 5, 6, 8}. Note the '8' (azure) appears inside.
    *   Colors in Output Interior: {0, 4, 5, 6} (background {1, 2, 3, 8} inside were replaced by 0)

*   **Example 2:**
    *   Input Shape: 13x22
    *   Output Shape: 9x12
    *   Expected Frame Color: 3 (green)
    *   Expected Frame Outer Bounds: (3, 5, 11, 16)
    *   Expected Inner Bounds: (4, 6, 10, 15)
    *   Colors Strictly *Outside* Frame Bounds (r<3, r>11, c<5, c>16): {0, 1, 2, 4} -> `background_colors` = {0, 1, 2, 4}
    *   Colors *Inside* Inner Bounds (before filtering): {0, 1, 2, 3, 4, 6, 8}. Note the '3' (green) appears inside.
    *   Colors in Output Interior: {0, 4, 6, 8} (background {1, 2, 3, 4} inside were replaced by 0. *Wait*, yellow 4 is *not* background here, it's only background because it appears outside the frame. The yellow 4s inside the frame are preserved.) Let's re-evaluate background: Colors outside are {0, 1, 2}. -> `background_colors` = {0, 1, 2}. Yellow (4) is *not* background. Okay, re-analyzing output: {0, 4, 6, 8}. Colors {1, 2, 3} inside were replaced by 0. Yellow 4 was *preserved*. This confirms background colors are determined *only* from outside.

*   **Example 3:**
    *   Input Shape: 16x23
    *   Output Shape: 8x8
    *   Expected Frame Color: 3 (green)
    *   Expected Frame Outer Bounds: (1, 2, 8, 9)
    *   Expected Inner Bounds: (2, 3, 7, 8)
    *   Colors Strictly *Outside* Frame Bounds (r<1, r>8, c<2, c>9): {0, 1, 4} -> `background_colors` = {0, 1, 4}
    *   Colors *Inside* Inner Bounds (before filtering): {8}. (The 4s are outside the *inner* bounds).
    *   Let's recheck: The yellow 4s *are* inside the green frame (frame is at r=1..8, c=2..9). The inner region is r=2..7, c=3..8. Yes, yellow 4s are inside at r=4,5,6 c=12,13,14... wait, the coordinates seem off in the initial analysis. Let's find the frame visually in example 3.
        *   Green (3) frame seems to be: rows 1 to 8, columns 2 to 9.
        *   Inner area: rows 2 to 7, columns 3 to 8.
        *   Colors outside this frame (rows < 1 or > 8, columns < 2 or > 9): {0, 1, 4}. -> `background_colors` = {0, 1, 4}.
        *   Colors inside inner area (rows 2-7, cols 3-8): {8}.
        *   Output interior contains: {4, 8}. Background {0, 1} inside were replaced by 0 (but none were present). Yellow 4 was *not* replaced. This confirms the `background_colors` are {0, 1}. The yellow (4) that appears outside the frame (at r=4,5,6 c=12,13,14) makes {4} part of the *potential* background set, but since the yellow inside wasn't filtered, it implies the filtering rule is more specific.

**Revised Hypothesis:** The background colors used for filtering are *only* those colors present both *outside* the frame AND *inside* the frame before filtering. White (0) is always treated as background.

Let's test this revised hypothesis:
*   **Example 1:** Outside {0, 1, 2, 3}. Inside {0, 1, 2, 3, 4, 5, 6, 8}. Intersection {0, 1, 2, 3}. Plus 0 -> Filter Set {0, 1, 2, 3}. Output Interior {0, 4, 5, 6}. Looks correct (8 was inside but not outside, so not filtered). *Wait*, 8 *was* filtered. The output interior doesn't contain 8. Why? Let's look at the output again. Oh, the output *does* contain 8, but only as the border. The interior contains {0, 4, 5, 6}. Why was 8 filtered? It wasn't outside. Why were 1, 2, 3 filtered? They were outside and inside.
*   **Example 2:** Outside {0, 1, 2}. Inside {0, 1, 2, 3, 4, 6, 8}. Intersection {0, 1, 2}. Plus 0 -> Filter Set {0, 1, 2}. Output Interior {0, 3, 4, 6, 8}. Looks correct (3, 4, 6, 8 were inside but not outside, so preserved).
*   **Example 3:** Outside {0, 1, 4}. Inside {8}. Intersection {}. Plus 0 -> Filter Set {0}. Output Interior {4, 8}. Looks correct (8 was inside only, 4 was outside only, neither filtered based on intersection). *Wait*, the output has 4s. Where did they come from? Ah, the yellow 4s *are* inside the frame in the input! Input at (4, 12) is 4. Frame is (1..8, 2..9). So (4, 12) is *outside*. Okay, let's find the *actual* yellow 4s inside the frame. Input (4, 12), (5, 12), (6, 12), (4, 13), (5, 13), (6, 13), (4, 14), (5, 14), (6, 14). Are these inside the frame (1..8, 2..9)? No. Where are the yellow 4s in the *output*? Output is 8x8. Output interior is (1..6, 1..6). Yellow 4s are at output (4, 1), (4, 2), (4, 3), (5, 1)... etc. These correspond to input positions (relative to inner frame start 2, 3): (4+2-1, 1+3-1) = (5, 3), (5, 4), (5, 5), etc. Let's check input[5, 3], input[5, 4], input[5, 5]. They are 8, 8, 8. This is confusing.

Let's restart the analysis of Example 3 Input/Output simply:
Input Frame: Green (3), rows 1-8, cols 2-9. Outer bounds (1, 2) to (8, 9).
Input Inner Region: rows 2-7, cols 3-8. Contains only Azure (8).
Input Outer Region: Contains White (0), Blue (1), Green (3), Yellow (4). Background Colors = {0, 1, 4}.
Output Frame: Green (3), 8x8. Output Inner region rows 1-6, cols 1-6.
Expected Output Interior: Based on Input Inner Region {8} and Background {0, 1, 4}, we expect only {8} with {0} replacing any {0, 1, 4} if they were present inside.
Actual Output Interior: Contains Azure (8) AND Yellow (4).

Where could the Yellow (4) come from? It exists *outside* the Green (3) frame in the input. It seems like there are *two* distinct objects defined by frames in Example 3: a Green (3) frame and a Yellow (4) frame/object.
Green Frame: (1, 2) to (8, 9). Contains Azure (8).
Yellow Object/Frame?: (4, 12) to (6, 14). Contains only Yellow (4).

The output combines these. It takes the Green frame as the *outer* boundary. It takes the content of the Green frame (Azure 8) and overlays or combines it with the Yellow object. How is the Yellow object positioned?
Yellow object input bounds: (4, 12) to (6, 14). Size 3x3.
Output grid size: 8x8. Inner area 6x6.
Yellow object output position: rows 4-6, cols 1-3 (relative to inner area 1,1).
Mapping input (4, 12) to output (4, 1)? Doesn't seem direct.

Let's reconsider the simplest explanation:
1. Find the single-color, 1-pixel thick, rectangular frame (e.g., Green 3 in Ex 3).
2. Identify background colors from *outside* this frame ({0, 1, 4} in Ex 3).
3. Extract the *entire* content inside the frame ({8} in Ex 3).
4. Filter this content, replacing background colors with white 0 (No change in Ex 3 inner content).
5. Create the output grid with the frame border.
6. Place the filtered content.
7. **Overlay/Stamp:** Find *other* significant non-background objects *anywhere* in the input grid. If their bounding box *overlaps* with the main frame's inner bounding box, copy those objects into the output grid relative to the output frame, preserving their colors.

Testing the Overlay Hypothesis:
*   **Example 1:** Frame 8. Background {0, 1, 2, 3}. Inner {0, 1, 2, 3, 4, 5, 6, 8}. Filtered Inner {0, 4, 5, 6}. Are there other significant objects outside? The background pattern is not significant. Output matches filtered inner content. No overlay needed.
*   **Example 2:** Frame 3. Background {0, 1, 2}. Inner {0, 1, 2, 3, 4, 6, 8}. Filtered Inner {0, 3, 4, 6, 8}. Output matches. No overlay needed.
*   **Example 3:** Frame 3. Background {0, 1, 4}. Inner {8}. Filtered Inner {8}. Significant object: Yellow 4 block at (4, 12) to (6, 14). Does its bounding box overlap the inner frame region (2..7, 3..8)? No. This hypothesis fails.

What if the "background" colors are simply the most frequent colors outside the frame?
*   Ex 1: Outside colors {0, 1, 2, 3}. All frequent. Background {0, 1, 2, 3}. Seems same.
*   Ex 2: Outside colors {0, 1, 2, 4}. Frequencies: 0, 1, 2 are high, 4 is low (only 4 pixels). Background {0, 1, 2}. Matches.
*   Ex 3: Outside colors {0, 1, 3, 4}. Frequencies: 0, 1 are high, 3 is only frame, 4 is low (9 pixels). Background {0, 1}. Matches.

**Revised Background Rule:** Background colors are white (0) plus any color C such that C appears *outside* the frame's outer bounding box AND C is one of the N most frequent colors in the entire input grid (excluding the frame color, maybe N=2 or N=3?). Or perhaps simpler: Background colors = {0} + {colors appearing outside frame} - {colors forming significant objects inside frame}? This seems circular.

Let's stick to the frequency idea: Background = {0} + {most frequent colors appearing outside the frame}. How many? Maybe frequency > threshold?


*code_execution:*
```python
import numpy as np
from collections import Counter

def analyze_example(grid_list, frame_bounds):
    grid = np.array(grid_list)
    rows, cols = grid.shape
    frame_min_r, frame_min_c, frame_max_r, frame_max_c = frame_bounds

    outside_colors = []
    inside_colors = []
    all_colors = []

    frame_color = grid[frame_min_r, frame_min_c] # Assume top-left pixel is frame color

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            all_colors.append(color)
            if r < frame_min_r or r > frame_max_r or c < frame_min_c or c > frame_max_c:
                outside_colors.append(color)
            elif r > frame_min_r and r < frame_max_r and c > frame_min_c and c < frame_max_c:
                 inside_colors.append(color)

    outside_counts = Counter(outside_colors)
    inside_counts = Counter(inside_colors)
    all_counts = Counter(all_colors)

    print(f"Frame Color: {frame_color}")
    print(f"Outside Colors: {sorted(outside_counts.items())}")
    print(f"Inside Colors (initial): {sorted(inside_counts.items())}")
    print(f"All Colors: {sorted(all_counts.items())}")
    # Determine potential background based on frequency outside (excluding frame color)
    potential_bg = {0} # Always include 0
    # Heuristic: Add colors outside if they are frequent enough (e.g., > 10% of outside pixels?)
    # Or maybe just the top 2 most frequent non-zero outside colors?
    sorted_outside = sorted([item for item in outside_counts.items() if item[0] != 0 and item[0] != frame_color], key=lambda x: x[1], reverse=True)
    print(f"Sorted Non-Zero Outside (excluding frame): {sorted_outside}")
    # Let's try adding the top 2
    limit = 2
    for i in range(min(limit, len(sorted_outside))):
        potential_bg.add(sorted_outside[i][0])

    print(f"Potential Background Colors: {potential_bg}")


# Example 1
grid1 = [[0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1], [1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2], [0, 8, 2, 3, 0, 1, 2, 3, 0, 1, 2, 8, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1], [1, 8, 3, 0, 1, 2, 3, 0, 4, 4, 4, 4, 4, 4, 4, 0, 1, 2, 3, 0, 1, 2], [0, 8, 2, 3, 0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 0, 1, 2, 3, 0, 1], [1, 8, 3, 0, 1, 2, 3, 0, 4, 5, 5, 5, 5, 5, 4, 0, 1, 2, 3, 0, 1, 2], [0, 8, 2, 3, 0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 0, 1, 2, 3, 0, 1], [1, 8, 3, 0, 1, 2, 3, 0, 4, 5, 5, 5, 5, 5, 4, 0, 1, 2, 3, 0, 1, 2], [0, 8, 2, 3, 0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 0, 6, 6, 3, 0, 1], [1, 8, 3, 0, 1, 2, 3, 0, 1, 2, 3, 8, 1, 2, 3, 0, 1, 6, 6, 0, 1, 2], [0, 8, 2, 3, 0, 1, 2, 3, 0, 1, 2, 8, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1], [1, 8, 3, 0, 1, 2, 3, 0, 1, 2, 3, 8, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2], [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1], [1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2]]
frame1_bounds = (1, 1, 12, 11) # Outer bounds of frame pixels
print("--- Example 1 ---")
analyze_example(grid1, frame1_bounds)

# Example 2
grid2 = [[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 4, 4, 1, 2, 0, 1], [1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 8, 8, 8, 4, 4, 2, 0, 1, 2], [1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 8, 6, 6, 6, 8, 2, 0, 1, 2], [0, 1, 2, 0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 6, 6, 6, 8, 1, 2, 0, 1], [1, 2, 0, 1, 2, 3, 1, 2, 0, 1, 2, 0, 1, 2, 8, 6, 6, 6, 8, 2, 0, 1, 2], [1, 2, 0, 1, 2, 3, 1, 2, 0, 1, 2, 0, 1, 2, 8, 8, 8, 8, 8, 2, 0, 1, 2], [0, 1, 2, 0, 1, 3, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 3, 2, 0, 1, 2, 0, 1], [1, 2, 0, 1, 2, 3, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 3, 0, 1, 2, 0, 1, 2], [1, 2, 0, 1, 2, 3, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 3, 0, 1, 2, 0, 1, 2], [0, 1, 2, 0, 1, 3, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 3, 2, 0, 1, 2, 0, 1], [1, 2, 0, 1, 2, 3, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 3, 0, 1, 2, 0, 1, 2], [1, 2, 0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 1, 2, 0, 1, 2], [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1]]
frame2_bounds = (3, 5, 11, 16) # Outer bounds of frame pixels
print("\n--- Example 2 ---")
analyze_example(grid2, frame2_bounds)

# Example 3
grid3 = [[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 3, 8, 8, 8, 8, 8, 8, 3, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 3, 8, 8, 8, 8, 8, 8, 3, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 3, 8, 8, 8, 8, 8, 8, 3, 0, 1, 4, 4, 4, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 3, 8, 8, 8, 8, 8, 8, 3, 1, 0, 4, 4, 4, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 3, 8, 8, 8, 8, 8, 8, 3, 0, 1, 4, 4, 4, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 3, 8, 8, 8, 8, 8, 8, 3, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 3, 3, 3, 3, 3, 3, 3, 3, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]]
frame3_bounds = (1, 2, 8, 9) # Outer bounds of frame pixels
print("\n--- Example 3 ---")
analyze_example(grid3, frame3_bounds)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 ---
Frame Color: 8
Outside Colors: [(np.int64(0), 44), (np.int64(1), 47), (np.int64(2), 33), (np.int64(3), 30), (np.int64(4), 10), (np.int64(5), 8), (np.int64(6), 4)]
Inside Colors (initial): [(np.int64(0), 17), (np.int64(1), 14), (np.int64(2), 19), (np.int64(3), 22), (np.int64(4), 10), (np.int64(5), 8)]
All Colors: [(np.int64(0), 61), (np.int64(1), 61), (np.int64(2), 52), (np.int64(3), 52), (np.int64(4), 22), (np.int64(5), 20), (np.int64(6), 4), (np.int64(8), 36)]
Sorted Non-Zero Outside (excluding frame): [(np.int64(1), 47), (np.int64(2), 33), (np.int64(3), 30), (np.int64(4), 10), (np.int64(5), 8), (np.int64(6), 4)]
Potential Background Colors: {0, np.int64(1), np.int64(2)}

--- Example 2 ---
Frame Color: 3
Outside Colors: [(np.int64(0), 52), (np.int64(1), 62), (np.int64(2), 59), (np.int64(4), 4), (np.int64(6), 5), (np.int64(8), 9)]
Inside Colors (initial): [(np.int64(0), 21), (np.int64(1), 24), (np.int64(2), 21), (np.int64(6), 1), (np.int64(8), 3)]
All Colors: [(np.int64(0), 73), (np.int64(1), 86), (np.int64(2), 80), (np.int64(3), 33), (np.int64(4), 4), (np.int64(6), 9), (np.int64(8), 14)]
Sorted Non-Zero Outside (excluding frame): [(np.int64(1), 62), (np.int64(2), 59), (np.int64(8), 9), (np.int64(6), 5), (np.int64(4), 4)]
Potential Background Colors: {0, np.int64(1), np.int64(2)}

--- Example 3 ---
Frame Color: 3
Outside Colors: [(np.int64(0), 147), (np.int64(1), 148), (np.int64(4), 9)]
Inside Colors (initial): [(np.int64(8), 36)]
All Colors: [(np.int64(0), 147), (np.int64(1), 148), (np.int64(3), 28), (np.int64(4), 9), (np.int64(8), 36)]
Sorted Non-Zero Outside (excluding frame): [(np.int64(1), 148), (np.int64(4), 9)]
Potential Background Colors: {0, np.int64(1), np.int64(4)}

```
**Analysis of Frequency Data:**

The frequency analysis supports the idea that "background" colors are the most frequent ones found outside the frame.

*   **Example 1:** Outside top 2 non-zero (excluding frame 8) are 1 (blue) and 2 (red). Adding 0 gives {0, 1, 2}. Actual filtered colors were {1, 2, 3}. This heuristic (top 2) misses green (3).
*   **Example 2:** Outside top 2 non-zero (excluding frame 3) are 1 (blue) and 2 (red). Adding 0 gives {0, 1, 2}. Actual filtered colors were {1, 2}. This heuristic works.
*   **Example 3:** Outside top 2 non-zero (excluding frame 3) are 1 (blue) and 4 (yellow). Adding 0 gives {0, 1, 4}. Actual filtered colors were {}. This heuristic doesn't match, as nothing was filtered.

Let's reconsider the *simplest* definition of background colors that fits the outputs:
**Background Colors = {0} U {Set of all colors appearing anywhere outside the frame's outer bounding box}**

Let's test this definition:
*   **Example 1:** Outside colors = {0, 1, 2, 3, 4, 5, 6}. Background = {0, 1, 2, 3, 4, 5, 6}. Filtered colors inside = {1, 2, 3}. Output interior = {0, 4, 5, 6}. This definition means 4, 5, 6 should *also* be filtered, but they are not. Fails.
*   **Example 2:** Outside colors = {0, 1, 2, 4, 6, 8}. Background = {0, 1, 2, 4, 6, 8}. Filtered colors inside = {1, 2}. Output interior = {0, 3, 4, 6, 8}. This definition means 4, 6, 8 should also be filtered. Fails.
*   **Example 3:** Outside colors = {0, 1, 4}. Background = {0, 1, 4}. Filtered colors inside = {}. Output interior = {4, 8}. This definition predicts the correct filtering (none). However, it doesn't explain where the '4' in the output came from, as it wasn't inside the *frame's* inner region.

**Revisiting Example 3 Output Origin:**
The output *must* be constructed from the contents found *within* the input frame.
Input Frame: Green (3) at (1..8, 2..9).
Input Inner Region: (2..7, 3..8).
Content of Input Inner Region: Azure (8) only.
Content of Output Inner Region: Azure (8) and Yellow (4).

This discrepancy is the key. Is it possible the frame identified is wrong for Example 3? Are the Yellow 4s *also* considered inside the frame?
If the frame is Green(3), the Yellow(4) block at (4..6, 12..14) is definitely outside.
What if the rule is:
1. Find the frame.
2. Identify background colors (using a consistent rule, maybe frequency outside?).
3. Create output grid with frame border.
4. Copy *all* non-background pixels from *inside* the input frame to the output grid interior.
5. Copy *all* non-background pixels from *outside* the input frame to the output grid interior, placing them relative to the frame center or some anchor? This seems overly complex.

Let's assume the frame finding and background filtering (`{0, 1, 2}` for Ex 2, `{0, 1, 4}` for Ex 3) is mostly correct, but the content selection is wrong.

**Final Hypothesis:**
1.  Find the single-colored, 1-pixel thick, non-white rectangular frame. Record its color (`frame_color`) and inner bounding box (`inner_box`).
2.  Determine the set of `background_colors`. Let's use the simple definition for now: `background_colors` = {0} U {all colors appearing outside the frame's outer bounding box}.
3.  Create the output grid, sized based on `inner_box`, with a 1-pixel border of `frame_color`.
4.  Iterate through all pixels `(r, c)` within the `inner_box` of the input grid.
5.  If `input[r, c]` is NOT in `background_colors`, copy `input[r, c]` to the corresponding position in the output grid's interior.
6.  If `input[r, c]` IS in `background_colors`, place white (0) in the corresponding position in the output grid's interior.

Let's re-test this final hypothesis:
*   **Example 1:** Frame 8. Background {0, 1, 2, 3, 4, 5, 6}. Inner content {0, 1, 2, 3, 4, 5, 6, 8}. Pixels to keep (not background): {8}. Output interior should be all {0} except where input was {8}? The actual output interior is {0, 4, 5, 6}. This hypothesis FAILS BADLY. The background definition must be wrong.

**Back to Basics: What is preserved?**
*   Ex 1: Preserved {4, 5, 6}. Filtered {1, 2, 3, 8}. Background candidates outside: {0, 1, 2, 3, 4, 5, 6}.
*   Ex 2: Preserved {3, 4, 6, 8}. Filtered {1, 2}. Background candidates outside: {0, 1, 2, 4, 6, 8}.
*   Ex 3: Preserved {8, 4}. Filtered {}. Background candidates outside: {0, 1, 4}. (Note: The preserved '4' must come from inside the frame, my previous analysis of inner content was wrong).

Let's re-examine Ex 3 inner content: Frame (1..8, 2..9). Inner (2..7, 3..8). Input pixels in this region are *all* 8. Where does the output '4' come from? It MUST be that the Yellow object outside the green frame is somehow copied in.

**Okay, one more try - Combining Frame Content and External Objects:**
1. Find the main frame (color `C_frame`, inner box `B_inner`).
2. Determine background colors `BG_colors` (e.g., {0} + common colors outside frame: {0,1,2,3} in E1, {0,1,2} in E2, {0,1} in E3).
3. Create output grid based on `B_inner` with `C_frame` border, interior initially white (0).
4. **Copy filtered frame contents:** Iterate through `B_inner` in the input. If `input[r,c]` is not in `BG_colors`, place `input[r,c]` at the corresponding output interior location.
5. **Copy significant external objects:** Find all contiguous objects outside the frame. For each object, if its color is *not* `C_frame` and not in `BG_colors`, copy this object into the output grid interior, maintaining its shape and relative position *if its bounding box overlaps with B_inner*? No, overlap didn't work for E3. What if we just copy *all* non-background, non-frame-color objects into the output, positioned relative to the frame?

This seems too complex. Let's simplify the background idea again.

**What if Background = {0, 1, 2, 3}?**
*   Ex 1: BG = {0,1,2,3}. Frame 8. Inside {0,1,2,3,4,5,6,8}. Keep {4,5,6,8}. Output has {4,5,6}. Why is 8 removed? Maybe Frame Color is always removed from inside?
*   Ex 2: BG = {0,1,2,3}. Frame 3. Inside {0,1,2,3,4,6,8}. Keep {4,6,8}. Output has {3,4,6,8}. Why is 3 kept? Maybe Frame Color is *not* removed if it's Frame 3? This smells arbitrary.
*   Ex 3: BG = {0,1,2,3}. Frame 3. Inside {8}. Keep {8}. Output has {4,8}. Where does 4 come from?

**Possibility: The background pattern itself is identified and removed.**
The background is often a repeating 2x2 or simple sequence (0,1,2,3,... or 0,1,0,1,...).
1. Identify the frame (color `C_frame`, inner box `B_inner`).
2. Identify the background pattern `P_bg` based on the area outside the frame.
3. Create output grid based on `B_inner` with `C_frame` border.
4. Fill the output interior by iterating through `B_inner`. At each position `(r, c)` in the input's `B_inner`, check if `input[r, c]` matches the expected background pattern `P_bg` at that location (potentially offset).
5. If `input[r, c]` matches `P_bg`, place white (0) in the output.
6. Otherwise, copy `input[r, c]` to the output.

This seems promising as it directly addresses the pattern removal.
*   Ex 1: Background pattern 0,1,2,3 repeating. Frame 8. Inside contains this pattern plus objects 4, 5, 6, and some 8s. Removing the pattern leaves 4, 5, 6, 8. If frame color is also removed -> {4, 5, 6}. Matches!
*   Ex 2: Background pattern 0,1,2 repeating. Frame 3. Inside contains this pattern plus objects 4, 6, 8, and some 3s. Removing the pattern leaves {3, 4, 6, 8}. Frame color 3 is *not* removed. Matches!
*   Ex 3: Background pattern 0,1 repeating. Frame 3. Inside contains only object 8. Removing the pattern (if 0 or 1 were present) leaves {8}. Frame color 3 is not removed (not present inside). Output has {4, 8}. Still doesn't explain the 4.

**Maybe the rule in Ex 3 is different? Or the Yellow 4s are part of the 'inside' in some way?** What if the frame is defined not just by color but by being the outermost rectangle? In Ex 3, the green 3 is outermost.

Let's stick to the "remove background pattern" idea and assume Ex 3 has a quirk or my inner content analysis was wrong.

**YAML Facts (Based on Pattern Removal Hypothesis)**


```yaml
elements:
  - element: background_pattern
    description: A repeating pattern of low-value colors (e.g., 0,1,2,3 or 0,1) covering large areas of the input grid, identified from the region outside the main frame.
    properties:
      - repetitive
      - composed of specific colors (e.g., {0,1,2,3} or {0,1})
      - pattern_unit (e.g., 2x2, 1xN sequence)
      - identified_from_outside_frame
  - element: frame
    description: The outermost, hollow rectangle, one pixel thick, made of a single non-white color. It encloses other objects and potentially some background pattern elements.
    properties:
      - rectangular_shape
      - hollow
      - thickness: 1 pixel
      - single_color (varies: azure, green)
      - non_white
      - outermost_rectangle_of_single_color
      - encloses_other_elements
  - element: inner_objects
    description: Contiguous shapes or blocks of pixels located spatially inside the 'frame' whose color does not match the identified background pattern at that location. Includes the frame color itself in some cases (Ex 2).
    properties:
      - located_inside_frame
      - color_mismatch_with_background_pattern
      - may_include_frame_color

actions:
  - action: identify_frame
    description: Find the outermost, single-colored, non-white, 1-pixel thick, rectangular frame in the input grid. Determine its color and the bounding box of the area it encloses.
  - action: identify_background_pattern
    description: Analyze the region outside the frame to determine the repeating background pattern unit and colors.
  - action: extract_inner_content
    description: Select the portion of the input grid located strictly inside the identified frame.
  - action: filter_background_pattern
    description: Within the extracted inner content, compare each pixel's color and position to the expected background pattern. Replace matching pixels with white (0). Exception: Do not replace the frame color if it matches the pattern (as seen in Ex 2).
  - action: construct_output
    description: Create a new grid. Set its border (1 pixel thick) to the frame's color. Place the filtered inner content into the center of this new grid.

relationships:
  - relationship: containment
    description: The 'frame' contains the 'inner_objects' and some 'background_pattern' elements.
  - relationship: pattern_removal
    description: Pixels inside the input frame matching the 'background_pattern' are removed (set to white), unless the pixel color is the frame color itself. Other pixels ('inner_objects') are preserved.
```


**Natural Language Program (Based on Pattern Removal Hypothesis)**

1.  **Find Frame:** Scan the input grid to locate the *outermost* rectangular, hollow frame that is exactly one pixel thick and composed of a single, non-white color (`frame_color`). Identify the rectangular region strictly *inside* this frame (`inner_region`).
2.  **Identify Background Pattern:** Analyze the area *outside* the frame's bounding box to determine the repeating color pattern (`background_pattern`). Note the colors involved (`background_colors`).
3.  **Create Output Grid:** Create a new grid whose dimensions are 2 plus the height and 2 plus the width of the `inner_region`.
4.  **Draw Border:** Draw a border, one pixel thick, around the edge of the output grid using the `frame_color`. Initialize the interior of the output grid to white (0).
5.  **Filter and Copy:** Iterate through each pixel `(r, c)` within the `inner_region` of the input grid. Let the color be `P`.
6.  **Check Pattern:** Determine if the pixel `P` at `(r, c)` matches the expected `background_pattern` for that position.
7.  **Apply Filter:**
    *   If `P` matches the `background_pattern` AND `P` is NOT equal to `frame_color`, place white (0) at the corresponding position in the output grid's interior.
    *   Otherwise (if `P` does not match the pattern, or if `P` matches the pattern *but* `P` == `frame_color`), copy the color `P` to the corresponding position in the output grid's interior.
8.  **Output:** Return the completed output grid.

*(Self-correction: Still doesn't explain Example 3's yellow '4'. The simplest explanation remaining is that my `find_frame` logic needs debugging, or Example 3's yellow block is somehow considered "inside" despite coordinates.)* Given the consistent failure of `find_frame`, debugging that is the highest priority before adding complexity like pattern matching. The initial N L program was likely closer, but the frame finding failed. Let's revert to the simpler background definition (colors outside) and focus on fixing `find_frame`.


**Revised Natural Language Program (Simpler Background, focus on fixing frame finding)**

1.  **Find Frame:** Scan the input grid to locate a rectangular, hollow frame that is exactly one pixel thick and composed of a single, non-white color (`frame_color`). Identify the rectangular region strictly *inside* this frame (`inner_region`). *[Coder Note: This step needs robust implementation]*
2.  **Identify Background Colors:** Determine the set `background_colors` containing white (0) and all unique pixel colors present in the input grid *outside* the bounding box of the found frame (including the frame pixels themselves is acceptable).
3.  **Create Output Grid:** Create a new grid whose dimensions are 2 plus the height and 2 plus the width of the `inner_region`.
4.  **Draw Border:** Draw a border, one pixel thick, around the edge of the output grid using the `frame_color`. Initialize the interior of the output grid to white (0).
5.  **Filter and Copy:** Iterate through each pixel `(r, c)` within the `inner_region` of the input grid. Let the color be `P`.
6.  **Check Background:** Determine if the input pixel color `P` is present in the `background_colors` set.
7.  **Apply Filter:**
    *   If `P` is in `background_colors`, place white (0) at the corresponding position `(r_out, c_out)` in the output grid's interior.
    *   Else (if `P` is *not* in `background_colors`), copy the color `P` to the corresponding position `(r_out, c_out)` in the output grid's interior.
8.  **Output:** Return the completed output grid.


*(Final thought: Example 3's Yellow '4' might be handled implicitly if the background colors are defined correctly. In Ex 3, outside colors are {0, 1, 4}. If the Background set is {0, 1, 4}, and the inner content is just {8}, then filtering leaves {8}. If the Yellow 4 block IS somehow inside the true frame, and 4 is NOT background, it would be preserved. This hinges entirely on finding the correct frame and its contents.)*
