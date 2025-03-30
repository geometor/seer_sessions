
Previous Code:
```python
import numpy as np
from collections import deque, Counter

"""
The transformation identifies enclosed regions of white pixels (color 0) within the input grid. An enclosed region is one that does not touch the grid border.
For each enclosed white region, it identifies "marker" pixels. A marker pixel is defined as a non-white pixel that is 8-directionally adjacent to at least one pixel of the white region, but is *not* part of the immediate 4-directional boundary of that region. The 4-directional boundary consists of the non-white pixels directly adjacent (up, down, left, right) to the white region pixels.
The transformation counts the occurrences of each unique color among these marker pixels.
If the number of *unique marker colors* found for an enclosed region is greater than 1, the transformation proceeds to fill that region.
The fill color is determined by finding the most frequent color among the markers. In case of a tie in frequency, the color with the lowest numerical index (e.g., red (2) wins over green (3) if both appear twice and that's the max frequency) is chosen.
All the white pixels belonging to that specific enclosed region are then recolored to this chosen fill color in the output grid.
If an enclosed white region has 1 or 0 unique marker colors, or if a white region is not fully enclosed, its white pixels remain unchanged. Non-white pixels in the input always remain unchanged in the output.
"""

def find_connected_white_region(grid, start_pos, global_visited):
    """
    Performs a BFS starting from start_pos to find a connected region of white pixels.

    Args:
        grid (np.ndarray): The input grid.
        start_pos (tuple): The starting (row, col) for the BFS (must be white).
        global_visited (np.ndarray): A boolean grid tracking visited pixels across all searches.

    Returns:
        tuple: (region_pixels, boundary_pixels, is_enclosed)
               region_pixels (set): Set of (row, col) tuples for the white region.
               boundary_pixels (set): Set of (row, col) tuples for non-white pixels 4-directionally adjacent to the region.
               is_enclosed (bool): True if the region does not touch the grid border.
    """
    H, W = grid.shape
    q = deque([start_pos])
    region_pixels = set()
    boundary_pixels = set() # Pixels defining the immediate 4-directional boundary
    is_enclosed = True
    local_visited = set([start_pos]) # Track visited within this BFS to avoid cycles

    while q:
        r, c = q.popleft()

        # Check if pixel is on the border
        if r == 0 or r == H - 1 or c == 0 or c == W - 1:
            is_enclosed = False # Touched edge, cannot be filled later

        region_pixels.add((r, c))
        global_visited[r, c] = True # Mark globally visited

        # Explore neighbors (4-directional for region connectivity and boundary definition)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < H and 0 <= nc < W:
                neighbor_color = grid[nr, nc]
                neighbor_pos = (nr, nc)

                if neighbor_color == 0: # Neighbor is white
                    if neighbor_pos not in local_visited:
                        local_visited.add(neighbor_pos)
                        q.append(neighbor_pos)
                else: # Neighbor is non-white (part of a 4-dir boundary)
                    boundary_pixels.add(neighbor_pos) # Collect boundary pixel position
            # If neighbor is out of bounds, the region touches the edge. The is_enclosed flag handles this.

    return region_pixels, boundary_pixels, is_enclosed


def find_adjacent_markers(grid, region_pixels, boundary_pixels):
    """
    Finds marker pixels adjacent (8-directionally) to the region's white pixels,
    excluding the immediate 4-directional boundary pixels.

    Args:
        grid (np.ndarray): The input grid.
        region_pixels (set): Set of (row, col) for the enclosed white region.
        boundary_pixels (set): Set of (row, col) for the 4-directional boundary pixels.

    Returns:
        list: A list of dictionaries, each {'pos': (r, c), 'color': color} for a unique marker pixel position.
    """
    H, W = grid.shape
    found_markers = {} # Use dict {pos: color} to store unique marker positions and their colors

    # Iterate through each white pixel in the region
    for r, c in region_pixels:
        # Check all 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip self
                
                nr, nc = r + dr, c + dc

                # Check bounds
                if 0 <= nr < H and 0 <= nc < W:
                    neighbor_pos = (nr, nc)
                    neighbor_color = grid[nr, nc]

                    # Check if the neighbor is a potential marker:
                    # 1. It must not be white (color 0).
                    # 2. It must not be part of the immediate 4-directional boundary.
                    if neighbor_color != 0 and neighbor_pos not in boundary_pixels:
                        # Add to found_markers. If position exists, it's overwritten, ensuring uniqueness by position.
                        found_markers[neighbor_pos] = neighbor_color

    # Convert the dictionary of unique markers into the desired list format
    marker_list = [{'pos': pos, 'color': color} for pos, color in found_markers.items()]
    return marker_list


def transform(input_grid):
    """
    Transforms the input grid by finding enclosed white regions and filling them based on adjacent marker colors.
    """
    output_grid = np.copy(input_grid)
    H, W = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool) # Track visited white pixels globally

    # Iterate through each pixel to find starting points for white regions
    for r in range(H):
        for c in range(W):
            # If it's a white pixel and hasn't been visited by any previous region search
            if input_grid[r, c] == 0 and not visited[r, c]:
                
                # Find the connected white region and its properties using BFS
                region_pixels, boundary_pixels, is_enclosed = find_connected_white_region(input_grid, (r, c), visited)

                # Process only if the region is fully enclosed and non-empty
                if is_enclosed and region_pixels:
                    
                    # Find unique marker pixels adjacent (8-dir) to the region, excluding the 4-dir boundary
                    markers = find_adjacent_markers(input_grid, region_pixels, boundary_pixels)
                    
                    # Collect the colors of the found markers
                    marker_colors = [m['color'] for m in markers]
                    
                    # Only proceed if there are any markers found
                    if marker_colors:
                        # Count the frequency of each marker color
                        color_counts = Counter(marker_colors)
                        unique_colors = list(color_counts.keys())
                        
                        # Check if the number of unique marker colors is greater than 1
                        if len(unique_colors) > 1:
                            # Find the most frequent color, with tie-breaking (lowest color index wins)
                            max_count = 0
                            most_common_color = -1 
                            
                            # Sort unique colors by index to ensure lowest index wins ties
                            sorted_colors = sorted(unique_colors) 
                            
                            for color in sorted_colors:
                                count = color_counts[color]
                                if count > max_count:
                                    max_count = count
                                    most_common_color = color
                                # If count == max_count, the lower color index (already processed or current) remains the choice.
                                # Since we iterate sorted colors, the first one encountered with max_count is kept.

                            fill_color = most_common_color

                            # Fill the identified white region in the output grid with the determined fill color
                            for pr, pc in region_pixels:
                                output_grid[pr, pc] = fill_color
                                
                # If not enclosed, or <= 1 unique marker color, the region remains white (as copied initially)
                # The 'visited' array ensures we don't re-process white pixels of already found regions.

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 5 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 8 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 8 0 0 8 2 0 0 0 0 3 3 3 3 0 0 0
0 0 0 2 0 0 0 0 0 2 0 0 0 0 3 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0 0 3 0 8 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0
0 0 0 0 0 0 1 1 1 1 1 0 0 0 3 3 3 3 3 3 0
0 0 0 0 1 1 1 0 0 8 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 5 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 5 0 5 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 1 1 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 8 8 8 8 8 2 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 8 8 8 8 8 2 0 0 0 0 0 0 0 0 0
0 0 0 2 8 8 8 8 8 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 2 8 8 8 8 8 2 0 0 0 0 3 3 3 3 0 0 0
0 0 0 2 8 8 8 8 8 2 0 0 0 0 3 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0 0 3 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0
0 0 0 0 0 0 1 1 1 1 1 0 0 0 3 3 3 3 3 3 0
0 0 0 0 1 1 1 5 5 5 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 5 5 5 5 5 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 5 5 5 5 5 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 5 5 5 5 5 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 5 5 5 5 5 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 1 1 5 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 5 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 8 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 8 0 0 8 2 0 0 0 0 3 3 3 3 0 0 0
0 0 0 2 0 0 0 0 0 2 0 0 0 0 3 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0 0 3 0 8 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 3 0
0 0 0 0 0 0 1 1 1 1 1 0 0 0 3 3 3 3 3 3 0
0 0 0 0 1 1 1 0 0 8 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 5 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 5 0 5 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 1 1 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 44
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 19.95464852607708

## Example 2:
Input:
```
0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 2 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 3 0 2 0 0 6 6 6 0 0
0 0 2 0 0 0 0 0 0 0 2 0 0 6 0 3 0 0
0 0 2 2 2 0 3 0 0 0 2 0 0 6 0 0 0 0
0 0 0 0 2 0 0 0 0 0 2 0 0 6 6 6 6 6
0 0 0 0 2 0 0 0 8 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 4 4 4 4 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4 0 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0 4 0 8 0
3 0 0 0 0 0 0 4 8 0 3 0 8 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 8 0 4 0 0 0
0 0 0 3 0 0 0 4 4 4 4 4 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0
0 0 2 2 2 2 2 3 3 3 2 0 0 0 0 0 0 0
0 0 2 3 3 3 3 3 3 3 2 0 0 6 6 6 0 0
0 0 2 3 3 3 3 3 3 3 2 0 0 6 0 0 0 0
0 0 2 2 2 3 3 3 3 3 2 0 0 6 0 0 0 0
0 0 0 0 2 3 3 3 3 3 2 0 0 6 6 6 6 6
0 0 0 0 2 3 3 3 3 3 2 0 0 0 0 0 0 0
0 0 0 0 2 3 3 3 3 3 2 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4 8 8 4 0 0 0
0 0 0 0 0 0 0 4 8 8 8 8 8 8 4 0 0 0
0 0 0 0 0 0 0 4 8 8 8 8 8 8 4 0 0 0
0 0 0 0 0 0 0 4 8 8 8 8 8 8 4 0 0 0
0 0 0 0 0 0 0 4 8 8 8 8 8 8 4 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4 8 8 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 2 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 3 0 2 0 0 6 6 6 0 0
0 0 2 0 0 0 0 0 0 0 2 0 0 6 0 3 0 0
0 0 2 2 2 0 3 0 0 0 2 0 0 6 0 0 0 0
0 0 0 0 2 0 0 0 0 0 2 0 0 6 6 6 6 6
0 0 0 0 2 0 0 0 8 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 4 4 4 4 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4 0 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0 4 0 8 0
3 0 0 0 0 0 0 4 8 0 3 0 8 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 8 0 4 0 0 0
0 0 0 3 0 0 0 4 4 4 4 4 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 66
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 38.59649122807019

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 3 0 0 2 0 0 0 3 0 0 0
0 3 3 3 0 0 0 0 0 0 3 0 0 0
0 3 0 0 0 8 0 0 8 0 3 0 0 0
0 3 0 0 0 0 0 0 0 0 3 0 0 0
0 3 3 3 0 0 0 0 0 0 3 3 0 0
0 0 0 3 0 6 0 0 2 0 0 3 0 0
0 0 0 3 0 0 0 0 0 0 0 3 0 0
0 0 3 3 0 0 0 0 0 0 0 3 0 0
0 0 3 0 0 0 0 6 0 0 0 3 0 0
0 0 3 0 0 6 0 3 3 3 3 3 0 0
0 0 3 0 0 0 0 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 3 6 6 6 6 6 6 3 0 0 0
0 3 3 3 6 6 6 6 6 6 3 0 0 0
0 3 6 6 6 6 6 6 6 6 3 0 0 0
0 3 6 6 6 6 6 6 6 6 3 0 0 0
0 3 3 3 6 6 6 6 6 6 3 3 0 0
0 0 0 3 6 6 6 6 6 6 6 3 0 0
0 0 0 3 6 6 6 6 6 6 6 3 0 0
0 0 3 3 6 6 6 6 6 6 6 3 0 0
0 0 3 6 6 6 6 6 6 6 6 3 0 0
0 0 3 6 6 6 6 3 3 3 3 3 0 0
0 0 3 6 6 6 6 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 3 0 0 2 0 0 0 3 0 0 0
0 3 3 3 0 0 0 0 0 0 3 0 0 0
0 3 0 0 0 8 0 0 8 0 3 0 0 0
0 3 0 0 0 0 0 0 0 0 3 0 0 0
0 3 3 3 0 0 0 0 0 0 3 3 0 0
0 0 0 3 0 6 0 0 2 0 0 3 0 0
0 0 0 3 0 0 0 0 0 0 0 3 0 0
0 0 3 3 0 0 0 0 0 0 0 3 0 0
0 0 3 0 0 0 0 6 0 0 0 3 0 0
0 0 3 0 0 6 0 3 3 3 3 3 0 0
0 0 3 0 0 0 0 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 68
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 121.42857142857144
