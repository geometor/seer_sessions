import numpy as np
from typing import List, Tuple, Set

"""
Transformation Rule:
1. Identify the overall orientation of the distinct, non-white color bands in the input grid (either horizontal or vertical).
2. Find all white pixels (color 0), referred to as 'defects'.
3. For each defect:
    a. Determine the color of the band it resides in by checking its non-white neighbors in the original input grid.
    b. If the band orientation is horizontal, change all pixels in the defect's column to white, but only within the rows that originally had the same color as the defect's band.
    c. If the band orientation is vertical, change all pixels in the defect's row to white, but only within the columns that originally had the same color as the defect's band.
4. The output grid reflects these changes, with defects projecting lines within their original color bands.
"""

def _determine_orientation(grid: np.ndarray) -> str:
    """
    Determines if the non-white bands are arranged horizontally or vertically.
    Assumes bands span the full width or height respectively.
    """
    height, width = grid.shape
    
    # Check for horizontal bands: any row contains multiple *different* non-white colors?
    is_horizontal = True
    for r in range(height):
        unique_non_white_colors = set(grid[r, c] for c in range(width) if grid[r, c] != 0)
        if len(unique_non_white_colors) > 1:
            is_horizontal = False
            break
            
    if is_horizontal:
        # Verify it's not just a single color grid
        all_colors = set(grid.flatten()) - {0}
        if len(all_colors) > 1 or height == 1: # Treat single band as horizontal potentially? Check examples. Yes, ex 1 is single band horizontally split. Needs refinement.
             # Let's check if there are *any* horizontal boundaries
             has_horizontal_boundary = False
             for r in range(height - 1):
                 if not np.array_equal(grid[r,:], grid[r+1,:]):
                    # Check if the change involves non-white colors
                    row1_colors = set(grid[r, c] for c in range(width) if grid[r, c] != 0)
                    row2_colors = set(grid[r+1, c] for c in range(width) if grid[r+1, c] != 0)
                    if row1_colors and row2_colors and row1_colors != row2_colors:
                        has_horizontal_boundary = True
                        break
             if has_horizontal_boundary:
                 return "horizontal"
        # Fall through if not definitively horizontal by boundary check

    # Check for vertical bands: any column contains multiple *different* non-white colors?
    is_vertical = True
    for c in range(width):
        unique_non_white_colors = set(grid[r, c] for r in range(height) if grid[r, c] != 0)
        if len(unique_non_white_colors) > 1:
            is_vertical = False
            break

    if is_vertical:
         # Check if there are *any* vertical boundaries
        has_vertical_boundary = False
        for c in range(width - 1):
             if not np.array_equal(grid[:,c], grid[:,c+1]):
                # Check if the change involves non-white colors
                col1_colors = set(grid[r, c] for r in range(height) if grid[r, c] != 0)
                col2_colors = set(grid[r, c+1] for r in range(height) if grid[r, c+1] != 0)
                if col1_colors and col2_colors and col1_colors != col2_colors:
                    has_vertical_boundary = True
                    break
        if has_vertical_boundary:
             return "vertical"
             
    # If only one passed the simple check, return that. This handles single-band cases implicitly.
    if is_horizontal and not is_vertical: return "horizontal"
    if is_vertical and not is_horizontal: return "vertical"
    
    # Default or ambiguous case - based on examples, horizontal seems more likely if both pass? Revisit.
    # Let's stick to the primary check for now, assuming valid inputs based on examples.
    # A grid entirely of one color could be either, but the projection rule needs an orientation.
    # Example 1 has multiple horizontal bands -> horizontal.
    # Example 2 has multiple vertical bands -> vertical.
    # If only one band exists, the projection rule still needs to apply. Let's re-evaluate simple checks.
    
    # Simplified re-check:
    non_white_grid = grid[grid != 0]
    if len(np.unique(non_white_grid)) <= 1:
        # Single color band. Does it have defects? If so, need a rule.
        # Let's assume horizontal if height >= width, vertical otherwise for single color? No, examples don't support this.
        # The examples always have multiple bands or clear separation.
        # If truly one solid color + defects, the rule is ambiguous. Assume problem constraints ensure multiple bands or clear separation.
        # Revert to initial simple checks.
        
        can_be_horizontal = True
        for r in range(height):
            unique_non_white_colors = set(grid[r, c] for c in range(width) if grid[r, c] != 0)
            if len(unique_non_white_colors) > 1:
                can_be_horizontal = False
                break
                
        can_be_vertical = True
        for c in range(width):
            unique_non_white_colors = set(grid[r, c] for r in range(height) if grid[r, c] != 0)
            if len(unique_non_white_colors) > 1:
                can_be_vertical = False
                break
        
        if can_be_horizontal and not can_be_vertical: return "horizontal"
        if can_be_vertical and not can_be_horizontal: return "vertical"
        # If both are true (e.g., single color grid), or neither (checkerboard?), requires more complex logic or assumptions.
        # Based on examples, one should be true and the other false.
        if can_be_horizontal: return "horizontal" # Default preference if ambiguous
        if can_be_vertical: return "vertical"


    # If we are here, something is complex. Let's refine the multi-color check.
    # If any row has multiple non-white colors -> not horizontal bands.
    # If any col has multiple non-white colors -> not vertical bands.
    
    has_multi_color_row = False
    for r in range(height):
        unique_non_white_colors = set(grid[r, c] for c in range(width) if grid[r, c] != 0)
        if len(unique_non_white_colors) > 1:
            has_multi_color_row = True
            break
            
    has_multi_color_col = False
    for c in range(width):
        unique_non_white_colors = set(grid[r, c] for r in range(height) if grid[r, c] != 0)
        if len(unique_non_white_colors) > 1:
            has_multi_color_col = True
            break
            
    if has_multi_color_col and not has_multi_color_row:
        return "horizontal" # Colors change row-wise
    elif has_multi_color_row and not has_multi_color_col:
        return "vertical" # Colors change column-wise
    else:
        # This case *shouldn't* happen based on examples (e.g. checkerboard would fail both)
        # Or a single color band would pass both initial checks.
        # Let's assume horizontal if height > width, vertical otherwise? Seems arbitrary.
        # Fallback based on first check
        if can_be_horizontal: return "horizontal"
        if can_be_vertical: return "vertical"
        return "horizontal" # Final fallback


