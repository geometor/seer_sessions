
## train_1

**input:**
```
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0 0 0 6 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 6 6 6 6 6 0 0 0 0 0
0 0 6 6 6 6 6 6 6 0 0 0 0
0 0 0 6 6 6 6 6 6 6 0 0 0
0 0 0 0 6 6 6 6 6 6 6 0 0
0 0 0 0 0 6 6 6 6 6 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 3 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 3 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0
0 3 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the task examples.

**Perception of Elements:**

1.  **Train_1 Example:**
    *   The input grid contains several scattered magenta (6) pixels against a white (0) background. These pixels are not connected to each other.
    *   The output grid retains the original magenta pixels and fills the area "between" them with more magenta pixels. The resulting shape looks like the convex hull of the initial set of magenta points.
2.  **Train_2 Example:**
    *   The input grid contains a single, solid, connected green (3) diamond shape against a white (0) background.
    *   The output grid shows only the outline or border pixels of the input diamond shape in green. The interior pixels of the diamond have been changed to white (0).

**Analysis:**

The task seems to involve two distinct transformations based on the properties of the non-white pixels in the input:

*   **Case 1 (Scattered Points):** If the input contains multiple disconnected pixels of the same color, the transformation finds the smallest convex polygon enclosing all these points (the convex hull) and fills this polygon with the input color.
*   **Case 2 (Solid Object):** If the input contains a single, connected, solid object of one color, the transformation extracts the boundary/outline of this object, keeping only the boundary pixels and changing the interior pixels to the background color (white).

The key distinguishing factor appears to be whether the non-white pixels form a single connected component or are scattered as multiple individual points/components.

**YAML Facts:**


```yaml
task_description: Apply one of two transformations based on the connectivity of non-white pixels.

example_1:
  input_features:
    - objects: Multiple disconnected magenta (6) pixels.
    - arrangement: Scattered points.
    - background_color: white (0)
  output_features:
    - objects: A single solid magenta (6) object.
    - shape: Convex hull of the input points.
    - background_color: white (0)
  action:
    - type: Geometric construction
    - name: Convex Hull Filling
    - description: Find the convex hull of the input magenta pixels and fill the enclosed area with magenta.

example_2:
  input_features:
    - objects: A single connected green (3) object.
    - shape: Diamond (filled).
    - background_color: white (0)
  output_features:
    - objects: Multiple connected green (3) pixels forming an outline.
    - shape: Diamond (outline).
    - background_color: white (0)
  action:
    - type: Boundary extraction
    - name: Outline Finding
    - description: Identify the boundary pixels of the input green object and discard the interior pixels (set to white).

general_logic:
  condition: Check connectivity of non-white pixels (using 8-way adjacency, including diagonals).
  if_single_connected_object: Apply Outline Finding.
  if_multiple_disconnected_pixels_or_objects: Apply Convex Hull Filling using the color of the input pixels.
```


**Natural Language Program:**

1.  Identify all non-white pixels in the input grid and determine their color (let's call it `C`). Record their coordinates.
2.  Analyze the connectivity of these non-white pixels (using 8-way adjacency, considering diagonal neighbors). Determine if they form a single connected component or multiple disconnected components/pixels.
3.  **If** the non-white pixels form a *single connected component*:
    a.  Create a new grid of the same dimensions as the input, filled with the background color (white, 0).
    b.  Iterate through each non-white pixel (`P`) of color `C` in the input grid.
    c.  Check if `P` has at least one neighbor (including diagonals) that is the background color (white, 0).
    d.  If `P` has a background-colored neighbor, mark the corresponding pixel in the new grid with color `C`.
    e.  The resulting new grid is the output.
4.  **Else (if** the non-white pixels are *not* a single connected component):
    a.  Create a new grid of the same dimensions as the input, filled with the background color (white, 0).
    b.  Find the set of all coordinates `(row, col)` corresponding to the non-white pixels.
    c.  Calculate the convex hull polygon enclosing this set of coordinates.
    d.  Iterate through every pixel `(r, c)` in the new grid.
    e.  If the pixel `(r, c)` lies inside or on the boundary of the calculated convex hull polygon, set its color to `C`.
    f.  The resulting new grid is the output.
```python
import numpy as np
from scipy.spatial import ConvexHull
from skimage.measure import label
from skimage.draw import polygon

