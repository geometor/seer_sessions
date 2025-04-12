import numpy as np
from scipy.ndimage import label, generate_binary_structure

"""
Transformation Rule:

1. Identify the two distinct non-white colors (Color A, Color B) and their pixel locations in the input grid.
2. Determine which color acts as the 'interrupting' color. This is done by temporarily removing one color (setting its pixels to white) and checking if the other color's pixels remain a single connected component.
3. The color whose pixels *remain* connected when the *other* color is removed is the 'kept' color (it was the one being interrupted). The other color is the 'interrupting' color and is discarded.
4. Calculate the union of the pixel locations of both original non-white colors.
5. Create an output grid of the same dimensions as the input, filled with the background color (white, 0).
6. Fill the pixels corresponding to the calculated union shape with the 'kept' color.
"""

def find_colors(grid: np.ndarray) -> tuple[int, int]:
    """Finds the two distinct non-background (0) colors in the grid."""
    unique_colors = np.unique(grid)
    non_background_colors = unique_colors[unique_colors != 0]
    if len(non_background_colors) != 2:
        # This case might need more robust handling depending on task variations
        # For this specific task based on examples, we expect exactly 2.
        raise ValueError(f"Expected 2 non-background colors, found {len(non_background_colors)}")
    return tuple(non_background_colors)

def get_pixel_coords(grid: np.ndarray, color: int) -> set[tuple[int, int]]:
    """Gets the coordinates of all pixels with the specified color."""
    rows, cols = np.where(grid == color)
    return set(zip(rows, cols))

def is_connected(grid: np.ndarray, color: int) -> bool:
    """Checks if all pixels of a given color form a single connected component (4-connectivity)."""
    # Create a binary mask for the target color
    mask = (grid == color)
    
    # Define 4-connectivity structure
    connectivity_structure = generate_binary_structure(2, 1) # Rank 2, connectivity 1 (von Neumann)
    
    # Label connected components
    labeled_array, num_features = label(mask, structure=connectivity_structure)
    
    # Return True if exactly one component is found
    return num_features == 1

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the object interruption rule.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape
    background_color = 0

    # 1. Identify the two distinct non-white colors and their pixels
    try:
        color_a, color_b = find_colors(grid_np)
    except ValueError:
        # Handle cases where the input doesn't match expectations (e.g., < 2 colors)
        # For this task, returning the input or an empty grid might be options,
        # but based on examples, we assume valid input. Let's return an empty grid of same size.
         return [[background_color for _ in range(width)] for _ in range(height)]


    coords_a = get_pixel_coords(grid_np, color_a)
    coords_b = get_pixel_coords(grid_np, color_b)

    # 2. & 3. Determine which color is interrupting / kept
    
    # Create a temporary grid removing color B
    temp_grid_a = grid_np.copy()
    for r, c in coords_b:
        temp_grid_a[r, c] = background_color
    # Check if color A is still connected
    a_connected_without_b = is_connected(temp_grid_a, color_a)

    # Create a temporary grid removing color A
    temp_grid_b = grid_np.copy()
    for r, c in coords_a:
        temp_grid_b[r, c] = background_color
    # Check if color B is still connected
    b_connected_without_a = is_connected(temp_grid_b, color_b)

    kept_color = -1 # Initialize with invalid value
    if a_connected_without_b and not b_connected_without_a:
        # A remained connected when B was removed, so A was interrupted by B. Keep A.
        kept_color = color_a
    elif not a_connected_without_b and b_connected_without_a:
        # B remained connected when A was removed, so B was interrupted by A. Keep B.
        kept_color = color_b
    else:
        # This case suggests either both remained connected (no interruption?) 
        # or both became disconnected (mutual interruption?), or only one color present initially.
        # Based on problem description, one should interrupt the other.
        # If logic fails, default or error handling needed. For now, assume one case holds true.
        # Let's check if one was actually present to begin with
        if not coords_a: return [[background_color for _ in range(width)] for _ in range(height)] # No color A
        if not coords_b: return [[background_color for _ in range(width)] for _ in range(height)] # No color B
        # If both present and neither/both are interrupted, the logic might need refinement for edge cases
        # For the given examples, this shouldn't happen.
        # Defaulting to returning background if logic is inconclusive.
        return [[background_color for _ in range(width)] for _ in range(height)]
        

    # 4. Calculate the union of pixel locations
    union_coords = coords_a.union(coords_b)

    # 5. Create the output grid, initially filled with background color
    output_grid_np = np.full((height, width), background_color, dtype=int)

    # 6. Fill the union shape with the kept color
    for r, c in union_coords:
        output_grid_np[r, c] = kept_color

    # Convert back to list of lists for the required output format
    return output_grid_np.tolist()