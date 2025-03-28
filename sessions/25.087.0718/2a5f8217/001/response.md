```python
import numpy as np

"""
Examine the input grid and identify all unique pixel colors present, excluding white (0) and blue (1). 
Let this set of colors be InfluencerColors.
If the set InfluencerColors is empty, make no changes to the grid; the output is identical to the input.
If the set InfluencerColors is not empty, find the color within this set that has the smallest numerical index. Let this color be TargetColor.
Create the output grid by copying the input grid.
Iterate through every pixel in the output grid. If a pixel's color is blue (1), change its color to TargetColor. Otherwise, keep its original color.
Return the modified output grid.
This rule is derived from examples 1 and 2, example 3 seems to follow a different pattern.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the presence of non-white, non-blue colors.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array if necessary
    grid = np.array(input_grid)

    # Find all unique colors present in the grid
    unique_colors = np.unique(grid)

    # Identify influencer colors (non-white (0) and non-blue (1))
    influencer_colors = [color for color in unique_colors if color != 0 and color != 1]

    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()

    # Check if there are any influencer colors
    if influencer_colors:
        # Find the color with the minimum numerical index among influencer colors
        target_color = min(influencer_colors)

        # Find the locations of all blue (1) pixels
        blue_pixels = (output_grid == 1)

        # Change the color of all blue pixels to the target color
        output_grid[blue_pixels] = target_color
    # Else (no influencer colors), the output grid remains unchanged (already copied)

    return output_grid.tolist() # Convert back to list of lists for consistency if needed

```