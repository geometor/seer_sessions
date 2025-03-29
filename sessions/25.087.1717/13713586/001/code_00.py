import numpy as np

"""
Identify the location of the gray (5) border line (top, bottom, left, or right).
Initialize the output grid as a copy of the input grid.
Determine the fill direction based on the border location (towards the border).
Iterate through each line (row or column) perpendicular to the gray border.
For each line, iterate through its pixels starting from the edge opposite the border and moving towards it.
Maintain a 'current_fill_color' initialized to white (0).
If a non-white, non-gray pixel is encountered in the input line, update the 'current_fill_color'.
Set the corresponding pixel in the output line to the 'current_fill_color'.
Ensure the original gray border is preserved (handled by initializing output as a copy).
Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies a color propagation transformation based on a gray border.

    Colors propagate towards the gray border, filling white space.
    The fill color changes when a new non-white, non-gray color is encountered
    along the propagation path.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape
    
    border_color = 5
    background_color = 0

    # Find the gray border location
    border_location = None
    border_index = -1

    # Check top row
    if np.all(input_np[0, :] == border_color):
        border_location = "top"
        border_index = 0
    # Check bottom row
    elif np.all(input_np[height - 1, :] == border_color):
        border_location = "bottom"
        border_index = height - 1
    # Check left column
    elif np.all(input_np[:, 0] == border_color):
        border_location = "left"
        border_index = 0
    # Check right column
    elif np.all(input_np[:, width - 1] == border_color):
        border_location = "right"
        border_index = width - 1

    # Apply the transformation based on border location
    if border_location == "right":
        # Iterate through each row
        for r in range(height):
            # Skip the border row itself if it's horizontal
            if border_location in ["top", "bottom"] and r == border_index:
                 continue
            current_fill_color = background_color
            # Iterate through columns from left towards the right border
            for c in range(width):
                 # Stop if we hit the border column
                 if c == border_index:
                     break
                 
                 input_color = input_np[r, c]
                 # Update fill color if we find a non-background, non-border color
                 if input_color != background_color and input_color != border_color:
                     current_fill_color = input_color
                 
                 # Update the output grid with the current fill color
                 # Only overwrite if the current fill color is not background,
                 # or if the target cell is background (don't overwrite existing colors with background)
                 if current_fill_color != background_color or output_grid[r, c] == background_color:
                    output_grid[r, c] = current_fill_color
                    
    elif border_location == "left":
        # Iterate through each row
        for r in range(height):
             if border_location in ["top", "bottom"] and r == border_index:
                 continue
             current_fill_color = background_color
             # Iterate through columns from right towards the left border
             for c in range(width - 1, -1, -1):
                 if c == border_index:
                     break
                 
                 input_color = input_np[r, c]
                 if input_color != background_color and input_color != border_color:
                     current_fill_color = input_color
                 
                 if current_fill_color != background_color or output_grid[r, c] == background_color:
                     output_grid[r, c] = current_fill_color

    elif border_location == "bottom":
        # Iterate through each column
        for c in range(width):
            if border_location in ["left", "right"] and c == border_index:
                 continue
            current_fill_color = background_color
            # Iterate through rows from top towards the bottom border
            for r in range(height):
                if r == border_index:
                    break

                input_color = input_np[r, c]
                if input_color != background_color and input_color != border_color:
                    current_fill_color = input_color
                
                if current_fill_color != background_color or output_grid[r, c] == background_color:
                    output_grid[r, c] = current_fill_color

    elif border_location == "top":
        # Iterate through each column
        for c in range(width):
            if border_location in ["left", "right"] and c == border_index:
                 continue
            current_fill_color = background_color
            # Iterate through rows from bottom towards the top border
            for r in range(height - 1, -1, -1):
                if r == border_index:
                    break

                input_color = input_np[r, c]
                if input_color != background_color and input_color != border_color:
                    current_fill_color = input_color
                
                if current_fill_color != background_color or output_grid[r, c] == background_color:
                     output_grid[r, c] = current_fill_color
    
    # The gray border is preserved because we copied the input initially
    # and the loops stop before reaching the border index.

    return output_grid.tolist()