"""
Identify all non-white pixels (color C) in the input grid.
Determine if these pixels form a single connected component (8-way adjacency) or multiple components.

If a single connected component exists:
  Keep only the boundary pixels of this component (pixels of color C that are adjacent, including diagonally, to at least one white pixel).
  Change the interior pixels of the component to white.

If multiple disconnected components/pixels exist:
  Calculate the convex hull enclosing all non-white pixel coordinates.
  Fill the area inside and on the boundary of this convex hull with color C.
  The rest of the grid remains white.
"""

def find_non_background_pixels(grid_np, background_color=0):
    """Finds coordinates and the unique color of non-background pixels."""
    coords = np.argwhere(grid_np != background_color)
    if coords.size == 0:
        return [], -1  # No non-background pixels
    
    colors = grid_np[coords[:, 0], coords[:, 1]]
    unique_colors = np.unique(colors)
    
    if len(unique_colors) > 1:
         # This specific task seems to assume only one non-background color
         # Handle error or specific logic if multiple colors are possible
         # For now, let's take the first one found or the most frequent one
         print(f"Warning: Multiple non-background colors found: {unique_colors}. Using {unique_colors[0]}.")
         main_color = unique_colors[0]
         # Filter coords for the main color if necessary, but the logic seems to operate on all non-bg collectively
    elif len(unique_colors) == 1:
        main_color = unique_colors[0]
    else: # Should not happen if coords.size > 0
        return [], -1
        
    # Return coordinates as list of tuples for easier processing later
    return [tuple(coord) for coord in coords], main_color

def check_connectivity(grid_np, background_color=0):
    """Checks the connectivity of non-background pixels."""
    binary_grid = (grid_np != background_color).astype(int)
    # Use connectivity=2 for 8-way adjacency (including diagonals)
    labeled_grid, num_labels = label(binary_grid, connectivity=2, background=0, return_num=True)
    return num_labels

def find_outline(grid_np, non_bg_coords, color, background_color=0):
    """Keeps only boundary pixels of a single connected component."""
    output_grid = np.full(grid_np.shape, background_color, dtype=int)
    rows, cols = grid_np.shape
    
    for r, c in non_bg_coords:
        is_boundary = False
        # Check 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip self
                
                nr, nc = r + dr, c + dc
                
                # Check bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid_np[nr, nc] == background_color:
                        is_boundary = True
                        break # Found a background neighbor, it's a boundary pixel
                else:
                    # Pixel is on the grid edge, implicitly adjacent to 'outside' which we can consider background
                    is_boundary = True
                    break
            if is_boundary:
                break
                
        if is_boundary:
            output_grid[r, c] = color
            
    return output_grid

def fill_convex_hull(grid_shape, non_bg_coords, color, background_color=0):
    """Fills the convex hull of the given coordinates."""
    output_grid = np.full(grid_shape, background_color, dtype=int)
    
    if not non_bg_coords:
        return output_grid # Return empty grid if no points
        
    points = np.array(non_bg_coords)
    
    if len(points) <= 2:
        # Handle cases with 0, 1 or 2 points (line)
        for r, c in non_bg_coords:
             # Check bounds just in case, though coords should be valid
             if 0 <= r < grid_shape[0] and 0 <= c < grid_shape[1]:
                 output_grid[r, c] = color
        # If 2 points, draw a line? The examples don't cover this.
        # For now, just color the points themselves. Convex hull isn't well-defined.
        # Example 1 implies filling, maybe just draw the points if hull fails.
        # Let's stick to coloring just the points for < 3 points.
        return output_grid

    try:
        hull = ConvexHull(points)
        # Get the vertices of the hull
        hull_vertices = points[hull.vertices]
        
        # Use skimage.draw.polygon to get all points inside the hull
        # Note: polygon needs row and column coordinates separately
        rr, cc = polygon(hull_vertices[:, 0], hull_vertices[:, 1], shape=grid_shape)
        
        # Ensure coordinates are within bounds (polygon might sometimes slightly exceed?)
        valid_indices = (rr >= 0) & (rr < grid_shape[0]) & (cc >= 0) & (cc < grid_shape[1])
        rr_valid = rr[valid_indices]
        cc_valid = cc[valid_indices]

        output_grid[rr_valid, cc_valid] = color
        
    except Exception as e:
        # ConvexHull can fail if points are collinear
        print(f"Convex Hull calculation failed: {e}. Coloring original points.")
        # Fallback: just color the original points if hull fails
        for r, c in non_bg_coords:
            if 0 <= r < grid_shape[0] and 0 <= c < grid_shape[1]:
                output_grid[r, c] = color

    return output_grid

