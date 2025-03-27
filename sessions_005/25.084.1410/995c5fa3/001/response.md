```python
import numpy as np

def find_significant_color(section):
    """
    Finds the unique color in a grid section that is not gray (5) or white (0).

    Args:
        section (np.array): A 2D numpy array representing a section of the grid.

    Returns:
        int: The significant color found, or -1 if none is found (should not happen based on task examples).
    """
    # Flatten the 2D section into a 1D array and find unique colors
    unique_colors = set(section.flatten())
    
    # Iterate through unique colors to find the one that isn't gray or white
    for color in unique_colors:
        if color != 5 and color != 0:
            return color  # Return the first significant color found
            
    # Return -1 if no significant color is found (as a fallback)
    return -1 

def transform(input_grid):
    """
    Identifies the unique non-background color (not gray 5 or white 0) in 
    three distinct 4x4 sections of the 4x14 input grid. These sections are 
    separated by white (0) columns at indices 4 and 9. It then creates a 
    3x3 output grid where the first row is filled with the color from the 
    first section, the second row with the color from the second section, 
    and the third row with the color from the third section.
    """
    # Convert the input list of lists to a numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)

    # Define the column ranges for the three sections
    # Section 1: columns 0-3
    # Section 2: columns 5-8
    # Section 3: columns 10-13
    section1_cols = slice(0, 4)
    section2_cols = slice(5, 9)
    section3_cols = slice(10, 14)

    # Extract the three sections from the input grid
    section1 = input_array[:, section1_cols]
    section2 = input_array[:, section2_cols]
    section3 = input_array[:, section3_cols]

    # Find the significant color for each section using the helper function
    color1 = find_significant_color(section1)
    color2 = find_significant_color(section2)
    color3 = find_significant_color(section3)

    # Initialize the 3x3 output grid with zeros (or any placeholder)
    output_grid = np.zeros((3, 3), dtype=int)

    # Fill the rows of the output grid with the corresponding significant colors
    output_grid[0, :] = color1  # Fill first row with color from section 1
    output_grid[1, :] = color2  # Fill second row with color from section 2
    output_grid[2, :] = color3  # Fill third row with color from section 3

    # Convert the numpy array back to a list of lists for the final output
    return output_grid.tolist()
```