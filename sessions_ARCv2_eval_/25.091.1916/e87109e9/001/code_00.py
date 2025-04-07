import numpy as np
from collections import deque, Counter

def find_most_frequent_excluding(grid, exclude_value):
    """Finds the most frequent value in a grid, excluding a specific value."""
    # Flatten the grid to easily count pixel values
    flat_grid = grid.flatten()
    
    # Filter out the value to exclude
    filtered_values = flat_grid[flat_grid != exclude_value]
    
    # If no values remain after filtering, return None or a default
    if filtered_values.size == 0:
        # Check if the grid only contained the excluded value
        if np.all(flat_grid == exclude_value):
             # Or maybe the original grid was empty? Although ARC constraints likely prevent this.
             # If only excluded value was present, there's no background to fill.
             # Let's return None to signify this. The caller should handle it.
             # Or, perhaps return the exclude_value itself if that makes sense in context?
             # Let's stick with None for now.
             return None
        else: # Grid was empty or had other values but none meeting criteria
             return None # Or maybe default to 0 (white)? Let's stick with None.


    # Count occurrences of each remaining value
    counts = Counter(filtered_values)
    
    # Find the value with the highest count
    if not counts: # handles case where filtered_values was empty
        return None
        
    most_common_value = counts.most_common(1)[0][0]
    return most_common_value

def solve(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Isolate the Drawing Grid: Extract the subgrid from the input grid starting from row index 6 and column index 1.
    2. Identify Background Color: Find the most frequent pixel color in the drawing grid, excluding azure (8).
    3. Identify Seed Pixels: Locate all initial azure (8) pixels in the drawing grid.
    4. Perform Expansion (Flood Fill): Starting from the seed pixels, expand the azure color outwards (up, down, left, right) onto adjacent pixels that match the background color. Expansion stops at grid boundaries or pixels that are not the background color.
    5. Return the modified drawing grid.
    """
    # 1. Isolate the Drawing Grid
    # Extracts rows 6 onwards and columns 1 onwards
    working_grid = input_grid[6:, 1:].copy() # Use copy to avoid modifying slice of input
    output_grid = working_grid # Start output as a copy of the working area

    # Get dimensions for boundary checks
    rows, cols = output_grid.shape

    # 2. Identify Background Color
    background_color = find_most_frequent_excluding(working_grid, 8) # 8 is azure

    # Handle case where no background color is found (e.g., grid only contains azure)
    if background_color is None:
        # If there's no background color to fill, the grid likely remains unchanged
        # or maybe it should all become azure? The examples suggest barriers stop fill,
        # so if only azure exists, nothing happens.
        # Let's assume returning the initial state is correct.
        return output_grid

    # 3. Identify Seed Pixels
    seed_pixels_coords = np.argwhere(working_grid == 8)

    # 4. Initialize Expansion structures
    queue = deque(seed_pixels_coords.tolist()) # Use deque for efficient popleft
    visited = np.zeros_like(working_grid, dtype=bool)
    
    # Mark initial seeds as visited
    for r, c in seed_pixels_coords:
        visited[r, c] = True

    # 5. Perform Expansion (Flood Fill / BFS)
    while queue:
        r, c = queue.popleft()

        # Define the four cardinal neighbors
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

        for nr, nc in neighbors:
            # Check if the neighbor is within the grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is the background color AND hasn't been visited
                if output_grid[nr, nc] == background_color and not visited[nr, nc]:
                    # Change the neighbor's color to azure
                    output_grid[nr, nc] = 8
                    # Mark as visited
                    visited[nr, nc] = True
                    # Add the neighbor to the queue for further expansion
                    queue.append((nr, nc))

    # 6. Final Output
    return output_grid
