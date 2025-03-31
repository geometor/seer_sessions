```python
import numpy as np
from collections import Counter
from typing import List, Tuple, Dict, Optional, Set

"""
Transformation Rule:

1.  Create a copy of the input grid to serve as the output grid.
2.  Determine the background color by finding the most frequent pixel value in the input grid.
3.  Identify all contiguous non-background objects and calculate their bounding boxes (`min_row`, `min_col`, `max_row`, `max_col`).
4.  Select the object whose bounding box top-left corner (`min_row`, `min_col`) is lexicographically smallest as the Top-Left Anchor (TL_Anchor).
5.  Select the object whose bounding box bottom-right corner (`max_row`, `max_col`) is lexicographically largest as the Bottom-Right Anchor (BR_Anchor).
6.  Verify that TL_Anchor and BR_Anchor are distinct objects and that they have the same color, same height (`max_row - min_row + 1`), and same width (`max_col - min_col + 1`). If these conditions are not met, return the original input grid.
7.  Define the Vertical Pattern Region coordinates: Start Row = `TL_Anchor.min_row`, End Row (exclusive) = `TL_Anchor.max_row + 1`, Start Column = `TL_Anchor.max_col + 1`, End Column (exclusive) = `BR_Anchor.min_col`.
8.  Define the Horizontal Pattern Region coordinates: Start Row = `TL_Anchor.max_row + 1`, End Row (exclusive) = `BR_Anchor.min_row`, Start Column = `TL_Anchor.min_col`, End Column (exclusive) = `TL_Anchor.max_col + 1`.
9.  Check if both pattern regions have valid dimensions (End Row > Start Row and End Column > Start Column). If not, return the original input grid.
10. Extract the `Vertical_Pattern` subgrid from the input grid using the calculated Vertical Pattern Region coordinates.
11. Extract the `Horizontal_Pattern` subgrid from the input grid using the calculated Horizontal Pattern Region coordinates.
12. Check if the extracted `Vertical_Pattern` and `Horizontal_Pattern` have non-zero dimensions (height > 0 and width > 0). If either is empty, return the original input grid.
13. Determine the `Vertical_Frame_Color`: Scan the Vertical Pattern Region (defined in step 7) in the input grid (row by row, then column by column) and find the color of the first non-background pixel encountered.
14. Determine the `Horizontal_Frame_Color`: Scan the Horizontal Pattern Region (defined in step 8) in the input grid (row by row, then column by column) and find the color of the first non-background pixel encountered.
15. If either `Vertical_Frame_Color` or `Horizontal_Frame_Color` could not be determined (because the respective region contained only background pixels), return the original input grid.
16. Tile the `Vertical_Pattern` into the output grid: For each column `c` from `vp_c_start` to `vp_c_end - 1`, calculate the source column index in the pattern as `(c - vp_c_start) % Vertical_Pattern.width`. Copy the pixels from this source column of `Vertical_Pattern` into the output grid at column `c` and rows `vp_r_start` to `vp_r_end - 1`.
17. Tile the `Horizontal_Pattern` into the output grid: For each row `r` from `hp_r_start` to `hp_r_end - 1`, calculate the source row index in the pattern as `(r - hp_r_start) % Horizontal_Pattern.height`. Copy the pixels from this source row of `Horizontal_Pattern` into the output grid at row `r` and columns `hp_c_start` to `hp_c_end - 1`.
18. Define frame coordinates: `frame_top = TL_Anchor.min_row - 1`, `frame_bottom = BR_Anchor.max_row + 1`, `frame_left = TL_Anchor.min_col - 1`, `frame_right = BR_Anchor.max_col + 1`.
19. Draw the frame onto the output grid, respecting grid boundaries:
    *   Fill column `frame_left` from row `frame_top` to `frame_bottom` (inclusive) with `Horizontal_Frame_Color`.
    *   Fill column `frame_right` from row `frame_top` to `frame_bottom` (inclusive) with `Horizontal_Frame_Color`.
    *   Fill row `frame_top` from column `frame_left + 1` to `frame_right - 1` (inclusive) with `Vertical_Frame_Color`.
    *   Fill row `frame_bottom` from column `frame_left + 1` to `frame_right - 1` (inclusive) with `Vertical_Frame_Color`.
20. Return the modified output grid.
"""

# Helper class to store object information
class GridObject:
    """Represents a contiguous object in the grid with its properties."""
    def __init__(self, color: int, pixels: Set[Tuple[int, int]]):
        self.color = color
        self.pixels = pixels
        if not pixels:
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
    """Finds the first non-background color in a specified region (row-major scan)."""
    height, width = grid.shape
    # Ensure ranges are valid and within grid bounds before iterating
    r_start_safe = max(0, r_start)
    r_end_safe = min(height, r_end) # r_end is exclusive for range
    c_start_safe = max(0, c_start)
    c_end_safe = min(width, c_end)   # c_end is exclusive for range

    for r in range(r_start_safe, r_end_safe):
        for c in range(c_start_safe, c_end_safe):
             if grid[r, c] != background_color:
                 return grid[r, c]
    return None # No non-background color found


def transform(input_grid: np.ndarray) -> np.ndarray:
    # 1. Create a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 2. Determine the background color
    counts = Counter(input_grid.flatten())
    if not counts: # Handle empty grid case
        return output_grid
    background_color = counts.most_common(1)[0][0]

    # 3. Identify all non-background objects
    objects = find_objects(input_grid, background_color)
    if not objects:
        return output_grid # No transformation if no objects

    # 4. Select the Top-Left Anchor (TL_Anchor)
    objects.sort(key=lambda o: (o.min_row, o.min_col))
    tl_anchor = objects[0]
    
    # 5. Select the Bottom-Right Anchor (BR_Anchor)
    objects.sort(key=lambda o: (o.max_row, o.max_col), reverse=True)
    br_anchor = objects[0]

    # Ensure distinct anchors if multiple objects exist
    if len(objects) > 1 and tl_anchor is br_anchor:
         # Re-evaluate BR if TL and BR are the same initially
         potential_br_candidates = sorted([o for o in objects if o is not tl_anchor], 
                                          key=lambda o: (o.max_row, o.max_col), 
                                          reverse=True)
         if potential_br_candidates:
             br_anchor = potential_br_candidates[0]
         else: # Only one effective object was found
             return output_grid
             
    # Final check if anchors are distinct
    if tl_anchor is br_anchor:
         return output_grid # Cannot proceed if anchors are not distinct

    # 6. Verify anchors match (color, height, width)
    if tl_anchor.color != br_anchor.color or \
       tl_anchor.height != br_anchor.height or \
       tl_anchor.width != br_anchor.width:
        return output_grid # Anchors don't match criteria

    # 7. Define the Vertical Pattern Region coordinates
    vp_r_start = tl_anchor.min_row
    vp_r_end = tl_anchor.max_row + 1 # Exclusive end for slicing
    vp_c_start = tl_anchor.max_col + 1
    vp_c_end = br_anchor.min_col     # Exclusive end for slicing

    # 8. Define the Horizontal Pattern Region coordinates
    hp_r_start = tl_anchor.max_row + 1
    hp_r_end = br_anchor.min_row     # Exclusive end for slicing
    hp_c_start = tl_anchor.min_col
    hp_c_end = tl_anchor.max_col + 1 # Exclusive end for slicing

    # 9. Check if pattern regions have valid dimensions
    valid_vp_region = (vp_r_end > vp_r_start) and (vp_c_end > vp_c_start)
    valid_hp_region = (hp_r_end > hp_r_start) and (hp_c_end > hp_c_start)

    # Both regions must be valid based on the problem structure
    if not valid_vp_region or not valid_hp_region:
         # If anchors are adjacent or overlapping such that no pattern region exists
         return output_grid 

    # 10. Extract the Vertical_Pattern subgrid
    vertical_pattern = input_grid[vp_r_start:vp_r_end, vp_c_start:vp_c_end]
    
    # 11. Extract the Horizontal_Pattern subgrid
    horizontal_pattern = input_grid[hp_r_start:hp_r_end, hp_c_start:hp_c_end]

    # 12. Check if extracted patterns have non-zero dimensions
    vp_h, vp_w = vertical_pattern.shape
    hp_h, hp_w = horizontal_pattern.shape
    if vp_h == 0 or vp_w == 0 or hp_h == 0 or hp_w == 0:
        # This case should be covered by step 9, but added for robustness
        return output_grid # Cannot tile with empty patterns

    # 13. Determine the Vertical_Frame_Color
    vertical_frame_color = find_first_non_background(input_grid, background_color, 
                                                     vp_r_start, vp_r_end, 
                                                     vp_c_start, vp_c_end)
                                                      
    # 14. Determine the Horizontal_Frame_Color
    horizontal_frame_color = find_first_non_background(input_grid, background_color,
                                                       hp_r_start, hp_r_end,
                                                       hp_c_start, hp_c_end)

    # 15. Check if frame colors were found
    if vertical_frame_color is None or horizontal_frame_color is None:
        # If regions are valid but no color found, rule may not apply
        return output_grid 

    # 16. Tile the Vertical_Pattern horizontally
    target_vp_rows = slice(vp_r_start, vp_r_end) # Rows to fill
    for c in range(vp_c_start, vp_c_end):
        if c >= width: break # Boundary check
        pattern_col_idx = (c - vp_c_start) % vp_w
        output_grid[target_vp_rows, c] = vertical_pattern[:, pattern_col_idx]

    # 17. Tile the Horizontal_Pattern vertically
    target_hp_cols = slice(hp_c_start, hp_c_end) # Columns to fill
    for r in range(hp_r_start, hp_r_end):
        if r >= height: break # Boundary check
        pattern_row_idx = (r - hp_r_start) % hp_h
        output_grid[r, target_hp_cols] = horizontal_pattern[pattern_row_idx, :]

    # 18. Define frame coordinates
    frame_top = tl_anchor.min_row - 1
    frame_bottom = br_anchor.max_row + 1
    frame_left = tl_anchor.min_col - 1
    frame_right = br_anchor.max_col + 1

    # 19. Draw the frame onto the output grid, respecting grid boundaries
    # Draw vertical bars (left/right) - including corners
    if 0 <= frame_left < width:
        row_start_safe = max(0, frame_top)
        row_end_safe = min(height, frame_bottom + 1) # +1 for inclusive row end range
        if row_end_safe > row_start_safe: # Ensure there's at least one row to draw
             output_grid[row_start_safe:row_end_safe, frame_left] = horizontal_frame_color
    
    if 0 <= frame_right < width:
        row_start_safe = max(0, frame_top)
        row_end_safe = min(height, frame_bottom + 1) # +1 for inclusive row end range
        if row_end_safe > row_start_safe:
             output_grid[row_start_safe:row_end_safe, frame_right] = horizontal_frame_color

    # Draw horizontal bars (top/bottom) - between vertical bars' inner edges
    col_start_safe = max(0, frame_left + 1)
    col_end_safe = min(width, frame_right) # Exclusive end index for slicing
    
    if 0 <= frame_top < height and col_end_safe > col_start_safe: # Check row valid and width > 0
        output_grid[frame_top, col_start_safe:col_end_safe] = vertical_frame_color
        
    if 0 <= frame_bottom < height and col_end_safe > col_start_safe:
        output_grid[frame_bottom, col_start_safe:col_end_safe] = vertical_frame_color

    # 20. Return the modified output grid
    return output_grid
```