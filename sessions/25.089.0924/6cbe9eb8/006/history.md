
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
```python
import numpy as np
from typing import List, Tuple, Set, Optional

"""
Transformation Rule:

1.  Identify a rectangular, hollow frame in the input grid that is exactly one pixel thick and composed of a single, non-white color. Record the frame's color and the bounding box of the region strictly inside it.
2.  Determine the set of 'background colors' containing white (0) and all unique pixel colors present in the input grid strictly *outside* the identified frame's bounding box.
3.  Create a new output grid whose dimensions are sized to fit the inner region identified in step 1, plus a one-pixel border on all sides.
4.  Fill the one-pixel border of the output grid with the frame's color identified in step 1. Initialize the interior to white (0).
5.  Iterate through each pixel within the inner region of the input grid.
6.  For each pixel, check if its color is in the set of 'background colors' identified in step 2.
7.  If the pixel's color is a background color, keep the corresponding output pixel as white (0).
8.  Otherwise (if the pixel's color is not a background color), copy the pixel's original color to the corresponding position within the output grid's interior.
9.  Return the constructed output grid.
"""

def find_frame_coords(grid: np.ndarray) -> Optional[Tuple[int, int, int, int, int]]:
    """
    Finds a 1-pixel thick, single-color, non-white, hollow rectangular frame.
    Focuses on checking perimeter count and shape.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple (frame_color, outer_min_r, outer_min_c, outer_max_r, outer_max_c)
        representing the frame's color and the outer bounding box of the frame itself,
        or None if no such frame is found.
    """
    rows, cols = grid.shape
    for color in range(1, 10):  # Iterate through possible frame colors (1-9)
        coords = np.argwhere(grid == color)
        if coords.size == 0:
            continue

        min_r, min_c = coords.min(axis=0)
        max_r, max_c = coords.max(axis=0)

        # Potential frame dimensions
        height = max_r - min_r + 1
        width = max_c - min_c + 1

        # Frame must be at least 3x3 to be hollow
        if height < 3 or width < 3:
            continue

        # Check 1: Count pixels. Should match perimeter length for a hollow rect.
        # Perimeter count = 2 * height + 2 * width - 4 (accounts for corners)
        expected_perimeter_pixels = 2 * height + 2 * width - 4
        if coords.shape[0] != expected_perimeter_pixels:
             continue # Pixel count doesn't match perimeter

        # Check 2: Shape. Verify all pixels on the perimeter have the correct color.
        is_perimeter_correct = True
        try: # Add try-except for boundary checks
            # Top/Bottom rows
            if not np.all(grid[min_r, min_c:max_c+1] == color) or \
               not np.all(grid[max_r, min_c:max_c+1] == color):
                is_perimeter_correct = False
            # Left/Right columns (excluding corners already checked)
            if is_perimeter_correct and height > 1: # Check columns if height > 1
                 if not np.all(grid[min_r+1:max_r, min_c] == color) or \
                    not np.all(grid[min_r+1:max_r, max_c] == color):
                     is_perimeter_correct = False
        except IndexError:
            is_perimeter_correct = False # Index out of bounds means shape is wrong

        if not is_perimeter_correct:
            continue # Pixels forming the bounding box don't all match the color

        # Check 3: Hollow. Ensure no pixels *inside* the perimeter have the frame color.
        if height > 2 and width > 2: # Only check inner slice if it exists
            inner_slice = grid[min_r + 1 : max_r, min_c + 1 : max_c]
            if np.any(inner_slice == color):
                 continue # Frame color found inside the perimeter

        # Check 4: Thickness 1 (Outer check - optional but good sanity check)
        # Ensure pixels immediately outside the frame are not the frame color
        outer_thick = False
        # Check above (if possible)
        if min_r > 0 and np.any(grid[min_r - 1, min_c:max_c+1] == color): outer_thick = True
        # Check below (if possible)
        if not outer_thick and max_r < rows - 1 and np.any(grid[max_r + 1, min_c:max_c+1] == color): outer_thick = True
        # Check left (if possible)
        if not outer_thick and min_c > 0 and np.any(grid[min_r:max_r+1, min_c - 1] == color): outer_thick = True
        # Check right (if possible)
        if not outer_thick and max_c < cols - 1 and np.any(grid[min_r:max_r+1, max_c + 1] == color): outer_thick = True

        if outer_thick:
            continue # Frame appears thicker than 1 pixel externally

        # If all checks pass, we found our frame
        # Return frame color and OUTER bounds
        return color, min_r, min_c, max_r, max_c

    return None # No frame found


def get_background_colors(grid: np.ndarray, frame_outer_min_r: int, frame_outer_min_c: int, frame_outer_max_r: int, frame_outer_max_c: int) -> Set[int]:
    """
    Identifies colors outside the frame's outer bounding box.

    Args:
        grid: The input grid as a numpy array.
        frame_outer_min_r, frame_outer_min_c, frame_outer_max_r, frame_outer_max_c: Coordinates defining
            the outer bounding box of the frame itself.

    Returns:
        A set containing 0 (white) and all unique colors found strictly outside the frame.
    """
    rows, cols = grid.shape
    background_colors = set([0]) # Always include white

    # Create a mask that is True *inside* the frame's outer box, False otherwise
    mask = np.zeros(grid.shape, dtype=bool)
    # Ensure indices are within grid bounds before slicing
    r_start = max(0, frame_outer_min_r)
    r_end = min(rows, frame_outer_max_r + 1)
    c_start = max(0, frame_outer_min_c)
    c_end = min(cols, frame_outer_max_c + 1)
    
    if r_start < r_end and c_start < c_end:
        mask[r_start:r_end, c_start:c_end] = True 

    # Select pixels where the mask is False (i.e., outside the frame)
    outside_pixels = grid[~mask]
    
    # Get unique colors from the outside pixels
    if outside_pixels.size > 0:
        unique_outside = np.unique(outside_pixels)
        for color in unique_outside:
            background_colors.add(int(color)) # Add numpy int to set

    return background_colors


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # 1. Find the frame and its outer coordinates
    frame_info = find_frame_coords(grid_np)
    if frame_info is None:
        # If no frame found, return the input grid unmodified as per some ARC task conventions
        # or handle as an error case (e.g., raise ValueError or return empty list).
        # Returning input seems safer if unsure about specific task requirements.
        # print("Debug: No frame found.")
        return input_grid

    frame_color, frame_outer_min_r, frame_outer_min_c, frame_outer_max_r, frame_outer_max_c = frame_info

    # Define inner region coordinates (1 pixel inside the outer frame)
    inner_min_r = frame_outer_min_r + 1
    inner_min_c = frame_outer_min_c + 1
    inner_max_r = frame_outer_max_r - 1
    inner_max_c = frame_outer_max_c - 1

    # Check if inner region is valid (should be guaranteed by find_frame checks)
    if inner_min_r > inner_max_r or inner_min_c > inner_max_c:
         # This case should ideally not happen if find_frame works correctly
         # print("Debug: Invalid inner region derived.")
         return input_grid # Return input if something went wrong

    # 2. Identify background colors (strictly outside the frame)
    background_colors = get_background_colors(grid_np, frame_outer_min_r, frame_outer_min_c, frame_outer_max_r, frame_outer_max_c)
    # print(f"Debug: Found Frame Color {frame_color} at ({frame_outer_min_r},{frame_outer_min_c})->({frame_outer_max_r},{frame_outer_max_c})")
    # print(f"Debug: Background Colors Identified: {background_colors}")


    # 3. Create the output grid
    inner_height = inner_max_r - inner_min_r + 1
    inner_width = inner_max_c - inner_min_c + 1
    output_height = inner_height + 2
    output_width = inner_width + 2

    # Initialize with white (0) - border will be overwritten later
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    # 4. Draw the border with frame_color
    output_grid_np[0, :] = frame_color          # Top row
    output_grid_np[-1, :] = frame_color         # Bottom row
    output_grid_np[:, 0] = frame_color          # Left column
    output_grid_np[:, -1] = frame_color         # Right column

    # 5-8. Iterate through the inner region of the input grid, filter, and place in output
    for r_in in range(inner_min_r, inner_max_r + 1):
        for c_in in range(inner_min_c, inner_max_c + 1):
            # Ensure we don't read out of input bounds (shouldn't happen)
            if not (0 <= r_in < rows and 0 <= c_in < cols):
                 continue

            input_pixel_color = grid_np[r_in, c_in]

            # Calculate corresponding output coordinates (offset by 1 for the border)
            r_out = r_in - inner_min_r + 1
            c_out = c_in - inner_min_c + 1

            # Ensure we don't write out of output bounds (shouldn't happen)
            if not (1 <= r_out < output_height - 1 and 1 <= c_out < output_width - 1):
                 continue

            # Check if the input color is a background color
            if input_pixel_color in background_colors:
                # Already initialized to 0, so no action needed, but explicit for clarity
                output_grid_np[r_out, c_out] = 0 # Set to white
            else:
                # Copy the original color if it's not background
                output_grid_np[r_out, c_out] = input_pixel_color

    # 9. Return the completed grid as a list of lists
    return output_grid_np.tolist()
```
```python
import numpy as np
from typing import List, Tuple, Set, Optional

"""
Transformation Rule:

1.  Identify the most prominent rectangular, hollow frame in the input grid that is exactly one pixel thick and composed of a single, non-white color. "Prominent" might mean largest perimeter or area. Record the frame's color and its outer bounding box coordinates.
2.  Determine the set of 'background colors'. This set includes white (0) and all unique colors found immediately adjacent to the *outside* perimeter of the identified frame.
3.  Create a new output grid. Its dimensions are determined by the size of the region strictly *inside* the identified frame, plus a one-pixel border on all sides.
4.  Fill the one-pixel border of the output grid with the frame's color identified in step 1. Initialize the interior of the output grid to white (0).
5.  Iterate through each pixel within the inner region of the input grid (the area inside the frame).
6.  For each input pixel, check if its color is present in the set of 'background colors' identified in step 2.
7.  If the input pixel's color *is* a background color, leave the corresponding pixel in the output grid's interior as white (0).
8.  Otherwise (if the input pixel's color is *not* a background color), copy the input pixel's original color to the corresponding position within the output grid's interior.
9.  Return the constructed output grid. If no suitable frame is found, return the original input grid.
"""

def _find_potential_frames(grid: np.ndarray) -> List[Tuple[int, int, int, int, int]]:
    """
    Finds all potential 1-pixel thick, single-color, non-white, hollow rectangular frames.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A list of tuples (frame_color, outer_min_r, outer_min_c, outer_max_r, outer_max_c)
        for each potential frame found.
    """
    rows, cols = grid.shape
    potential_frames = []

    for color in range(1, 10):  # Iterate through possible frame colors (1-9)
        coords = np.argwhere(grid == color)
        if coords.size == 0:
            continue

        min_r, min_c = coords.min(axis=0)
        max_r, max_c = coords.max(axis=0)

        # Potential frame dimensions
        height = max_r - min_r + 1
        width = max_c - min_c + 1

        # Frame must be at least 3x3 to be hollow
        if height < 3 or width < 3:
            continue

        # Check 1: Verify all pixels on the exact perimeter match the color
        is_perimeter_complete = True
        try:
            # Top row
            if not np.all(grid[min_r, min_c:max_c + 1] == color): is_perimeter_complete = False
            # Bottom row
            if is_perimeter_complete and not np.all(grid[max_r, min_c:max_c + 1] == color): is_perimeter_complete = False
            # Left column (excluding corners)
            if is_perimeter_complete and not np.all(grid[min_r + 1:max_r, min_c] == color): is_perimeter_complete = False
            # Right column (excluding corners)
            if is_perimeter_complete and not np.all(grid[min_r + 1:max_r, max_c] == color): is_perimeter_complete = False
        except IndexError:
             is_perimeter_complete = False # Should not happen if bounds are correct, but safety check

        if not is_perimeter_complete:
             continue # The bounding box perimeter isn't solely the frame color

        # Check 2: Hollow. Ensure no pixels *inside* the perimeter have the frame color.
        if height > 2 and width > 2:
            inner_slice = grid[min_r + 1:max_r, min_c + 1:max_c]
            if np.any(inner_slice == color):
                continue # Frame color found inside

        # Check 3: Thickness 1 (External check). Ensure no adjacent pixels *outside* the frame have the frame color.
        is_thick = False
        # Check row above
        if min_r > 0 and np.any(grid[min_r - 1, min_c:max_c + 1] == color): is_thick = True
        # Check row below
        if not is_thick and max_r < rows - 1 and np.any(grid[max_r + 1, min_c:max_c + 1] == color): is_thick = True
        # Check column left
        if not is_thick and min_c > 0 and np.any(grid[min_r:max_r + 1, min_c - 1] == color): is_thick = True
        # Check column right
        if not is_thick and max_c < cols - 1 and np.any(grid[min_r:max_r + 1, max_c + 1] == color): is_thick = True

        if is_thick:
            continue # Frame appears thicker than 1 pixel

        # If all checks pass, add to potential frames
        potential_frames.append((color, min_r, min_c, max_r, max_c))

    return potential_frames


def _get_adjacent_outside_colors(grid: np.ndarray, min_r: int, min_c: int, max_r: int, max_c: int) -> Set[int]:
    """Gets unique colors adjacent to the *outside* of a bounding box."""
    rows, cols = grid.shape
    adjacent_colors = set()

    # Check row above (r = min_r - 1)
    if min_r > 0:
        r_check = min_r - 1
        for c_check in range(max(0, min_c), min(cols, max_c + 1)):
             adjacent_colors.add(grid[r_check, c_check])

    # Check row below (r = max_r + 1)
    if max_r < rows - 1:
        r_check = max_r + 1
        for c_check in range(max(0, min_c), min(cols, max_c + 1)):
             adjacent_colors.add(grid[r_check, c_check])

    # Check column left (c = min_c - 1)
    if min_c > 0:
        c_check = min_c - 1
        # Exclude corners already checked by row checks
        for r_check in range(max(0, min_r + 1), min(rows, max_r)):
             adjacent_colors.add(grid[r_check, c_check])

    # Check column right (c = max_c + 1)
    if max_c < cols - 1:
        c_check = max_c + 1
        # Exclude corners already checked by row checks
        for r_check in range(max(0, min_r + 1), min(rows, max_r)):
             adjacent_colors.add(grid[r_check, c_check])

    return adjacent_colors


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule: extracts content within a frame,
    filters out background colors (adjacent to frame + white), and adds frame border.
    """
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # 1. Find potential frames
    potential_frames = _find_potential_frames(grid_np)

    # If no frames found, return original grid
    if not potential_frames:
        #print("Debug: No valid frames found.")
        return input_grid

    # Select the best frame (e.g., largest perimeter or area). Let's use area.
    best_frame = max(potential_frames, key=lambda f: (f[3] - f[1] + 1) * (f[4] - f[2] + 1))
    frame_color, frame_outer_min_r, frame_outer_min_c, frame_outer_max_r, frame_outer_max_c = best_frame
    #print(f"Debug: Selected Frame Color {frame_color} at ({frame_outer_min_r},{frame_outer_min_c})->({frame_outer_max_r},{frame_outer_max_c})")


    # Define inner region coordinates
    inner_min_r = frame_outer_min_r + 1
    inner_min_c = frame_outer_min_c + 1
    inner_max_r = frame_outer_max_r - 1
    inner_max_c = frame_outer_max_c - 1

    # Check for valid inner region (should be guaranteed by find_frame)
    if inner_min_r > inner_max_r or inner_min_c > inner_max_c:
         #print("Debug: Invalid inner region derived.")
         return input_grid # Should not happen

    # 2. Identify background colors (adjacent outside + white)
    adjacent_colors = _get_adjacent_outside_colors(grid_np, frame_outer_min_r, frame_outer_min_c, frame_outer_max_r, frame_outer_max_c)
    background_colors = adjacent_colors.union({0}) # Add white
    #print(f"Debug: Background Colors Identified: {background_colors}")

    # 3. Create the output grid dimensions
    inner_height = inner_max_r - inner_min_r + 1
    inner_width = inner_max_c - inner_min_c + 1
    output_height = inner_height + 2
    output_width = inner_width + 2

    # 4. Initialize output grid and draw border
    output_grid_np = np.zeros((output_height, output_width), dtype=int) # Init with white (0)
    output_grid_np[0, :] = frame_color          # Top row
    output_grid_np[-1, :] = frame_color         # Bottom row
    output_grid_np[:, 0] = frame_color          # Left column
    output_grid_np[:, -1] = frame_color         # Right column

    # 5-8. Process the inner region
    for r_in in range(inner_min_r, inner_max_r + 1):
        for c_in in range(inner_min_c, inner_max_c + 1):
            input_pixel_color = grid_np[r_in, c_in]

            # Calculate corresponding output coordinates (offset by 1 for the border)
            r_out = r_in - inner_min_r + 1
            c_out = c_in - inner_min_c + 1

            # Check if the input color is a background color
            if input_pixel_color not in background_colors:
                # Copy the original color if it's not background
                 output_grid_np[r_out, c_out] = input_pixel_color
            # Else: leave it as 0 (white), which was the initialization value

    # 9. Return the completed grid
    return output_grid_np.tolist()
```
