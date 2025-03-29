```python
import numpy as np

"""
Identifies all square subgrids within the input grid that meet two criteria:
1. The border of the square consists entirely of Azure (8) pixels.
2. All pixels within the square (including the border) are either Azure (8) or Red (2).

Among these qualifying square subgrids, it further filters to find those that contain at least one Red (2) pixel.

Finally, it selects and returns the unique pattern (subgrid) from this filtered set that appears exactly once within the input grid. If no such unique pattern exists, it returns an empty list.
"""

def check_pattern(grid_np):
    """
    Checks if a given square numpy grid meets the required criteria.
    - Border must be all Azure (8).
    - Content must be only Azure (8) or Red (2).
    """
    rows, cols = grid_np.shape
    # Must be a square of size at least 2x2
    if rows != cols or rows < 2: 
        return False
        
    # Check content: Allow only 8 (Azure) and 2 (Red)
    allowed_colors = {8, 2}
    if not np.all(np.isin(grid_np, list(allowed_colors))): 
        return False
        
    # Check border: Ensure all border pixels are Azure (8)
    is_border_azure = True
    # Top row
    if not np.all(grid_np[0, :] == 8): is_border_azure = False
    # Bottom row
    if not np.all(grid_np[-1, :] == 8): is_border_azure = False
    # Left and Right columns (handle sizes >= 2)
    if rows > 1:
        # Check corners explicitly for size 2
        if rows == 2:
             if not (grid_np[0,0]==8 and grid_np[0,1]==8 and grid_np[1,0]==8 and grid_np[1,1]==8):
                 is_border_azure = False
        # Check side columns (excluding corners) for sizes > 2
        elif rows > 2:
            if not np.all(grid_np[1:-1, 0] == 8): is_border_azure = False
            if not np.all(grid_np[1:-1, -1] == 8): is_border_azure = False

    return is_border_azure


def transform(input_grid):
    """
    Finds the unique qualifying square pattern containing red that appears exactly once.
    """
    input_np = np.array(input_grid)
    height, width = input_np.shape
    
    # Dictionary to store unique patterns found and their locations
    # Key: tuple(tuple(row)) representation of the pattern
    # Value: list of (row, col) tuples where the pattern starts
    unique_qualifying_patterns = {} 

    # Iterate through all possible square sizes (from min size 2)
    for size in range(2, min(height, width) + 1):
        # Iterate through all possible top-left starting positions (r, c)
        for r in range(height - size + 1):
            for c in range(width - size + 1):
                # Extract the candidate subgrid
                candidate_subgrid_np = input_np[r:r+size, c:c+size]
                
                # Check if the candidate meets the criteria (Azure border, Azure/Red content)
                if check_pattern(candidate_subgrid_np):
                    # Convert numpy array to tuple of tuples for use as dictionary key
                    pattern_tuple = tuple(map(tuple, candidate_subgrid_np.tolist()))
                    
                    # Record the location of this pattern instance
                    if pattern_tuple not in unique_qualifying_patterns:
                        unique_qualifying_patterns[pattern_tuple] = []
                    unique_qualifying_patterns[pattern_tuple].append((r, c))

    # Filter the found unique patterns to keep only those containing Red(2)
    red_patterns_info = []
    for pattern_tuple, locations in unique_qualifying_patterns.items():
        pattern_np = np.array(pattern_tuple)
        # Check if any pixel in the pattern is Red (2)
        if np.any(pattern_np == 2):
            red_patterns_info.append({
                "pattern": list(map(list, pattern_tuple)), # Store as list of lists
                "count": len(locations),
                # "locations": locations # Keep track if needed for debugging
            })

    # Find patterns from the 'red_patterns_info' list that occur exactly once
    single_occurrence_patterns = [p_info for p_info in red_patterns_info if p_info["count"] == 1]

    # If exactly one such pattern is found, return it
    if len(single_occurrence_patterns) == 1:
        return single_occurrence_patterns[0]["pattern"]
    else:
        # Fallback: Return empty list if zero or multiple patterns meet the final criteria
        # Based on examples, this case should not be reached.
        return []
```