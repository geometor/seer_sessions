import copy
import collections # Although not strictly needed for the current logic, good to keep for potential future object analysis

"""
Transforms the input grid based on the global count of unique non-background colors.
If exactly two distinct non-background colors (e.g., Color A and Color B) are present 
in the entire input grid, all occurrences of Color A are replaced with Color B, and 
all occurrences of Color B are replaced with Color A. Pixels with the background 
color (0) remain unchanged. If the number of unique non-background colors in the 
input grid is not exactly two, the grid is returned unchanged.
"""

def find_unique_non_background_colors(grid):
    """
    Finds the set of unique colors in the grid, excluding the background color (0).

    Args:
        grid (list[list[int]]): The input grid.

    Returns:
        set: A set containing the unique non-background color values.
    """
    unique_colors = set()
    if not grid or not grid[0]: # Handle empty grid
        return unique_colors
        
    height = len(grid)
    width = len(grid[0])
    
    for r in range(height):
        for c in range(width):
            pixel_color = grid[r][c]
            if pixel_color != 0: # Exclude background color (0)
                unique_colors.add(pixel_color)
    return unique_colors

def transform(input_grid):
    """
    Applies a color swap transformation based on the global count of non-background colors.

    Args:
        input_grid (list[list[int]]): A 2D list of integers representing the input grid.

    Returns:
        list[list[int]]: A 2D list of integers representing the transformed output grid.
    """
    # Handle empty input grid scenario
    if not input_grid or not input_grid[0]:
        return []

    height = len(input_grid)
    width = len(input_grid[0])

    # --- Step 1: Determine the set of unique non-background colors in the input grid ---
    unique_non_background_colors = find_unique_non_background_colors(input_grid)

    # --- Step 2: Check if the condition for transformation (exactly two colors) is met ---
    if len(unique_non_background_colors) == 2:
        # Condition met: Exactly two non-background colors found. Proceed with swap.
        
        # Extract the two colors to be swapped.
        # Convert set to list/tuple to access elements by index
        colors_to_swap = list(unique_non_background_colors)
        color_a = colors_to_swap[0]
        color_b = colors_to_swap[1]
        
        # Initialize the output grid as a deep copy to modify.
        # This preserves the background and any other structure initially.
        output_grid = copy.deepcopy(input_grid) 

        # --- Step 3: Iterate through the grid and perform the swap ---
        for r in range(height):
            for c in range(width):
                # Check the color in the *original* input grid to decide the swap.
                # Modify the pixel in the *output_grid*.
                if input_grid[r][c] == color_a:
                    output_grid[r][c] = color_b
                elif input_grid[r][c] == color_b:
                    output_grid[r][c] = color_a
                # Background pixels (color 0) remain unchanged implicitly because
                # output_grid started as a copy and they match neither color_a nor color_b.
        
        # Return the modified grid.
        return output_grid
        
    else:
        # Condition not met: The number of unique non-background colors is not two.
        # Return an unchanged copy of the input grid.
        # Using deepcopy ensures the original input is not modified if it's passed elsewhere.
        output_grid = copy.deepcopy(input_grid)
        return output_grid
