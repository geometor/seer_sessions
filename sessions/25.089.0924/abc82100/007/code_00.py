import numpy as np
from collections import Counter

"""
Transforms an input grid based on a hierarchical set of rules:

1.  Vertical Red Line Rule: If a contiguous vertical line of Red (2) pixels exists spanning the grid's height at column 'c':
    - Create a new white (0) output grid.
    - Fill the area in the output grid to the left of the line (columns < c) with Red (2).
    - Fill the column 'c' in the output grid with Blue (1).
    - Leave the area to the right (columns > c) as white (0).
    This rule takes precedence over all others.

2.  Azure Presence Rule: If no vertical Red line is found, check if Azure (8) is present in the input grid.
    - If Azure (8) is NOT present: Return a copy of the input grid.
    - If Azure (8) IS present:
        a. Count the frequency of all non-white (0) and non-azure (8) colors.
        b. If no such colors exist (only white and/or azure present): Create the output grid by copying the input grid and changing all Azure(8) pixels to white(0).
        c. If other colors exist, find the Most Frequent Color (MFC) among them. If counts are tied, the color with the lower numerical value is chosen.
        d. Apply transformation based on MFC:
            - If MFC is Blue (1):
                i. Find all contiguous Blue (1) objects using 8-way adjacency (including diagonals).
                ii. Identify the largest Blue object by pixel count.
                iii. Create a new output grid filled entirely with white (0).
                iv. Draw the shape of the largest Blue object onto the output grid using Red (2).
            - If MFC is Magenta (6):
                i. Create an intermediate grid, initially filled with white (0).
                ii. Populate the intermediate grid based on the input grid: Input Magenta(6)->Output Orange(7), Input Orange(7)->Output Magenta(6), Input Red(2)->Output Yellow(4), Input Yellow(4)->Output Red(2). All other input colors result in white(0).
                iii. Initialize the final output grid as a copy of this intermediate grid.
                iv. Iterate through the *intermediate grid* rows 0 to height-2. For each pixel (r, c):
                   - If intermediate(r, c) is Orange(7) AND intermediate(r+1, c) is white(0), set *final output*(r+1, c) to Orange(7).
                   - If intermediate(r, c) is Magenta(6) AND intermediate(r+1, c) is white(0), set *final output*(r+1, c) to Magenta(6).
            - If MFC is Yellow (4):
                i. Initialize the output grid filled entirely with white (0).
                ii. Iterate through the input grid (r, c):
                   - If input(r, c) is Yellow(4): Set output(r, c) = Red(2).
                   - If input(r, c) is Blue(1): Set output(r, c) = Orange(7).
                   (All other input colors result in white(0)).
            - If MFC is any other color: (Fallback based on observed Azure removal) Create the output grid by copying the input grid and changing all Azure(8) pixels to white(0).

3.  Default Rule: If no vertical Red line is found AND Azure (8) is not present, return the input grid unchanged (handled by step 2).
"""


def find_objects(grid, color, adjacency=8):
    """Finds all contiguous objects of a given color using specified adjacency."""
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    # Define neighbor offsets based on adjacency
    if adjacency == 8:
        neighbor_deltas = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    else: # Default to 4-way
        neighbor_deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Iterate through each pixel
    for r in range(height):
        for c in range(width):
            # If pixel matches color and hasn't been visited, start BFS
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = [(r, c)]
                visited[r, c] = True
                while q:
                    row, col = q.pop(0)
                    obj_coords.add((row, col))
                    # Check neighbors
                    for dr, dc in neighbor_deltas:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if neighbor matches color and is unvisited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                # Add found object coordinates to the list
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def find_vertical_line_column(grid, color):
    """Checks for a vertical line of a specific color spanning the full height
       and returns its column index, or None if not found."""
    height, width = grid.shape
    if height == 0: return None # Handle empty grid

    # Check each column
    for c in range(width):
        is_line = True
        # Check each row in the current column
        for r in range(height):
            if grid[r, c] != color:
                is_line = False
                break
        # If all pixels in the column match the color, return the column index
        if is_line:
            return c
    return None # No full vertical line found

def get_color_counts(grid):
    """Counts the frequency of non-white (0) and non-azure (8) colors."""
    counts = Counter()
    if grid.size == 0: return counts # Handle empty grid
    # Iterate through all pixels
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            # Count only if not white and not azure
            if color != 0 and color != 8:
                counts[color] += 1
    return counts

