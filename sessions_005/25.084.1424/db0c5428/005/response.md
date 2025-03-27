```python
import numpy as np

"""
Transforms an input grid containing a single central pattern on a uniform background.
The transformation involves:
1. Identifying the background color (from the top-left corner).
2. Finding the bounding box and extracting the central pattern (P).
3. Creating an output grid of the same size, filled with the background color.
4. Placing four transformed versions of the pattern P into the corners of the output grid:
   - Top-Left: P rotated 90 degrees clockwise.
   - Top-Right: P rotated 90 degrees counter-clockwise.
   - Bottom-Left: P rotated 180 degrees.
   - Bottom-Right: The original pattern P.
The original location of P in the input is left as the background color in the output.
"""

# --- Helper Functions (copied from previous iteration) ---

def find_background_color(grid):
  """
  Determines the background color of the grid.
  Assumes the background color is the color present at the top-left corner.
  
  Args:
    grid: A numpy array representing the input grid.
  
  Returns:
    The integer color value of the background.
  """
  # Check if grid is empty or has zero size
  if grid.size == 0:
      # Handle empty grid case, perhaps return a default or raise error
      # For now, let's assume valid grids and return 0 (common default)
      # or handle based on task specification if available
      # Returning 0 might be problematic if 0 is a valid non-bg color.
      # A safer default might be -1 or None, requiring calling code to check.
      # Given ARC context, grids are non-empty, so [0,0] is usually safe.
      raise ValueError("Input grid is empty") 
  return grid[0, 0]

def find_pattern_bbox(grid, bg_color):
  """
  Finds the bounding box of non-background pixels.
  
  Args:
    grid: A numpy array representing the input grid.
    bg_color: The background color integer.
  
  Returns:
    A tuple (min_r, max_r, min_c, max_c) representing the bounding box 
    of non-background pixels, or None if no non-background pixels are found.
  """
  # Find coordinates of all pixels that are not the background color
  non_bg_pixels = np.where(grid != bg_color)
  
  # If there are no non-background pixels, return None
  if len(non_bg_pixels[0]) == 0:
    return None 
    
  # Determine the minimum and maximum row and column indices
  min_r = np.min(non_bg_pixels[0])
  max_r = np.max(non_bg_pixels[0])
  min_c = np.min(non_bg_pixels[1])
  max_c = np.max(non_bg_pixels[1])
  
  return min_r, max_r, min_c, max_c

def extract_pattern(grid, bbox):
   """
   Extracts the subgrid (pattern) defined by the bounding box.
   
   Args:
     grid: A numpy array representing the input grid.
     bbox: A tuple (min_r, max_r, min_c, max_c) defining the bounding box.
     
   Returns:
     A numpy array representing the extracted pattern.
   """
   if bbox is None:
       return np.array([[]]) # Return empty array if no bbox
   min_r, max_r, min_c, max_c = bbox
   # Slice the grid using the bounding box coordinates
   # Note: slicing is exclusive of the end index, so add 1 to max_r and max_c
   return grid[min_r:max_r+1, min_c:max_c+1]

def place_pattern(output_grid, pattern, r_start, c_start):
    """
    Places a pattern onto the output grid at the specified top-left corner.
    Overwrites existing pixels in the output grid. Handles partial placements
    if the pattern goes out of bounds.
    
    Args:
      output_grid: The numpy array representing the grid to place the pattern onto.
      pattern: The numpy array representing the pattern to place.
      r_start: The starting row index for the top-left corner of the placement.
      c_start: The starting column index for the top-left corner of the placement.
    """
    if pattern.size == 0: # Do nothing if the pattern is empty
        return
        
    pH, pW = pattern.shape
    H, W = output_grid.shape
    
    # Ensure starting indices are non-negative
    r_start = max(0, r_start)
    c_start = max(0, c_start)

    # Calculate the actual end row and column, respecting grid boundaries
    r_end = min(r_start + pH, H)
    c_end = min(c_start + pW, W)
    
    # Calculate the height and width of the slice to take from the pattern
    # This handles cases where the pattern placement starts off the grid or goes partially off
    slice_pH = r_end - r_start
    slice_pW = c_end - c_start
    
    # Determine the corresponding slice from the pattern
    pattern_r_start = 0
    pattern_c_start = 0
    # Adjust pattern slice start if placement started off-grid (negative r_start/c_start initially)
    # Although we clamped r_start/c_start to 0, this logic would handle it if we hadn't.
    # The main purpose here is to ensure we take the correct part of the pattern
    # if only a portion fits onto the grid.
    
    pattern_r_end = slice_pH
    pattern_c_end = slice_pW
    
    # Place the pattern slice if the slice dimensions are positive
    if slice_pH > 0 and slice_pW > 0:
        output_grid[r_start:r_end, c_start:c_end] = pattern[pattern_r_start:pattern_r_end, pattern_c_start:pattern_c_end]


# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the revised transformation based on multi-example analysis.
    """
    # Convert input list of lists to a numpy array for efficient manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Handle potentially empty input grid gracefully
    if input_np.size == 0:
        return [] # Or handle as per specific requirements for empty input

    H, W = input_np.shape

    # 1. Determine the background color
    bg_color = find_background_color(input_np)

    # 2. Initialize the output grid filled with the background color
    output_np = np.full_like(input_np, bg_color)

    # 3. Find the bounding box enclosing all non-background pixels
    bbox = find_pattern_bbox(input_np, bg_color)

    # If no non-background pattern is found, return the grid filled with background color
    if bbox is None:
      return output_np.tolist()

    # 4. Extract the pattern P based on the bounding box
    pattern_P = extract_pattern(input_np, bbox)
    
    # Check if pattern extraction was successful (bbox wasn't None)
    if pattern_P.size == 0:
        return output_np.tolist() # Return background grid if pattern is empty
        
    pH, pW = pattern_P.shape # Get height and width of the pattern

    # Ensure pattern dimensions are valid
    if pH <= 0 or pW <= 0:
        # This check might be redundant given the size check above, but doesn't hurt
        return output_np.tolist() 
      
    # 5. Calculate the geometrically transformed versions of the pattern
    P_rot90_cw = np.rot90(pattern_P, k=-1)   # Rotate 90 degrees clockwise (k=3 is equivalent)
    P_rot90_ccw = np.rot90(pattern_P, k=1)   # Rotate 90 degrees counter-clockwise
    P_rot180 = np.rot90(pattern_P, k=2)      # Rotate 180 degrees
    P_original = pattern_P                   # Original pattern

    # --- 6. Place the transformed patterns onto the output grid corners ---

    # Place rotated 90 deg CW pattern at top-left (0, 0)
    place_pattern(output_np, P_rot90_cw, 0, 0)

    # Place rotated 90 deg CCW pattern at top-right (0, W-pW)
    place_pattern(output_np, P_rot90_ccw, 0, W - pW)

    # Place rotated 180 deg pattern at bottom-left (H-pH, 0)
    place_pattern(output_np, P_rot180, H - pH, 0)

    # Place the original pattern P at bottom-right (H-pH, W-pW)
    place_pattern(output_np, P_original, H - pH, W - pW)

    # 7. Convert the final numpy array back to a list of lists for the required output format
    return output_np.tolist()
```