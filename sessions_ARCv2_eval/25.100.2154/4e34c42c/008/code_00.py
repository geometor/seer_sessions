import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter
import collections

"""
Determines the background digit (most frequent). Identifies connected objects 
of non-background digits. Finds a pair of objects (A=Left, B=Right) sharing a unique 
height (H_pair). Finds the widest object (C) among the remaining (ignored) objects. 
If no ignored object C exists, or if C's width (W_C) is not greater than B's 
width (W_B), applies the Simple Rule: horizontally concatenates B's content 
and A's content (excluding A's first column). 
If W_C > W_B, applies the Complex Rule: 
1. Creates a Padding grid by vertically centering the first W_C-2 columns of C's 
   content to height H_pair.
2. Creates an Assembly grid by horizontally concatenating A's content (excluding 
   A's first two columns) and B's content (excluding B's last two columns).
3. Finally, concatenates the Padding and Assembly grids horizontally. 
Returns the resulting grid.
"""

def find_background(grid: np.ndarray) -> int:
    """Finds the most frequent element in the grid, assumed to be the background."""
    if grid.size == 0:
        return 0 # Default for empty grid
    counts = Counter(grid.flatten())
    # If multiple elements have the same highest frequency, pick one (e.g., the lowest value)
    # This shouldn't matter for ARC tasks typically.
    background_digit = counts.most_common(1)[0][0]
    return background_digit

def find_connected_objects(grid: np.ndarray, background_digit: int) -> list[dict]:
    """Finds connected components of non-background digits and returns their properties."""
    mask = grid != background_digit
    # Use 8-connectivity (default for label)
    labeled_array, num_features = label(mask) 
    
    objects = []
    slices = find_objects(labeled_array)
    
    if not slices: 
        return []

    for i, slc in enumerate(slices):
        if slc is None: 
             continue
        obj_id = i + 1 # Labels start from 1
        
        # Extract content and properties from the bounding box slice
        obj_content_full = grid[slc] 
        height = slc[0].stop - slc[0].start
        width = slc[1].stop - slc[1].start
        min_row = slc[0].start
        min_col = slc[1].start
        
        # Ensure the extracted object is not empty
        if height <= 0 or width <= 0:
            continue

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
    
    # Handle cases with empty dimensions
    if current_width == 0:
        return np.full((target_height, 0), pad_value, dtype=content.dtype)
    if current_height == 0:
         # If input content has no height but some width, return full background
        return np.full((target_height, current_width), pad_value, dtype=content.dtype)

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
    # Convert input to numpy array
    grid = np.array(input_grid, dtype=int)
    if grid.size == 0:
        return [] # Handle empty input grid

    # Step 1: Determine background digit
    background_digit = find_background(grid)
    
    # Step 2: Identify all distinct connected objects
    all_objects = find_connected_objects(grid, background_digit)
    if not all_objects:
        return [] # No foreground objects found

    # Step 3: Group objects by height and find the pair height
    height_groups = collections.defaultdict(list)
    for obj in all_objects:
        height_groups[obj['height']].append(obj)
        
    selected_pair = []
    H_pair = -1
    for height, objs in height_groups.items():
        if len(objs) == 2:
            selected_pair = objs
            H_pair = height
            break # Assume only one such height exists per problem constraints
            
    if not selected_pair:
        # Error case: No pair with unique matching height found.
        # Based on examples, this shouldn't happen for valid inputs.
        print("Error: No pair of objects with the same unique height found.")
        return [] 

    # Step 4: Identify Left (A) and Right (B) objects in the selected pair
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

    # Step 5: Identify the ignored set
    ignored_set = [obj for obj in all_objects if obj['id'] != object_A['id'] and obj['id'] != object_B['id']]

    # Step 6: Find the widest ignored object C
    widest_ignored_object_C = None
    W_C_maxW = 0
    if ignored_set:
        # Sort by width (descending) to find the widest
        ignored_set.sort(key=lambda x: x['width'], reverse=True)
        widest_ignored_object_C = ignored_set[0]
        W_C_maxW = widest_ignored_object_C['width']

    # Step 7: Apply conditional transformation rule
    output_grid_np = None
    if widest_ignored_object_C is None or W_C_maxW <= W_B:
        # === Apply the Simple Rule ===
        
        # Slice A: remove first column
        if W_A <= 1:
             sliced_content_A = np.empty((H_pair, 0), dtype=content_A.dtype) 
        else:
             sliced_content_A = content_A[:, 1:]
             
        # Concatenate B and Sliced A
        output_grid_np = np.hstack((content_B, sliced_content_A))

    else:
        # === Apply the Complex Rule (W_C_maxW > W_B) ===
        content_C = widest_ignored_object_C['content']
        
        # --- 1. Create Padding grid ---
        pad_W = W_C_maxW - 2
        padding_base = None
        if pad_W <= 0:
             # If C is too narrow (width 1 or 2), padding base is empty
             # Need the height of C to create an empty array of correct type/dims
             h_C = content_C.shape[0]
             padding_base = np.empty((h_C, 0), dtype=content_C.dtype) 
        else:
             padding_base = content_C[:, :pad_W]

        # Vertically center the padding base
        padding_grid = vertically_center(padding_base, H_pair, background_digit)
        
        # --- 2. Create Assembly grid ---
        # a. Slice A: remove first two columns
        assembly_slice_A = None
        if W_A <= 2:
            assembly_slice_A = np.empty((H_pair, 0), dtype=content_A.dtype) 
        else:
            assembly_slice_A = content_A[:, 2:]
            
        # b. Slice B: remove last two columns
        assembly_slice_B = None
        if W_B <= 2:
             assembly_slice_B = np.empty((H_pair, 0), dtype=content_B.dtype)
        else:
             assembly_slice_B = content_B[:, :-2]
        
        # c. Concatenate Assembly parts
        assembly_grid = np.hstack((assembly_slice_A, assembly_slice_B))

        # --- 3. Combine Padding and Assembly ---
        output_grid_np = np.hstack((padding_grid, assembly_grid))

    # Convert final numpy array back to list of lists
    if output_grid_np is None:
        # Should not happen if logic covers all cases, but as a safeguard
        return [] 
    output_grid = output_grid_np.tolist()
    
    return output_grid