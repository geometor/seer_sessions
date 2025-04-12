```python
import numpy as np
from scipy.ndimage import label, binary_fill_holes, generate_binary_structure
from collections import Counter

"""
Transforms the input grid by identifying the largest connected non-background object (shape),
finding all enclosed background regions (potential holes) within it using binary_fill_holes,
and then filling only those potential hole regions that consist of 1 or 2 pixels 
with the color of the largest shape. Uses 4-way connectivity throughout.
"""

def _find_largest_shape_mask_and_color(grid: np.ndarray, background_color: int = 0) -> tuple[np.ndarray | None, int]:
    """
    Finds the mask and color of the largest 4-connected non-background object.

    Args:
        grid: The input grid as a numpy array.
        background_color: The integer value representing the background.

    Returns:
        A tuple containing:
        - A boolean numpy array mask for the largest shape, or None if no shape found.
        - The integer color of the largest shape, or background_color if no shape found.
    """
    non_background_mask = grid != background_color
    if not np.any(non_background_mask):
        return None, background_color

    # Use 4-connectivity for defining shapes
    structure = generate_binary_structure(2, 1) 
    labeled_array, num_features = label(non_background_mask, structure=structure)

    if num_features == 0:
        return None, background_color

    # Find the size of each component, ignoring label 0 (background)
    component_sizes = np.bincount(labeled_array.ravel())
    if len(component_sizes) > 0:
        component_sizes[0] = 0 
    
    if np.all(component_sizes == 0):
        return None, background_color # No non-background components found

    # Find the label of the largest component
    largest_component_label = np.argmax(component_sizes)
    
    # Create mask for the largest shape
    largest_shape_mask = (labeled_array == largest_component_label)
    
    # Get the color of the largest shape
    # Find the first coordinate of the shape to get its color
    coords = np.argwhere(largest_shape_mask)
    if coords.size > 0:
        shape_color = int(grid[coords[0, 0], coords[0, 1]])
        return largest_shape_mask, shape_color
    else:
        # Should not happen if component_sizes had non-zero entries
        return None, background_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the transformation rule to fill small (<= 2 pixels) holes 
    within the largest connected non-background shape.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array and initialize output grid
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    background_color = 0
    
    # 1. Find the largest connected non-background shape, its mask, and its color
    largest_shape_mask, shape_color = _find_largest_shape_mask_and_color(grid, background_color)

    # If no shape found, return the original grid
    if largest_shape_mask is None:
        return output_grid.tolist()

    # 2. Identify potential holes using binary_fill_holes
    # Use 4-connectivity for hole structure consistency
    hole_structure = generate_binary_structure(2, 1)
    filled_mask = binary_fill_holes(largest_shape_mask, structure=hole_structure)
    
    # Mask identifying only the pixels filled by binary_fill_holes
    potential_hole_mask = filled_mask & ~largest_shape_mask
    
    # If no potential holes were found, return the original grid copy
    if not np.any(potential_hole_mask):
         return output_grid.tolist()

    # 3. Label the connected components within the potential holes mask
    # Use 4-connectivity for hole components
    labeled_holes, num_hole_features = label(potential_hole_mask, structure=hole_structure)

    if num_hole_features == 0:
        # Should not happen if np.any(potential_hole_mask) was true, but check defensively
        return output_grid.tolist()

    # 4. Calculate the size of each hole component
    hole_labels = labeled_holes[labeled_holes > 0] # Exclude background label 0
    if hole_labels.size == 0:
        return output_grid.tolist() # No actual hole regions found
        
    hole_sizes = Counter(hole_labels) # More direct than bincount when labels might not be contiguous

    # 5. Iterate through hole components and fill small ones (size <= 2)
    for hole_label, size in hole_sizes.items():
        if size <= 2:
            # Find pixels belonging to this small hole component
            hole_coords = np.argwhere(labeled_holes == hole_label)
            # Fill these pixels in the output grid with the shape color
            for r, c in hole_coords:
                output_grid[r, c] = shape_color
                
    # Convert the final grid back to list of lists and return
    return output_grid.tolist()
```