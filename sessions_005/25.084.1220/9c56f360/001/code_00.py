import numpy as np

"""
Transformation Rule:
Identifies green (3) pixels in the input grid. For each green pixel, determines a target destination column within the same row by scanning leftwards until an azure (8) pixel (obstacle) or the grid edge (column 0) is encountered. The target column is the one immediately to the right of the obstacle, or column 0 if no obstacle is found. If multiple green pixels in the same row target the same initial column, they stack horizontally to the right, preserving their original relative left-to-right order. The leftmost original pixel takes the target column, the next takes the column to its right, and so on. Azure pixels (8) remain static. Original positions of moved green pixels become white (0).
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving azure pixels and background
    output_np = input_np.copy()
    rows, cols = input_np.shape

    # --- Step 1: Identify green pixels and clear their original positions ---
    green_pixels_orig = []
    for r in range(rows):
        for c in range(cols):
            if input_np[r, c] == 3:
                green_pixels_orig.append((r, c))
                # Clear the original position in the output grid
                # Obstacles (8) are not cleared as they are static
                if output_np[r, c] == 3:
                     output_np[r, c] = 0

    # --- Step 2: Calculate initial target column for each green pixel ---
    # Stores dictionaries: {'orig': (r, c_orig), 'target_col': c_target}
    moves = []
    for r, c_orig in green_pixels_orig:
        c_target = 0 # Default target is the leftmost column (0)
        # Scan leftwards from the column just left of the original position
        for c_scan in range(c_orig - 1, -1, -1):
            # Check for an obstacle (azure pixel, color 8) in the input grid
            if input_np[r, c_scan] == 8:
                # Target column is the one immediately to the right of the obstacle
                c_target = c_scan + 1
                break # Stop scanning left once the first obstacle is found
        moves.append({'orig': (r, c_orig), 'target_col': c_target})

    # --- Step 3: Process moves row by row to handle stacking ---
    # Stores the final (r, c_dest) coordinates where green pixels will be placed
    final_placements = []

    # Group moves by row for independent processing
    moves_by_row = {}
    for move in moves:
        r = move['orig'][0]
        if r not in moves_by_row:
            moves_by_row[r] = []
        moves_by_row[r].append(move)

    # Process each row that contains green pixels
    for r, row_moves in moves_by_row.items():
        # Sort moves within the row:
        # Primary key: target_col (ascending) - groups pixels aiming for the same spot
        # Secondary key: original column c_orig (ascending) - preserves relative order
        sorted_row_moves = sorted(row_moves, key=lambda m: (m['target_col'], m['orig'][1]))

        # Keep track of columns occupied by static obstacles (8) or already placed green pixels in this row
        # Initialize with the positions of azure (8) pixels in the current row
        occupied_cols_in_row = set()
        for c in range(cols):
             if output_np[r, c] == 8: # Check the output grid copy which holds static elements
                 occupied_cols_in_row.add(c)

        # Determine final destination for each move in the sorted list
        for move in sorted_row_moves:
            c_target = move['target_col']
            # Start checking for placement at the initial target column
            c_dest = c_target

            # Resolve collisions/stacking: find the first available column >= c_target
            while c_dest in occupied_cols_in_row:
                c_dest += 1 # Move one column to the right

            # Check if the destination is within grid bounds
            if c_dest < cols:
                # Record the final placement coordinates
                final_placements.append((r, c_dest))
                # Mark this column as occupied for subsequent pixels in the same row
                occupied_cols_in_row.add(c_dest)
            # else: Pixel would be pushed off the grid edge. Based on examples, this case might not occur or is handled implicitly.

    # --- Step 4: Place green pixels in their final determined positions ---
    # Update the output grid with the final positions of the green pixels
    for r, c_dest in final_placements:
         # Ensure coordinates are valid (redundant check if logic is perfect, but safe)
         if 0 <= r < rows and 0 <= c_dest < cols:
             # Place the green pixel (3)
             output_np[r, c_dest] = 3

    # Convert the final NumPy array back to a list of lists for the required output format
    return output_np.tolist()