def transform(input_grid):
    """
    Applies the transformation rule based on the presence of a vertical red line
    or the most frequent color alongside azure.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    if height == 0 or width == 0: # Handle empty input
        return []

    # 1. Check for Vertical Red Line (Rule 1)
    red_line_col = find_vertical_line_column(input_grid_np, 2)
    if red_line_col is not None:
        # Initialize output grid as white
        output_grid = np.zeros_like(input_grid_np)
        # Fill left side with Red (2)
        if red_line_col > 0:
            output_grid[:, :red_line_col] = 2
        # Change line itself to Blue (1)
        output_grid[:, red_line_col] = 1
        # Right side remains white (0) - already initialized
        return output_grid.tolist()

    # 2. Check for Azure (8) (Rule 2)
    if 8 not in input_grid_np:
        # If no Azure, return input unchanged
        return input_grid_np.tolist()
    else:
        # Azure is present, proceed with Azure rules
        color_counts = get_color_counts(input_grid_np)

        # 2.b Handle cases where only white and/or azure exist
        if not color_counts:
             # Change Azure to white and return
             output_grid = np.where(input_grid_np == 8, 0, input_grid_np)
             return output_grid.tolist()

        # 2.c Find MFC (highest count, lowest color value tie-breaker)
        mfc = -1
        max_count = -1
        # Iterate through sorted colors (keys) to handle tie-breaking correctly
        # Colors are 1-9 excluding 8. Sorting ensures lower number wins tie.
        for color in sorted(color_counts.keys()):
            count = color_counts[color]
            if count > max_count:
                max_count = count
                mfc = color
        # If count == max_count, the lower color value (already processed due to sort) remains mfc.

        # Check if a valid MFC was found
        if mfc == -1:
             # Fallback: should not happen, but safest to just clear azure
             output_grid = np.where(input_grid_np == 8, 0, input_grid_np)
             return output_grid.tolist()


        # 2.d Apply transformation based on MFC

        # MFC is Blue (1)
        if mfc == 1:
            # Find largest blue object using 8-way adjacency
            blue_objects = find_objects(input_grid_np, 1, adjacency=8)
            if not blue_objects:
                # Fallback if no blue objects found despite MFC being blue
                 output_grid = np.where(input_grid_np == 8, 0, input_grid_np)
                 return output_grid.tolist()

            # Find the object with the maximum number of pixels
            largest_blue_object = max(blue_objects, key=len)
            # Initialize output grid as white
            output_grid = np.zeros_like(input_grid_np)
            # Draw the largest blue object's shape in Red
            for r, c in largest_blue_object:
                if 0 <= r < height and 0 <= c < width: # Boundary check just in case
                    output_grid[r, c] = 2
            return output_grid.tolist()

        # MFC is Magenta (6)
        elif mfc == 6:
            # Create intermediate grid with initial swaps
            intermediate_grid = np.zeros_like(input_grid_np)
            for r in range(height):
                for c in range(width):
                    color = input_grid_np[r, c]
                    if color == 6: intermediate_grid[r, c] = 7 # Magenta -> Orange
                    elif color == 7: intermediate_grid[r, c] = 6 # Orange -> Magenta
                    elif color == 2: intermediate_grid[r, c] = 4 # Red -> Yellow
                    elif color == 4: intermediate_grid[r, c] = 2 # Yellow -> Red
                    # Other colors (0, 1, 3, 5, 8, 9) result in 0

            # Copy intermediate to final output grid for modification
            output_grid = np.array(intermediate_grid)

            # Apply row duplication logic based on *intermediate* grid's state
            for r in range(height - 1): # Iterate up to second to last row
                for c in range(width):
                    intermediate_color = intermediate_grid[r, c]
                    below_intermediate_color = intermediate_grid[r + 1, c]

                    # Check condition for Orange drop-down effect
                    if intermediate_color == 7 and below_intermediate_color == 0:
                        output_grid[r + 1, c] = 7 # Color below Orange in final output
                    # Check condition for Magenta drop-down effect
                    elif intermediate_color == 6 and below_intermediate_color == 0:
                        output_grid[r + 1, c] = 6 # Color below Magenta in final output

            return output_grid.tolist()

        # MFC is Yellow (4)
        elif mfc == 4:
            # Initialize output grid as white
            output_grid = np.zeros_like(input_grid_np)
            for r in range(height):
                for c in range(width):
                    color = input_grid_np[r, c]
                    # Yellow -> Red (pixel-wise)
                    if color == 4:
                         output_grid[r, c] = 2
                    # Blue -> Orange (pixel-wise)
                    elif color == 1:
                         output_grid[r, c] = 7
                    # Other colors (including Azure, Red, Orange etc.) remain white (0)
            return output_grid.tolist()

        # MFC is any other color (Fallback)
        else:
             # Default action for other MFCs: just remove Azure
             output_grid = np.where(input_grid_np == 8, 0, input_grid_np)
             return output_grid.tolist()

    # Fallback return (should not be reached ideally)
    return input_grid_np.tolist()