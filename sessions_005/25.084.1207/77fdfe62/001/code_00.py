import numpy as np

"""
Transforms the input grid based on the following rules:
1. Identify a rectangular frame of Blue (1) pixels.
2. Extract the inner pattern enclosed by the frame.
3. Identify the colors at the four absolute corners of the input grid.
4. Create an output grid with the same dimensions as the inner pattern.
5. For each pixel in the inner pattern:
   - If it's White (0), the corresponding output pixel is White (0).
   - If it's Azure (8), determine its quadrant (Top-Left, Top-Right, Bottom-Left, Bottom-Right) within the inner pattern.
   - Replace the Azure pixel with the color from the corresponding corner of the *input* grid (TL_color, TR_color, BL_color, BR_color).
"""

def find_frame_boundaries(grid):
    """
    Finds the minimum and maximum row and column indices of the Blue (1) pixels
    that form the outermost frame structure (excluding grid edges if corners are different).

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) defining the frame boundaries.
               Returns None if no blue frame pixels are found.
    """
    # Find coordinates of all blue pixels
    blue_coords = np.argwhere(grid == 1)

    # Check if any blue pixels were found
    if blue_coords.size == 0:
        # Based on examples, a frame is expected. Handle this case defensively.
        # In a real scenario, might raise an error or return a specific indicator.
        # For ARC, assume valid structure per examples. Let's return None to signal issue.
        print("Warning: No blue frame pixels found.")
        return None

    # Determine the extent of the blue pixels
    min_r = np.min(blue_coords[:, 0])
    max_r = np.max(blue_coords[:, 0])
    min_c = np.min(blue_coords[:, 1])
    max_c = np.max(blue_coords[:, 1])

    return min_r, max_r, min_c, max_c

def transform(input_grid):
    """
    Applies the quadrant-based color replacement transformation.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Check for trivial cases (e.g., grid too small to have frame + corners + inner)
    if H < 3 or W < 3:
        # Cannot possibly contain the expected structure
        print("Warning: Input grid too small.")
        return [] # Return empty list for invalid structure

    # --- Step 1: Identify the Frame ---
    frame_bounds = find_frame_boundaries(input_np)
    if frame_bounds is None:
        # Handle case where frame identification failed
        return [] # Return empty list
    min_r, max_r, min_c, max_c = frame_bounds

    # --- Step 2: Extract Inner Pattern ---
    # The inner pattern is the area strictly inside the frame boundaries
    inner_pattern = input_np[min_r + 1 : max_r, min_c + 1 : max_c]
    H_inner, W_inner = inner_pattern.shape

    # Check if inner pattern is valid
    if H_inner <= 0 or W_inner <= 0:
        print("Warning: Invalid frame or no inner pattern found.")
        return [] # Return empty list for invalid structure

    # --- Step 3: Identify Corner Colors ---
    TL_color = input_np[0, 0]
    TR_color = input_np[0, W - 1]
    BL_color = input_np[H - 1, 0]
    BR_color = input_np[H - 1, W - 1]

    # --- Step 4: Create Output Grid ---
    # Initialize with White (0), as White pixels map directly
    output_grid = np.zeros_like(inner_pattern)

    # --- Step 5: Populate Output Grid ---
    # Calculate the midpoints for quadrant division (integer division)
    mid_row = H_inner // 2
    mid_col = W_inner // 2

    # Iterate through each pixel of the inner pattern
    for r in range(H_inner):
        for c in range(W_inner):
            current_color = inner_pattern[r, c]

            if current_color == 0: # White pixel
                # Output is already initialized to 0 (White), so no change needed
                # output_grid[r, c] = 0
                pass
            elif current_color == 8: # Azure pixel
                # Determine the quadrant based on row and column relative to midpoints
                if r < mid_row and c < mid_col: # Top-Left Quadrant
                    output_grid[r, c] = TL_color
                elif r < mid_row and c >= mid_col: # Top-Right Quadrant
                    output_grid[r, c] = TR_color
                elif r >= mid_row and c < mid_col: # Bottom-Left Quadrant
                    output_grid[r, c] = BL_color
                elif r >= mid_row and c >= mid_col: # Bottom-Right Quadrant
                    output_grid[r, c] = BR_color
            # else:
                # If inner_pattern contains colors other than 0 or 8, they remain 0 in output.
                # This matches the observed behavior (only 0 and 8 seem relevant).
                # print(f"Warning: Unexpected color {current_color} found in inner pattern at ({r},{c}). It will be mapped to 0.")
                # pass

    # --- Step 6: Return Output Grid ---
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()