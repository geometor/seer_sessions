```python
import numpy as np

"""
Transformation Rule:
1. Initialize the output grid as a copy of the input grid.
2. Remove any pre-existing Maroon (9) pixels by changing them to the background color (Orange, 7).
3. Iterate through each row of the grid.
4. In each row, identify all pairs of Red (2) pixels.
5. For each pair of Red pixels (at columns left_col and right_col, where left_col < right_col), check if all pixels strictly between them (from column left_col + 1 to right_col - 1) are the background color (Orange, 7).
6. If the condition is met (only Orange pixels between the pair), change the color of these intervening Orange pixels to Maroon (9) in the output grid.
7. Leave all other pixels, including the Red pixels forming the pairs, unchanged.
"""

def transform(input_grid):
    """
    Fills the horizontal space between pairs of red pixels (2) with maroon pixels (9)
    if the space contains only the background color (orange, 7),
    and removes any original maroon pixels from the input.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = input_np.copy()
    
    rows, cols = output_grid.shape
    background_color = 7
    red_color = 2
    maroon_color = 9

    # Step 2: Remove any pre-existing Maroon (9) pixels
    output_grid[output_grid == maroon_color] = background_color

    # Step 3: Iterate through each row
    for r in range(rows):
        row = output_grid[r, :]
        
        # Step 4: Find indices of Red (2) pixels in the current row
        red_indices = np.where(row == red_color)[0]
        
        # Step 5: Identify pairs and check the space between them
        num_reds = len(red_indices)
        if num_reds >= 2:
            for i in range(num_reds):
                for j in range(i + 1, num_reds):
                    left_col = red_indices[i]
                    right_col = red_indices[j]
                    
                    # Ensure there is space between them
                    if right_col > left_col + 1:
                        # Check if all pixels between them are the background color
                        space_between = row[left_col + 1 : right_col]
                        is_background_only = np.all(space_between == background_color)
                        
                        # Step 6: Fill with Maroon if the condition is met
                        if is_background_only:
                            output_grid[r, left_col + 1 : right_col] = maroon_color
                            
    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```