
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

Previous Code:
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
4 4 4 4 4 4 4
4 5 5 5 5 5 4
4 5 5 5 5 5 4
4 5 5 5 5 5 4
4 5 5 5 5 5 4
4 4 4 4 4 4 4
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
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
3 3 3 3 3 3 3 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 28.125
**General Assessment**

The previous attempt failed because the frame identification logic was flawed. It relied on finding perfect, single-color rectangles using `np.argwhere` and bounding boxes, which failed when the frame wasn't perfectly rectangular (Ex 2) or when multiple potential rectangular shapes existed (Ex 1, Ex 3 - finding inner shapes or incorrect frames). The background filtering was dependent on the correctly identified frame and its adjacent external colors, leading to further errors.

The new strategy focuses on:
1.  Defining a fixed set of background colors {white:0, blue:1, red:2, green:3}.
2.  Identifying the area of interest by finding the bounding box of *all* non-background pixels.
3.  Determining the frame color by checking which single, non-background color forms a 1-pixel border around this bounding box.
4.  Extracting the content within this frame (bounding box minus the 1-pixel border).
5.  Filtering this extracted content by replacing pixels matching the background colors {0, 1, 2, 3} with white (0).
6.  Constructing the output grid with the identified frame color as the border and the filtered content inside.

This revised approach correctly handles all three examples conceptually and aligns with the observed input-output transformations.

**Metrics Analysis**

*   **Example 1:**
    *   `input_shape`: (14, 22), `output_shape`: (12, 11)
    *   `input_colors`: {0, 1, 2, 3, 4, 5, 6, 8} (white, blue, red, green, yellow, gray, magenta, azure)
    *   `output_colors`: {0, 4, 5, 6, 8} (white, yellow, gray, magenta, azure)
    *   `non_background_bbox`: (r=1, c=1) -> (r=12, c=18)
    *   *Failure*: Incorrect frame ID led to wrong size (6, 7) and content (only yellow/gray kept, border missing).
    *   *Correction Need*: Identify frame based on non-background bbox (1,1)-(12,18). Check perimeter for single color. Azure (8) forms the relevant border sections. Inner area (2,2)-(11,17). Filter using {0,1,2,3}.

*   **Example 2:**
    *   `input_shape`: (13, 23), `output_shape`: (9, 12)
    *   `input_colors`: {0, 1, 2, 3, 4, 6, 8} (white, blue, red, green, yellow, magenta, azure)
    *   `output_colors`: {0, 3, 4, 6, 8} (white, green, yellow, magenta, azure)
    *   `non_background_bbox`: (r=0, c=14) -> (r=5, c=18). *Wait*, the code output for this bbox is wrong. Let's re-run the calculation mentally. Non-background = {3, 4, 6, 8}. Coords for 3: (3,5)-(3,13), (11,5)-(11,16), (4,5)-(10,5), ... BBox should be much larger. The code used `invert=True` on `np.isin` - maybe that's only checking *not* 0, 1, 2, *or* 3? Yes. Correct non-bg set {4, 5, 6, 8} for Ex 1, {4, 6, 8} for Ex 2, {4, 8} for Ex 3. Let's recalculate the bboxes based on these sets.
        *   Ex 1: {4,5,6,8}. Min/Max Rs: 1, 12. Min/Max Cs: 1, 18. BBox: (1,1) -> (12,18). Correct.
        *   Ex 2: {4,6,8}. Min/Max Rs: 1, 5. Min/Max Cs: 14, 18. BBox: (1,14) -> (5,18). Correct.
        *   Ex 3: {4,8}. Min/Max Rs: 2, 7. Min/Max Cs: 3, 14. BBox: (2,3) -> (7,14). Correct.
    *   *Failure*: Frame finding failed entirely (returned input).
    *   *Correction Need*: Identify frame based on non-background bbox (1,14)-(5,18). The actual frame uses Green(3). This contradicts the non-background definition.

**Revised Revised Hypothesis:**
The background isn't *just* {0,1,2,3}. The *frame* color is also not part of the "content".
1.  Identify the single color `C` that forms a 1-pixel thick perimeter enclosing some area. This must be the frame identification step. Use the `_find_potential_frames` logic, but maybe simplify the thickness check. Find the largest such frame.
2.  Let the frame color be `frame_color` and its outer bounding box be `(min_r, min_c) -> (max_r, max_c)`.
3.  Identify background colors: {0} plus any colors adjacent *outside* the frame's bounding box. `bg_colors = {0}.union(_get_adjacent_outside_colors(grid, min_r, min_c, max_r, max_c))`
4.  Extract inner region: `grid[min_r+1:max_r, min_c+1:max_c]`
5.  Filter: Replace pixels in `bg_colors` with 0.
6.  Construct output.

