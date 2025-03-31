
## train_1

**input:**
```
1 0 1
1 7 1
1 1 1
```


**output:**
```
1 0 1
1 0 1
1 1 1
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 0 0 0
0 2 2 0 5 5 0 0 0 0 0
0 2 2 0 5 5 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 6 6 8 0 0 0 0
0 0 0 0 6 0 0 8 0 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 6 6 6 0 0 0 0 0 0 0
0 0 0 3 0 0 6 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 6 0 0 0 0 0 0 0 0 0 0 0
0 3 0 6 6 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 7 8 0 7 0 0 0
0 0 0 0 0 0 0 7 0 8 8 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 8 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 8 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 6 6 6 0 0 0 0 0 0 0
0 0 0 3 0 0 6 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 7 0 0 0
0 0 0 0 0 0 0 7 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 8 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 8 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 2 2 0 5 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 6 6 0 0 0 0 9
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 6 6 0 0 0 0 9
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the task based on the examples provided.

**Perception of Elements:**

1.  **Input/Output Grids:** Both input and output are grids of pixels with different colors.
2.  **Objects:** The non-white pixels often form contiguous shapes or regions. Some of these shapes appear to act as containers or boundaries.
3.  **Background:** The white (0) pixels seem to represent the background or empty space.
4.  **Colors:** Various colors (blue, red, green, yellow, gray, magenta, orange, azure, maroon) are used. White (0) is the background. Specific colors like gray (5), orange (7), azure (8), and magenta (6) appear *inside* other colored shapes in the inputs.
5.  **Transformation:** The core transformation seems to involve identifying pixels enclosed within certain shapes and changing their color to white (0). The enclosing shapes themselves remain unchanged. Pixels not enclosed also remain unchanged.

**YAML Documentation of Facts:**


```yaml
Task: Enclosed Pixel Removal

Examples:
  - ID: train_1
    Input: 3x3 grid with a blue (1) border enclosing an orange (7) pixel.
    Output: Blue border remains, enclosed orange (7) pixel becomes white (0).
    Objects:
      - Type: Boundary
        Color: blue (1)
        Shape: Square frame
      - Type: Enclosed Pixel
        Color: orange (7)
        Position: Center
    Action: Change color of Enclosed Pixel to white (0).
    Relationship: orange (7) pixel is enclosed by the blue (1) boundary.

  - ID: train_2
    Input: Grid with two main shapes: red (2) 'C' enclosing gray (5) pixels, magenta (6) 'L' enclosing an azure (8) pixel.
    Output: Red and magenta shapes remain, enclosed gray (5) and azure (8) pixels become white (0).
    Objects:
      - Type: Boundary
        Color: red (2)
        Encloses: gray (5) pixels
      - Type: Boundary
        Color: magenta (6)
        Encloses: azure (8) pixel
    Action: Change color of enclosed gray (5) and azure (8) pixels to white (0).
    Relationship: gray (5) pixels enclosed by red (2), azure (8) pixel enclosed by magenta (6).

  - ID: train_3
    Input: Grid with green (3) shape enclosing magenta (6) pixels, and orange (7) shape enclosing azure (8) pixels. Other pixels exist outside these enclosures.
    Output: Green and orange shapes remain. Enclosed magenta (6) and azure (8) pixels become white (0). Other pixels unchanged.
    Objects:
      - Type: Boundary
        Color: green (3)
        Encloses: magenta (6) pixels
      - Type: Boundary
        Color: orange (7)
        Encloses: azure (8) pixels
    Action: Change color of enclosed magenta (6) and azure (8) pixels to white (0).
    Relationship: magenta (6) pixels enclosed by green (3), azure (8) pixels enclosed by orange (7).

  - ID: train_4
    Input: Grid with red (2) 'C' enclosing a gray (5) pixel. A magenta (6) shape and a maroon (9) pixel exist but do not enclose anything or are not enclosed.
    Output: Red shape remains. Enclosed gray (5) pixel becomes white (0). Magenta shape and maroon pixel remain unchanged.
    Objects:
      - Type: Boundary
        Color: red (2)
        Encloses: gray (5) pixel
      - Type: Shape (Not a boundary in this context)
        Color: magenta (6)
      - Type: Pixel
        Color: maroon (9)
    Action: Change color of enclosed gray (5) pixel to white (0).
    Relationship: gray (5) pixel enclosed by red (2). Magenta (6) and maroon (9) are not involved in enclosure.