def transform(input_grid):
    """
    Applies transformation based on connectivity of non-background pixels.
    - If single connected component: Extracts the outline.
    - If multiple components: Fills the convex hull.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    
    # Find non-background pixels and their color
    non_bg_coords, color = find_non_background_pixels(input_grid_np)
    
    # Handle edge case: no non-background pixels
    if not non_bg_coords:
        return input_grid # Return original grid if nothing to transform
        
    # Check connectivity
    num_components = check_connectivity(input_grid_np)
    
    # Apply transformation based on connectivity
    if num_components == 1:
        # Single component -> Find outline
        output_grid_np = find_outline(input_grid_np, non_bg_coords, color)
    else: # num_components > 1 or num_components == 0 (but handled above)
        # Multiple components -> Fill convex hull
        output_grid_np = fill_convex_hull(input_grid_np.shape, non_bg_coords, color)
        
    # Convert back to list of lists
    output_grid = output_grid_np.tolist()
    
    return output_grid

```
```python
import numpy as np
from scipy.spatial import ConvexHull
from skimage.measure import label
from skimage.draw import polygon
import math # Import math for potential use, though not strictly needed for hull/polygon

"""
Transforms the input grid based on the connectivity of its non-background pixels (assuming white '0' is background).

1.  If the non-background pixels form a single connected component (using 8-way adjacency), 
    the output grid contains only the boundary pixels of that component. Boundary pixels are 
    those non-background pixels adjacent (including diagonally) to at least one background pixel 
    or the grid edge.

2.  If the non-background pixels form multiple disconnected components (or are isolated pixels),
    the output grid is the original grid with the area defined by the convex hull of all 
    non-background pixels filled with their color. If fewer than 3 non-background pixels exist,
    only those pixels are colored in the output.