Let's re-test this on the failures:
*   **Ex 1:** Largest frame is Azure(8) at (1,1)-(12,11). `frame_color=8`. Adjacent outside colors = {0, 1, 2, 3}. `bg_colors = {0, 1, 2, 3}`. Inner region `grid[2:12, 2:11]` contains {0,1,2,3,4,5,6}. Filter {0,1,2,3} -> 0. Keep {4,5,6}. Looks correct.
*   **Ex 2:** Frame finding failed previously. Why? The Green(3) object isn't a perfect rectangle defined by its min/max coords. The `_find_potential_frames` check `np.all(grid[min_r, min_c:max_c + 1] == color)` fails because the top edge has 0s/1s/2s interspersed. Frame finding needs to be more robust - perhaps find largest connected component of a single color, check if it's 1 pixel thick and encloses other colors.
*   **Ex 3:** Previous code found Green(3) at (1,2)-(8,9). Adjacent outside = {0, 1}. `bg_colors = {0, 1}`. Inner region `grid[2:8, 3:9]` contains only {8}. Filtering keeps {8}. The Yellow(4) object at `grid[4:7, 12:15]` is *outside* this frame. This means the frame found (1,2)-(8,9) is *wrong*. The *intended* frame must enclose the 4s as well.

**Conclusion:** The core difficulty is robustly identifying the correct "frame" and the "content" it encloses, especially when the frame isn't a simple rectangle or when multiple potential frames exist. The definition of "background" also seems tied to what's *outside* the true frame.

**Final Approach Attempt:**
1.  Find *all* potential frames using the `_find_potential_frames` logic (single color, 1-pixel thick, hollow rectangle based on its own bounding box).
2.  For each potential frame `F` with color `C_F` and outer bounds `B_F`:
    *   Define its inner region `I_F`.
    *   Define background colors `BG_F = {0} + colors adjacent outside B_F`.
    *   Create a candidate output by filtering `I_F` (replace `BG_F` colors with 0) and adding `C_F` border.
3.  Select the candidate output that seems "best" - perhaps largest size, or most non-white pixels? Compare against expected outputs. All expected outputs are rectangular and contain non-background colors.
4.  Try selecting the frame that encloses the largest number of non-zero pixels that are *not* the frame color and *not* the adjacent background colors.


```yaml
elements:
  - element: background_pixels
    description: Pixels considered part of the background noise or pattern, primarily located outside the main frame. Often consists of low-value colors (0, 1, 2, 3 in examples) in a repeating pattern. White (0) is always considered background. The exact set can also include colors found immediately adjacent to the outside of the identified frame.
    properties:
      - low_value_colors (often 0, 1, 2, 3)
      - repetitive_pattern (often)
      - located_outside_frame (primarily)
      - includes_white (0)
      - includes_colors_adjacent_outside_frame
  - element: frame
    description: A hollow, rectangular structure, exactly one pixel thick, made of a single non-background color. It encloses the 'content_pixels'. Identified as the largest valid frame object in the input.
    properties:
      - rectangular_shape
      - hollow
      - thickness_1_pixel
      - single_color
      - non_background_color
      - encloses_content_pixels
      - largest_valid_frame (heuristic)
  - element: content_pixels
    description: Pixels located spatially inside the 'frame'. These include the actual objects of interest and potentially some 'background_pixels' that need filtering.
    properties:
      - located_inside_frame
      - may_include_objects_of_interest
      - may_include_background_pixels

actions:
  - action: identify_candidate_frames
    description: Find all single-colored, non-white, 1-pixel thick, hollow rectangular structures in the input grid based on their own bounding boxes.
  - action: select_main_frame
    description: From the candidates, select the 'best' frame. Heuristic likely involves selecting the largest frame (by area or perimeter). Record its color (`frame_color`) and outer bounding box (`frame_bounds`).
  - action: determine_background_colors
    description: Create a set of background colors consisting of white (0) plus all unique colors found immediately adjacent to the *outside* perimeter defined by `frame_bounds`.
  - action: extract_inner_content
    description: Select the portion of the input grid located strictly inside the `frame_bounds` (i.e., excluding the frame itself).
  - action: filter_background_from_content
    description: Within the extracted inner content, replace any pixel whose color belongs to the determined background color set with white (0).
  - action: construct_output
    description: Create a new grid sized to fit the inner content plus a 1-pixel border. Draw the border using `frame_color`. Place the filtered inner content into the center.

relationships:
  - relationship: containment
    description: The selected 'frame' contains the 'content_pixels'.
  - relationship: adjacency
    description: The 'background_pixels' used for filtering are determined by adjacency to the outside of the selected 'frame'.
  - relationship: filtering
    description: Pixels within the 'content_pixels' are checked against the 'background_colors'. If a match occurs, the pixel is replaced with white (0) in the output; otherwise, it's preserved.
```


