import numpy as np

"""
Identify the bounding box of all gray (5) pixels in the input grid.
Extract a subgrid from the input grid. The subgrid's columns range from the minimum column index to the maximum column index of the gray bounding box.
The subgrid's rows range from one row above the minimum row index of the gray bounding box to one row below the maximum row index of the gray bounding box.
"""

def find_color_coordinates(grid, color):
    """Finds all coordinates (row, col) of a given color in the grid."""
    coordinates = np.argwhere(grid == color)
    return coordinates

def get_bounding_box(coordinates):
    """Calculates the bounding box (min_row, max_row, min_col, max_col) from a list of coordinates."""
    if len(coordinates) == 0:
        return None # Or raise an error, or return a default
    min_row = np.min(coordinates[:, 0])
    max_row = np.max(coordinates[:, 0])
    min_col = np.min(coordinates[:, 1])
    max_col = np.max(coordinates[:, 1])
    return min_row, max_row, min_col, max_col

def extract_subgrid(grid, r_start, r_end, c_start, c_end):
    """Extracts a subgrid based on inclusive start and end row/column indices."""
    # Adjust end indices for numpy slicing (exclusive)
    return grid[r_start:r_end + 1, c_start:c_end + 1]

def transform(input_grid):
    """
    Transforms the input grid by extracting a subgrid defined by the bounding box of gray pixels,
    expanded by one row above and one row below.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Identify all pixels in the input grid that have the color gray (5).
    gray_coords = find_color_coordinates(input_np, 5)
    
    # Check if any gray pixels were found (as per examples, they always exist)
    if len(gray_coords) == 0:
        # Behavior is undefined by examples, returning input or empty might be options.
        # Based on the deterministic nature of ARC tasks, let's assume gray pixels are always present.
        # If this assumption fails on test cases, we might need to adjust.
        # For now, let's raise an error or return something predictable if needed.
        # Returning the original grid might be safest if no clear instruction.
        # Let's stick to the derived rule assuming gray pixels exist.
        pass 
        
    # 2. Determine the minimum/maximum row/column indices for gray pixels.
    min_r, max_r, min_c, max_c = get_bounding_box(gray_coords)
    
    # 3. Define the row range for extraction (expanded by 1 above and below).
    start_row = min_r - 1
    end_row = max_r + 1
    
    # 4. Define the column range for extraction (same as gray bbox).
    start_col = min_c
    end_col = max_c
    
    # Handle potential boundary issues (though not seen in examples)
    # Ensure indices are within the original grid dimensions
    grid_height, grid_width = input_np.shape
    start_row = max(0, start_row)
    end_row = min(grid_height - 1, end_row)
    start_col = max(0, start_col)
    end_col = min(grid_width - 1, end_col)

    # 5. Extract the subgrid using the calculated ranges.
    output_np = extract_subgrid(input_np, start_row, end_row, start_col, end_col)
    
    # 6. Convert the output numpy array back to a list of lists.
    output_grid = output_np.tolist()

    return output_grid