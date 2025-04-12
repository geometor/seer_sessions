```python
import numpy as np
from scipy.ndimage import label, find_objects

"""
Identifies all distinct contiguous groups (connected components) of non-background colored pixels 
in the input grid using 8-way connectivity. Calculates the size (number of pixels) of each group.
Determines the group with the maximum size (the "largest object"). Creates an output grid of the 
same dimensions as the input, filled with the background color (black, 0). Copies only the pixels 
belonging to the largest identified object from the input grid to the output grid at their 
original locations and with their original color.
"""

def find_largest_component(grid: np.ndarray, background_color: int = 0) -> tuple[np.ndarray | None, int | None]:
    """
    Finds the coordinates and color of the largest connected component of non-background pixels.

    Args:
        grid: The input grid as a numpy array.
        background_color: The integer value representing the background color.

    Returns:
        A tuple containing:
        - A boolean mask of the same shape as the grid, where True indicates a pixel
          belongs to the largest component. None if no non-background components exist.
        - The color of the largest component. None if no non-background components exist.
    """
    # Create a boolean mask where non-background pixels are True
    mask = grid != background_color

    # Define 8-way connectivity
    connectivity_structure = np.array([[1, 1, 1],
                                       [1, 1, 1],
                                       [1, 1, 1]], dtype=bool)

    # Label connected components
    # labeled_array contains integers identifying each component (0 for background)
    # num_features is the total number of components found (excluding background)
    labeled_array, num_features = label(mask, structure=connectivity_structure)

    # Handle the case where there are no non-background pixels
    if num_features == 0:
        return None, None

    # Find the size of each component (excluding background label 0)
    component_sizes = np.bincount(labeled_array.ravel())
    # Ignore the count for the background (label 0)
    component_sizes = component_sizes[1:]

    # Find the label of the largest component
    # Add 1 back because we sliced off the background count at index 0
    largest_component_label = np.argmax(component_sizes) + 1

    # Create a mask for the largest component
    largest_component_mask = (labeled_array == largest_component_label)

    # Find the coordinates of the first pixel in the largest component to get its color
    coords = np.argwhere(largest_component_mask)
    if len(coords) == 0: # Should not happen if num_features > 0, but good practice
         return None, None
    first_pixel_coords = tuple(coords[0])
    component_color = grid[first_pixel_coords]


    return largest_component_mask, component_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by isolating the largest connected component of
    non-background pixels and placing it on a background grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid with only the largest component.
    """
    # Convert input grid to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Define the background color (assuming 0 based on perception)
    background_color = 0

    # Initialize the output grid with the background color
    output_array = np.full((rows, cols), background_color, dtype=int)

    # Find the mask and color of the largest component
    largest_component_mask, component_color = find_largest_component(input_array, background_color)

    # If a largest component was found, draw it onto the output grid
    if largest_component_mask is not None and component_color is not None:
        # Apply the mask: where the mask is True, set the output array pixel
        # to the component's color
        output_array[largest_component_mask] = component_color

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```