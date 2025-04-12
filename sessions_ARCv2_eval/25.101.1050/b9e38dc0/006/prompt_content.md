
Previous Code:
```python
import collections
from collections import Counter

"""
Transforms the input grid by performing a fill operation based on parameters derived
heuristically from the input grid itself.

The process involves:
1. Analyzing the input grid to heuristically identify:
    - The background color (assumed to be the most frequent color).
    - The fill color (assumed to be the least frequent color adjacent to the background color).
    - Seed pixel locations (initial positions of the identified fill color).
2. Determining the fill type based on a heuristic:
    - 'left' fill if the identified background color is 0 (white).
    - 'flood' fill (4-directional) otherwise.
3. Executing the determined fill operation on a copy of the input grid:
    - Flood fill expands from seed pixels into adjacent background pixels.
    - Left fill expands leftwards from existing fill pixels into adjacent background pixels.
4. Returning the modified grid. If analysis fails (e.g., cannot determine distinct
   background/fill colors) or no seed pixels are found for the identified fill color,
   a copy of the original input grid is returned.
"""

# --- Helper Functions ---

def _get_neighbors(r, c, height, width):
    """
    Generates valid 4-way neighbors (up, down, left, right) for a given cell (r, c).
    Ensures neighbors are within the grid boundaries (0 <= nr < height, 0 <= nc < width).
    """
    neighbors = []
    # Up
    if r > 0: neighbors.append((r - 1, c))
    # Down
    if r < height - 1: neighbors.append((r + 1, c))
    # Left
    if c > 0: neighbors.append((r, c - 1))
    # Right
    if c < width - 1: neighbors.append((r, c + 1))
    return neighbors

def _identify_parameters(grid):
    """
    Identifies background, fill, seed colors/pixels, and fill type using input-only heuristics.

    Returns:
        A dictionary containing identified parameters ('background_color', 'fill_color',
        'seed_pixels', 'fill_type'), or None if analysis fails.
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    if height == 0 or width == 0:
        return None # Invalid grid

    # 1. Calculate color counts and find all unique colors
    color_counts = Counter()
    all_colors = set()
    for r in range(height):
        for c in range(width):
            color = grid[r][c]
            color_counts[color] += 1
            all_colors.add(color)

    if not color_counts or len(all_colors) < 2:
        # Need at least two colors for a meaningful fill operation
        return None

    # 2. Identify Background Color (heuristic: most frequent overall)
    background_color = color_counts.most_common(1)[0][0]

    # 3. Find Interface Colors and their frequencies
    # Interface colors are non-background colors adjacent to background colors
    interface_colors_freq = {}
    processed_neighbors = set() # Track neighbors checked to avoid redundant lookups
    for r in range(height):
        for c in range(width):
            if grid[r][c] == background_color:
                for nr, nc in _get_neighbors(r, c, height, width):
                    neighbor_coord = (nr, nc)
                    if neighbor_coord not in processed_neighbors:
                        processed_neighbors.add(neighbor_coord)
                        neighbor_color = grid[nr][nc]
                        if neighbor_color != background_color:
                            # Store the overall grid frequency of this neighbor color
                            interface_colors_freq[neighbor_color] = color_counts[neighbor_color]

    if not interface_colors_freq:
         # Fallback: If no interface colors found adjacent to the most frequent color.
         # Try identifying fill as simply the least frequent color overall that isn't background.
         potential_fills = {color: count for color, count in color_counts.items() if color != background_color}
         if not potential_fills: return None # Only one color in grid
         # Choose the color with the absolute minimum count
         fill_color = min(potential_fills, key=potential_fills.get)
    else:
        # 4. Identify Fill Color (heuristic: least frequent interface color)
        # Choose the color with the minimum overall count among the interface colors
        fill_color = min(interface_colors_freq, key=interface_colors_freq.get)

    # 5. Find initial seed coordinates (locations of the identified fill color)
    start_coords = []
    for r in range(height):
        for c in range(width):
            if grid[r][c] == fill_color:
                start_coords.append((r, c))

    # 6. Determine Fill Type (heuristic: based on identified background color)
    fill_type = "left" if background_color == 0 else "flood"

    return {
        "background_color": background_color,
        "fill_color": fill_color,
        "seed_pixels": start_coords,
        "fill_type": fill_type
    }


def _perform_flood_fill(grid, start_coords, fill_color, background_color):
    """
    Performs a 4-directional flood fill IN PLACE on the grid.
    Starts from start_coords and replaces background_color with fill_color.
    Boundary colors (anything not background or fill) implicitly halt the fill.
    """
    height = len(grid)
    width = len(grid[0])
    if not start_coords: # No seeds, nothing to fill
        return

    q = collections.deque(start_coords)
    visited = set(start_coords) # Track visited to prevent cycles and redundant checks

    while q:
        r, c = q.popleft()

        # Check neighbors of the current dequeued pixel
        for nr, nc in _get_neighbors(r, c, height, width):
            if (nr, nc) not in visited:
                # Only fill if the neighbor is the specific background color
                if grid[nr][nc] == background_color:
                    visited.add((nr, nc))       # Mark as visited
                    grid[nr][nc] = fill_color   # Fill the pixel
                    q.append((nr, nc))          # Add to queue for further expansion

def _perform_left_fill(grid, fill_color, background_color):
    """
    Performs a directional fill propagating only leftwards, IN PLACE.
    Iteratively scans the grid, changing background pixels to the fill color
    if the pixel immediately to their right is the fill color.
    Continues until no more changes can be made in a full pass.
    """
    height = len(grid)
    width = len(grid[0])

    changed_in_pass = True
    while changed_in_pass:
        changed_in_pass = False
        # Iterate rows from top to bottom
        for r in range(height):
            # Iterate columns from right-to-left (index width-2 down to 0)
            for c in range(width - 2, -1, -1):
                 # Check the pixel at (r, c)
                 # If it's the background color...
                 if grid[r][c] == background_color:
                     # ...and the pixel to its right (r, c+1) is the fill color...
                     if grid[r][c+1] == fill_color:
                         # ...change the current pixel to the fill color.
                         grid[r][c] = fill_color
                         changed_in_pass = True # Mark that a change occurred in this pass

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a fill transformation to the input grid based on heuristically
    identified parameters.
    """
    # 1. Analyze the input grid to find heuristic parameters
    params = _identify_parameters(input_grid)

    # 2. Check if analysis was successful and seeds were found
    if params is None or not params["seed_pixels"]:
        # If analysis fails or no seeds found for the heuristically determined
        # fill color, return an unmodified copy of the input.
        return [row[:] for row in input_grid]

    # 3. Extract parameters
    background_color = params["background_color"]
    fill_color = params["fill_color"]
    seed_pixels = params["seed_pixels"]
    fill_type = params["fill_type"]

    # 4. Create a mutable copy of the input grid to modify
    output_grid = [row[:] for row in input_grid]

    # 5. Perform the transformation based on fill type
    if fill_type == "flood":
        _perform_flood_fill(output_grid, seed_pixels, fill_color, background_color)
    elif fill_type == "left":
        # Left fill propagates from *any* fill_color pixel, not just seeds explicitly
        _perform_left_fill(output_grid, fill_color, background_color)

    # 6. Return the transformed grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 3 3 3 3 3 3 1 1 1
1 1 1 1 1 3 1 1 9 1 1 1 3 1 1
1 1 1 1 3 1 1 1 1 3 3 3 1 1 1
1 1 1 1 3 1 1 1 3 1 1 1 1 1 1
1 1 1 1 1 3 1 1 3 1 1 1 1 1 1
1 1 1 1 1 1 3 1 1 3 1 1 1 1 1
1 1 1 1 1 3 1 1 1 1 3 1 1 1 1
1 1 1 1 3 1 1 1 1 1 1 3 1 1 1
1 1 1 1 1 1 1 5 5 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 3 3 3 3 3 3 1 1 1
1 1 1 1 1 3 9 9 9 9 9 9 3 1 1
1 1 1 1 3 9 9 9 9 3 3 3 1 1 1
1 1 1 1 3 9 9 9 3 1 1 1 1 1 1
1 1 1 1 1 3 9 9 3 1 1 1 1 1 1
1 1 1 1 1 1 3 9 9 3 1 1 1 1 1
1 1 1 1 1 3 9 9 9 9 3 1 1 1 1
1 1 1 1 3 9 9 9 9 9 9 3 1 1 1
1 1 1 1 9 9 9 5 5 9 9 9 1 1 1
1 1 1 9 9 9 9 1 1 9 9 9 9 1 1
1 1 9 9 9 9 9 1 1 9 9 9 9 9 1
1 9 9 9 9 9 9 1 1 9 9 9 9 9 9
```
Transformed Output:
```
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 3 3 3 3 3 3 9 9 9
9 9 9 9 9 3 9 9 9 9 9 9 3 9 9
9 9 9 9 3 9 9 9 9 3 3 3 9 9 9
9 9 9 9 3 9 9 9 3 9 9 9 9 9 9
9 9 9 9 9 3 9 9 3 9 9 9 9 9 9
9 9 9 9 9 9 3 9 9 3 9 9 9 9 9
9 9 9 9 9 3 9 9 9 9 3 9 9 9 9
9 9 9 9 3 9 9 9 9 9 9 3 9 9 9
9 9 9 9 9 9 9 5 5 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
```
Match: False
Pixels Off: 138
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 122.66666666666667

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 5 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0 5 0 0 4 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 0 0 5 0 5 5 5 5 0
```
Expected Output:
```
4 4 4 4 4 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 5 0 0 0 5 5 5 0
4 4 4 4 4 4 4 4 5 0 5 4 4 5 0
4 4 4 4 4 4 4 4 4 5 4 4 4 5 0
4 4 4 4 4 4 4 4 4 4 4 4 4 5 0
4 4 4 4 4 4 4 4 4 5 4 4 4 5 0
4 4 4 4 4 4 4 4 5 0 5 5 5 5 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 5 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0 5 4 4 4 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 0 0 5 0 5 5 5 5 0
```
Match: False
Pixels Off: 70
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 116.66666666666666

## Example 3:
Input:
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 6 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 9 7 7 7 7 7 9 7 7 7 7 7
7 7 7 7 9 7 7 6 7 7 9 7 7 7 7 7
7 7 7 7 7 9 7 7 7 9 7 7 7 7 7 7
7 7 7 7 7 9 7 7 7 9 7 7 7 7 7 7
7 7 7 7 7 7 9 7 9 7 7 7 7 7 7 7
7 7 7 7 7 7 9 7 9 7 7 7 7 7 7 7
7 7 7 7 7 9 7 7 9 9 9 7 7 7 7 7
7 7 7 7 9 7 7 7 7 3 9 7 7 7 7 7
7 7 7 7 9 7 7 3 3 3 9 7 7 7 7 7
7 7 7 7 7 9 7 3 3 9 7 7 7 7 7 7
7 7 7 7 7 7 9 9 9 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 6 7 7
7 7 6 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 8 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
```
Expected Output:
```
7 7 7 3 3 7 3 7 3 3 3 3 7 7 7 7
7 7 7 7 3 6 3 7 3 3 3 7 7 7 7 7
7 7 7 7 3 3 3 7 3 3 3 7 7 7 7 7
7 7 7 7 9 3 3 7 3 3 9 7 7 7 7 7
7 7 7 7 9 3 3 6 3 3 9 7 7 7 7 7
7 7 7 7 7 9 3 3 3 9 7 7 7 7 7 7
7 7 7 7 7 9 3 3 3 9 7 7 7 7 7 7
7 7 7 7 7 7 9 3 9 7 7 7 7 7 7 7
7 7 7 7 7 7 9 3 9 7 7 7 7 7 7 7
7 7 7 7 7 9 3 3 9 9 9 7 7 7 7 7
7 7 7 7 9 3 3 3 3 3 9 7 7 7 7 7
7 7 7 7 9 3 3 3 3 3 9 7 7 7 7 7
7 7 7 7 7 9 3 3 3 9 7 7 7 7 7 7
7 7 7 7 7 7 9 9 9 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 6 7 7
7 7 6 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 8 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 9 8 8 8 8 8 9 8 8 8 8 8
8 8 8 8 9 8 8 6 8 8 9 8 8 8 8 8
8 8 8 8 8 9 8 8 8 9 8 8 8 8 8 8
8 8 8 8 8 9 8 8 8 9 8 8 8 8 8 8
8 8 8 8 8 8 9 8 9 8 8 8 8 8 8 8
8 8 8 8 8 8 9 8 9 8 8 8 8 8 8 8
8 8 8 8 8 9 8 8 9 9 9 8 8 8 8 8
8 8 8 8 9 8 8 8 8 3 9 8 8 8 8 8
8 8 8 8 9 8 8 3 3 3 9 8 8 8 8 8
8 8 8 8 8 9 8 3 3 9 8 8 8 8 8 8
8 8 8 8 8 8 9 9 9 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8
8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 252
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 175.0