"""

def find_non_background_pixels(grid_np, background_color=0):
    """Finds coordinates and the unique color of non-background pixels."""
    coords = np.argwhere(grid_np != background_color)
    if coords.size == 0:
        return [], -1  # No non-background pixels, return empty list and invalid color

    # Extract colors at found coordinates
    colors = grid_np[coords[:, 0], coords[:, 1]]
    unique_colors = np.unique(colors)

    # Assuming a single non-background color per task based on examples
    if len(unique_colors) == 1:
        main_color = int(unique_colors[0]) # Convert numpy dtype to standard int
    elif len(unique_colors) > 1:
        # Fallback: use the most frequent color or the first one if tie.
        # This might need adjustment based on specific task rules if multiple colors appear.
        print(f"Warning: Multiple non-background colors found: {unique_colors}. Using the first one: {unique_colors[0]}.")
        main_color = int(unique_colors[0])
        # Filter coordinates to only include those of the main color
        # Although the logic branches based on connectivity of *all* non-bg pixels together.
        # Let's return all coords but identify the primary color to use for drawing.
    else: # Should not happen if coords.size > 0
         return [], -1

    # Return coordinates as list of tuples (standard ints) for easier processing
    return [tuple(map(int, coord)) for coord in coords], main_color

def check_connectivity(grid_np, background_color=0):
    """Checks the connectivity of non-background pixels using 8-way adjacency."""
    # Create a binary grid: 1 for non-background, 0 for background
    binary_grid = (grid_np != background_color).astype(int)
    # Label connected components using 8-way connectivity
    # connectivity=2 corresponds to 8-way adjacency in skimage.measure.label
    labeled_grid, num_labels = label(binary_grid, connectivity=2, background=0, return_num=True)
    return int(num_labels) # Return the number of distinct components found

def find_outline(grid_np, non_bg_coords, color, background_color=0):
    """Keeps only boundary pixels of a single connected component."""
    output_grid = np.full(grid_np.shape, background_color, dtype=int)
    rows, cols = grid_np.shape

    for r, c in non_bg_coords:
        is_boundary = False
        # Check 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the pixel itself

                nr, nc = r + dr, c + dc

                # Check if neighbor is outside grid bounds
                if not (0 <= nr < rows and 0 <= nc < cols):
                    is_boundary = True  # Pixel is on the edge, thus a boundary pixel
                    break
                # Check if neighbor is background color
                elif grid_np[nr, nc] == background_color:
                    is_boundary = True
                    break # Found a background neighbor, it's a boundary pixel

            if is_boundary:
                break # No need to check further neighbors for this pixel

        # If it was determined to be a boundary pixel, color it in the output
        if is_boundary:
            output_grid[r, c] = color

    return output_grid

def fill_convex_hull(grid_shape, non_bg_coords, color, background_color=0):
    """Fills the convex hull of the given coordinates."""
    output_grid = np.full(grid_shape, background_color, dtype=int)

    if not non_bg_coords:
        return output_grid # Return empty grid if no points

    points = np.array(non_bg_coords)

    # Handle cases with fewer than 3 points where ConvexHull is not defined or is trivial
    if len(points) < 3:
        for r, c in non_bg_coords:
             # Ensure coordinates are within bounds before coloring
             if 0 <= r < grid_shape[0] and 0 <= c < grid_shape[1]:
                 output_grid[r, c] = color
        return output_grid

    try:
        # Calculate the convex hull
        hull = ConvexHull(points)
        # Get the vertices of the hull polygon
        hull_vertices = points[hull.vertices]

        # Get all integer coordinates inside the polygon defined by hull_vertices
        # Note: polygon requires row and column coordinates separately
        rr, cc = polygon(hull_vertices[:, 0], hull_vertices[:, 1], shape=grid_shape)

        # Ensure coordinates from polygon are within grid bounds before coloring
        valid_indices = (rr >= 0) & (rr < grid_shape[0]) & (cc >= 0) & (cc < grid_shape[1])
        rr_valid = rr[valid_indices]
        cc_valid = cc[valid_indices]

        # Color the pixels inside the hull
        output_grid[rr_valid, cc_valid] = color

    except Exception as e:
        # ConvexHull can fail if points are collinear or other geometric issues occur.
        # Or polygon rasterization might have issues.
        print(f"Convex Hull / Polygon filling failed: {e}. Coloring original points as fallback.")
        # Fallback: color the original non-background points if hull calculation/filling fails
        for r, c in non_bg_coords:
            if 0 <= r < grid_shape[0] and 0 <= c < grid_shape[1]:
                output_grid[r, c] = color

    return output_grid


def transform(input_grid):
    """
    Applies the transformation logic: outline for single component, convex hull fill for multiple.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    background_color = 0 # Assuming background is always 0

    # Find the non-background pixels and their primary color
    non_bg_coords, color = find_non_background_pixels(input_grid_np, background_color)

    # If there are no non-background pixels, return the original grid
    if not non_bg_coords:
        return input_grid

    # Check the connectivity of these pixels
    num_components = check_connectivity(input_grid_np, background_color)

    # --- Apply transformation based on connectivity ---
    if num_components == 1:
        # Case 1: Single connected component -> Find its outline
        output_grid_np = find_outline(input_grid_np, non_bg_coords, color, background_color)
    else: # Case 2: Multiple components (num_components > 1) or potentially 0 if logic missed edge case
        # Fill the convex hull defined by the points
        output_grid_np = fill_convex_hull(input_grid_np.shape, non_bg_coords, color, background_color)

    # Convert the resulting numpy array back to a list of lists for the expected output format
    output_grid = output_grid_np.tolist()

    return output_grid

```

Previous Code:
```python
import numpy as np
from scipy.spatial import ConvexHull
from skimage.measure import label
from skimage.draw import polygon
import math # Import math for potential use, though not strictly needed for hull/polygon

