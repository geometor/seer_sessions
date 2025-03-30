```python
import numpy as np
from scipy import ndimage
import collections

"""
Transforms an input grid based on the following rules:
1. Preserves magenta (6) pixels from the input.
2. Creates a green (3) border by changing azure (8) pixels that are orthogonally or diagonally adjacent to any magenta (6) pixel.
3. Identifies regions of azure (8) pixels in the input that are enclosed by magenta (6) pixels (cannot reach the grid border via azure pixels).
4. Fills these enclosed regions in the output grid:
    - If the enclosed region consists of exactly a 2x2 block of azure pixels, fill with green (3).
    - Otherwise, fill with yellow (4).
5. Azure pixels not part of the border or fill remain azure (8).
"""

def find_adjacent_pixels(grid, target_color):
    """Finds pixels adjacent (ortho & diag) to the target color."""
    H, W = grid.shape
    target_mask = (grid == target_color)
    # Use binary dilation with a 3x3 structure to find pixels touching the target color
    structure = np.ones((3, 3), dtype=bool)
    dilated_mask = ndimage.binary_dilation(target_mask, structure=structure)
    # Adjacent pixels are those marked by dilation but not part of the original target
    adjacent_mask = dilated_mask & (~target_mask)
    return adjacent_mask

def find_enclosed_regions(grid, background_color, wall_color):
    """Finds connected regions of background_color enclosed by wall_color."""
    H, W = grid.shape
    background_mask = (grid == background_color)
    
    # Use BFS starting from border background pixels to find reachable background pixels
    visited = np.zeros_like(grid, dtype=bool)
    queue = collections.deque()

    # Add all border background pixels to the queue
    for r in range(H):
        for c in [0, W - 1]:
            if background_mask[r, c] and not visited[r, c]:
                visited[r, c] = True
                queue.append((r, c))
    for c in range(W):
        for r in [0, H - 1]:
             if background_mask[r, c] and not visited[r, c]:
                visited[r, c] = True
                queue.append((r, c))
                
    # BFS to find all reachable background pixels
    while queue:
        r, c = queue.popleft()
        # Check orthogonal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W:
                if background_mask[nr, nc] and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    # Enclosed regions are background pixels that were not visited
    enclosed_mask = background_mask & (~visited)
    
    # Label the connected components of enclosed background pixels
    # Use orthogonal connectivity (structure)
    connectivity_structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool)
    labeled_enclosed, num_labels = ndimage.label(enclosed_mask, structure=connectivity_structure)
    
    return labeled_enclosed, num_labels


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    """
    # Define colors
    AZURE = 8
    MAGENTA = 6
    GREEN = 3
    YELLOW = 4
    
    # Initialize output grid as a copy of the input
    output_grid = input_grid.copy()
    H, W = input_grid.shape

    # --- Step 1: Preserve Magenta (already done by copying) ---

    # --- Step 2: Create Green Border ---
    # Find azure pixels adjacent to magenta
    magenta_adjacency_mask = find_adjacent_pixels(input_grid, MAGENTA)
    border_pixels_mask = magenta_adjacency_mask & (input_grid == AZURE)
    # Change these azure pixels to green in the output
    output_grid[border_pixels_mask] = GREEN

    # --- Step 3 & 4: Identify and Fill Enclosed Azure Regions ---
    # Find enclosed azure regions
    labeled_enclosed, num_labels = find_enclosed_regions(input_grid, AZURE, MAGENTA)

    if num_labels > 0:
        # Iterate through each unique enclosed region label
        for i in range(1, num_labels + 1):
            # Get a mask for the current component
            component_mask = (labeled_enclosed == i)
            # Get coordinates of the pixels in this component
            coords = np.argwhere(component_mask)
            
            num_pixels = len(coords)
            if num_pixels == 0: # Should not happen with labels > 0
                continue

            # Calculate the bounding box dimensions of the azure pixels
            min_r, min_c = coords.min(axis=0)
            max_r, max_c = coords.max(axis=0)
            height = max_r - min_r + 1
            width = max_c - min_c + 1

            # Determine fill color based on size: green if exactly 2x2, yellow otherwise
            # Check height, width, and total number of pixels to ensure it's a filled 2x2 square
            if height == 2 and width == 2 and num_pixels == 4:
                fill_color = GREEN
            else:
                fill_color = YELLOW
            
            # Apply the fill color to the enclosed region in the output grid
            # This overwrites the original azure pixels. It might overwrite
            # green border pixels if an enclosed pixel was also adjacent to magenta,
            # but the logic seems to prioritize the fill color based on examples.
            output_grid[component_mask] = fill_color

    # --- Step 5: Return final grid ---
    return output_grid
```