import numpy as np
from typing import List, Tuple

"""
Transforms an input grid based on the following rules:
1. Identify the single contiguous azure (8) object.
2. Determine its minimal bounding box.
3. Extract the pattern within the bounding box (raw_pattern).
4. Create a 3x3 base pattern grid, initialized to white (0).
5. Place the raw_pattern into the 3x3 base_pattern grid, aligning the raw_pattern's bottom-left corner with the base_pattern's bottom-left corner. If the raw_pattern is smaller than 3x3, the remaining cells in base_pattern stay white. If larger, the bottom-left 3x3 portion of raw_pattern is used.
6. Count the number of yellow (4) pixels (N) in the input grid.
7. Construct the output grid by tiling the 3x3 base_pattern horizontally N times. The output grid dimensions will be 3 rows by (3 * N) columns.
"""

def get_color_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def get_bounding_box(pixels: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Calculates the minimal bounding box (min_row, min_col, max_row, max_col) for a list of pixels."""
    if not pixels:
        # Or raise an error, or return a default? Based on problem constraints, this shouldn't happen.
        return (0, 0, -1, -1) 
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    min_row = min(rows)
    min_col = min(cols)
    max_row = max(rows)
    max_col = max(cols)
    return min_row, min_col, max_row, max_col

def extract_subgrid(grid: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Extracts a subgrid based on bounding box coordinates."""
    min_row, min_col, max_row, max_col = bbox
    if min_row > max_row or min_col > max_col:
        return np.array([[]]) # Return empty if bounding box is invalid
    return grid[min_row:max_row+1, min_col:max_col+1]

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by extracting an azure pattern, creating a 
    3x3 base pattern aligned to the bottom-left, counting yellow markers, 
    and tiling the base pattern horizontally based on the count.
    """
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Locate the azure object and its bounding box
    azure_color = 8
    azure_pixels = get_color_pixels(input_array, azure_color)
    if not azure_pixels:
         # Handle case with no azure object if necessary, based on constraints.
         # Assuming one always exists per problem description.
         # Returning empty or input might be options depending on exact rules.
         # For now, let's assume it exists.
         pass 
    
    # 2. Determine bounding box
    bbox = get_bounding_box(azure_pixels)
    
    # 3. Extract the raw pattern
    raw_pattern = extract_subgrid(input_array, bbox)
    raw_h, raw_w = raw_pattern.shape
    
    # 4. Initialize the 3x3 base pattern
    base_pattern = np.zeros((3, 3), dtype=int) # Initialized to white (0)
    
    # 5. Copy raw_pattern into base_pattern (bottom-left aligned)
    # Determine the part of raw_pattern to copy (bottom-left 3x3 portion)
    src_h = min(raw_h, 3)
    src_w = min(raw_w, 3)
    src_start_row = raw_h - src_h
    src_start_col = 0 # Always align to left within the source for simplicity of slicing
    
    # Determine where to place it in base_pattern (bottom-left)
    dest_start_row = 3 - src_h
    dest_start_col = 0
    
    # Perform the copy
    base_pattern[dest_start_row : dest_start_row + src_h, 
                 dest_start_col : dest_start_col + src_w] = \
        raw_pattern[src_start_row : src_start_row + src_h, 
                    src_start_col : src_start_col + src_w]

    # 6. Count yellow markers
    yellow_color = 4
    num_yellow = np.count_nonzero(input_array == yellow_color)
    
    # Handle N=0 case explicitly if needed. np.tile with 0 reps creates empty dimension.
    if num_yellow == 0:
        # Return empty grid or a default? Based on examples, N >= 1.
        # Let's return a 3x0 grid representation for consistency with tiling.
         output_grid = np.zeros((3,0), dtype=int)
    else:
        # 7. Tile the base pattern horizontally N times
        output_grid = np.tile(base_pattern, (1, num_yellow))
        
    # Convert back to list of lists for the required output format
    return output_grid.tolist()