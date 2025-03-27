```python
import numpy as np

def find_foreground_color(grid):
    """Finds the first non-zero color in the grid."""
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return color
    # Should not happen based on task examples, but handle just in case
    return 0 

def transform(input_grid):
    """
    Transforms the input grid by inverting colors based on a specific mapping.
    Pixels with the background color (0) are replaced by a target foreground color,
    and pixels with the input foreground color are replaced by the background color (0).
    The target foreground color depends on the input foreground color:
    - green (3) maps to blue (1)
    - gray (5) maps to yellow (4)
    - azure (8) maps to red (2)
    """
    # Convert input list of lists to numpy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Get grid dimensions
    height, width = input_grid_np.shape
    
    # Initialize the output grid with zeros (background color)
    # We will fill in the correct colors during iteration
    output_grid_np = np.zeros_like(input_grid_np)

    # Define the color mapping from input foreground to output foreground
    color_map = {
        3: 1,  # green -> blue
        5: 4,  # gray -> yellow
        8: 2   # azure -> red
    }

    # Identify the input foreground color (assuming only one non-zero color besides background)
    input_fg_color = find_foreground_color(input_grid_np)
    
    # Determine the output foreground color based on the mapping
    # Handle case where input might be all background (though not in examples)
    if input_fg_color in color_map:
        output_fg_color = color_map[input_fg_color]
    else:
        # Default behavior if input foreground color is not in the map or is 0
        # Based on the examples, this path shouldn't be taken.
        # If the input is all 0, the output should arguably be all the corresponding output_fg_color.
        # Let's assume if input is all 0, output is all 0 for now, or handle based on a default map entry if needed.
        # For this problem, input_fg_color will always be 3, 5, or 8.
        output_fg_color = 0 # Or raise an error, depending on desired robustness

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Apply the transformation rule
            if input_grid_np[r, c] == 0:
                # If input pixel is background, set output pixel to output foreground color
                output_grid_np[r, c] = output_fg_color
            else: # Implies input_grid_np[r, c] == input_fg_color
                # If input pixel is input foreground, set output pixel to background (0)
                output_grid_np[r, c] = 0
                
    # Convert numpy array back to list of lists for the expected output format
    output_grid = output_grid_np.tolist()

    return output_grid
```