**Natural Language Program**

1.  **Scan** the input grid to find all possible candidate "frames". A candidate frame must be a perfectly rectangular, hollow shape, exactly one pixel thick, composed of a single color (not white), based on the bounding box of that color's pixels.
2.  **Select** the "main frame" from the candidates. Use a heuristic: choose the frame with the largest area (height * width). Record its color (`frame_color`) and its outer bounding box coordinates (`min_r`, `min_c`, `max_r`, `max_c`). If no candidate frames are found, return the original input grid.
3.  **Determine** the set of `background_colors`. This set initially contains only white (0). Then, examine all pixels immediately adjacent to the *outside* of the main frame's bounding box (pixels at `r=min_r-1`, `r=max_r+1`, `c=min_c-1`, `c=max_c+1` where they exist within grid bounds and border the frame). Add all unique colors found in these adjacent positions to the `background_colors` set.
4.  **Calculate** the dimensions of the region strictly inside the main frame: `inner_height = max_r - min_r - 1`, `inner_width = max_c - min_c - 1`.
5.  **Create** a new output grid initialized with white (0), with dimensions `(inner_height + 2) x (inner_width + 2)`.
6.  **Draw** a border, one pixel thick, around the edge of the output grid using the `frame_color`.
7.  **Iterate** through each pixel `(r_in, c_in)` within the inner region of the input grid (from `r = min_r + 1` to `max_r - 1`, and `c = min_c + 1` to `max_c - 1`). Let the color of this input pixel be `P`.
8.  **Calculate** the corresponding position `(r_out, c_out)` in the output grid's interior (`r_out = r_in - min_r`, `c_out = c_in - min_c`).
9.  **Check** if the input pixel color `P` is present in the `background_colors` set.
10. **If** `P` is *not* in `background_colors`, set the pixel at `(r_out, c_out)` in the output grid to `P`. (Otherwise, leave it as the initialized white color).
11. **Output** the completed grid.**General Assessment**

The previous code failed primarily due to an incorrect frame identification strategy and, consequently, incorrect background color determination.
*   **Example 1:** Identified an inner yellow shape as the frame instead of the outer azure one.
*   **Example 2:** Failed to identify any frame because the correct green frame wasn't a perfect rectangle fill within its bounding box. The frame-finding logic (`_find_potential_frames`) required all pixels on the perimeter defined by `min_r, min_c, max_r, max_c` to be the frame color, which wasn't true here.
*   **Example 3:** Identified a smaller green frame, excluding the yellow object which should have been part of the content. This again stemmed from the frame identification logic selecting the wrong candidate.

The core issues are:
1.  **Frame Identification:** The logic must correctly identify the single, intended frame object, even if it's not a perfect rectangle or if other shapes exist. The heuristic of selecting the largest frame by area seems promising based on the examples.
2.  **Background Definition:** The background colors to be filtered from the inside seem to be defined by white (0) plus whatever colors are immediately adjacent to the *outside* of the correctly identified frame.

The refined strategy is to find all candidate rectangular frames, select the largest one by area, determine background colors based on its exterior adjacency, and then filter the content within that frame.

**Metrics Analysis**