"""
Transforms the input grid based on the connectivity of its non-background pixels (assuming white '0' is background).

1.  If the non-background pixels form a single connected component (using 8-way adjacency), 
    the output grid contains only the boundary pixels of that component. Boundary pixels are 
    those non-background pixels adjacent (including diagonally) to at least one background pixel 
    or the grid edge.

2.  If the non-background pixels form multiple disconnected components (or are isolated pixels),
    the output grid is the original grid with the area defined by the convex hull of all 
    non-background pixels filled with their color. If fewer than 3 non-background pixels exist,
    only those pixels are colored in the output.
"""

def find_non_background_pixels(grid_np, background_color=0):
    """Finds coordinates and the unique color of non-background pixels."""
    coords = np.argwhere(grid_np != background_color)
    if coords.size == 0:
        return [], -1  # No non-background pixels, return empty list and invalid color

    # Extract colors at found coordinates
    colors = grid_np[coords[:, 0], coords[:, 1]]
    unique_colors = np.unique(colors)

    # Assuming a single non-background color per task based on examples
    if len(unique_colors) == 1:
        main_color = int(unique_colors[0]) # Convert numpy dtype to standard int
    elif len(unique_colors) > 1:
        # Fallback: use the most frequent color or the first one if tie.
        # This might need adjustment based on specific task rules if multiple colors appear.
        print(f"Warning: Multiple non-background colors found: {unique_colors}. Using the first one: {unique_colors[0]}.")
        main_color = int(unique_colors[0])
        # Filter coordinates to only include those of the main color
        # Although the logic branches based on connectivity of *all* non-bg pixels together.
        # Let's return all coords but identify the primary color to use for drawing.
    else: # Should not happen if coords.size > 0
         return [], -1

    # Return coordinates as list of tuples (standard ints) for easier processing
    return [tuple(map(int, coord)) for coord in coords], main_color

def check_connectivity(grid_np, background_color=0):
    """Checks the connectivity of non-background pixels using 8-way adjacency."""
    # Create a binary grid: 1 for non-background, 0 for background
    binary_grid = (grid_np != background_color).astype(int)
    # Label connected components using 8-way connectivity
    # connectivity=2 corresponds to 8-way adjacency in skimage.measure.label
    labeled_grid, num_labels = label(binary_grid, connectivity=2, background=0, return_num=True)
    return int(num_labels) # Return the number of distinct components found

def find_outline(grid_np, non_bg_coords, color, background_color=0):
    """Keeps only boundary pixels of a single connected component."""
    output_grid = np.full(grid_np.shape, background_color, dtype=int)
    rows, cols = grid_np.shape

    for r, c in non_bg_coords:
        is_boundary = False
        # Check 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the pixel itself

                nr, nc = r + dr, c + dc

                # Check if neighbor is outside grid bounds
                if not (0 <= nr < rows and 0 <= nc < cols):
                    is_boundary = True  # Pixel is on the edge, thus a boundary pixel
                    break
                # Check if neighbor is background color
                elif grid_np[nr, nc] == background_color:
                    is_boundary = True
                    break # Found a background neighbor, it's a boundary pixel

            if is_boundary:
                break # No need to check further neighbors for this pixel

        # If it was determined to be a boundary pixel, color it in the output
        if is_boundary:
            output_grid[r, c] = color

    return output_grid

def fill_convex_hull(grid_shape, non_bg_coords, color, background_color=0):
    """Fills the convex hull of the given coordinates."""
    output_grid = np.full(grid_shape, background_color, dtype=int)

    if not non_bg_coords:
        return output_grid # Return empty grid if no points

    points = np.array(non_bg_coords)

    # Handle cases with fewer than 3 points where ConvexHull is not defined or is trivial
    if len(points) < 3:
        for r, c in non_bg_coords:
             # Ensure coordinates are within bounds before coloring
             if 0 <= r < grid_shape[0] and 0 <= c < grid_shape[1]:
                 output_grid[r, c] = color
        return output_grid

    try:
        # Calculate the convex hull
        hull = ConvexHull(points)
        # Get the vertices of the hull polygon
        hull_vertices = points[hull.vertices]

        # Get all integer coordinates inside the polygon defined by hull_vertices
        # Note: polygon requires row and column coordinates separately
        rr, cc = polygon(hull_vertices[:, 0], hull_vertices[:, 1], shape=grid_shape)

        # Ensure coordinates from polygon are within grid bounds before coloring
        valid_indices = (rr >= 0) & (rr < grid_shape[0]) & (cc >= 0) & (cc < grid_shape[1])
        rr_valid = rr[valid_indices]
        cc_valid = cc[valid_indices]

        # Color the pixels inside the hull
        output_grid[rr_valid, cc_valid] = color

    except Exception as e:
        # ConvexHull can fail if points are collinear or other geometric issues occur.
        # Or polygon rasterization might have issues.
        print(f"Convex Hull / Polygon filling failed: {e}. Coloring original points as fallback.")
        # Fallback: color the original non-background points if hull calculation/filling fails
        for r, c in non_bg_coords:
            if 0 <= r < grid_shape[0] and 0 <= c < grid_shape[1]:
                output_grid[r, c] = color

    return output_grid


