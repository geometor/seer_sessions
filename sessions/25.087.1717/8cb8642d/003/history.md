
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies contiguous shapes of a single non-white color in the input grid. 
For each shape, it checks if it contains exactly one 'marker' pixel of a different color.
If a marker is found, a diamond-shaped boundary pattern is drawn expanding outwards from the marker's location using the marker's color. 
The pattern only colors pixels that originally belonged to the shape (had the shape's primary color). 
The expansion stops when the pattern reaches pixels that were not part of the original shape.
All pixels that originally belonged to the shape but were not colored by the diamond pattern (including the original marker pixel) are then set to white (0).
Shapes without a marker remain unchanged.
"""

def find_shapes_and_markers(grid):
    """
    Finds contiguous shapes of non-white colors and identifies any single marker pixel within them.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a shape and contains:
              'coords': set of (row, col) tuples for the shape.
              'color': the primary color of the shape.
              'marker_coord': (row, col) of the marker, or None.
              'marker_color': color of the marker, or None.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    shapes = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                # Found the start of a potential shape
                q = deque([(r, c)])
                visited[r, c] = True
                shape_coords = set([(r, c)])
                potential_primary_color = grid[r,c]
                possible_markers = [] # Store potential markers (different color)

                while q:
                    row, col = q.popleft()
                    
                    # Check neighbors (4-directional connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and not visited[nr, nc] and grid[nr, nc] != 0:
                             # If neighbor color matches potential primary, add to shape
                            if grid[nr, nc] == potential_primary_color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                shape_coords.add((nr, nc))
                            # If neighbor color is different, it's a potential marker
                            else:
                                # Only add if not already visited as part of *this* shape search
                                # This handles cases where a marker touches the main color block
                                if (nr, nc) not in shape_coords:
                                    possible_markers.append(((nr,nc), grid[nr,nc]))
                                    # Mark as visited to avoid starting a new shape from the marker
                                    visited[nr, nc] = True 
                                    shape_coords.add((nr, nc)) # Add marker coord to shape area initially

                # Analyze potential markers found for this connected component
                actual_marker_coord = None
                actual_marker_color = None
                primary_color = potential_primary_color # Assume initially
                final_shape_coords = set() # Recalculate coords excluding marker if necessary

                markers_found = []
                non_primary_coords = set()

                # First pass: Identify the dominant color and potential markers within the found coords
                color_counts = {}
                for sr, sc in shape_coords:
                   color = grid[sr, sc]
                   color_counts[color] = color_counts.get(color, 0) + 1
                
                if not color_counts: continue # Skip if shape is empty (shouldn't happen with logic)

                # Determine primary color (most frequent)
                primary_color = max(color_counts, key=color_counts.get)
                
                # Second pass: Separate primary coords and marker coords
                for sr, sc in shape_coords:
                    color = grid[sr, sc]
                    if color == primary_color:
                        final_shape_coords.add((sr, sc))
                    else:
                        markers_found.append(((sr, sc), color))
                        non_primary_coords.add((sr,sc))

                # Check if exactly one marker pixel exists
                if len(markers_found) == 1:
                    actual_marker_coord, actual_marker_color = markers_found[0]
                    # Ensure the marker coord is NOT included in the coords to be cleared/patterned initially
                    # The final clearing step will handle the marker coord location.
                    # The 'final_shape_coords' should only contain pixels of the primary color.

                # Store the shape details
                shapes.append({
                    'coords': final_shape_coords, # Only coords with primary color
                    'color': primary_color,
                    'marker_coord': actual_marker_coord,
                    'marker_color': actual_marker_color,
                    'all_coords_incl_marker' : shape_coords # Keep track of full extent for bounds checks if needed
                })


    return shapes


def transform(input_grid):
    """
    Transforms the input grid based on the diamond pattern rule for shapes with markers.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Find all shapes and their potential markers
    shapes = find_shapes_and_markers(input_np)

    # Process each shape
    for shape in shapes:
        if shape['marker_coord'] is not None:
            # This shape has a single marker, apply the transformation
            marker_r, marker_c = shape['marker_coord']
            marker_color = shape['marker_color']
            primary_color = shape['color']
            shape_primary_coords = shape['coords'] # Coords with the primary color

            pixels_colored_by_pattern = set()
            
            # Expand diamond pattern layer by layer (Manhattan distance)
            d = 1
            while True:
                colored_in_this_layer = False
                coords_at_distance_d = []

                # Generate coordinates at distance d
                for i in range(d + 1):
                    j = d - i
                    # Check all four quadrants relative to the marker
                    coords_at_distance_d.append((marker_r + i, marker_c + j))
                    if i != 0: coords_at_distance_d.append((marker_r - i, marker_c + j))
                    if j != 0: coords_at_distance_d.append((marker_r + i, marker_c - j))
                    if i != 0 and j != 0: coords_at_distance_d.append((marker_r - i, marker_c - j))
                
                # Filter and color valid coordinates
                for r, c in coords_at_distance_d:
                    # Check grid bounds
                    if 0 <= r < height and 0 <= c < width:
                         # Check if the target pixel originally belonged to the shape's primary color area
                         if (r,c) in shape_primary_coords:
                             output_np[r, c] = marker_color
                             pixels_colored_by_pattern.add((r, c))
                             colored_in_this_layer = True
                
                # Stop if no pixels were colored in this layer (pattern hit boundary or filled area)
                if not colored_in_this_layer:
                    break
                
                d += 1 # Move to the next distance layer

            # Clear the remaining interior pixels (including marker position) to white (0)
            # Iterate through all coordinates that originally had the primary color
            for r, c in shape_primary_coords:
                # If a pixel was not colored by the diamond pattern, set it to white
                if (r, c) not in pixels_colored_by_pattern:
                    output_np[r, c] = 0
            
            # Also explicitly clear the original marker position to white
            if shape['marker_coord'] is not None:
                 mr, mc = shape['marker_coord']
                 # Check if marker coord is within bounds (should always be)
                 if 0 <= mr < height and 0 <= mc < width:
                    # Ensure it wasn't somehow colored by the pattern (shouldn't happen as d starts at 1)
                    if (mr, mc) not in pixels_colored_by_pattern:
                         output_np[mr, mc] = 0


    return output_np.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 6 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 6 0 0 0 0 0 6 3 0 0 0
0 0 3 0 6 0 0 0 6 0 3 0 0 0
0 0 3 0 0 6 0 6 0 0 3 0 0 0
0 0 3 0 0 0 6 0 0 0 3 0 0 0
0 0 3 0 0 0 6 0 0 0 3 0 0 0
0 0 3 0 0 6 0 6 0 0 3 0 0 0
0 0 3 0 6 0 0 0 6 0 3 0 0 0
0 0 3 6 0 0 0 0 0 6 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 6 6 6 0 0 0
0 0 6 6 6 6 6 6 6 0 6 0 0 0
0 0 6 6 6 6 6 6 6 6 6 0 0 0
0 0 6 6 6 6 6 6 6 6 6 0 0 0
0 0 6 6 6 6 6 6 6 6 6 0 0 0
0 0 6 6 6 6 6 6 6 6 6 0 0 0
0 0 6 6 6 6 6 6 6 6 6 0 0 0
0 0 6 6 6 6 6 6 6 6 6 0 0 0
0 0 6 6 6 6 6 6 6 6 6 0 0 0
0 0 6 6 6 6 6 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 77
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 84.61538461538463

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 2 1 2 2 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 2 1 0 0 0 0 1 2 0 0 0 0 0 0
0 2 0 1 0 0 1 0 2 0 0 0 0 0 0
0 2 0 0 1 1 0 0 2 0 0 0 0 0 0
0 2 0 1 0 0 1 0 2 0 0 0 0 0 0
0 2 1 0 0 0 0 1 2 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 0 0 0 0 0 0
0 1 0 1 1 1 1 1 1 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 47
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 52.22222222222223

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 0 0 3 3 3 3 3 3 0
0 0 1 1 1 1 1 1 1 0 0 3 3 3 3 2 3 0
0 0 1 1 1 1 1 1 1 0 0 3 3 3 3 3 3 0
0 0 1 1 1 1 1 1 1 0 0 3 3 3 3 3 3 0
0 0 1 1 1 1 1 1 1 0 0 3 3 3 3 3 3 0
0 0 1 1 1 1 1 2 1 0 0 3 3 3 3 3 3 0
0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 4 3 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 0 0 3 3 3 3 3 3 0
0 0 1 2 0 0 0 2 1 0 0 3 2 0 0 2 3 0
0 0 1 0 2 0 2 0 1 0 0 3 0 2 2 0 3 0
0 0 1 0 0 2 0 0 1 0 0 3 0 2 2 0 3 0
0 0 1 0 2 0 2 0 1 0 0 3 2 0 0 2 3 0
0 0 1 2 0 0 0 2 1 0 0 3 3 3 3 3 3 0
0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 4 3 0 0 0 0 0 0 0 3 4 0
0 0 0 0 0 0 4 0 3 0 0 0 0 0 3 0 4 0
0 0 0 0 0 0 4 0 0 3 3 3 3 3 0 0 4 0
0 0 0 0 0 0 4 0 3 0 0 0 0 0 3 0 4 0
0 0 0 0 0 0 4 3 0 0 0 0 0 0 0 3 4 0
0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 0 0 2 2 2 2 2 2 0
0 0 2 2 2 2 2 2 2 0 0 2 2 2 2 0 2 0
0 0 2 2 2 2 2 2 2 0 0 2 2 2 2 2 2 0
0 0 2 2 2 2 2 2 2 0 0 2 2 2 2 2 2 0
0 0 2 2 2 2 2 2 2 0 0 2 2 2 2 2 2 0
0 0 2 2 2 2 2 0 2 0 0 2 2 2 2 2 2 0
0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 3 0 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 135
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 88.23529411764706
## General Assessment

The previous code correctly identified shapes composed of a primary color and containing exactly one pixel of a different "marker" color. However, it failed to accurately implement the transformation rule observed in the examples. The primary issues were:

1.  **Incorrect Coloring:** The code colored almost the entire shape with the marker color, instead of just the pixels forming the diamond pattern.
2.  **Border Preservation:** The original border pixels of the shape were incorrectly modified, whereas the expected output shows they should retain their original primary color.
3.  **Interior Clearing:** The logic for clearing the interior pixels (those not part of the border and not part of the diamond pattern) was flawed, leading to incorrect pixels being set to white (0) or not being cleared when they should have been. The marker pixel itself also needs to be cleared.
4.  **Diamond Expansion Termination:** The condition for stopping the diamond expansion might have been incorrect, potentially expanding too far or stopping too early. The expansion should likely continue as long as the pattern intersects with the shape's original area and stop when it goes beyond or completely fills the available space within the border.

The strategy to resolve these errors involves:
1.  Explicitly identifying the border pixels of the shape.
2.  Refining the diamond pattern generation: color only the pixels on the diamond path that fall within the original shape's primary color area.
3.  Implementing the correct clearing logic: After drawing the diamond pattern, iterate through the shape's original primary-colored pixels. If a pixel is *not* on the border and *not* colored by the diamond pattern, set it to white (0). Also, set the original marker position to white (0).
4.  Ensuring the border pixels retain their original primary color throughout the process.

## Metrics and Analysis

Let's analyze the first example to illustrate the discrepancies and the required logic.

**Example 1 Input:**

```
. . . . . . . . . . . . . .
. . G G G G G G G G G . . .
. . G G G G G G G M G . . .  (M=Magenta=6 at (2,9), G=Green=3)
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . G G G G G G G G G . . .
. . . . . . . . . . . . . .
. . . . . . . . . . . . . .
```


**Shape:** A green (3) rectangle from (1,2) to (10,10), containing a magenta (6) marker at (2,9).
**Primary Color:** Green (3)
**Marker Color:** Magenta (6)
**Marker Position:** (2, 9)

**Border Pixels:** These are the green pixels adjacent (N, S, E, W) to a non-green, non-magenta pixel (in this case, white=0 or outside the grid). This forms the outer perimeter of the green rectangle.


*code_execution:*
```python
import numpy as np

grid_str = """
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 6 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
"""
grid = np.array([list(map(int, row.split())) for row in grid_str.strip().split('\n')])
height, width = grid.shape
shape_primary_coords = set()
marker_coord = None
primary_color = 3
marker_color = 6
for r in range(height):
    for c in range(width):
        if grid[r,c] == primary_color:
            shape_primary_coords.add((r,c))
        elif grid[r,c] == marker_color:
             marker_coord = (r,c)

border_coords = set()
for r, c in shape_primary_coords:
    is_border = False
    # Check 4 neighbors
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        # Check if neighbor is outside grid OR is not part of the shape's area (not primary color AND not the marker)
        if not (0 <= nr < height and 0 <= nc < width) or \
           (grid[nr, nc] != primary_color and (nr, nc) != marker_coord):
             is_border = True
             break
    if is_border:
        border_coords.add((r, c))

print(f"Example 1:")
print(f"Shape Primary Coords Count: {len(shape_primary_coords)}")
print(f"Border Coords Count: {len(border_coords)}")
print(f"Marker Coord: {marker_coord}")
print(f"Marker Color: {marker_color}")
print(f"Primary Color: {primary_color}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example 1:
Shape Primary Coords Count: 89
Border Coords Count: 34
Marker Coord: (2, 9)
Marker Color: 6
Primary Color: 3

```
**Diamond Pattern:** Expands from (2,9). Pixels at Manhattan distance `d` from (2,9) that were originally green (3) are colored magenta (6).
- d=1: (1,9), (3,9), (2,8), (2,10). All originally green.
- d=2: (0,9), (4,9), (1,8), (3,8), (1,10), (3,10), (2,7), (2,11). Check original color: (4,9)=3, (1,8)=3, (3,8)=3, (1,10)=3, (3,10)=3, (2,7)=3, (2,11)=3. (0,9) is 0.
- ...and so on. Expansion stops when the diamond layer has no intersection with the original green pixels.

**Expected Output Logic:**
1.  Start with the input grid.
2.  Identify the border pixels (34 green pixels). These remain green.
3.  Draw the magenta diamond pattern starting from (2,9). Only color pixels that were originally green. Keep track of pixels colored magenta.
4.  Iterate through the original 89 green pixels.
5.  If a green pixel is *not* a border pixel AND was *not* colored magenta by the diamond pattern, change it to white (0).
6.  Change the original marker pixel (2,9) to white (0).

**Comparison with Actual Output (Example 1):**
The actual output colored almost all original green pixels (and the marker location) magenta (6), indicating a failure in steps 3, 4, 5, and 6. It did not preserve the border and did not clear the correct interior pixels.

Similar analysis applies to Examples 2 and 3, showing the same pattern of failures: border not preserved, incorrect interior clearing, and over-coloring with the marker color.

## Fact Extraction


```yaml
Task: Draw a hollow diamond pattern inside marked shapes.

Input_Features:
  - Grids containing contiguous shapes of uniform color (primary_color), potentially embedded with pixels of other colors.
  - Background is white (0).
  - Shapes are defined by 4-directional connectivity of non-white pixels.

Output_Features:
  - Grids where specific shapes have been modified.
  - Shapes without a single, unique internal marker pixel remain unchanged.

Transformation_Objects:
  - Shape: A contiguous area of pixels sharing the same non-white color (primary_color).
  - Marker: A single pixel of a different color (marker_color) located within or adjacent to the primary_color pixels of a shape, such that the marker and the primary pixels form one connected component (including the marker).
  - Border: The subset of a shape's primary_color pixels that are adjacent (4-directionally) to pixels not belonging to that shape (background or another shape, excluding the marker pixel itself during adjacency check).
  - Interior: The subset of a shape's primary_color pixels that are not part of the Border.
  - Diamond_Pattern: A diamond shape (defined by Manhattan distance) centered at the Marker's position.

Actions:
  1. Identify: Find all connected components of non-white pixels.
  2. Analyze_Components: For each component, determine if it consists of a primary_color area and exactly one marker_color pixel.
  3. Identify_Border: For qualifying shapes, determine the Border pixels.
  4. Generate_Pattern: Create a Diamond_Pattern expanding outwards from the Marker position layer by layer (increasing Manhattan distance).
  5. Apply_Pattern: For each pixel generated by the Diamond_Pattern, if it falls within the shape's original primary_color area, change its color to the marker_color in the output grid. Keep track of pixels changed by the pattern.
  6. Preserve_Border: Ensure all identified Border pixels retain their original primary_color in the output grid.
  7. Clear_Interior: For all pixels originally belonging to the shape's primary_color area: if a pixel is not a Border pixel and was not colored by the Apply_Pattern step, change its color to white (0) in the output grid.
  8. Clear_Marker: Change the color of the original Marker pixel's location to white (0) in the output grid.
  9. No_Change: If a shape does not have exactly one marker, or if a component is just a single pixel or doesn't fit the criteria, leave it unchanged in the output grid.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct connected shapes in the input grid. A shape is a group of connected non-white pixels. Connectivity is 4-directional.
3.  For each shape found:
    a.  Count the occurrences of each color within the shape's pixels.
    b.  Determine the most frequent color; this is the `primary_color`.
    c.  Identify all pixels within the shape that do *not* have the `primary_color`. These are potential `marker` pixels.
    d.  Check if there is exactly one `marker` pixel within the shape.
    e.  If there is exactly one `marker` pixel (with `marker_color` at `marker_coord`):
        i.  Identify the set of pixels belonging to the shape that have the `primary_color` (`primary_pixels`).
        ii. Identify the `border_pixels`: the subset of `primary_pixels` where at least one 4-directionally adjacent neighbor is either outside the grid boundaries or has a color different from `primary_color` and is not the `marker_coord`.
        iii. Initialize an empty set `pattern_pixels` to store coordinates colored by the diamond pattern.
        iv. Expand a diamond pattern outwards from `marker_coord`, layer by layer based on Manhattan distance `d` (starting with `d=1`).
        v.  For each distance `d`:
            1.  Generate all coordinates `(r, c)` that are exactly Manhattan distance `d` away from `marker_coord`.
            2.  Track if any pixels are colored in this layer (`colored_this_layer = false`).
            3.  For each generated coordinate `(r, c)`:
                a.  Check if `(r, c)` is within the grid boundaries.
                b.  Check if `(r, c)` is in the set `primary_pixels`.
                c.  If both conditions are true, change the color of `(r, c)` in the output grid to `marker_color`, add `(r, c)` to `pattern_pixels`, and set `colored_this_layer = true`.
            4.  If `colored_this_layer` is false after checking all coordinates at distance `d`, stop the diamond expansion. Otherwise, increment `d` and continue to the next layer.
        vi. Iterate through all coordinates `(r, c)` in the original `primary_pixels` set.
        vii. If `(r, c)` is *not* in `border_pixels` AND `(r, c)` is *not* in `pattern_pixels`, change the color of `(r, c)` in the output grid to white (0).
        viii. Change the color of the original `marker_coord` in the output grid to white (0).
    f.  If the shape does not have exactly one marker, leave it unchanged in the output grid.
4.  Return the modified output grid.
