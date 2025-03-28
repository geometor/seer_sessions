import numpy as np

"""
The transformation identifies a single non-background object in the input grid, where the background color is Azure (8). 
It then creates two copies of this object. 
A conditional color swap is applied to both copies: if the original object contains both Blue (1) and Red (2) pixels, then Blue and Red are swapped in the copies.
Finally, the two copies (potentially with swapped colors) are placed onto an output grid of the same dimensions as the input, initialized with the background color. 
The placement involves specific constant shifts relative to the original object's top-left position:
- Copy A (Bottom-Left) is always shifted by (4 rows down, 1 column left) -> (Δrow=4, Δcol=-1).
- Copy B (Top-Right) is always shifted by (0 rows down, 5 columns right) -> (Δrow=0, Δcol=5).
If multiple objects exist or no object exists, the behavior is undefined by the examples; this implementation assumes a single object and returns an empty grid if none is found.
"""

def find_single_object(grid_np, background_color):
    """
    Finds the pixels, colors, and top-left corner of a single non-background object.
    Uses Breadth-First Search (BFS) to find the first connected component.
    Assumes only one object exists based on the task description.

    Args:
        grid_np (np.ndarray): The input grid as a NumPy array.
        background_color (int): The color designated as the background.

    Returns:
        tuple: (object_pixels, object_colors, min_row, min_col) or (None, None, None, None) if no object found.
               object_pixels: List of (row, col) tuples for object pixels.
               object_colors: Set of unique colors in the object.
               min_row, min_col: Coordinates of the top-left bounding box corner.
    """
    rows, cols = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    
    for r_start in range(rows):
        for c_start in range(cols):
            if grid_np[r_start, c_start] != background_color and not visited[r_start, c_start]:
                # Found the start of an object, perform BFS
                object_pixels = []
                object_colors = set()
                min_row, min_col = r_start, c_start
                q = [(r_start, c_start)]
                visited[r_start, c_start] = True

                while q:
                    r, c = q.pop(0)
                    color = grid_np[r, c]
                    object_pixels.append((r, c))
                    object_colors.add(color)
                    min_row = min(min_row, r)
                    min_col = min(min_col, c)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid_np[nr, nc] != background_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Since we assume only one object, return immediately after finding the first one
                return object_pixels, object_colors, min_row, min_col

    # If no non-background pixels found
    return None, None, None, None


def transform(input_grid):
    """
    Transforms the input grid by duplicating, shifting, and potentially 
    color-swapping a single non-background object based on specific rules.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    background_color = 8  # Azure is the background color

    # 1. Initialize output grid with background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # 2. Identify the single non-background object
    object_pixels, object_colors, min_row, min_col = find_single_object(input_np, background_color)

    # If there's no object (only background), return the empty output grid
    if object_pixels is None:
        return output_grid.tolist()

    # 3. Check if color swapping is needed (Blue=1 and Red=2 present)
    needs_swap = (1 in object_colors and 2 in object_colors)

    # 4. Define the constant shift vectors
    shift_A = (4, -1)  # Bottom-Left copy shift (delta_row, delta_col)
    shift_B = (0, 5)   # Top-Right copy shift (delta_row, delta_col)

    # 5. Iterate through object pixels, calculate target positions, apply color swap if needed, and place pixels
    for r, c in object_pixels:
        original_color = input_np[r, c]
        
        # Determine the output color (apply swap if needed for both copies)
        output_color = original_color
        if needs_swap:
            if original_color == 1:
                output_color = 2
            elif original_color == 2:
                output_color = 1
        
        # Calculate relative position within the object
        rel_r = r - min_row
        rel_c = c - min_col

        # Calculate target position for Copy A (Bottom-Left)
        target_r_A = min_row + rel_r + shift_A[0]
        target_c_A = min_col + rel_c + shift_A[1]
        # Place pixel if within bounds
        if 0 <= target_r_A < rows and 0 <= target_c_A < cols:
            output_grid[target_r_A, target_c_A] = output_color

        # Calculate target position for Copy B (Top-Right)
        target_r_B = min_row + rel_r + shift_B[0]
        target_c_B = min_col + rel_c + shift_B[1]
        # Place pixel if within bounds
        if 0 <= target_r_B < rows and 0 <= target_c_B < cols:
            output_grid[target_r_B, target_c_B] = output_color 

    # 6. Return the final grid as a list of lists
    return output_grid.tolist()