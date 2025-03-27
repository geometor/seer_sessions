import numpy as np

"""
Identifies three 4x4 patterns within a 4x14 input grid, separated by white vertical lines at columns 4 and 9. 
Maps each pattern (from left to right) to a specific color:
- Solid gray square -> Red (2)
- Gray square frame with 2x2 white center -> Azure (8)
- Gray top 2 rows, gray border bottom 2 rows like [[5,0,0,5],[5,0,0,5]] -> Yellow (4)
- Gray top/bottom rows, middle rows like [[0,5,5,0],[0,5,5,0]] -> Green (3)
Constructs a 3x3 output grid where the first row is filled with the color corresponding to the first pattern, the second row with the color from the second pattern, and the third row with the color from the third pattern.
"""

# Define the four known 4x4 patterns
# Using tuples of tuples for dictionary keys as numpy arrays are not hashable
PATTERN_SOLID_GRAY = tuple(map(tuple, np.full((4, 4), 5)))
PATTERN_FRAME = tuple(map(tuple, np.array([
    [5, 5, 5, 5], 
    [5, 0, 0, 5], 
    [5, 0, 0, 5], 
    [5, 5, 5, 5]
])))
PATTERN_LOWER_C = tuple(map(tuple, np.array([
    [5, 5, 5, 5], 
    [5, 5, 5, 5], 
    [5, 0, 0, 5], 
    [5, 0, 0, 5]
])))
PATTERN_H = tuple(map(tuple, np.array([
    [5, 5, 5, 5], 
    [0, 5, 5, 0], 
    [0, 5, 5, 0], 
    [5, 5, 5, 5]
])))

# Map patterns to their corresponding output colors
PATTERN_TO_COLOR_MAP = {
    PATTERN_SOLID_GRAY: 2, # Red
    PATTERN_FRAME: 8,      # Azure
    PATTERN_LOWER_C: 4,    # Yellow
    PATTERN_H: 3           # Green
}

def identify_pattern_color(subgrid_arr):
    """
    Identifies which known pattern the subgrid matches and returns the corresponding color.
    
    Args:
        subgrid_arr (np.array): A 4x4 numpy array representing the subgrid.
        
    Returns:
        int: The color code associated with the matched pattern, or -1 if no match.
    """
    # Convert the numpy array subgrid to a tuple of tuples for dictionary lookup
    subgrid_tuple = tuple(map(tuple, subgrid_arr))
    
    # Look up the pattern in the map
    return PATTERN_TO_COLOR_MAP.get(subgrid_tuple, -1) # Return -1 if pattern not found

def transform(input_grid):
    """
    Transforms the input 4x14 grid into a 3x3 output grid based on pattern recognition.
    
    Args:
        input_grid (np.array): A 4x14 numpy array.
        
    Returns:
        np.array: A 3x3 numpy array representing the transformed output.
    """
    # Ensure input is a numpy array
    input_arr = np.array(input_grid)
    
    # Define the column indices for the three subgrids
    subgrid_cols = [
        slice(0, 4),  # Columns 0-3
        slice(5, 9),  # Columns 5-8
        slice(10, 14) # Columns 10-13
    ]
    
    # Initialize the output grid (3x3) with a default value (e.g., 0)
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Process each subgrid
    for i in range(3):
        # Extract the i-th 4x4 subgrid
        subgrid = input_arr[:, subgrid_cols[i]]
        
        # Identify the pattern and get the corresponding color
        color = identify_pattern_color(subgrid)
        
        # Check if a valid color was found
        if color != -1:
            # Fill the i-th row of the output grid with the identified color
            output_grid[i, :] = color
        else:
            # Optional: Handle cases where the pattern is not recognized
            # For this task, we assume all patterns will be recognized.
            # If not, the row remains filled with the default value (0).
            print(f"Warning: Pattern not recognized in subgrid {i+1}")

    return output_grid