*code_execution:*
```python
import numpy as np

def get_metrics(input_grid_list, output_grid_list, transformed_grid_list, example_num):
    input_grid = np.array(input_grid_list)
    output_grid = np.array(output_grid_list)
    transformed_grid = np.array(transformed_grid_list) if transformed_grid_list else np.array([[]])

    metrics = {}
    metrics['example'] = example_num
    metrics['input_shape'] = input_grid.shape
    metrics['output_shape'] = output_grid.shape
    metrics['transformed_shape'] = transformed_grid.shape if transformed_grid.size > 0 else (0, 0)

    metrics['input_colors'] = sorted(list(np.unique(input_grid)))
    metrics['output_colors'] = sorted(list(np.unique(output_grid)))
    metrics['transformed_colors'] = sorted(list(np.unique(transformed_grid))) if transformed_grid.size > 0 else []

    metrics['output_size_correct'] = (metrics['output_shape'] == metrics['transformed_shape'])
    metrics['output_colors_correct'] = (metrics['output_colors'] == metrics['transformed_colors'])

    if metrics['output_size_correct']:
        match = np.array_equal(output_grid, transformed_grid)
        metrics['match'] = bool(match)
        metrics['pixels_off'] = int(np.sum(output_grid != transformed_grid)) if not match else 0
    else:
        metrics['match'] = False
        metrics['pixels_off'] = None # Cannot compare pixels if shapes differ

    print(metrics)

# --- Example 1 Data ---
input_1 = [[0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1],[1,8,8,8,8,8,8,8,8,8,8,8,1,2,3,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,0,1,2,8,0,1,2,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,4,4,4,4,4,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,5,5,5,5,5,4,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,5,5,5,5,5,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,5,5,5,5,5,4,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,5,5,5,5,5,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,4,4,4,4,4,4,3,0,6,6,3,0,1],[1,8,3,0,1,2,3,0,1,2,3,8,1,2,3,0,1,6,6,0,1,2],[0,8,2,3,0,1,2,3,0,1,2,8,0,1,2,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,1,2,3,8,1,2,3,0,1,2,3,0,1,2],[0,8,8,8,8,8,8,8,8,8,8,8,0,1,2,3,0,1,2,3,0,1],[1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2]]
output_1 = [[8,8,8,8,8,8,8,8,8,8,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,4,4,4,4,4,4,4,0,0,8],[8,4,5,5,5,5,5,4,0,0,8],[8,4,5,5,5,5,5,4,0,0,8],[8,4,6,6,5,5,5,4,0,0,8],[8,4,6,6,5,5,5,4,0,0,8],[8,4,4,4,4,4,4,4,0,0,8],[8,8,8,8,8,8,8,8,8,8,8]]
# Previous transformed output was based on incorrect frame ID
transformed_1 = [[4,4,4,4,4,4,4],[4,5,5,5,5,5,4],[4,5,5,5,5,5,4],[4,5,5,5,5,5,4],[4,5,5,5,5,5,4],[4,4,4,4,4,4,4]]
print("--- Example 1 Metrics (Previous Run) ---")
get_metrics(input_1, output_1, transformed_1, 1)

# --- Example 2 Data ---
input_2 = [[0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,4,4,1,2,0,1],[1,2,0,1,2,0,1,2,0,1,2,0,1,2,8,8,8,4,4,2,0,1,2],[1,2,0,1,2,0,1,2,0,1,2,0,1,2,8,6,6,6,8,2,0,1,2],[0,1,2,0,1,3,3,3,3,3,3,3,3,3,8,6,6,6,8,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,8,6,6,6,8,2,0,1,2],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,8,8,8,8,8,2,0,1,2],[0,1,2,0,1,3,0,1,2,0,1,2,0,1,2,0,3,2,0,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[0,1,2,0,1,3,0,1,2,0,1,2,0,1,2,0,3,2,0,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[1,2,0,1,2,3,3,3,3,3,3,3,3,3,3,3,3,0,1,2,0,1,2],[0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1]]
output_2 = [[3,3,3,3,3,3,3,3,3,3,3,3],[3,0,0,0,0,0,0,0,0,0,0,3],[3,0,0,0,0,0,0,0,0,0,0,3],[3,8,8,8,8,8,0,0,0,0,0,3],[3,8,6,6,6,8,0,0,0,0,0,3],[3,8,4,4,6,8,0,0,0,0,0,3],[3,8,4,4,6,8,0,0,0,0,0,3],[3,8,8,8,8,8,0,0,0,0,0,3],[3,3,3,3,3,3,3,3,3,3,3,3]]
# Previous transformed output was original input because no frame found
transformed_2 = input_2
print("\n--- Example 2 Metrics (Previous Run) ---")
get_metrics(input_2, output_2, transformed_2, 2)

# --- Example 3 Data ---
input_3 = [[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,3,3,3,3,3,3,3,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,4,4,4,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,4,4,4,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,4,4,4,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,3,3,3,3,3,3,3,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]]
output_3 = [[3,3,3,3,3,3,3,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,4,4,4,8,8,8,3],[3,4,4,4,8,8,8,3],[3,4,4,4,8,8,8,3],[3,3,3,3,3,3,3,3]]
# Previous transformed output was based on incorrect frame ID, missing the yellow part
transformed_3 = [[3,3,3,3,3,3,3,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,3,3,3,3,3,3,3]]
print("\n--- Example 3 Metrics (Previous Run) ---")
get_metrics(input_3, output_3, transformed_3, 3)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 Metrics (Previous Run) ---
{'example': 1, 'input_shape': (14, 22), 'output_shape': (12, 11), 'transformed_shape': (6, 7), 'input_colors': [np.int64(0), np.int64(1), np.int64(2), np.int64(3), np.int64(4), np.int64(5), np.int64(6), np.int64(8)], 'output_colors': [np.int64(0), np.int64(4), np.int64(5), np.int64(6), np.int64(8)], 'transformed_colors': [np.int64(4), np.int64(5)], 'output_size_correct': False, 'output_colors_correct': False, 'match': False, 'pixels_off': None}

--- Example 2 Metrics (Previous Run) ---
{'example': 2, 'input_shape': (13, 23), 'output_shape': (9, 12), 'transformed_shape': (13, 23), 'input_colors': [np.int64(0), np.int64(1), np.int64(2), np.int64(3), np.int64(4), np.int64(6), np.int64(8)], 'output_colors': [np.int64(0), np.int64(3), np.int64(4), np.int64(6), np.int64(8)], 'transformed_colors': [np.int64(0), np.int64(1), np.int64(2), np.int64(3), np.int64(4), np.int64(6), np.int64(8)], 'output_size_correct': False, 'output_colors_correct': False, 'match': False, 'pixels_off': None}

--- Example 3 Metrics (Previous Run) ---
{'example': 3, 'input_shape': (16, 23), 'output_shape': (8, 8), 'transformed_shape': (8, 8), 'input_colors': [np.int64(0), np.int64(1), np.int64(3), np.int64(4), np.int64(8)], 'output_colors': [np.int64(3), np.int64(4), np.int64(8)], 'transformed_colors': [np.int64(3), np.int64(8)], 'output_size_correct': True, 'output_colors_correct': False, 'match': False, 'pixels_off': 9}

```
**YAML Facts**


