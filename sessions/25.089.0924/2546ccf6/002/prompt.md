
Previous Code:
```python
import numpy as np
from collections import defaultdict

"""
Identifies regions partitioned by grid lines of a single color. 
Groups regions containing identical patterns (ignoring background and grid line colors).
Within each group of identical patterns, sorts the regions by their top-left corner (row-major order).
Swaps the content of consecutive pairs of regions in the sorted list (1st with 2nd, 3rd with 4th, etc.). 
Grid lines, empty regions, regions with unique patterns, and the last region in odd-sized groups remain unchanged.
"""

def find_grid_lines(grid):
    """
    Finds horizontal and vertical grid lines and the dominant color forming them.
    A grid line is a full row or column composed of a single non-background color.
    """
    height, width = grid.shape
    rows = []
    cols = []
    potential_colors = set()
    
    # Check rows
    for r in range(height):
        unique_colors = np.unique(grid[r, :])
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            rows.append(r)
            potential_colors.add(unique_colors[0])
            
    # Check columns
    for c in range(width):
        unique_colors = np.unique(grid[:, c])
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            cols.append(c)
            potential_colors.add(unique_colors[0])

    if not potential_colors:
        # Handle cases with no grid lines? Or assume they always exist based on examples.
        # For now, assume they exist and there's only one color.
         return None, [], [] # Or raise error
    
    # In the examples, there's only one grid line color
    # If multiple colors form full lines, this logic might need adjustment.
    # We assume the color forming both row and col lines (if both exist) is the grid color.
    grid_line_color = list(potential_colors)[0] # Simplistic assumption for now

    # Verify consistency if needed (e.g., check if all line colors match)
    
    return grid_line_color, sorted(rows), sorted(cols)

def define_regions(height, width, grid_rows, grid_cols):
    """
    Defines region boundaries based on grid lines.
    Returns a list of tuples: (r1, c1, r2, c2) where r1, c1 are inclusive top-left
    and r2, c2 are exclusive bottom-right coordinates.
    """
    regions = []
    row_starts = [0] + [r + 1 for r in grid_rows]
    row_ends = [r for r in grid_rows] + [height]
    col_starts = [0] + [c + 1 for c in grid_cols]
    col_ends = [c for c in grid_cols] + [width]

    for r_start, r_end in zip(row_starts, row_ends):
        for c_start, c_end in zip(col_starts, col_ends):
             # Ensure region has valid dimensions (handles adjacent grid lines)
             if r_start < r_end and c_start < c_end:
                regions.append((r_start, c_start, r_end, c_end))
                
    return regions

def extract_content(grid, r1, c1, r2, c2):
    """Extracts the subgrid content of a region."""
    return grid[r1:r2, c1:c2]

def get_pattern_tuple(content, background_color=0, grid_line_color=None):
    """
    Creates a hashable representation (tuple of tuples) of the pattern within content,
    ignoring background and grid line colors. Returns None if the region is empty
    (only contains background/grid lines).
    """
    pattern_list = []
    has_pattern = False
    for r in range(content.shape[0]):
        row_list = []
        for c in range(content.shape[1]):
            pixel = content[r, c]
            if pixel != background_color and pixel != grid_line_color:
                 row_list.append(pixel)
                 has_pattern = True
            else:
                 row_list.append(background_color) # Use background as placeholder
        pattern_list.append(tuple(row_list))
        
    if not has_pattern:
        return None # Indicate empty or non-pattern region

    # Normalize by removing all-background rows/cols from edges? Might not be needed if regions are tight.
    # For now, just return the tuple representation.
    return tuple(pattern_list)

def place_content(grid, r1, c1, r2, c2, content_to_place):
    """Places the content_to_place into the specified region of the grid."""
    grid[r1:r2, c1:c2] = content_to_place

def transform(input_grid):
    """
    Transforms the input grid by swapping contents of regions with identical patterns.

    1. Identifies grid lines and regions.
    2. Extracts patterns from regions (ignoring grid lines and background).
    3. Groups regions by identical patterns.
    4. Sorts regions within each group by location (top-left corner, row-major).
    5. Swaps the *full content* of paired regions (1st/2nd, 3rd/4th, etc.) in each group.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    background_color = 0

    # 1. Identify Grid Structure
    grid_line_color, grid_rows, grid_cols = find_grid_lines(input_grid)
    
    if grid_line_color is None:
         # If no grid lines detected, maybe return input as is?
         # Based on examples, grid lines seem guaranteed.
         print("Warning: No grid lines detected.")
         return output_grid

    # 2. Define Regions
    region_coords = define_regions(height, width, grid_rows, grid_cols)

    # 3. Extract and Characterize Region Contents & Group Regions
    region_patterns = {} # Store pattern for each region coords: {(r1,c1,r2,c2): pattern_tuple}
    pattern_groups = defaultdict(list) # Group coords by pattern: {pattern_tuple: [(r1,c1,r2,c2), ...]}

    for coords in region_coords:
        r1, c1, r2, c2 = coords
        content = extract_content(input_grid, r1, c1, r2, c2)
        pattern = get_pattern_tuple(content, background_color, grid_line_color)
        
        region_patterns[coords] = pattern
        if pattern is not None: # Only group regions with actual patterns
            pattern_groups[pattern].append(coords)

    # 4. Identify Swap Pairs
    swaps_to_perform = [] # List of pairs of coords to swap: [ ((rA1,cA1,rA2,cA2), (rB1,cB1,rB2,cB2)), ... ]

    for pattern, coords_list in pattern_groups.items():
        if len(coords_list) >= 2:
            # Sort regions by top-left corner (row, then column)
            sorted_coords = sorted(coords_list, key=lambda c: (c[0], c[1]))
            
            # Pair consecutive regions
            for i in range(0, len(sorted_coords) // 2 * 2, 2):
                region_A_coords = sorted_coords[i]
                region_B_coords = sorted_coords[i+1]
                swaps_to_perform.append((region_A_coords, region_B_coords))

    # 5. Perform Swaps
    # We need to extract content *before* modifying the output grid to avoid double-swapping issues
    content_cache = {}
    for coords_A, coords_B in swaps_to_perform:
        if coords_A not in content_cache:
            content_cache[coords_A] = extract_content(input_grid, *coords_A)
        if coords_B not in content_cache:
            content_cache[coords_B] = extract_content(input_grid, *coords_B)

    # Now place the cached content into the output grid
    for coords_A, coords_B in swaps_to_perform:
        content_A = content_cache[coords_A]
        content_B = content_cache[coords_B]
        
        # Place content B into region A location
        place_content(output_grid, *coords_A, content_B)
        # Place content A into region B location
        place_content(output_grid, *coords_B, content_A)

    # 6. Finalize Output
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
3 0 3 3 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 3 3 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 0 3 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 3 0 2 0 3 0 0 2 0 0 0 0 2 0 0 0
0 3 3 0 2 0 3 3 0 2 0 0 0 0 2 0 0 0
3 0 3 3 2 3 3 0 3 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 1 0 0 2 0 0 1 0 2 0 0 0
0 0 0 0 2 0 0 1 1 2 1 1 0 0 2 0 0 0
0 0 0 0 2 0 0 1 0 2 0 1 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 0 0 0 2 0 1 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 1 1 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 1 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
```
Expected Output:
```
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
3 0 3 3 2 3 3 0 3 2 0 0 0 0 2 0 0 0
0 3 3 0 2 0 3 3 0 2 0 0 0 0 2 0 0 0
0 0 3 0 2 0 3 0 0 2 0 0 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 3 0 2 0 3 0 0 2 0 0 0 0 2 0 0 0
0 3 3 0 2 0 3 3 0 2 0 0 0 0 2 0 0 0
3 0 3 3 2 3 3 0 3 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 1 0 0 2 0 0 1 0 2 0 0 0
0 0 0 0 2 0 0 1 1 2 1 1 0 0 2 0 0 0
0 0 0 0 2 0 0 1 0 2 0 1 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 0 1 0 2 0 1 0 0 2 0 0 0
0 0 0 0 2 0 0 1 1 2 1 1 0 0 2 0 0 0
0 0 0 0 2 0 1 0 0 2 0 0 1 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
```
Transformed Output:
```
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
3 0 3 3 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 3 3 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 0 3 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 3 0 2 0 3 0 0 2 0 0 0 0 2 0 0 0
0 3 3 0 2 0 3 3 0 2 0 0 0 0 2 0 0 0
3 0 3 3 2 3 3 0 3 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 1 0 0 2 0 0 1 0 2 0 0 0
0 0 0 0 2 0 0 1 1 2 1 1 0 0 2 0 0 0
0 0 0 0 2 0 0 1 0 2 0 1 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 0 0 0 2 0 1 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 1 1 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 1 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 5.847953216374293

## Example 2:
Input:
```
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 0 4 6 4 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
0 0 0 0 6 0 4 4 0 6 0 4 4 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 4 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 4 4 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 4 6 0 0 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
```
Expected Output:
```
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 0 4 6 4 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
0 0 0 0 6 0 4 4 0 6 0 4 4 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
0 0 0 0 6 0 4 4 0 6 0 4 4 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 4 6 4 0 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
```
Transformed Output:
```
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 0 4 6 4 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
0 0 0 0 6 0 4 4 0 6 0 4 4 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 4 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 4 4 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 4 6 0 0 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 3.0959752321981284
