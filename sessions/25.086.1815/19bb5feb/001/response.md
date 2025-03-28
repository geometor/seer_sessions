```python
import numpy as np

"""
Identifies 2x2 colored squares within a larger azure (8) region in the input grid. 
Maps the color of each square to a cell in a 2x2 output grid based on the square's 
quadrant relative to the center of the azure region. If a quadrant contains no 
such square, the corresponding output cell remains white (0).
"""

def find_azure_bounding_box(grid):
    """Finds the minimum bounding box containing all azure (8) pixels."""
    azure_coords = np.argwhere(grid == 8)
    if azure_coords.size == 0:
        return None # No azure region found
    min_row = np.min(azure_coords[:, 0])
    max_row = np.max(azure_coords[:, 0])
    min_col = np.min(azure_coords[:, 1])
    max_col = np.max(azure_coords[:, 1])
    return min_row, max_row, min_col, max_col

def find_colored_squares(grid):
    """Finds all 2x2 squares of a single color (not white 0 or azure 8)."""
    squares = []
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            color = grid[r, c]
            # Check if the color is valid (not white or azure)
            if color != 0 and color != 8:
                # Check if it forms a 2x2 square
                if (grid[r+1, c] == color and
                    grid[r, c+1] == color and
                    grid[r+1, c+1] == color):
                    squares.append({'color': color, 'row': r, 'col': c})
    return squares

def transform(input_grid):
    """
    Transforms the input grid by finding 2x2 colored squares within an azure region
    and mapping them to a 2x2 output grid based on their relative quadrant.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    
    # Initialize an empty 2x2 output grid, filled with white (0).
    output_grid = np.zeros((2, 2), dtype=int)

    # Identify the bounding box of the azure (8) colored region.
    bbox = find_azure_bounding_box(input_grid)
    if bbox is None:
        # If no azure region, return the default white 2x2 grid (though examples suggest one always exists)
        return output_grid.tolist() 
        
    min_row, max_row, min_col, max_col = bbox
    
    # Calculate the center coordinates of the azure bounding box.
    # Note: Center might be between pixels. Comparison logic handles partitioning.
    center_row = (min_row + max_row) / 2.0
    center_col = (min_col + max_col) / 2.0

    # Find all distinct 2x2 squares composed of a single color (excluding white and azure).
    colored_squares = find_colored_squares(input_grid)

    # For each found colored 2x2 square, determine its quadrant and update the output grid.
    for square in colored_squares:
        r, c = square['row'], square['col']
        color = square['color']
        
        # Check if the square's top-left corner is within the azure bounding box 
        # (or at least relevant to its structure - this check might be optional depending on task rules)
        # The logic relies on relative position to the center, so strict containment isn't strictly necessary
        # as long as the squares are the ones 'intended' by the pattern. Let's proceed without strict bbox check first.

        # Determine the quadrant based on the top-left corner (r, c) relative to the center.
        if r < center_row:
            if c < center_col:
                # Top-Left quadrant
                output_grid[0, 0] = color
            else:
                # Top-Right quadrant
                output_grid[0, 1] = color
        else: # r >= center_row
            if c < center_col:
                # Bottom-Left quadrant
                output_grid[1, 0] = color
            else:
                # Bottom-Right quadrant
                output_grid[1, 1] = color

    # Return the final 2x2 output grid.
    return output_grid.tolist()
```