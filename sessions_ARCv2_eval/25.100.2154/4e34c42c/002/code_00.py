"""
Identifies connected components (objects) of non-background digits in an input grid.
Determines the background digit as the most frequent digit.
Finds the height (H_pair) shared by exactly two objects (selected_pair).
Identifies the left (A) and right (B) objects within the selected_pair.
Finds the widest object (C) among the remaining (ignored) objects.
Applies one of two transformation rules based on whether the width of C (W_C) is greater than the width of B (W_B):
1. Simple Rule (W_C <= W_B): Concatenates the content of B with the content of A (excluding A's first column).
2. Complex Rule (W_C > W_B): 
   - Creates a padding grid by vertically centering the first W_C-2 columns of C's content to height H_pair.
   - Takes the content of A excluding the first two columns (Slice_A).
   - Reorders the columns of B's content: column 2, then columns 0-1, then columns 3+ (Slice_B).
   - Concatenates Padding, Slice_A, and Slice_B horizontally.
Returns the resulting grid.
"""

import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter
import collections

def find_background(grid: np.ndarray) -> int:
    """Finds the most frequent element in the grid."""
    counts = Counter(grid.flatten())
    # Assume the most frequent is the background
    background_digit = counts.most_common(1)[0][0]
    return background_digit

def find_objects(grid: np.ndarray, background_digit: int) -> list[dict]:
    """Finds connected components of non-background digits."""
    mask = grid != background_digit
    labeled_array, num_features = label(mask)
    
    objects = []
    slices = find_objects(labeled_array)
    
    if not slices: # Handle cases with no foreground objects
        return []

    for i, slc in enumerate(slices):
        if slc is None: # Might happen if labels are not contiguous? Skip.
             continue
        obj_id = i + 1 # Labels start from 1
        # Ensure we only consider the actual object, not the bounding box padding
        component_mask = labeled_array[slc] == obj_id
        obj_content_full = grid[slc] # Content within bounding box
        # Extract only the non-background digits for shape calculation (alternative bounding box)
        # rows, cols = np.where(component_mask)
        # min_r, max_r = rows.min(), rows.max()
        # min_c, max_c = cols.min(), cols.max()
        # height = max_r - min_r + 1
        # width = max_c - min_c + 1
        
        # Use bounding box dimensions directly from find_objects slice
        height = slc[0].stop - slc[0].start
        width = slc[1].stop - slc[1].start
        min_row = slc[0].start
        min_col = slc[1].start

        objects.append({
            'id': obj_id,
            'slice': slc,
            'content': obj_content_full,
            'height': height,
            'width': width,
            'min_row': min_row,
            'min_col': min_col
        })
        
    return objects

def vertically_center(content: np.ndarray, target_height: int, pad_value: int) -> np.ndarray:
    """Centers 'content' vertically within a grid of 'target_height', padding with 'pad_value'."""
    current_height, current_width = content.shape
    if current_height >= target_height:
        # If content is taller or equal, take the central part
        start_row = (current_height - target_height) // 2
        return content[start_row:start_row + target_height, :]

    # Calculate padding needed above and below
    pad_total = target_height - current_height
    pad_top = pad_total // 2
    pad_bottom = pad_total - pad_top

    # Create padding arrays
    top_padding = np.full((pad_top, current_width), pad_value, dtype=content.dtype)
    bottom_padding = np.full((pad_bottom, current_width), pad_value, dtype=content.dtype)

    # Stack them vertically
    centered_content = np.vstack((top_padding, content, bottom_padding))
    return centered_content


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation logic to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    
    # 1. Find Background Digit
    background_digit = find_background(grid)
    
    # 2. Find Objects
    all_objects = find_objects(grid, background_digit)
    if not all_objects:
        return [] # Or handle as error, return empty grid?

    # 3. Group by height and find the pair height
    height_groups = collections.defaultdict(list)
    for obj in all_objects:
        height_groups[obj['height']].append(obj)
        
    selected_pair = []
    H_pair = -1
    for height, objs in height_groups.items():
        if len(objs) == 2:
            selected_pair = objs
            H_pair = height
            break
            
    if not selected_pair:
        # Handle error: No pair with unique matching height found
        # This case is not covered by the examples, returning empty for now.
        print("Error: No pair of objects with the same unique height found.")
        return []

    # 4. Identify Left/Right in selected_pair
    obj1, obj2 = selected_pair
    if obj1['min_col'] < obj2['min_col']:
        object_A = obj1 # Left
        object_B = obj2 # Right
    else:
        object_A = obj2 # Left
        object_B = obj1 # Right
        
    content_A = object_A['content']
    content_B = object_B['content']
    W_A = object_A['width']
    W_B = object_B['width']

    # 5. Identify Ignored Set
    ignored_set = [obj for obj in all_objects if obj not in selected_pair]

    # 6. Find Widest Ignored Object
    widest_ignored_object = None
    W_C_maxW = 0
    if ignored_set:
        widest_ignored_object = max(ignored_set, key=lambda obj: obj['width'])
        W_C_maxW = widest_ignored_object['width']

    # 7. Apply Conditional Rule Selection
    if widest_ignored_object and W_C_maxW > W_B:
        # Apply the Complex Rule
        content_C = widest_ignored_object['content']
        
        pad_W = W_C_maxW - 2
        if pad_W <= 0:
             # If widest ignored is too thin, maybe default to simple rule or handle error?
             # Based on example 2, C has width 8, B has width 7 -> pad_W = 6.
             # Let's assume pad_W will be positive based on the logic W_C > W_B.
             # If C has width 1 or 2, this rule might behave unexpectedly.
             # If W_C = 3 and W_B = 2, pad_W=1. Seems okay.
             # If W_C = 2 and W_B = 1, pad_W=0. Padding will be empty.
             padding_base = np.empty((content_C.shape[0], 0), dtype=content_C.dtype) # Empty base if pad_W is 0
        else:
             padding_base = content_C[:, :pad_W]

        # Create padding grid
        padding_grid = vertically_center(padding_base, H_pair, background_digit)
        
        # Slice A (remove first two columns)
        if W_A <= 2:
            slice_A = np.empty((H_pair, 0), dtype=content_A.dtype) # Empty slice
        else:
            slice_A = content_A[:, 2:]
            
        # Slice and reassemble B
        parts_B = []
        # Part 1: Column 2 (index 2)
        if W_B > 2:
            parts_B.append(content_B[:, 2:3])
        # Part 2: Columns 0, 1 (index 0, 1)
        if W_B > 0:
             parts_B.append(content_B[:, 0:min(2, W_B)]) # Take up to first 2 cols
        # Part 3: Columns 3 onwards (index 3+)
        if W_B > 3:
            parts_B.append(content_B[:, 3:])
            
        if not parts_B:
             slice_B = np.empty((H_pair, 0), dtype=content_B.dtype) # Empty slice if B is too small
        else:
             slice_B = np.hstack(parts_B)

        # Concatenate final output for complex rule
        output_grid_np = np.hstack((padding_grid, slice_A, slice_B))

    else:
        # Apply the Simple Rule
        # Slice A (remove first column)
        if W_A <= 1:
             sliced_content_A = np.empty((H_pair, 0), dtype=content_A.dtype) # Empty slice
        else:
             sliced_content_A = content_A[:, 1:]
             
        # Concatenate final output for simple rule
        output_grid_np = np.hstack((content_B, sliced_content_A))

    # Convert back to list of lists
    output_grid = output_grid_np.tolist()
    
    return output_grid