```yaml
elements:
  - element: potential_background_pattern
    description: Pixels often composed of low-value colors (e.g., white, blue, red, green - 0, 1, 2, 3) sometimes forming a repeating pattern, primarily outside the main frame.
    properties:
      - low_value_colors
      - often_repetitive
      - primarily_outside_frame
  - element: frame_object
    description: A structure, typically rectangular but not always perfectly filled, exactly one pixel thick, composed of a single non-white color. It encloses the content objects. It's identified as the 'best' candidate frame, often the largest by area.
    properties:
      - hollow_structure
      - thickness_1_pixel
      - single_color (non-white)
      - encloses_content_objects
      - identified_via_heuristics (e.g., largest area among valid candidates)
  - element: content_objects
    description: Discrete shapes or blocks of pixels located spatially inside the frame_object, whose colors are distinct from the frame color and typically distinct from the colors identified as background for filtering purposes.
    properties:
      - located_inside_frame
      - colors_distinct_from_frame
      - colors_distinct_from_filtered_background
      - contiguous_shapes (usually)
  - element: filtered_background_colors
    description: A set of colors dynamically determined for filtering. Always includes white (0). Also includes all unique colors found immediately adjacent to the *outside* border of the identified frame_object.
    properties:
      - includes_white_0
      - includes_colors_adjacent_to_outside_of_frame

actions:
  - action: identify_candidate_frames
    description: Find all single-colored, non-white, 1-pixel thick, hollow rectangular structures based on their individual bounding boxes. Check for perimeter completeness, hollowness, and external thickness=1 relative to *that color*.
  - action: select_main_frame
    description: Choose the best frame from the candidates, typically the one with the largest area (height * width). Record its color (`frame_color`) and outer bounding box (`frame_bounds`). Handle cases where no valid frame is found.
  - action: determine_filtering_colors
    description: Identify the set of `filtered_background_colors` by taking white (0) and adding any unique colors adjacent to the outside perimeter defined by `frame_bounds`.
  - action: extract_inner_region
    description: Get the grid portion strictly inside `frame_bounds`.
  - action: filter_content
    description: Create a copy of the inner region. Replace pixels whose color is in `filtered_background_colors` with white (0).
  - action: construct_output
    description: Create a new grid sized for the filtered content plus a 1-pixel border. Draw the border using `frame_color`. Place the filtered content inside.

relationships:
  - relationship: enclosure
    description: The selected 'frame_object' spatially encloses the 'content_objects' and potentially some pixels matching 'filtered_background_colors'.
  - relationship: adjacency_based_filtering
    description: The set of 'filtered_background_colors' is determined by adjacency to the selected 'frame_object', linking the frame choice to the filtering process.
  - relationship: preservation_vs_removal
    description: Within the area defined by the frame, pixels matching 'filtered_background_colors' are removed (set to white), while other pixels ('content_objects') are preserved.
```