Summary:
  - Identify contiguous regions of a single non-white color that form closed boundaries.
  - Identify pixels located strictly *inside* these boundaries.
  - The color of the boundary object is irrelevant to the action, only its shape matters.
  - The color of the enclosed pixel is irrelevant; *any* non-white pixel inside a boundary (that isn't part of the boundary itself) is targeted.
  - Pixels that are part of the boundary, or pixels outside any boundary, are not modified.
  - The action is always to change the color of the enclosed pixel(s) to white (0).
```


**Natural Language Program:**

1.  Create a copy of the input grid to serve as the output grid.
2.  Iterate through each pixel `(r, c)` in the input grid.
3.  If the pixel at `(r, c)` in the output grid is not white (0) and has not yet been processed as part of an identified enclosed region:
    a.  Check if this pixel `(r, c)` is enclosed by a single-colored boundary. To do this:
        i.  Perform a flood fill (or similar search like Breadth-First Search) starting from `(r, c)`, only moving to adjacent (up, down, left, right) cells that are *not* the same color as the pixel at `(r, c)` in the *input* grid.
        ii. During the search, keep track of the different colors encountered. Let the color of the starting pixel `(r, c)` be `target_color`.
        iii. If the search encounters the grid boundary or a white (0) pixel *before* encountering any other color, the pixel `(r, c)` is *not* enclosed. Stop the check for this pixel.
        iv. If the search encounters pixels of only *one* specific non-white color (let's call it `boundary_color`) before hitting the grid edge or a white pixel, and `boundary_color` is different from `target_color`, then the pixel `(r, c)` *might* be enclosed by `boundary_color`. Continue the search.
        v. If the search completes (cannot expand further) and has only encountered `boundary_color` pixels (besides the initial `target_color` pixels) and has *not* reached the grid edge or a white pixel, then the pixel `(r, c)` is confirmed to be enclosed by the `boundary_color`.
    b. If the pixel `(r, c)` is confirmed to be enclosed:
        i.  Change the color of the pixel at `(r, c)` in the *output* grid to white (0).
        ii. Mark all pixels visited during the successful enclosure check flood fill (those with `target_color`) as processed to avoid re-checking them.
4.  Return the modified output grid.
```python
import numpy as np
from collections import deque

def find_enclosed_region(grid, r, c, processed_mask):
    """
    Performs a Breadth-First Search (BFS) starting from (r, c) to find a potentially 
    enclosed region of the same color, checking the color(s) of its adjacent boundary.

    The region is considered enclosed if:
    1. The BFS explores all contiguous pixels of the starting color ('target_color').
    2. During the BFS, it only encounters adjacent pixels of *one* specific non-white, 
       non-target color ('boundary_color').
    3. The BFS does not reach the grid boundary or a white (0) pixel directly from 
       a pixel of 'target_color'.

    Args:
        grid (np.array): The input grid.
        r (int): Starting row index.
        c (int): Starting column index.
        processed_mask (np.array): Boolean mask indicating pixels that have already 
                                   been processed (e.g., identified as part of a 
                                   previously found enclosed region).

    Returns:
        tuple: (is_enclosed, enclosed_pixels_set)
               is_enclosed (bool): True if the region starting at (r, c) is enclosed
                                   by a single non-white color different from its own, 
                                   False otherwise.
               enclosed_pixels_set (set): A set of coordinates {(row, col)} belonging
                                          to the contiguous region of 'target_color' 
                                          if is_enclosed is True, otherwise an empty set.
    """
    H, W = grid.shape
    target_color = grid[r, c]

    # Cannot be enclosed if starting on white or already processed as enclosed
    if target_color == 0 or processed_mask[r, c]:
        return False, set()

    queue = deque([(r, c)])
    # visited_this_fill tracks pixels visited *during this specific BFS*
    visited_this_fill = set([(r, c)]) 
    # potential_enclosed_pixels stores coordinates of the contiguous target_color region found
    potential_enclosed_pixels = set([(r, c)])
    # boundary_color stores the color of the single enclosing boundary, if found
    boundary_color = None
    # escaped flag is set if the region touches the grid edge, white pixels, or has a multi-colored boundary
    escaped = False

    while queue:
        curr_r, curr_c = queue.popleft()

        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_r + dr, curr_c + dc

            # Check if neighbor is outside the grid bounds -> Escape condition
            if not (0 <= nr < H and 0 <= nc < W):
                escaped = True
                break # Reached grid edge

            neighbor_coord = (nr, nc)
            
            # Skip if already visited in this specific BFS run
            if neighbor_coord in visited_this_fill:
                continue 

            neighbor_color = grid[nr, nc]

            # If neighbor is white (background) -> Escape condition
            if neighbor_color == 0:
                escaped = True
                break # Reached background

            # If neighbor is the same color as the target region
            if neighbor_color == target_color:
                 # Add to BFS queue and track only if not already processed globally
                if not processed_mask[nr, nc]: 
                    visited_this_fill.add(neighbor_coord)
                    potential_enclosed_pixels.add(neighbor_coord)
                    queue.append(neighbor_coord)
                # If it *is* processed, we've reached a previously handled region.
                # This shouldn't happen if the starting check `processed_mask[r, c]` works,
                # unless regions touch. We treat it as non-enclosed for safety, though
                # this specific case might not occur in the examples.
                # else: 
                #    escaped = True
                #    break

            # If neighbor is a different, non-white color (potential boundary)
            else: 
                # This is the first boundary pixel encountered
                if boundary_color is None:
                    boundary_color = neighbor_color
                # If this boundary pixel has a different color than previously found ones -> Escape condition
                elif neighbor_color != boundary_color:
                    escaped = True # Boundary is not monochromatic
                    break
                # Note: Boundary pixels are *not* added to the queue or visited_this_fill

        if escaped:
            break # Stop BFS immediately if an escape condition is met

    # If we escaped, or if we never encountered any boundary pixels (e.g., a single pixel alone), it's not enclosed.
    if escaped or boundary_color is None:
        return False, set()
    else:
        # Successfully explored the region without escaping, and found a single boundary color.
        return True, potential_enclosed_pixels


def transform(input_grid):
    """
    Identifies contiguous regions of pixels that are fully enclosed by a boundary 
    composed of a single, different non-white color. Changes the color of all 
    pixels within each such enclosed region to white (0). Pixels forming the 
    boundaries and pixels in regions that are not enclosed (touch the grid edge, 
    touch white pixels, or have multi-colored boundaries) remain unchanged.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    H, W = grid.shape
    # Create a copy to modify, preserving the original input grid structure for checks
    output_grid = np.copy(grid)
    # Create a mask to keep track of pixels that have been identified as part 
    # of an enclosed region and set to white. This prevents redundant checks.
    processed_mask = np.zeros((H, W), dtype=bool) 

    # Iterate through each pixel in the grid
    for r in range(H):
        for c in range(W):
            # Check if this pixel could be the start of an enclosed region:
            # - Must not be white (background)
            # - Must not have already been processed as part of a found enclosed region
            if grid[r, c] != 0 and not processed_mask[r, c]:
                
                # Perform BFS to check for enclosure and get the region's pixels if enclosed
                is_enclosed, enclosed_pixels = find_enclosed_region(grid, r, c, processed_mask)

                # If the region starting at (r, c) is confirmed to be enclosed
                if is_enclosed:
                    # Iterate through all pixels identified as belonging to this enclosed region
                    for er, ec in enclosed_pixels:
                        # Change the color of these pixels to white (0) in the output grid
                        output_grid[er, ec] = 0
                        # Mark these pixels as processed in the mask to avoid re-checking
                        processed_mask[er, ec] = True
                # If not enclosed, we do nothing to the output grid for this region, 
                # and we don't mark the pixels in processed_mask (as they might be part
                # of a boundary for *another* region check). The loop will continue,
                # potentially starting checks from other pixels in this same non-enclosed region,
                # but the `find_enclosed_region` will correctly identify them as not enclosed each time.

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
```
```python
import numpy as np
from collections import deque

def check_enclosure_and_get_region(grid, start_r, start_c):
    """
    Performs a BFS starting from (start_r, start_c) to find the contiguous region 
    of the same color and determine if it's enclosed by a single other non-white color.

    Args:
        grid (np.array): The input grid.
        start_r (int): Starting row index.
        start_c (int): Starting column index.

    Returns:
        tuple: (is_enclosed, region_pixels)
               is_enclosed (bool): True if the region is enclosed, False otherwise.
               region_pixels (set): Set of coordinates {(r, c)} belonging to the 
                                     contiguous region starting at (start_r, start_c).
                                     Returns the region regardless of enclosure status.
    """
    H, W = grid.shape
    target_color = grid[start_r, start_c]

    # Should not be called on white pixels, but as a safeguard:
    if target_color == 0:
        return False, set()

    queue = deque([(start_r, start_c)])
    # Tracks pixels visited during this specific BFS to avoid cycles within the search
    visited_during_search = set([(start_r, start_c)]) 
    # Stores coordinates of the contiguous target_color region found
    region_pixels = set([(start_r, start_c)])
    # Stores the colors of adjacent, non-target, non-white pixels
    boundary_colors = set()
    # Flag set if the search reaches the grid edge or a white pixel 
    # *directly from* a pixel of target_color
    is_escaped = False

    while queue:
        curr_r, curr_c = queue.popleft()

        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_r + dr, curr_c + dc

            # Check 1: Is neighbor outside the grid? -> Escape condition
            if not (0 <= nr < H and 0 <= nc < W):
                is_escaped = True
                break # Reached grid edge from a target pixel

            neighbor_color = grid[nr, nc]
            neighbor_coord = (nr, nc)

            # Check 2: Is neighbor white (background)? -> Escape condition
            if neighbor_color == 0:
                is_escaped = True
                break # Reached background from a target pixel

            # Check 3: Is neighbor the same color as the target region?
            if neighbor_color == target_color:
                # If not already visited in this search, add to queue and sets
                if neighbor_coord not in visited_during_search:
                    visited_during_search.add(neighbor_coord)
                    region_pixels.add(neighbor_coord)
                    queue.append(neighbor_coord)
            
            # Check 4: Is neighbor a different, non-white color? -> Potential boundary
            else: 
                boundary_colors.add(neighbor_color)

        # If an escape condition was met during neighbor checks, stop the BFS early
        if is_escaped:
            break 

    # Determine enclosure based on BFS results
    # Condition: Not escaped AND exactly one boundary color was found
    is_enclosed = (not is_escaped) and (len(boundary_colors) == 1)
    
    return is_enclosed, region_pixels


def transform(input_grid):
    """
    Identifies contiguous regions of pixels that are fully enclosed by a boundary 
    composed of a single, different non-white color. Changes the color of all 
    pixels within each such enclosed region to white (0). Pixels forming the 
    boundaries and pixels in regions that are not enclosed (touch the grid edge, 
    touch white pixels, or have multi-colored/no boundaries) remain unchanged.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    H, W = grid.shape
    
    # Create a copy of the grid to modify and return
    output_grid = np.copy(grid)
    
    # Create a mask to keep track of pixels that have already been processed 
    # (either identified as enclosed or checked as part of a region).
    # This prevents redundant BFS calls for pixels in the same region.
    processed_mask = np.zeros((H, W), dtype=bool) 

    # Iterate through each pixel in the grid
    for r in range(H):
        for c in range(W):
            # Process only non-white pixels that haven't been processed yet
            if grid[r, c] != 0 and not processed_mask[r, c]:
                
                # Perform BFS to check for enclosure and get the region's pixels
                is_enclosed, region_pixels = check_enclosure_and_get_region(grid, r, c)

                # Mark all pixels in the found region as processed, regardless of enclosure status,
                # to avoid re-checking them later.
                for pr, pc in region_pixels:
                    processed_mask[pr, pc] = True

                # If the region starting at (r, c) is confirmed to be enclosed
                if is_enclosed:
                    # Iterate through all pixels identified as belonging to this enclosed region
                    for er, ec in region_pixels:
                        # Change the color of these pixels to white (0) in the output grid
                        output_grid[er, ec] = 0
                        # Note: processed_mask was already updated for these pixels above.

    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()
```
```python
"""
Identifies contiguous regions of pixels (sharing the same non-white color) 
that are fully enclosed by a boundary composed entirely of a single, different, 
non-white color. The enclosure must be complete, meaning the enclosed region 
cannot touch the grid border or any white (0) pixels. 
If a region is identified as enclosed, all pixels within that region are 
changed to white (0) in the output grid. Pixels forming the boundaries 
and pixels in regions that are not enclosed remain unchanged.
"""

import numpy as np
from collections import deque

def find_contiguous_region(grid, start_r, start_c, processed_mask):
    """
    Finds all connected pixels of the same color as the starting pixel using BFS.
    Marks found pixels as processed in the mask.

    Args:
        grid (np.array): The input grid.
        start_r (int): Starting row index.
        start_c (int): Starting column index.
        processed_mask (np.array): Boolean mask to mark processed pixels.

    Returns:
        set: A set of coordinates {(r, c)} belonging to the contiguous region.
             Returns an empty set if the starting pixel is already processed or white.
    """
    H, W = grid.shape
    target_color = grid[start_r, start_c]

    # Avoid processing background or already processed pixels
    if target_color == 0 or processed_mask[start_r, start_c]:
        return set()

    region_pixels = set()
    queue = deque([(start_r, start_c)])
    
    # Mark the starting pixel as processed immediately
    processed_mask[start_r, start_c] = True
    region_pixels.add((start_r, start_c))

    while queue:
        curr_r, curr_c = queue.popleft()

        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_r + dr, curr_c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < H and 0 <= nc < W:
                neighbor_coord = (nr, nc)
                # Check if neighbor has the target color and hasn't been processed yet
                if grid[nr, nc] == target_color and not processed_mask[nr, nc]:
                    processed_mask[nr, nc] = True # Mark as processed
                    region_pixels.add(neighbor_coord)
                    queue.append(neighbor_coord)
    
    return region_pixels

def check_region_enclosure(grid, region_pixels, target_color):
    """
    Checks if a given region is fully enclosed by a single, non-white color
    different from the target color.

    Args:
        grid (np.array): The input grid.
        region_pixels (set): Set of coordinates {(r, c)} for the region.
        target_color (int): The color of the region being checked.

    Returns:
        bool: True if the region is enclosed, False otherwise.
    """
    H, W = grid.shape
    adjacent_boundary_pixels = set() # Store coords of adjacent pixels not in the region
    boundary_colors = set()         # Store colors of those adjacent pixels
    is_escaped = False              # Flag if region touches edge or background

    # Find all pixels adjacent to the region
    for r, c in region_pixels:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check 1: Neighbor is out of bounds -> Escape condition
            if not (0 <= nr < H and 0 <= nc < W):
                is_escaped = True
                break # Reached grid edge

            neighbor_coord = (nr, nc)
            
            # Check 2: Neighbor is inside the region itself -> Skip
            if neighbor_coord in region_pixels:
                continue

            # Check 3: Neighbor is white (background) -> Escape condition
            if grid[nr, nc] == 0:
                is_escaped = True
                break # Reached background

            # If neighbor is adjacent, not background, and not part of the region, 
            # it's a potential boundary pixel.
            adjacent_boundary_pixels.add(neighbor_coord)

        if is_escaped: # Stop checking neighbors if escaped
            break
            
    # If escaped, the region is not enclosed
    if is_escaped:
        return False

    # If no adjacent boundary pixels were found (e.g., region fills the whole grid or is isolated somehow?)
    # This shouldn't happen if it didn't escape, but handle defensively.
    if not adjacent_boundary_pixels:
        return False

    # Check the colors of the boundary pixels found
    boundary_color_found = None
    for ar, ac in adjacent_boundary_pixels:
        adj_color = grid[ar, ac]
        
        # Boundary pixel color must not be the target color (should be guaranteed by logic above, but check)
        # And must not be background (also checked above)
        if adj_color == target_color or adj_color == 0: 
             # This case indicates a logic error or unexpected input structure
             # print(f"Warning: Unexpected adjacent color {adj_color} found for region color {target_color}")
             return False 

        # If this is the first boundary color encountered
        if boundary_color_found is None:
            boundary_color_found = adj_color
        # If a different boundary color is found -> Not enclosed by a *single* color
        elif adj_color != boundary_color_found:
            return False

    # If we passed all checks: not escaped and exactly one boundary color found
    return boundary_color_found is not None


def transform(input_grid):
    """
    Transforms the input grid by finding enclosed regions and setting their pixels to white (0).
    """
    # Convert input list of lists to NumPy array for easier processing
    grid = np.array(input_grid, dtype=int)
    H, W = grid.shape
    
    # Create a copy to modify for the output
    output_grid = np.copy(grid)
    
    # Create a mask to track pixels already processed as part of a region
    processed_mask = np.zeros((H, W), dtype=bool) 

    # Iterate through each pixel in the grid
    for r in range(H):
        for c in range(W):
            # Check if this pixel is non-white and hasn't been processed yet
            if grid[r, c] != 0 and not processed_mask[r, c]:
                target_color = grid[r, c]
                
                # 1. Find the entire contiguous region starting from (r, c)
                #    This also marks all pixels in the region as processed in the mask.
                region_pixels = find_contiguous_region(grid, r, c, processed_mask)

                # If a valid region was found (find_contiguous_region handles the initial check)
                if region_pixels: 
                    # 2. Check if this identified region is enclosed
                    is_enclosed = check_region_enclosure(grid, region_pixels, target_color)

                    # 3. If the region is enclosed, change its pixels to white (0) in the output grid
                    if is_enclosed:
                        for pr, pc in region_pixels:
                            output_grid[pr, pc] = 0

    # Convert the final NumPy array back to a list of lists for the required output format
    return output_grid.tolist()
```
