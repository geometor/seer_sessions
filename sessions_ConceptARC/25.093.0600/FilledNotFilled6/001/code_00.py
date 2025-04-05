import numpy as np
from scipy.ndimage import label, find_objects, binary_fill_holes, generate_binary_structure

"""
The transformation identifies distinct connected objects of non-zero colors in the input grid.
For each object, it determines if it's "hollow" (contains enclosed background '0' cells) or "solid" (does not).
If an object is hollow in the input, the transformation fills the enclosed background cells with the object's color in the output.
If an object is solid in the input, the transformation hollows it out in the output by changing its interior cells (cells not on the border) to the background color '0', leaving only the border intact.
"""

def find_neighbors(r, c, shape):
    """ Get valid 4-connected neighbors within grid boundaries. """
    neighbors = []
    rows, cols = shape
    if r > 0: neighbors.append((r - 1, c))
    if r < rows - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < cols - 1: neighbors.append((r, c + 1))
    return neighbors

def transform(input_grid):
    """
    Applies the fill/hollow transformation based on object solidity.

    Args:
        input_grid: A list of lists or numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed grid.
    """
    # Convert input to numpy array for easier processing
    input_arr = np.array(input_grid, dtype=int)
    output_arr = np.copy(input_arr)
    rows, cols = input_arr.shape

    # Get unique non-zero colors
    unique_colors = np.unique(input_arr[input_arr != 0])

    # Define connectivity structure (4-connectivity)
    struct = generate_binary_structure(2, 1) 

    # Process each color separately
    for color in unique_colors:
        # Create a binary mask for the current color
        color_mask = (input_arr == color)

        # Label connected components (objects) for this color
        labeled_array, num_labels = label(color_mask, structure=struct)

        # Find the locations (slices) of each object
        object_slices = find_objects(labeled_array)

        # Iterate through each found object of the current color
        for i in range(num_labels):
            obj_label = i + 1
            obj_slice = object_slices[i]
            
            # Extract the object region from the labeled array and input array
            obj_region_labeled = labeled_array[obj_slice]
            obj_region_input = input_arr[obj_slice]
            
            # Create a mask for the current specific object within its slice
            current_object_mask_in_slice = (obj_region_labeled == obj_label)
            
            # --- Determine if the object is hollow (contains enclosed 0s) ---
            # Use binary_fill_holes on the object mask to find the filled shape
            filled_object_mask_in_slice = binary_fill_holes(current_object_mask_in_slice, structure=struct)
            
            # Identify the holes (enclosed background) by comparing filled vs original
            holes_mask_in_slice = filled_object_mask_in_slice & ~current_object_mask_in_slice
            
            is_hollow = np.any(holes_mask_in_slice)

            # Get coordinates of the object cells relative to the *full grid*
            object_coords_global = np.argwhere(labeled_array == obj_label)

            if is_hollow:
                # --- Fill Action ---
                # Find coordinates of holes relative to the full grid
                hole_coords_relative = np.argwhere(holes_mask_in_slice)
                # Adjust coordinates to be absolute in the full grid
                start_row, start_col = obj_slice[0].start, obj_slice[1].start
                hole_coords_global = [(r + start_row, c + start_col) for r, c in hole_coords_relative]
                
                # Fill the holes in the output grid with the object's color
                for r, c in hole_coords_global:
                    # Double check it was originally background in input
                    if input_arr[r,c] == 0: 
                         output_arr[r, c] = color
            else:
                # --- Hollow Out Action ---
                # Identify interior cells: object cells not adjacent to background (0) in the input
                interior_cells_global = []
                for r, c in object_coords_global:
                    is_border = False
                    for nr, nc in find_neighbors(r, c, input_arr.shape):
                        # Check if neighbor is outside the *current specific object*
                        # This means checking against the labeled array, not just color '0'
                        if labeled_array[nr, nc] != obj_label: 
                            is_border = True
                            break
                    if not is_border:
                        # Check if the cell is truly interior (not on the edge of the grid slice for this object)
                        # This check helps avoid hollowing single-pixel-thick parts incorrectly.
                        # A simpler check: if it wasn't identified as border, it's interior.
                        interior_cells_global.append((r, c))

                # Change interior cells to background color (0) in the output grid
                for r, c in interior_cells_global:
                     # Make sure we don't hollow out single-pixel width lines accidentally.
                     # This check requires careful thought. The current neighbour check is a proxy.
                     # A more robust check might involve comparing the original object mask with its erosion.
                     # For now, the neighbour check handles most cases seen in example.
                     output_arr[r, c] = 0
                     
    return output_arr.tolist() # Return as list of lists if needed, or keep as numpy array