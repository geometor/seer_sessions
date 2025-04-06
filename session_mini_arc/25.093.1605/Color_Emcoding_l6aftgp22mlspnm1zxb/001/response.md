```python
import numpy as np

"""
Transforms a 5x5 input grid containing 0s and 5s into a 5x5 output grid.

The transformation operates on four 2x2 quadrants defined by excluding the 
central row (index 2) and central column (index 2), which remain 0s. 
Each input quadrant's pattern of 0s and 5s maps to a specific single digit 
(1, 2, 3, or 4) which then fills the corresponding 2x2 output quadrant.

The specific pattern-to-value mapping is:
- [[0, 5], [5, 5]] -> 1
- [[5, 0], [5, 5]] -> 2
- [[5, 5], [0, 5]] -> 3
- [[5, 5], [5, 0]] -> 4
"""

def transform(input_grid):
    """
    Applies the quadrant-based pattern transformation to the input grid.

    Args:
        input_grid: A list of lists representing the 5x5 input grid.

    Returns:
        A numpy array representing the 5x5 transformed output grid.
    """
    # Convert input to numpy array for easier slicing
    input_np = np.array(input_grid)
    # Initialize output grid as a copy of the input to preserve central zeros
    output_grid = np.copy(input_np)

    # Define the coordinates for the input/output quadrants
    # (row_start, row_end_exclusive, col_start, col_end_exclusive)
    quadrant_coords = {
        "top_left": (0, 2, 0, 2),
        "top_right": (0, 2, 3, 5),
        "bottom_left": (3, 5, 0, 2),
        "bottom_right": (3, 5, 3, 5),
    }

    # Define the mapping from input pattern (as tuple of tuples) to output value
    # Using tuples makes the patterns hashable for dictionary keys
    pattern_map = {
        ((0, 5), (5, 5)): 1,
        ((5, 0), (5, 5)): 2,
        ((5, 5), (0, 5)): 3,
        ((5, 5), (5, 0)): 4,
    }

    # Process each quadrant
    for q_name, (r_start, r_end, c_start, c_end) in quadrant_coords.items():
        # Extract the 2x2 input quadrant
        input_quadrant = input_np[r_start:r_end, c_start:c_end]
        
        # Convert the numpy quadrant to a tuple of tuples for lookup
        input_pattern_tuple = tuple(map(tuple, input_quadrant))

        # Find the corresponding output value from the map
        # Default to 0 if a pattern isn't found (though all examples fit)
        output_value = pattern_map.get(input_pattern_tuple, 0) 

        # Fill the corresponding 2x2 output quadrant with the determined value
        output_grid[r_start:r_end, c_start:c_end] = output_value

    # The central row and column were already preserved from the copy
    # Return the modified grid
    return output_grid.tolist() # Convert back to list of lists if needed by caller

```