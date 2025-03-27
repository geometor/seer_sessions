```python
import numpy as np
from scipy.ndimage import label, find_objects, binary_dilation, generate_binary_structure

def find_most_frequent_color(grid):
    """Finds the most frequent color in the grid."""
    unique, counts = np.unique(grid, return_counts=True)
    return unique[np.argmax(counts)]

def get_object_pixels(labeled_grid, obj_label):
    """Gets the coordinates of pixels belonging to a specific object label."""
    return np.argwhere(labeled_grid == obj_label)

def get_bounding_box(pixels):
    """Calculates the bounding box (min_row, min_col, max_row, max_col) for a set of pixels."""
    if not pixels.size:
        return None
    min_row = np.min(pixels[:, 0])
    min_col = np.min(pixels[:, 1])
    max_row = np.max(pixels[:, 0])
    max_col = np.max(pixels[:, 1])
    return min_row, min_col, max_row, max_col

def check_adjacency(grid, obj_pixels, adj_color):
    """Checks if any pixel of the object is adjacent (including diagonals) to the adj_color."""
    rows, cols = grid.shape
    for r, c in obj_pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == adj_color:
                    return True
    return False

def get_adjacent_pixels(grid, obj_pixels, adj_color):
    """Finds all pixels of adj_color adjacent (including diagonals) to the object pixels."""
    rows, cols = grid.shape
    adjacent_coords = set()
    for r, c in obj_pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == adj_color:
                    adjacent_coords.add((nr, nc))
    return np.array(list(adjacent_coords)) if adjacent_coords else np.empty((0, 2), dtype=int)


def check_containment(grid, obj_pixels, contain_color):
    """Checks if any pixel within the object has the contain_color."""
    for r, c in obj_pixels:
        if grid[r, c] == contain_color:
            return True
    return False

def transform(input_grid):
    """
    Identifies distinct non-background objects in the input grid.
    Determines a selection criterion based on either adjacency to maroon (9)
    or containment of azure (8) pixels within the objects.
    Selects objects matching the criterion.
    Calculates the bounding box for each selected object. If the criterion is
    maroon adjacency, the bounding box includes the object pixels and any
    adjacent maroon pixels. Otherwise, it includes only the object pixels.
    Sorts the selected objects based on their original horizontal position:
    right-to-left if the criterion involves maroon, left-to-right otherwise.
    Extracts the subgrids corresponding to the bounding boxes.
    Concatenates the extracted subgrids horizontally in the determined order
    to form the output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify background color
    background_color = find_most_frequent_color(input_np)

    # 2. Identify all distinct non-background objects
    mask = input_np != background_color
    # Use 8-connectivity (including diagonals)
    structure = generate_binary_structure(2, 2)
    labeled_grid, num_objects = label(mask, structure=structure)

    target_objects_info = []
    criterion = None # 'maroon_adj' or 'azure_contain'

    # 3 & 4. Determine selection rule and filter objects
    objects_with_maroon_adj = []
    objects_with_azure_contain = []

    for i in range(1, num_objects + 1):
        obj_pixels = get_object_pixels(labeled_grid, i)
        if obj_pixels.size == 0:
            continue

        if check_adjacency(input_np, obj_pixels, 9): # Check for maroon (9) adjacency
             objects_with_maroon_adj.append(i)
        if check_containment(input_np, obj_pixels, 8): # Check for azure (8) containment
            objects_with_azure_contain.append(i)

    # Determine the criterion based on which list is non-empty
    # Prioritize maroon adjacency if both potentially apply? Examples suggest one rule per task.
    target_labels = []
    if objects_with_maroon_adj:
        criterion = 'maroon_adj'
        target_labels = objects_with_maroon_adj
    elif objects_with_azure_contain:
        criterion = 'azure_contain'
        target_labels = objects_with_azure_contain
    else:
        # No matching objects found based on the known criteria
        # This case might need refinement based on more examples,
        # for now return empty or original grid? Let's return empty.
        return []


    # 5. Calculate bounding boxes for target objects
    for obj_label in target_labels:
        obj_pixels = get_object_pixels(labeled_grid, obj_label)

        if criterion == 'maroon_adj':
            # Include adjacent maroon pixels in the bounding box calculation
            adj_maroon_pixels = get_adjacent_pixels(input_np, obj_pixels, 9)
            all_pixels_for_bbox = np.vstack((obj_pixels, adj_maroon_pixels)) if adj_maroon_pixels.size > 0 else obj_pixels
            bbox = get_bounding_box(all_pixels_for_bbox)
        elif criterion == 'azure_contain':
            # Bounding box includes only the object pixels
            bbox = get_bounding_box(obj_pixels)
        else: # Should not happen if target_labels is populated
             continue

        if bbox:
            min_r, min_c, max_r, max_c = bbox
            # Store bounding box and the leftmost column for sorting
            target_objects_info.append({
                "label": obj_label,
                "bbox": bbox,
                "min_col": min_c # Use min_col of the *object itself* for sorting origin
            })

    # 6. Determine assembly order
    if criterion == 'maroon_adj':
        # Sort descending by min_col (right-to-left)
        target_objects_info.sort(key=lambda x: x['min_col'], reverse=True)
    elif criterion == 'azure_contain':
        # Sort ascending by min_col (left-to-right)
        target_objects_info.sort(key=lambda x: x['min_col'], reverse=False)

    # 7. Extract subgrids
    extracted_subgrids = []
    for obj_info in target_objects_info:
        min_r, min_c, max_r, max_c = obj_info['bbox']
        subgrid = input_np[min_r : max_r + 1, min_c : max_c + 1]
        extracted_subgrids.append(subgrid)

    # 8. Concatenate horizontally
    if not extracted_subgrids:
        # Handle cases where no target objects were found or extracted
        return [] # Or maybe return input_grid? The examples suggest a transformation occurs.

    # Ensure all subgrids have the same height before concatenating.
    # Find the maximum height among all subgrids.
    # Pad shorter subgrids. This wasn't explicitly observed but might be needed.
    # Let's assume they naturally have the same height based on the examples.
    # Example 1 output height = 5. BBox for right obj: (11, 20, 15, 22) -> height 5. BBox for left obj: (6, 6, 10, 15) -> height 5. OK.
    # Example 2 output height = 5. BBox for left obj: (15, 5, 17, 7) -> height 3?? Error in manual bbox calculation?
    # Let's re-examine example 2 object bounding boxes.
    # Obj 1 (left): Contains azure(8) at (24, 7), (25, 7), (26, 7). Pixels range row 23-27, col 2-7. BBox (23, 2, 27, 7). Height 5.
    # Obj 2 (middle): Contains azure(8) at (2, 10), (3, 10), (4, 10). Pixels range row 1-5, col 10-16. BBox (1, 10, 5, 16). Height 5.
    # Obj 3 (right): Contains azure(8) at (16, 11). NO, azure is not in this object.
    # Let's re-read the description. Ah, the objects in example 2 ARE the ones containing azure.
    # Obj near bottom left: rows 23-27, cols 2-7. Contains azure at col 7. BBox (23, 2, 27, 7). Height 5.
    # Obj near top right: rows 1-5, cols 10-16. Contains azure at col 10. BBox (1, 10, 5, 16). Height 5.
    # Ok, heights match.

    try:
        output_np = np.concatenate(extracted_subgrids, axis=1)
    except ValueError as e:
        # This might happen if heights don't match, indicating an issue in logic or assumptions.
        print(f"Error concatenating subgrids: {e}")
        print(f"Subgrid shapes: {[sg.shape for sg in extracted_subgrids]}")
        # Handle error case, maybe return empty grid or raise exception
        return []


    # Convert final numpy array back to list of lists
    output_grid = output_np.tolist()

    return output_grid
```