**Natural Language Program**

1.  **Identify Candidate Frames:** Scan the input grid to find all possible candidate "frames". A candidate frame is defined as the set of all connected pixels of a single color `C` (where `C` is not white/0) that meets these criteria based on its bounding box (`min_r`, `min_c`, `max_r`, `max_c`):
    *   The bounding box must be at least 3x3 (`max_r - min_r >= 2` and `max_c - min_c >= 2`).
    *   All pixels along the perimeter of the bounding box (`grid[min_r, min_c:max_c+1]`, `grid[max_r, min_c:max_c+1]`, `grid[min_r+1:max_r, min_c]`, `grid[min_r+1:max_r, max_c]`) must have color `C`.
    *   No pixels strictly inside the bounding box (`grid[min_r+1:max_r, min_c+1:max_c]`) can have color `C`.
    *   No pixels immediately adjacent to the *outside* of the bounding box perimeter can have color `C` (ensuring thickness 1). Store each valid candidate frame's color and bounding box.
2.  **Select Main Frame:** If no candidate frames were found, return the original input grid. Otherwise, select the candidate frame with the largest area (`(max_r - min_r + 1) * (max_c - min_c + 1)`). Let its color be `frame_color` and its bounding box be (`frame_min_r`, `frame_min_c`, `frame_max_r`, `frame_max_c`).
3.  **Determine Background Colors:** Initialize a set `background_colors` containing only white (0). Examine the pixels immediately adjacent to the outside of the selected frame's bounding box (if they exist within the grid):
    *   Row above: `grid[frame_min_r - 1, frame_min_c : frame_max_c + 1]`
    *   Row below: `grid[frame_max_r + 1, frame_min_c : frame_max_c + 1]`
    *   Column left: `grid[frame_min_r : frame_max_r + 1, frame_min_c - 1]`
    *   Column right: `grid[frame_min_r : frame_max_r + 1, frame_max_c + 1]`
    Add all unique colors found in these adjacent positions to the `background_colors` set.
4.  **Calculate Inner Dimensions:** Determine the height and width of the region inside the frame: `inner_height = frame_max_r - frame_min_r - 1`, `inner_width = frame_max_c - frame_min_c - 1`.
5.  **Create Output Grid:** Create a new grid `output_grid` with dimensions `(inner_height + 2) x (inner_width + 2)`, initialized entirely with white (0).
6.  **Draw Border:** Set the 1-pixel thick border of the `output_grid` to `frame_color`.
7.  **Process Inner Content:** Iterate through the input grid's inner region, from row `r_in = frame_min_r + 1` to `frame_max_r - 1` and column `c_in = frame_min_c + 1` to `frame_max_c - 1`.
    *   Get the color `P = input_grid[r_in, c_in]`.
    *   Calculate the corresponding output coordinates: `r_out = r_in - frame_min_r`, `c_out = c_in - frame_min_c`.
    *   If the color `P` is **not** in the `background_colors` set, set `output_grid[r_out, c_out] = P`.
8.  **Return Output:** Return the completed `output_grid`.
