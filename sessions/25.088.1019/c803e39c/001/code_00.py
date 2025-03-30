import numpy as np

"""
Identifies the last two colored objects (P3, P4) in the input grid, typically separated by gray vertical lines.
Determines the square dimension (D x D) of these objects and their colors (C3, C4).
Creates an output grid of size (D*D) x (D*D).
Populates the output grid based on the patterns of P3 and P4. For each output cell (r, c), it maps back to a source coordinate (sr, sc) = (floor(r/D), floor(c/D)) within the DxD area.
The output cell color is C4 if the pixel at (sr, sc) within P4's bounding box is C4. Otherwise, it's C3 if the pixel at (sr, sc) within P3's bounding box is C3.
"""

def find_objects(grid, ignore_colors):
    """
    Finds contiguous objects of the same color in a grid.

    Args:
        grid (np.array): The input grid.
        ignore_colors (set): A set of color values to ignore (background, separators).

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (list of (r, c) tuples), and
              'bbox' (tuple: min_r, min_c, max_r, max_c).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check if the pixel belongs to a color to be detected and hasn't been visited yet
            if color not in ignore_colors and not visited[r, c]:
                obj_pixels = []
                q = [(r, c)]  # Use a queue for Breadth-First Search (BFS)
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Perform BFS to find all connected pixels of the same color
                while q:
                    row, col = q.pop(0)
                    obj_pixels.append((row, col))
                    # Update bounding box coordinates
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Store the found object's properties
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the patterns of the last two objects.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    
    # Define colors to ignore (background and separators)
    ignore_colors = {0, 5} 
    
    # Find all colored objects in the grid
    objects = find_objects(grid_np, ignore_colors)
    
    # Sort objects based on their horizontal position (left-to-right) using the minimum column of their bounding box
    objects.sort(key=lambda obj: obj['bbox'][1])
    
    # We are interested in the last two objects
    if len(objects) < 2:
        # Handle cases where fewer than two objects are found, though problem description implies at least two relevant ones.
        # Returning the input or an empty grid might be options depending on desired error handling.
        # For now, let's assume the structure is always present as per examples.
        # Consider raising an error or returning a default grid if needed.
        print("Warning: Less than two objects found. Returning empty grid.")
        return [[]] 
        
    obj_P3 = objects[-2] # Penultimate object
    obj_P4 = objects[-1] # Ultimate object
    
    # Extract colors and bounding boxes
    C3 = obj_P3['color']
    C4 = obj_P4['color']
    bbox3 = obj_P3['bbox'] # (min_r, min_c, max_r, max_c)
    bbox4 = obj_P4['bbox'] 
    
    r3_min, c3_min, r3_max, c3_max = bbox3
    r4_min, c4_min, r4_max, c4_max = bbox4
    
    # Determine the dimension D of the objects (assuming they are square and equal size)
    D_h = r3_max - r3_min + 1
    D_w = c3_max - c3_min + 1
    
    # Basic validation based on examples (square objects of same size)
    if D_h != D_w or (r4_max - r4_min + 1) != D_h or (c4_max - c4_min + 1) != D_w:
        print(f"Warning: Objects P3/P4 dimensions mismatch or not square. P3: {D_h}x{D_w}, P4: {(r4_max - r4_min + 1)}x{(c4_max - c4_min + 1)}. Using P3 height.")
        # Decide on error handling or proceed with P3's dimension
        
    D = D_h # Use the calculated dimension
        
    # Calculate the output grid dimension
    output_dim = D * D
    
    # Initialize the output grid (using a neutral color like 0 initially, will be overwritten)
    output_grid_np = np.zeros((output_dim, output_dim), dtype=int)

    # Iterate through each cell (r, c) of the output grid
    for r in range(output_dim):
        for c in range(output_dim):
            # Calculate the corresponding source coordinate (sr, sc) within the DxD object space
            sr = r // D
            sc = c // D
            
            # Calculate the absolute coordinates in the input grid to check P4
            check_r4 = r4_min + sr
            check_c4 = c4_min + sc
            
            # Check if the coordinate is within P4's bounding box (optional but safer)
            # And check the color at the source location within P4's pattern in the input grid
            if 0 <= check_r4 < grid_np.shape[0] and 0 <= check_c4 < grid_np.shape[1] and \
               grid_np[check_r4, check_c4] == C4:
                output_grid_np[r, c] = C4
            else:
                # If not C4 in P4, check the corresponding location in P3
                check_r3 = r3_min + sr
                check_c3 = c3_min + sc
                # Check if the coordinate is within P3's bounding box (optional but safer)
                # And check the color at the source location within P3's pattern
                if 0 <= check_r3 < grid_np.shape[0] and 0 <= check_c3 < grid_np.shape[1] and \
                   grid_np[check_r3, check_c3] == C3:
                   output_grid_np[r, c] = C3
                # Else: If neither P3 nor P4 has its color at the source pixel,
                # the output pixel remains 0 (or whatever the init value was).
                # Based on the examples, the union of P3 and P4 seems to cover the DxD box,
                # so this 'else' case might not occur for relevant pixels.

    # Convert the final numpy array back to a list of lists
    output_grid = output_grid_np.tolist()
    
    return output_grid