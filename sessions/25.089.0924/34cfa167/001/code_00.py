import numpy as np
from collections import Counter
from typing import List, Tuple, Dict, Optional, Set

"""
Transformation Rule:

1. Identify the background color (most frequent color).
2. Find all distinct, contiguous non-background objects.
3. Identify the top-leftmost object (TL_Anchor) and bottom-rightmost object (BR_Anchor).
4. Verify that TL_Anchor and BR_Anchor have the same color and shape (based on bounding box dimensions).
5. Extract the rectangular region immediately to the right of TL_Anchor, up to the column before BR_Anchor, as the Vertical_Pattern.
6. Extract the rectangular region immediately below TL_Anchor, up to the row before BR_Anchor, as the Horizontal_Pattern.
7. Determine the Vertical_Frame_Color by finding the first non-background color in the Vertical_Pattern region (scanning row by row, then column by column).
8. Determine the Horizontal_Frame_Color by finding the first non-background color in the Horizontal_Pattern region (scanning row by row, then column by column).
9. Create an output grid initialized as a copy of the input grid.
10. Tile the Vertical_Pattern horizontally in the output grid, filling the area between the anchors' vertical extent and between the right edge of TL_Anchor and the left edge of BR_Anchor.
11. Tile the Horizontal_Pattern vertically in the output grid, filling the area between the anchors' horizontal extent and between the bottom edge of TL_Anchor and the top edge of BR_Anchor.
12. Define a frame one pixel outside the combined bounding box of the TL_Anchor and BR_Anchor.
13. Draw the frame:
    - Left and Right vertical segments use Horizontal_Frame_Color.
    - Top and Bottom horizontal segments (between the vertical segments) use Vertical_Frame_Color.
"""

# Helper class to store object information
class GridObject:
    def __init__(self, color: int, pixels: Set[Tuple[int, int]]):
        self.color = color
        self.pixels = pixels
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
        # Simple shape comparison based on dimensions and color
        return self.color == other.color and self.height == other.height and self.width == other.width

    def __repr__(self):
        return f"Object(Color:{self.color}, Pos:({self.min_row},{self.min_col}) to ({self.max_row},{self.max_col}), Size:{self.height}x{self.width})"


