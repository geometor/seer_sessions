import numpy as np

"""
Transformation Rule:
1. Identify the horizontal and vertical azure (8) lines that divide the 9x9 input grid.
2. Locate the 6x6 quadrant containing a green (3) pattern (Pattern Quadrant, PQ) and the diagonally opposite 2x2 quadrant containing the color key (Color Quadrant, CQ).
3. Extract the 2x2 color key [[C1, C2], [C3, C4]] from the CQ.
4. Extract the 6x6 pattern from the PQ.
5. Create a 6x6 output grid initialized with white (0).
6. Iterate through the 6x6 PQ. If a cell (r, c) is green (3):
   - Determine which 3x3 sub-quadrant (TL, TR, BL, BR) the cell belongs to within the 6x6 PQ.
   - Map the green pixel to the corresponding color from the color key (C1 for TL, C2 for TR, C3 for BL, C4 for BR).
   - Place the mapped color into the output grid at the same position (r, c).
7. White (0) pixels from the PQ remain white (0) in the output.
8. Return the resulting 6x6 output grid.
"""

def find_dividers(grid):
    """Finds the row and column index of the solid azure (8) lines."""
    hr, vc = -1, -1
    rows, cols = grid.shape
    # Find horizontal divider
    for r in range(rows):
        if np.all(grid[r, :] == 8):
            hr = r
            break
    # Find vertical divider
    for c in range(cols):
        if np.all(grid[:, c] == 8):
            vc = c
            break
    return hr, vc

def get_quadrant_data(grid, hr, vc):
    """Identifies the Pattern Quadrant (PQ) and Color Quadrant (CQ)."""
    quadrants = {
        "TL": grid[0:hr, 0:vc],
        "TR": grid[0:hr, vc+1:],
        "BL": grid[hr+1:, 0:vc],
        "BR": grid[hr+1:, vc+1:]
    }

    pq_data = None
    pq_key = None
    cq_data = None
    cq_key = None

    # Identify PQ (6x6 with green 3)
    for key, quad in quadrants.items():
        if quad.shape == (6, 6) and np.any(quad == 3):
            pq_data = quad
            pq_key = key
            break

    if pq_key is None:
        raise ValueError("Pattern Quadrant (PQ) not found.")

    # Identify CQ (diagonally opposite to PQ)
    if pq_key == "TL": cq_key = "BR"
    elif pq_key == "TR": cq_key = "BL"
    elif pq_key == "BL": cq_key = "TR"
    elif pq_key == "BR": cq_key = "TL"

    cq_data = quadrants[cq_key]
    if cq_data.shape != (2, 2):
         raise ValueError(f"Color Quadrant (CQ) found at {cq_key} has incorrect shape {cq_data.shape}.")


    return pq_data, cq_data

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)

    # Find the azure dividing lines
    hr, vc = find_dividers(input_array)
    if hr == -1 or vc == -1:
        raise ValueError("Azure dividers not found.")

    # Identify Pattern Quadrant (PQ) and Color Quadrant (CQ)
    pq_grid, cq_grid = get_quadrant_data(input_array, hr, vc)

    # Extract the color key from CQ
    # cq_grid is already the 2x2 color key
    color_key = cq_grid

    # Initialize the output grid (6x6) with white (0)
    output_grid = np.zeros((6, 6), dtype=int)

    # Iterate through the Pattern Quadrant (PQ)
    for r in range(6):
        for c in range(6):
            # Check if the pixel in PQ is green (3)
            if pq_grid[r, c] == 3:
                # Determine the 3x3 sub-quadrant within the 6x6 PQ
                if r < 3 and c < 3:  # Top-Left sub-quadrant
                    target_color = color_key[0, 0]
                elif r < 3 and c >= 3: # Top-Right sub-quadrant
                    target_color = color_key[0, 1]
                elif r >= 3 and c < 3: # Bottom-Left sub-quadrant
                    target_color = color_key[1, 0]
                else: # r >= 3 and c >= 3 # Bottom-Right sub-quadrant
                    target_color = color_key[1, 1]

                # Update the output grid with the mapped color
                output_grid[r, c] = target_color
            # else: the output grid remains 0 (white) as initialized

    # Convert the result back to a list of lists
    return output_grid.tolist()