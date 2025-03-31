import numpy as np
from collections import Counter
from typing import List, Tuple, Dict, Optional, Set

"""
Transformation Rule:

1. Identify the background color (most frequent color).
2. Find all distinct, contiguous non-background objects.
3. Identify the top-leftmost object (TL_Anchor) and bottom-rightmost object (BR_Anchor).
4. Verify that TL_Anchor and BR_Anchor have the same color and shape (based on bounding box dimensions). If not, return the input grid unchanged.
5. Extract the repeating Vertical Pattern: Find the rectangular region immediately to the right of TL_Anchor that shares its rows. Scan columns rightwards from TL_Anchor's right edge until a column consisting entirely of the background color is found. The pattern is the block of columns before this background column. If no background column is found before BR_Anchor's left edge, use all columns up to BR_Anchor's left edge.
6. Extract the repeating Horizontal Pattern: Find the rectangular region immediately below TL_Anchor that shares its columns. Scan rows downwards from TL_Anchor's bottom edge until a row consisting entirely of the background color is found. The pattern is the block of rows before this background row. If no background row is found before BR_Anchor's top edge, use all rows up to BR_Anchor's top edge.
7. Determine the Vertical_Frame_Color: Scan the region defined by TL_Anchor's rows and the columns between TL_Anchor's right edge and BR_Anchor's left edge. Find the first non-background color encountered (scanning row by row, then column by column).
8. Determine the Horizontal_Frame_Color: Scan the region defined by TL_Anchor's columns and the rows between TL_Anchor's bottom edge and BR_Anchor's top edge. Find the first non-background color encountered (scanning row by row, then column by column).
9. If either frame color cannot be determined (e.g., regions are empty or all background), return the input grid unchanged.
10. Create an output grid initialized as a copy of the input grid.
11. Tile the extracted Vertical_Pattern horizontally in the output grid, filling the area defined by TL_Anchor's rows and the columns between the right edge of TL_Anchor and the left edge of BR_Anchor. Use modulo arithmetic based on the pattern's width for repetition.
12. Tile the extracted Horizontal_Pattern vertically in the output grid, filling the area defined by TL_Anchor's columns and the rows between the bottom edge of TL_Anchor and the top edge of BR_Anchor. Use modulo arithmetic based on the pattern's height for repetition.
13. Define a frame one pixel outside the combined bounding box of the TL_Anchor and BR_Anchor.
14. Draw the frame onto the output grid, ensuring it stays within grid bounds:
    - Left and Right vertical segments (including corners) use Horizontal_Frame_Color.
    - Top and Bottom horizontal segments (between the vertical segments) use Vertical_Frame_Color.
15. Return the modified output grid.
"""

# Helper class to store object information
class GridObject:
    def __init__(self, color: int, pixels: Set[Tuple[int, int]]):
        self.color = color
        self.pixels = pixels
        if not pixels:
             # Should not happen with valid objects, but prevent errors
            self.min_row, self.min_col = -1, -1
            self.max_row, self.max_col = -1, -1
            self.height, self.width = 0, 0
        else:
            rows = [r for r, c in pixels]
            cols = [c for r, c in pixels]
            self.min_row = min(rows)
            self.min_col = min(cols)
            self.max_row = max(rows)
            self.max_col = max(cols)
            self.height = self.max_row - self.min_row + 1
            self.width = self.max_col - self.min_col + 1

    def __eq__(self, other):
        if not isinstance(other, GridObject):
            return NotImplemented
        # Shape comparison based on dimensions and color
        return self.color == other.color and self.height == other.height and self.width == other.width

    def __repr__(self):
        return f"Object(Color:{self.color}, Pos:({self.min_row},{self.min_col}) to ({self.max_row},{self.max_col}), Size:{self.height}x{self.width})"

def find_objects(grid: np.ndarray, background_color: int) -> List[GridObject]:
    """Finds all contiguous objects of non-background colors using 4-connectivity."""
    objects = []
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                
                obj_pixels_list = [] # Keep order for easier debugging if needed
                
                while q:
                    row, col = q.pop(0)
                    pixels.add((row, col))
                    obj_pixels_list.append((row, col))

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if pixels:
                    objects.append(GridObject(color, pixels))
    return objects

