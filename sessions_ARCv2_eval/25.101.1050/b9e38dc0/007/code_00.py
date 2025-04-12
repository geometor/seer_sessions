import collections
from collections import Counter

"""
Transforms the input grid by performing a fill operation.

The transformation identifies key components heuristically from the input grid:
1. Background Color: Assumed to be the most frequent color in the grid.
2. Fill Color: Assumed to be the color adjacent (4-way) to the background color
   that has the minimum overall frequency in the entire grid. A fallback identifies
   it as the least frequent non-background color if no adjacent colors are found.
3. Seed Pixels: The locations of the identified Fill Color in the input grid.

Based on the identified Background Color, a fill type is chosen:
- If Background Color is 0 (white), a 'left_fill' operation is performed.
- Otherwise, a 4-directional 'flood_fill' operation is performed.

The fill operation modifies a copy of the input grid:
- Flood Fill: Starting from the seed pixels, it replaces adjacent background-colored
  pixels with the fill color, expanding outwards.
- Left Fill: It iteratively replaces background-colored pixels with the fill color
  if the pixel immediately to their right has the fill color, effectively propagating
  the fill leftwards across the grid.

Boundary colors (all colors other than the identified background and fill colors)
implicitly stop the fill propagation. If parameter identification fails or no
seed pixels are found, the original grid is returned unchanged.
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

    # 1. Calculate overall color counts and find all unique colors
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
    found_interface = False
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
                            found_interface = True # Mark that at least one interface color found

    # 4. Identify Fill Color
    if not found_interface:
         # Fallback: If no interface colors found adjacent to the most frequent color.
         # This might happen if seeds are not directly adjacent or BG is small.
         # Try identifying fill as simply the least frequent color overall that isn't background.
         potential_fills = {color: count for color, count in color_counts.items() if color != background_color}
         if not potential_fills: return None # Only one color in grid
         # Choose the color with the absolute minimum count
         fill_color = min(potential_fills, key=potential_fills.get)
    else:
        # Heuristic: least frequent interface color (based on overall count)
        # Choose the color with the minimum overall count among the interface colors found
        fill_color = min(interface_colors_freq, key=interface_colors_freq.get)

    # 5. Find initial seed coordinates (locations of the identified fill color)
    start_coords = []
    for r in range(height):
        for c in range(width):
            if grid[r][c] == fill_color:
                start_coords.append((r, c))

    # 6. Determine Fill Type (heuristic: based on identified background color)
    fill_type = "left" if background_color == 0 else "flood"

    # If no seeds are found, parameter identification might be wrong, but return params anyway.
    # The main transform function will handle the no-seed case.
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
    Uses a queue and visited set for correctness and efficiency.
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
                    visited.add((nr, nc))       # Mark as visited before adding to queue
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
            # This ensures changes propagate correctly leftward within a pass
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
    identified parameters derived solely from the input grid.
    """
    # 1. Analyze the input grid to find heuristic parameters
    params = _identify_parameters(input_grid)

    # 2. Check if analysis was successful and seeds were found
    if params is None or not params["seed_pixels"]:
        # If analysis fails (e.g., invalid grid, <2 colors) or no seeds found
        # for the heuristically determined fill color, return an unmodified copy.
        # This prevents errors if the heuristics misidentified the fill color.
        return [row[:] for row in input_grid]

    # 3. Extract parameters identified from the input grid
    background_color = params["background_color"]
    fill_color = params["fill_color"]
    seed_pixels = params["seed_pixels"]
    fill_type = params["fill_type"]

    # 4. Create a mutable copy of the input grid to perform the transformation on
    output_grid = [row[:] for row in input_grid]

    # 5. Perform the transformation based on the determined fill type
    if fill_type == "flood":
        # Execute 4-directional flood fill starting from seeds
        _perform_flood_fill(output_grid, seed_pixels, fill_color, background_color)
    elif fill_type == "left":
        # Execute iterative leftward fill; propagates from *any* fill_color pixel
        _perform_left_fill(output_grid, fill_color, background_color)

    # 6. Return the transformed grid
    return output_grid