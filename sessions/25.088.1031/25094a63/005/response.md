```python
import numpy as np
from typing import List, Tuple, Set, Dict, Optional
from collections import deque
import math

"""
Identifies the largest contiguous component (blob) for each non-white color 
present in the input grid. Determines the maximum size among these largest blobs.
Filters these largest blobs, keeping only those whose size is at least half of 
the maximum size found. Changes the color of all pixels within these filtered 
blobs to yellow (4). A component is defined as a group of connected pixels 
of the same color, where connectivity includes adjacent pixels (up, down, 
left, right).
"""

def find_blobs(grid: np.ndarray, color: int) -> List[Set[Tuple[int, int]]]:
    """
    Finds all contiguous blobs of a given color using BFS.

    Args:
        grid: The input grid as a NumPy array.
        color: The target color to search for.

    Returns:
        A list of sets, where each set contains the (row, col) tuples
        of pixels belonging to a single blob. Returns an empty list if no
        pixels of the specified color are found.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blobs = []
    # Directions for 4-way connectivity (right, left, down, up)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

    for r in range(height):
        for c in range(width):
            # If we find a pixel of the target color that hasn't been visited yet,
            # it's the start of a new potential blob.
            if grid[r, c] == color and not visited[r, c]:
                # Start Breadth-First Search (BFS) for this blob
                current_blob_pixels = set()
                queue = deque([(r, c)])
                visited[r, c] = True # Mark the starting pixel as visited

                while queue:
                    # Get the next pixel from the queue
                    row, col = queue.popleft()
                    # Add it to the set of pixels for the current blob
                    current_blob_pixels.add((row, col))

                    # Explore neighbors
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc
                        
                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if the neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == color and not visited[nr, nc]:
                                # Mark the neighbor as visited and add it to the queue
                                visited[nr, nc] = True
                                queue.append((nr, nc))

                # After the BFS completes for this starting pixel, 
                # add the found blob (set of pixels) to our list of blobs.
                if current_blob_pixels: 
                    blobs.append(current_blob_pixels)

    return blobs

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by finding the largest blob for each non-white 
    color, determining a size threshold based on the maximum size found, and 
    changing only those largest blobs meeting the threshold to yellow (4).

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    
    # Convert input list of lists to a NumPy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape
    
    # Find all unique colors present in the grid
    unique_colors = np.unique(input_grid_np)
    # Filter out the white color (0)
    non_white_colors = [c for c in unique_colors if c != 0]

    # Store information about the largest blob for each color
    # List of dictionaries: [{'color': c, 'size': s, 'pixels': {(r,c),...}}, ...]
    largest_blobs_info = []

    # Find the largest blob for each non-white color
    for color in non_white_colors:
        # Find all distinct contiguous blobs of the current color
        blobs = find_blobs(input_grid_np, color)
        
        # If blobs of this color were found
        if blobs:
            # Find the largest blob based on the number of pixels it contains
            largest_blob = max(blobs, key=len)
            # Store its information
            largest_blobs_info.append({
                'color': color,
                'size': len(largest_blob),
                'pixels': largest_blob
            })

    # If no non-white blobs were found at all, return the original grid
    if not largest_blobs_info:
        return output_grid.tolist()

    # Determine the overall maximum size among the largest blobs found
    max_size = 0
    for blob_info in largest_blobs_info:
        if blob_info['size'] > max_size:
            max_size = blob_info['size']
            
    # If max_size is 0 (only possible if all found blobs were empty, which shouldn't happen with current find_blobs),
    # or if no largest blobs were recorded, return original grid
    if max_size == 0:
         return output_grid.tolist()

    # Calculate the size threshold (half of the maximum size)
    # Using math.ceil ensures that if max_size is odd, the threshold leans towards inclusivity
    # Example: max_size=5, threshold=3. A blob of size 3 would meet >= 2.5 threshold.
    # Using simple division should also work due to >= comparison.
    threshold = max_size / 2.0 

    # Identify all pixels that need to be recolored based on the threshold
    pixels_to_recolor = set()
    for blob_info in largest_blobs_info:
        # If the size of this largest blob (for its color) meets the threshold
        if blob_info['size'] >= threshold:
            # Add all its pixels to the set for recoloring
            pixels_to_recolor.update(blob_info['pixels'])

    # Recolor the identified pixels in the output grid
    for r, c in pixels_to_recolor:
        # Check bounds just to be safe, although find_blobs should only return valid coords.
        if 0 <= r < height and 0 <= c < width: 
             # Change the color of the pixel in the output grid to yellow (4)
             output_grid[r, c] = 4
        
    # Convert the final NumPy array back to a list of lists format for the return value
    return output_grid.tolist()
```