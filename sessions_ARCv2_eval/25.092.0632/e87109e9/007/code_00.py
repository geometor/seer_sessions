import numpy as np
from collections import deque, Counter

"""
Transforms the input grid by performing an azure (8) flood fill on the
dominant background color of the canvas section.

1.  Isolates the 'Canvas' (rows below row 5, or whole grid if <= 6 rows).
2.  Identifies the single most frequent non-azure color in the Canvas as the
    'paintable_color'.
3.  Locates initial azure (8) 'seed' pixels in the Canvas.
4.  Performs an 8-way flood fill starting from seeds, replacing only
    'paintable_color' pixels with azure (8). Other colors act as barriers.
5.  Returns the modified Canvas.
"""

def get_background_color(canvas):
    """
    Identifies the single most frequent background color in the canvas, excluding azure (8).

    Args:
        canvas (np.ndarray): The canvas section of the input grid.

    Returns:
        int or None: The integer representing the background color, or None if no suitable background is found.
    """
    if canvas.size == 0:
        # Handle empty canvas case
        return None 

    # Count occurrences of each color in the canvas
    canvas_colors, counts = np.unique(canvas, return_counts=True)
    color_counts = Counter(dict(zip(canvas_colors, counts)))

    # Exclude azure (8) from being considered the background color
    if 8 in color_counts:
        del color_counts[8]

    # Find the most frequent remaining color
    if color_counts:
        # Get the color with the highest count
        background_color = color_counts.most_common(1)[0][0]
        # Ensure the return type is a standard Python int
        return int(background_color) 
    else:
        # Handle cases where the canvas only contains azure or is empty after excluding azure.
        return None

def transform(input_grid):
    """
    Applies the flood fill transformation based on the canvas background color.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid (canvas section only).
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=np.int64) 

    # --- 1. Isolate Canvas ---
    # Determine the number of rows belonging to the palette (top part)
    # Assume a standard palette height of 6 if the grid is tall enough
    palette_rows = 6 if input_grid_np.shape[0] > 6 else 0 
    
    if palette_rows > 0:
        # Extract the canvas part (below the palette)
        canvas = input_grid_np[palette_rows:, :]
    else:
        # If the grid is too short, the entire grid is treated as the canvas
        canvas = input_grid_np

    # Handle the edge case where the canvas might be empty after splitting
    if canvas.size == 0:
        return [] # Return an empty list if the canvas has no pixels

    # Initialize the output grid as a copy of the canvas; modifications will be made to this copy
    output_canvas = canvas.copy() 
    canvas_h, canvas_w = canvas.shape

    # --- 2. Identify Background Color (Paintable Color) ---
    # Use the helper function to find the color to be filled
    paintable_color = get_background_color(canvas)

    # If no paintable background color exists (e.g., canvas only has azure, or is empty),
    # no filling can occur. Return the original canvas section unchanged.
    if paintable_color is None:
        return output_canvas.tolist()

    # --- 3. Locate Azure Seeds ---
    # Initialize a queue for the Breadth-First Search (BFS) flood fill
    seed_points = deque()
    # Initialize a set to keep track of visited cells to prevent infinite loops and redundant checks
    visited_cells = set() 
    
    # Iterate through the canvas to find all initial azure (8) pixels
    for r in range(canvas_h):
        for c in range(canvas_w):
            # Check if the current pixel is azure
            if output_canvas[r, c] == 8:
                seed_tuple = (r, c)
                # Add the location of the azure pixel to the queue and visited set
                # This ensures seeds are processed and not re-visited unnecessarily
                if seed_tuple not in visited_cells:
                     seed_points.append(seed_tuple)
                     visited_cells.add(seed_tuple)

    # --- 4. Perform Flood Fill ---
    # Process cells from the queue until it's empty
    while seed_points:
        # Get the next cell coordinates from the front of the queue
        r, c = seed_points.popleft()

        # Explore the 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                # Skip the current cell itself (dr=0, dc=0)
                if dr == 0 and dc == 0:
                    continue 

                # Calculate neighbor coordinates
                nr, nc = r + dr, c + dc

                # Check if the neighbor coordinates are within the canvas bounds
                if 0 <= nr < canvas_h and 0 <= nc < canvas_w:
                    neighbor_loc = (nr, nc)

                    # Check if this neighbor has already been visited or added to the queue
                    if neighbor_loc not in visited_cells:
                        # Get the color of the neighbor pixel from the output canvas
                        current_neighbor_color = output_canvas[nr, nc]
                        
                        # Check if the neighbor's color is the designated 'paintable_color'
                        if current_neighbor_color == paintable_color:
                            # Change the neighbor's color to azure (8)
                            output_canvas[nr, nc] = 8 
                            # Mark the neighbor as visited
                            visited_cells.add(neighbor_loc) 
                            # Add the neighbor to the queue to explore from it later
                            seed_points.append(neighbor_loc) 
                        else:
                            # If the neighbor is not the paintable color (it's a barrier or already azure),
                            # mark it as visited anyway so we don't check it again from other cells.
                            visited_cells.add(neighbor_loc)

    # --- 5. Final Output ---
    # Convert the final modified numpy canvas back to a list of lists format
    return output_canvas.tolist()