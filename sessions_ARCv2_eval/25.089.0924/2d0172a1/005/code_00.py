import numpy as np
from scipy.ndimage import label, find_objects

def transform(input_grid):
    """
    Identifies the largest contiguous object (connected component) of the non-background color 
    in the input grid and returns the minimal bounding box containing that object.

    1. Convert the input list of lists to a NumPy array.
    2. Identify the background color as the most frequent color in the grid.
    3. Handle edge cases: If the grid is empty or contains only one color, return an empty list.
    4. Create a binary mask where non-background pixels are marked as True (1) and background pixels as False (0).
    5. Use `scipy.ndimage.label` to find all connected components (objects) of non-background pixels (using 4-connectivity, i.e., horizontal and vertical adjacency).
    6. If no non-background objects are found, return an empty list.
    7. Calculate the size (number of pixels) of each distinct object found.
    8. Identify the label corresponding to the largest object (the one with the most pixels).
    9. Find the coordinates (min_row, max_row, min_col, max_col) of the minimal bounding box containing only the pixels of the largest object.
    10. Extract the subgrid from the original input grid using these bounding box coordinates.
    11. Convert the extracted NumPy subgrid back to a list of lists and return it.
    """
    # 1. Convert the input list of lists to a NumPy array.
    grid = np.array(input_grid, dtype=int)

    # 2. Handle edge cases: Empty grid
    if grid.size == 0:
        return []

    # Find unique colors and their counts
    unique_colors, counts = np.unique(grid, return_counts=True)

    # 2. Handle edge cases: Grid with only one color
    if len(unique_colors) <= 1:
        return [] 

    # 3. Identify the background color (most frequent)
    background_color = unique_colors[np.argmax(counts)]

    # 4. Create a binary mask for non-background pixels
    object_mask = (grid != background_color)

    # 5. Find connected components (objects)
    # structure=np.array([[0,1,0],[1,1,1],[0,1,0]]) defines 4-connectivity (von Neumann neighborhood)
    labeled_array, num_features = label(object_mask, structure=np.array([[0,1,0],[1,1,1],[0,1,0]]))

    # 6. If no non-background objects are found, return an empty list.
    if num_features == 0:
        return []

    # 7. Calculate the size of each distinct object
    # Get unique labels (excluding 0 which represents background/non-object) and their counts
    unique_labels, label_counts = np.unique(labeled_array[labeled_array > 0], return_counts=True)

    # 8. Identify the label corresponding to the largest object
    if len(unique_labels) == 0: # Should technically be caught by num_features == 0, but belts and suspenders
        return []
        
    largest_object_label = unique_labels[np.argmax(label_counts)]

    # 9. Find the coordinates of the minimal bounding box for the largest object
    # Method 1: Using find_objects
    # objects_slices = find_objects(labeled_array)
    # largest_object_slice = objects_slices[largest_object_label - 1] # find_objects returns 0-indexed slices
    # min_row, max_row = largest_object_slice[0].start, largest_object_slice[0].stop
    # min_col, max_col = largest_object_slice[1].start, largest_object_slice[1].stop
    
    # Method 2: Finding coordinates manually (more robust if find_objects is not available or behaves unexpectedly)
    object_coords = np.argwhere(labeled_array == largest_object_label)
    if object_coords.size == 0:
        # This shouldn't happen if largest_object_label was found correctly
        return [] 
    min_row = np.min(object_coords[:, 0])
    max_row = np.max(object_coords[:, 0])
    min_col = np.min(object_coords[:, 1])
    max_col = np.max(object_coords[:, 1])


    # 10. Extract the subgrid using the bounding box coordinates
    # Note: NumPy slicing is exclusive of the stop index, so add 1 to max values
    output_grid_np = grid[min_row : max_row + 1, min_col : max_col + 1]

    # 11. Convert the resulting NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid