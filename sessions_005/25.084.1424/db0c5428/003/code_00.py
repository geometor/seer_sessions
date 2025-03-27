import numpy as np

def find_background_color(grid):
  """
  Determines the background color of the grid.
  Assumes the background color is the color present at the corners.
  Uses the top-left corner.
  
  Args:
    grid: A numpy array representing the input grid.
  
  Returns:
    The integer color value of the background.
  """
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
   min_r, max_r, min_c, max_c = bbox
   # Slice the grid using the bounding box coordinates
   # Note: slicing is exclusive of the end index, so add 1 to max_r and max_c
   return grid[min_r:max_r+1, min_c:max_c+1]

def place_pattern(output_grid, pattern, r_start, c_start):
    """
    Places a pattern onto the output grid at the specified top-left corner.
    Overwrites existing pixels in the output grid. Handles partial placements
    if the pattern goes out of bounds, though the calling logic should try
    to prevent completely out-of-bounds placements.
    
    Args:
      output_grid: The numpy array representing the grid to place the pattern onto.
      pattern: The numpy array representing the pattern to place.
      r_start: The starting row index for the top-left corner of the placement.
      c_start: The starting column index for the top-left corner of the placement.
    """
    pH, pW = pattern.shape
    H, W = output_grid.shape
    
    # Calculate the actual end row and column, respecting grid boundaries
    r_end = min(r_start + pH, H)
    c_end = min(c_start + pW, W)
    
    # Calculate the height and width of the slice to take from the pattern
    # This handles cases where the pattern placement goes partially off the grid
    slice_pH = r_end - r_start
    slice_pW = c_end - c_start

    # Ensure we only try to place if the starting indices are within bounds
    # and the calculated slice dimensions are positive
    if r_start < H and c_start < W and slice_pH > 0 and slice_pW > 0:
        # Place the potentially sliced pattern onto the output grid
        output_grid[r_start:r_end, c_start:c_end] = pattern[:slice_pH, :slice_pW]


def transform(input_grid):
    """
    The transformation identifies the background color (typically the color at the corners). 
    It finds the bounding box of the central rectangular pattern formed by non-background pixels. 
    Let this pattern be P, its height pH, its width pW, and its top-left corner in the input be (r0, c0). 
    An output grid of the same dimensions as the input is created, initially filled with the background color. 
    Four versions of the pattern P are placed onto the output grid:
    1. The 180-degree rotated version of P is placed at the top-left corner (0, 0).
    2. The vertically flipped version of P is placed at the top-right corner (0, W-pW).
    3. The horizontally flipped version of P is placed at the bottom-left corner (H-pH, 0).
    4. The original pattern P is placed at its original position (r0, c0).
    Placements overwrite existing pixels, with the final placement of the original pattern P taking precedence in case of overlaps.
    """
    # Convert input list of lists to a numpy array for efficient manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Determine the background color (assumed from top-left corner)
    bg_color = find_background_color(input_np)

    # Initialize the output grid filled with the background color
    output_np = np.full_like(input_np, bg_color)

    # Find the bounding box enclosing all non-background pixels
    bbox = find_pattern_bbox(input_np, bg_color)

    # If no non-background pattern is found, return the grid filled with background color
    if bbox is None:
      return output_np.tolist()

    # Unpack bounding box coordinates
    min_r, max_r, min_c, max_c = bbox
    
    # Extract the pattern P based on the bounding box
    pattern_P = extract_pattern(input_np, bbox)
    pH, pW = pattern_P.shape # Get height and width of the pattern

    # Check if pattern dimensions are valid (e.g., not exceeding grid size)
    # This is a safeguard, should not happen if bbox is correct.
    if pH <= 0 or pW <= 0:
        return output_np.tolist() 
      
    # Calculate the geometrically transformed versions of the pattern
    P_rot180 = np.rot90(pattern_P, 2)   # Rotate 180 degrees
    P_flipV = np.flipud(pattern_P)    # Flip vertically (up-down)
    P_flipH = np.fliplr(pattern_P)    # Flip horizontally (left-right)

    # --- Place the transformed patterns onto the output grid ---
    # The order matters if there are overlaps. We place the corner patterns first.

    # 1. Place 180-degree rotated pattern at the top-left corner (0, 0)
    # Check if placement is possible within grid bounds before calling place_pattern
    if 0 + pH <= H and 0 + pW <= W:
        place_pattern(output_np, P_rot180, 0, 0)
  
    # 2. Place vertically flipped pattern at the top-right corner (0, W-pW)
    # Check if placement is possible within grid bounds
    if 0 + pH <= H and W - pW >= 0:
        place_pattern(output_np, P_flipV, 0, W - pW)

    # 3. Place horizontally flipped pattern at the bottom-left corner (H-pH, 0)
    # Check if placement is possible within grid bounds
    if H - pH >= 0 and 0 + pW <= W:
        place_pattern(output_np, P_flipH, H - pH, 0)

    # 4. Place the original pattern P at its original position (min_r, min_c)
    # This is placed last, so it overwrites parts of the corner patterns in case of overlap.
    place_pattern(output_np, pattern_P, min_r, min_c)

    # Convert the final numpy array back to a list of lists for the required output format
    return output_np.tolist()