def transform(input_grid):
    """
    Applies the transformation logic: outline for single component, convex hull fill for multiple.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    background_color = 0 # Assuming background is always 0

    # Find the non-background pixels and their primary color
    non_bg_coords, color = find_non_background_pixels(input_grid_np, background_color)

    # If there are no non-background pixels, return the original grid
    if not non_bg_coords:
        return input_grid

    # Check the connectivity of these pixels
    num_components = check_connectivity(input_grid_np, background_color)

    # --- Apply transformation based on connectivity ---
    if num_components == 1:
        # Case 1: Single connected component -> Find its outline
        output_grid_np = find_outline(input_grid_np, non_bg_coords, color, background_color)
    else: # Case 2: Multiple components (num_components > 1) or potentially 0 if logic missed edge case
        # Fill the convex hull defined by the points
        output_grid_np = fill_convex_hull(input_grid_np.shape, non_bg_coords, color, background_color)

    # Convert the resulting numpy array back to a list of lists for the expected output format
    output_grid = output_grid_np.tolist()

    return output_grid

```
Results for code_00.py:
Train Set Error: error:
No module named 'skimage'
Okay, let's analyze the situation and refine the plan.

**General Assessment:**

The primary issue is the `No module named 'skimage'` error. The previous code relied on `skimage` for connected components analysis (`skimage.measure.label`) and polygon filling (`skimage.draw.polygon`). The core logic, distinguishing between single connected components (requiring outline extraction) and multiple components/pixels (requiring convex hull filling), appears correct based on the two examples.

**Strategy:**

1.  **Replace Dependencies:** Implement the necessary functionalities (connectivity check, polygon filling) using standard Python libraries, `numpy`, and potentially `scipy.spatial` if it's available (unlike `skimage`).
    *   **Connectivity:** Replace `skimage.measure.label` with a custom Breadth-First Search (BFS) or Depth-First Search (DFS) algorithm to count connected components of non-background pixels using 8-way adjacency.
    *   **Convex Hull:** Continue assuming `scipy.spatial.ConvexHull` might be available. If it's not, this task branch cannot be fully implemented as specified, and a fallback (like coloring only the original points) would be necessary.
    *   **Polygon Filling:** Replace `skimage.draw.polygon` with a custom point-in-polygon test (e.g., ray casting algorithm) applied to pixels within the bounding box of the hull, or potentially rasterize the polygon edges and fill.
2.  **Refine Logic:** Ensure the outline detection and convex hull filling algorithms handle grid boundaries and edge cases correctly.
3.  **Update Documentation:** Update the YAML facts and Natural Language Program to reflect the refined algorithms and remove specific library dependencies where replaced.

**Metrics and Analysis (Manual):**

*   **train_1:**
    *   Input: 13x13 grid. 9 magenta (6) pixels. Background: white (0).
    *   Connectivity Analysis: The 9 magenta pixels are disconnected. Number of components = 9.
    *   Expected Action: Convex Hull Filling.
    *   Output: 13x13 grid. A filled magenta shape approximating the convex hull of the input points. Background: white (0).
*   **train_2:**
    *   Input: 9x12 grid. 25 green (3) pixels forming a filled diamond. Background: white (0).
    *   Connectivity Analysis: The 25 green pixels form a single connected component (8-way adjacency). Number of components = 1.
    *   Expected Action: Outline Finding.
    *   Output: 9x12 grid. 16 green (3) pixels forming the outline of the input diamond. Interior is white (0). Background: white (0).

**YAML Facts:**


```yaml
task_description: Transforms grid based on non-background pixel connectivity.

constants:
  background_color: 0 # white
  adjacency: 8 # 8-way including diagonals

input_properties:
  - grid: 2D array of integers (colors)
  - non_background_pixels: All pixels with color != background_color
  - unique_color: The single color value of all non_background_pixels (assumption based on examples)
  - coordinates: List of (row, col) tuples for non_background_pixels

derived_properties:
  - connectivity: Number of connected components formed by non_background_pixels using specified adjacency.

logic_branches:
  - condition: connectivity == 1
    action: Outline Extraction
      - description: Identify boundary pixels of the single component. A pixel is boundary if it is adjacent (using specified adjacency) to a background_color pixel or the grid edge.
      - output_grid: Contains only the boundary pixels with their original unique_color, rest is background_color.
  - condition: connectivity > 1
    action: Convex Hull Filling
      - description: Calculate the convex hull polygon enclosing all non_background_pixel coordinates. Fill the area inside and on the boundary of this hull.
      - prerequisites: Requires a method to calculate convex hull (e.g., from scipy.spatial) and fill a polygon (e.g., point-in-polygon test).
      - output_grid: Contains pixels inside or on the hull boundary colored with unique_color, rest is background_color.
      - fallback (if < 3 points or hull fails): Color only the original non_background_pixels.

example_1_specifics:
  input_color: 6 # magenta
  input_connectivity: 9 (> 1)
  applied_action: Convex Hull Filling

example_2_specifics:
  input_color: 3 # green
  input_connectivity: 1
  applied_action: Outline Extraction
```


**Natural Language Program:**

1.  Define the background color as white (0).
2.  Identify all non-background pixels in the input grid. Record their coordinates and their single unique color (`C`). If no non-background pixels exist, return the input grid unchanged.
3.  Determine the number of connected components formed by these non-background pixels using 8-way adjacency (pixels are connected if they touch horizontally, vertically, or diagonally). This can be done using a graph traversal algorithm like Breadth-First Search (BFS):
    *   Initialize a 'visited' set for coordinates.
    *   Initialize a component counter to 0.
    *   Iterate through each non-background pixel coordinate `(r, c)`.
    *   If `(r, c)` is not visited:
        *   Increment the component counter.
        *   Start a BFS from `(r, c)`. Add `(r, c)` to the queue and the visited set.
        *   While the queue is not empty:
            *   Dequeue a coordinate `(curr_r, curr_c)`.
            *   Find all its 8 neighbors `(nr, nc)`.
            *   For each neighbor that is within grid bounds, is a non-background pixel, and is not visited: add it to the queue and the visited set.
    *   The final value of the component counter is the connectivity.
4.  **If** the connectivity is exactly 1:
    *   Create a new output grid of the same dimensions, filled with the background color.
    *   For each original non-background pixel `P` at `(r, c)`:
        *   Check its 8 neighbors `(nr, nc)`.
        *   If any neighbor is outside the grid boundaries OR has the background color in the input grid, then `P` is a boundary pixel.
        *   If `P` is a boundary pixel, set the corresponding pixel `(r, c)` in the output grid to color `C`.
    *   Return the output grid.
5.  **Else (if** the connectivity is greater than 1):
    *   Create a new output grid of the same dimensions, filled with the background color.
    *   If the number of non-background pixels is less than 3, simply color these pixels in the output grid with color `C` and return the grid.
    *   Otherwise (3 or more pixels):
        *   Attempt to compute the convex hull polygon using the coordinates of the non-background pixels. (Requires a suitable algorithm, potentially from `scipy.spatial`).
        *   If hull computation fails (e.g., points are collinear, library unavailable), color only the original non-background pixels in the output grid with color `C` and return the grid.
        *   If hull computation succeeds, determine the vertices of the hull polygon.
        *   Iterate through each pixel `(r, c)` within the bounding box of the hull vertices (or the whole grid).
        *   Test if the point `(r, c)` lies inside or on the boundary of the hull polygon (e.g., using a ray casting algorithm or similar point-in-polygon test).
        *   If the point `(r, c)` is inside or on the hull, set the corresponding pixel in the output grid to color `C`.
    *   Return the output grid.