def find_first_non_background(grid: np.ndarray, background_color: int, 
                             r_start: int, r_end: int, 
                             c_start: int, c_end: int) -> Optional[int]:
    """Finds the first non-background color in a specified region (row-major scan)."""
    height, width = grid.shape
    # Ensure ranges are valid and within grid bounds before iterating
    r_start_safe = max(0, r_start)
    r_end_safe = min(height, r_end)
    c_start_safe = max(0, c_start)
    c_end_safe = min(width, c_end)

    for r in range(r_start_safe, r_end_safe):
        for c in range(c_start_safe, c_end_safe):
             if grid[r, c] != background_color:
                 return grid[r, c]
    return None # No non-background color found


def transform(input_grid: np.ndarray) -> np.ndarray:
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Identify background color
    counts = Counter(input_grid.flatten())
    if not counts: # Handle empty grid case
        return output_grid
    background_color = counts.most_common(1)[0][0]

    # 2. Find all non-background objects
    objects = find_objects(input_grid, background_color)
    if not objects:
        return output_grid # No objects, no transformation

    # 3. Identify TL_Anchor and BR_Anchor
    # Sort by top-row, then left-column for TL
    objects.sort(key=lambda o: (o.min_row, o.min_col))
    tl_anchor = objects[0]
    
    # Sort by bottom-row (desc), then right-column (desc) for BR
    objects.sort(key=lambda o: (o.max_row, o.max_col), reverse=True)
    br_anchor = objects[0]

    # Ensure distinct anchors if multiple objects exist
    if len(objects) > 1 and tl_anchor is br_anchor:
         # If TL and BR based on initial sorts are the same, re-evaluate BR
         potential_br_candidates = sorted([o for o in objects if o is not tl_anchor], 
                                          key=lambda o: (o.max_row, o.max_col), 
                                          reverse=True)
         if potential_br_candidates:
             br_anchor = potential_br_candidates[0]
         else: # Only one object was found effectively
             return output_grid
             
    # Final check if anchors are distinct
    if tl_anchor is br_anchor:
         return output_grid # Cannot proceed if anchors are not distinct

    # 4. Verify anchors match in color and shape (dimensions)
    if tl_anchor.color != br_anchor.color or \
       tl_anchor.height != br_anchor.height or \
       tl_anchor.width != br_anchor.width:
        return output_grid # Anchors don't match criteria

    # --- Define Potential Regions for Frame Color Determination ---
    frame_vp_r_start = tl_anchor.min_row
    frame_vp_r_end = tl_anchor.max_row + 1
    frame_vp_c_start = tl_anchor.max_col + 1
    frame_vp_c_end = br_anchor.min_col

    frame_hp_r_start = tl_anchor.max_row + 1
    frame_hp_r_end = br_anchor.min_row
    frame_hp_c_start = tl_anchor.min_col
    frame_hp_c_end = tl_anchor.max_col + 1

    # Check if these frame determination regions have positive dimensions
    valid_frame_vp_region = frame_vp_r_end > frame_vp_r_start and frame_vp_c_end > frame_vp_c_start
    valid_frame_hp_region = frame_hp_r_end > frame_hp_r_start and frame_hp_c_end > frame_hp_c_start

    # 7. Determine Vertical_Frame_Color (from potential region)
    vertical_frame_color = None
    if valid_frame_vp_region:
        vertical_frame_color = find_first_non_background(input_grid, background_color, 
                                                         frame_vp_r_start, frame_vp_r_end, 
                                                         frame_vp_c_start, frame_vp_c_end)
                                                      
    # 8. Determine Horizontal_Frame_Color (from potential region)
    horizontal_frame_color = None
    if valid_frame_hp_region:
        horizontal_frame_color = find_first_non_background(input_grid, background_color,
                                                           frame_hp_r_start, frame_hp_r_end,
                                                           frame_hp_c_start, frame_hp_c_end)

    # 9. Check if frame colors were found (if regions were valid)
    if (valid_frame_vp_region and vertical_frame_color is None) or \
       (valid_frame_hp_region and horizontal_frame_color is None):
         # If a region exists but has no non-background color, rule might not apply
         # Or if frame colors are essential and missing, return original
         # For this task, frame colors seem essential.
         return output_grid
         
    # If a region didn't exist, we might still proceed if the other exists.
    # However, the examples imply both patterns and frame colors derived from them exist.
    # Let's enforce that both frame colors must be found if their regions are valid.
    if vertical_frame_color is None or horizontal_frame_color is None:
        return output_grid # Essential colors missing


    # --- Extract Actual Repeating Patterns ---
    
    # 5. Extract Vertical Pattern
    vp_rows = slice(tl_anchor.min_row, tl_anchor.max_row + 1)
    vp_start_col = tl_anchor.max_col + 1
    vp_end_col = vp_start_col 
    for c in range(vp_start_col, br_anchor.min_col):
        # Ensure column index is valid before checking
        if c >= width: break 
        # Check if the column slice within anchor rows is all background
        if np.all(input_grid[vp_rows, c] == background_color):
            vp_end_col = c # End column is the first background-only column
            break
    else: # No background column found before BR anchor
        vp_end_col = br_anchor.min_col

    # Check if vp_end_col makes sense (it must be > vp_start_col for a pattern)
    if vp_end_col <= vp_start_col:
         # Vertical pattern is empty or invalid
         return output_grid 
    vertical_pattern = input_grid[vp_rows, vp_start_col:vp_end_col]
    vp_h, vp_w = vertical_pattern.shape
    if vp_h == 0 or vp_w == 0: return output_grid # Pattern is empty

    # 6. Extract Horizontal Pattern
    hp_cols = slice(tl_anchor.min_col, tl_anchor.max_col + 1)
    hp_start_row = tl_anchor.max_row + 1
    hp_end_row = hp_start_row
    for r in range(hp_start_row, br_anchor.min_row):
        if r >= height: break
        if np.all(input_grid[r, hp_cols] == background_color):
            hp_end_row = r
            break
    else: # No background row found
        hp_end_row = br_anchor.min_row
        
    if hp_end_row <= hp_start_row:
        # Horizontal pattern is empty or invalid
        return output_grid
    horizontal_pattern = input_grid[hp_start_row:hp_end_row, hp_cols]
    hp_h, hp_w = horizontal_pattern.shape
    if hp_h == 0 or hp_w == 0: return output_grid # Pattern is empty


    # --- Apply Transformations to output_grid ---

    # 11. Tile Vertical_Pattern horizontally
    target_vp_rows = slice(tl_anchor.min_row, tl_anchor.max_row + 1) # Rows to fill
    target_vp_c_start = tl_anchor.max_col + 1
    target_vp_c_end = br_anchor.min_col 
    for c in range(target_vp_c_start, target_vp_c_end):
        # Check column bounds
        if c >= width: break 
        pattern_col_idx = (c - target_vp_c_start) % vp_w
        output_grid[target_vp_rows, c] = vertical_pattern[:, pattern_col_idx]

    # 12. Tile Horizontal_Pattern vertically
    target_hp_cols = slice(tl_anchor.min_col, tl_anchor.max_col + 1) # Columns to fill
    target_hp_r_start = tl_anchor.max_row + 1
    target_hp_r_end = br_anchor.min_row
    for r in range(target_hp_r_start, target_hp_r_end):
        if r >= height: break
        pattern_row_idx = (r - target_hp_r_start) % hp_h
        output_grid[r, target_hp_cols] = horizontal_pattern[pattern_row_idx, :]

    # --- Draw Frame ---
    # 13. Define frame boundaries
    frame_top = tl_anchor.min_row - 1
    frame_bottom = br_anchor.max_row + 1
    frame_left = tl_anchor.min_col - 1
    frame_right = br_anchor.max_col + 1

    # 14. Draw the frame safely within grid bounds
    # Draw vertical bars (left/right) - including corners
    if 0 <= frame_left < width:
        row_start_safe = max(0, frame_top)
        row_end_safe = min(height, frame_bottom + 1)
        if row_end_safe > row_start_safe: # Check if there's any row to draw
             output_grid[row_start_safe:row_end_safe, frame_left] = horizontal_frame_color
    
    if 0 <= frame_right < width:
        row_start_safe = max(0, frame_top)
        row_end_safe = min(height, frame_bottom + 1)
        if row_end_safe > row_start_safe:
             output_grid[row_start_safe:row_end_safe, frame_right] = horizontal_frame_color

    # Draw horizontal bars (top/bottom) - between vertical bars' inner edges
    col_start_safe = max(0, frame_left + 1)
    col_end_safe = min(width, frame_right) # End index is exclusive for slicing
    
    if 0 <= frame_top < height and col_end_safe > col_start_safe: # Check row valid and width > 0
        output_grid[frame_top, col_start_safe:col_end_safe] = vertical_frame_color
        
    if 0 <= frame_bottom < height and col_end_safe > col_start_safe:
        output_grid[frame_bottom, col_start_safe:col_end_safe] = vertical_frame_color

    # 15. Return final grid
    return output_grid