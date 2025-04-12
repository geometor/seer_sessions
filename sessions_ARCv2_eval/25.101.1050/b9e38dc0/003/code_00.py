import collections
from collections import Counter
# No other external libraries are strictly necessary for this implementation

# --- Helper Functions ---

def get_neighbors(r, c, height, width):
    """
    Generates valid 4-way neighbors (up, down, left, right) for a given cell.
    Ensures neighbors are within the grid boundaries.
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

def analyze_and_identify_params(grid):
    """
    Identifies background, fill, seed, and boundary colors, plus the fill type,
    using heuristics derived from observations of the training examples.

    Heuristics Used:
    - Background Color: The most frequent color in the input grid.
    - Fill Color: The color adjacent to the background color that has the
                  overall minimum frequency in the grid. (Handles ties by picking one).
    - Boundary Colors: All other colors present in the grid.
    - Seed Pixels: The locations of the Fill Color in the input grid.
    - Fill Type: 'left' if the identified Background Color is 0 (white),
                 otherwise 'flood'.

    Returns:
        A dictionary containing the identified parameters, or None if analysis fails
        (e.g., empty grid, cannot determine distinct colors).
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
        # Need at least two colors for a fill operation
        return None

    # 2. Identify Background Color (most frequent overall)
    background_color = color_counts.most_common(1)[0][0]

    # 3. Find Interface Colors and their frequencies
    # Interface colors are non-background colors adjacent to background colors
    interface_colors_freq = {}
    processed_neighbors = set() # Track neighbors checked to avoid redundant lookups
    for r in range(height):
        for c in range(width):
            if grid[r][c] == background_color:
                for nr, nc in get_neighbors(r, c, height, width):
                    neighbor_coord = (nr, nc)
                    if neighbor_coord not in processed_neighbors:
                        processed_neighbors.add(neighbor_coord)
                        neighbor_color = grid[nr][nc]
                        if neighbor_color != background_color:
                            # Store the overall frequency of this neighbor color
                            interface_colors_freq[neighbor_color] = color_counts[neighbor_color]

    if not interface_colors_freq:
         # Fallback: If no interface colors found adjacent to the most frequent color,
         # maybe the 'background' isn't the most frequent.
         # Or maybe the 'fill' color seeds aren't adjacent initially.
         # Try identifying fill as simply the least frequent color overall that isn't background.
         potential_fills = {color: count for color, count in color_counts.items() if color != background_color}
         if not potential_fills: return None # Only one color in grid
         fill_color = min(potential_fills, key=potential_fills.get)
    else:
        # 4. Identify Fill Color (least frequent interface color)
        fill_color = min(interface_colors_freq, key=interface_colors_freq.get)

    # 5. Identify Boundary Colors
    boundary_colors = all_colors - {background_color, fill_color}

    # 6. Find initial seed coordinates
    start_coords = []
    for r in range(height):
        for c in range(width):
            if grid[r][c] == fill_color:
                start_coords.append((r, c))

    # 7. Determine Fill Type (heuristic based on BG color)
    fill_type = "left" if background_color == 0 else "flood"

    # If no seeds are found for the identified fill color, the parameters might be wrong,
    # but we proceed, and the fill functions will likely do nothing.
    # A more robust solution might re-evaluate parameters here.

    return {
        "background_color": background_color,
        "fill_color": fill_color,
        "seed_pixels": start_coords,
        "boundary_colors": boundary_colors,
        "fill_type": fill_type
    }


def perform_flood_fill(grid, start_coords, fill_color, background_color):
    """
    Performs a 4-directional flood fill IN PLACE on the grid.
    Starts from start_coords and replaces background_color with fill_color.
    Uses a queue and a visited set to handle the fill efficiently.
    """
    height = len(grid)
    width = len(grid[0])
    if not start_coords: # No seeds, nothing to fill
        return

    q = collections.deque(start_coords)
    # Initialize visited with seeds only if they are on background (unlikely)
    # Or more simply, add seeds to visited to prevent re-adding if they are neighbors of others
    visited = set(start_coords)

    while q:
        r, c = q.popleft()

        # The pixel (r,c) itself is already the fill_color (or was an initial seed)
        # Check its neighbors to see if they should be filled
        for nr, nc in get_neighbors(r, c, height, width):
            # Check if the neighbor is within bounds (implicitly handled by get_neighbors)
            # Check if it hasn't been visited/processed yet
            if (nr, nc) not in visited:
                # Check if the neighbor is the background color
                if grid[nr][nc] == background_color:
                    visited.add((nr, nc))       # Mark as visited
                    grid[nr][nc] = fill_color   # Fill the pixel
                    q.append((nr, nc))          # Add to queue for further expansion
    # Modification happens in place, no return value needed.


def perform_left_fill(grid, fill_color, background_color):
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
            # Iterate columns from right-to-left (second-to-last column to first)
            # This allows changes to propagate leftwards within a single pass efficiently
            for c in range(width - 2, -1, -1):
                 # Check the pixel at (r, c)
                 # If it's the background color...
                 if grid[r][c] == background_color:
                     # ...and the pixel to its right (r, c+1) is the fill color...
                     if grid[r][c+1] == fill_color:
                         # ...change the current pixel to the fill color.
                         grid[r][c] = fill_color
                         changed_in_pass = True # Mark that a change occurred
    # Modification happens in place, no return value needed.

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the grid by performing a fill operation based on derived parameters.

    The process involves:
    1. Analyzing the input grid to heuristically identify the background color (most frequent),
       fill color (least frequent color adjacent to background), seed pixel locations
       (initial positions of fill color), and boundary colors (all others).
    2. Determining the fill type: 'left' fill if the background color is 0 (white),
       otherwise a 4-directional 'flood' fill.
    3. Executing the determined fill operation, modifying a copy of the input grid.
       - Flood fill expands from seed pixels into adjacent background pixels.
       - Left fill expands leftwards from existing fill pixels into adjacent background pixels.
    4. Returning the modified grid. If analysis fails or no seed pixels are found
       for the identified fill color, a copy of the original input grid is returned.
    """
    # 1. Analyze the input grid to find parameters
    params = analyze_and_identify_params(input_grid)

    # 2. Check if analysis was successful and seeds were found
    if params is None or not params["seed_pixels"]:
        # If analysis fails (e.g., invalid grid, <2 colors) or no seeds found
        # for the heuristically determined fill color, return a copy of the input.
        return [row[:] for row in input_grid]

    # Extract parameters
    background_color = params["background_color"]
    fill_color = params["fill_color"]
    seed_pixels = params["seed_pixels"]
    fill_type = params["fill_type"]
    # boundary_colors = params["boundary_colors"] # Boundaries implicitly handled by fill logic

    # 3. Create a mutable copy of the input grid to modify
    output_grid = [row[:] for row in input_grid]

    # 4. Perform the transformation based on fill type
    if fill_type == "flood":
        perform_flood_fill(output_grid, seed_pixels, fill_color, background_color)
    elif fill_type == "left":
        # Left fill doesn't strictly need seeds; it propagates from *any* fill_color pixel
        perform_left_fill(output_grid, fill_color, background_color)

    # 5. Return the transformed grid
    return output_grid