def _find_defects(grid: np.ndarray) -> List[Tuple[int, int]]:
    """Finds coordinates of all white pixels (color 0)."""
    defects = np.where(grid == 0)
    return list(zip(defects[0], defects[1])) # List of (row, col) tuples

def _get_band_color(grid: np.ndarray, defect_r: int, defect_c: int) -> int:
    """Determines the color of the band surrounding a defect."""
    height, width = grid.shape
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Check orthogonal neighbors
        nr, nc = defect_r + dr, defect_c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbor_color = grid[nr, nc]
            if neighbor_color != 0:
                return neighbor_color
    # Should not happen in valid examples where defect is within a band
    # If it happens (e.g., defect surrounded by other defects), we might need broader search
    # Or assume grid[defect_r, defect_c] was originally the band color, which is risky.
    # Let's return a default (e.g., -1) or raise error if no non-white neighbor found.
    # Trying diagonal neighbors
    for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        nr, nc = defect_r + dr, defect_c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbor_color = grid[nr, nc]
            if neighbor_color != 0:
                return neighbor_color
                
    print(f"Warning: Could not determine band color for defect at ({defect_r}, {defect_c})")
    return -1 # Indicate failure

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by projecting white defects (0) vertically within
    horizontal color bands, or horizontally within vertical color bands.
    """
    # Convert to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid_np = grid_np.copy()
    height, width = grid_np.shape

    # 1. Determine band orientation
    orientation = _determine_orientation(grid_np)
    
    # 2. Find all defects
    defects = _find_defects(grid_np)
    
    # 3. Project each defect
    for defect_r, defect_c in defects:
        # a. Find the original band color around the defect location
        #    We use the original grid (grid_np) for this check.
        band_color = _get_band_color(grid_np, defect_r, defect_c)
        
        if band_color == -1:
            # Skip if we couldn't determine band color (shouldn't happen with task examples)
            continue

        # b. Project based on orientation, modifying the output grid
        if orientation == "horizontal":
            # Project vertically within the band color
            for r in range(height):
                # Check if the pixel in the original grid belongs to the same band
                if grid_np[r, defect_c] == band_color:
                    output_grid_np[r, defect_c] = 0
            # Ensure the original defect location itself is white in output
            output_grid_np[defect_r, defect_c] = 0 
                    
        elif orientation == "vertical":
            # Project horizontally within the band color
            for c in range(width):
                 # Check if the pixel in the original grid belongs to the same band
                if grid_np[defect_r, c] == band_color:
                    output_grid_np[defect_r, c] = 0
            # Ensure the original defect location itself is white in output
            output_grid_np[defect_r, defect_c] = 0

    # Convert back to list of lists
    output_grid = output_grid_np.tolist()
    
    return output_grid