def find_objects(grid: np.ndarray, background_color: int) -> List[GridObject]:
    """Finds all contiguous objects of non-background colors."""
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
                
                while q:
                    row, col = q.pop(0)
                    pixels.add((row, col))

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
    """Finds the first non-background color in a specified region."""
    for r in range(r_start, r_end):
        for c in range(c_start, c_end):
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                if grid[r, c] != background_color:
                    return grid[r, c]
    return None # Should not happen based on examples, but good practice


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the tiling and framing transformation based on anchor objects.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Identify background color
    counts = Counter(input_grid.flatten())
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

    # Ensure we didn't pick the same object if there's only one
    if len(objects) == 1:
         return output_grid # Cannot form pattern with one object

    # Handle cases where TL and BR might be the same due to sorting criteria
    # Re-find BR by explicitly looking for max row/col if TL and BR are identical initially
    if tl_anchor is br_anchor:
         potential_br = [o for o in objects if o is not tl_anchor]
         if not potential_br:
              return output_grid # Still only one effective anchor
         potential_br.sort(key=lambda o: (o.max_row, o.max_col), reverse=True)
         br_anchor = potential_br[0]

    # Check if TL and BR are distinct and valid candidates
    if tl_anchor is br_anchor or not tl_anchor or not br_anchor:
        # Fallback or error: Cannot determine distinct anchors
        # Based on examples, this shouldn't happen if the pattern is applicable
        return output_grid

    # 4. Verify anchors match in color and shape (dimensions)
    if tl_anchor.color != br_anchor.color or \
       tl_anchor.height != br_anchor.height or \
       tl_anchor.width != br_anchor.width:
        # Anchors don't match criteria
        return output_grid

    # --- Define pattern regions ---
    vp_r_start = tl_anchor.min_row
    vp_r_end = tl_anchor.max_row + 1
    vp_c_start = tl_anchor.max_col + 1
    vp_c_end = br_anchor.min_col

    hp_r_start = tl_anchor.max_row + 1
    hp_r_end = br_anchor.min_row
    hp_c_start = tl_anchor.min_col
    hp_c_end = tl_anchor.max_col + 1

    # Check if regions have valid dimensions (end > start)
    valid_vp = vp_r_end > vp_r_start and vp_c_end > vp_c_start
    valid_hp = hp_r_end > hp_r_start and hp_c_end > hp_c_start

    if not valid_vp or not valid_hp:
         # If either pattern region is invalid/empty, cannot proceed
         return output_grid

    # 5. Extract Vertical_Pattern
    vertical_pattern = input_grid[vp_r_start:vp_r_end, vp_c_start:vp_c_end]
    vp_h, vp_w = vertical_pattern.shape

    # 6. Extract Horizontal_Pattern
    horizontal_pattern = input_grid[hp_r_start:hp_r_end, hp_c_start:hp_c_end]
    hp_h, hp_w = horizontal_pattern.shape

    # Check if patterns are empty (although region check should cover this)
    if vp_h == 0 or vp_w == 0 or hp_h == 0 or hp_w == 0:
         return output_grid

    # 7. Determine Vertical_Frame_Color
    vertical_frame_color = find_first_non_background(input_grid, background_color, 
                                                     vp_r_start, vp_r_end, 
                                                     vp_c_start, vp_c_end)
                                                      
    # 8. Determine Horizontal_Frame_Color
    horizontal_frame_color = find_first_non_background(input_grid, background_color,
                                                       hp_r_start, hp_r_end,
                                                       hp_c_start, hp_c_end)

    # Check if frame colors were found
    if vertical_frame_color is None or horizontal_frame_color is None:
        # Should not happen in valid examples
        return output_grid
        
    # --- Apply Transformations to output_grid ---

    # 10. Tile Vertical_Pattern horizontally
    target_c_start = tl_anchor.max_col + 1
    target_c_end = br_anchor.min_col
    for c in range(target_c_start, target_c_end):
        pattern_col_idx = (c - target_c_start) % vp_w
        output_grid[vp_r_start:vp_r_end, c] = vertical_pattern[:, pattern_col_idx]

    # 11. Tile Horizontal_Pattern vertically
    target_r_start = tl_anchor.max_row + 1
    target_r_end = br_anchor.min_row
    for r in range(target_r_start, target_r_end):
        pattern_row_idx = (r - target_r_start) % hp_h
        output_grid[r, hp_c_start:hp_c_end] = horizontal_pattern[pattern_row_idx, :]

    # --- Draw Frame ---
    # 12. Define frame boundaries
    frame_top = tl_anchor.min_row - 1
    frame_bottom = br_anchor.max_row + 1
    frame_left = tl_anchor.min_col - 1
    frame_right = br_anchor.max_col + 1

    # 13. Draw the frame safely within grid bounds
    # Draw vertical bars (left/right) - including corners
    if 0 <= frame_left < width:
        row_start = max(0, frame_top)
        row_end = min(height, frame_bottom + 1)
        output_grid[row_start:row_end, frame_left] = horizontal_frame_color
    
    if 0 <= frame_right < width:
        row_start = max(0, frame_top)
        row_end = min(height, frame_bottom + 1)
        output_grid[row_start:row_end, frame_right] = horizontal_frame_color

    # Draw horizontal bars (top/bottom) - between vertical bars
    col_start = max(0, frame_left + 1)
    col_end = min(width, frame_right)
    if 0 <= frame_top < height and col_end > col_start:
        output_grid[frame_top, col_start:col_end] = vertical_frame_color
        
    if 0 <= frame_bottom < height and col_end > col_start:
        output_grid[frame_bottom, col_start:col_end] = vertical_frame_color

    return output_grid