import numpy as np
from scipy.ndimage import label, generate_binary_structure
import collections

"""
Identifies marker pixels (color 9) in the input grid. For each connected 
component of marker pixels, finds its minimum row index. For each unique minimum 
row index found (`min_r`), defines a 5-row high slice starting at `min_r`. 
Within this 5-row slice (or fewer rows if near the grid bottom), identifies the 
horizontal bounding box (min/max columns) of all non-background, non-marker pixels. 
Extracts this rectangular region from the original grid using the defined rows 
and the calculated pattern columns. 

Collects these extracted slices, ensuring duplicates based on start row and 
column bounds are not added. Sorts the unique slices based on the minimum row 
index (`min_r`) that triggered their extraction, in descending order (highest 
row index first). Pads slices vertically with the background color if they are 
shorter than the maximum extracted height (typically 5). Finally, concatenates 
the sorted (and potentially padded) slices horizontally to produce the output grid. 
Handles cases like empty grids, missing markers, or no associated patterns found 
for markers by returning a default 1x1 background grid.
"""

def get_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent color in the grid, assuming it's the background.
    Returns 0 as default if the grid is empty or no color is dominant.
    """
    if grid.size == 0:
        return 0 # Default background for empty grid
    counts = collections.Counter(grid.flat)
    if counts:
         # most_common(1) returns list of tuples [(value, count)]
         return counts.most_common(1)[0][0]
    elif grid.size > 0:
         # Fallback if counter is empty but grid has elements (e.g., single pixel grid)
         return grid.flat[0] 
    else:
         return 0 # Default

def find_components_and_min_rows(grid: np.ndarray, target_color: int) -> list[int]:
    """
    Finds connected components of a specific target_color and returns a list 
    of the minimum row index for each distinct component found. Uses 8-way 
    connectivity.
    """
    binary_grid = (grid == target_color)
    # Use 8-way connectivity (diagnals included)
    structure = generate_binary_structure(2, 2) 
    labeled_grid, num_components = label(binary_grid, structure=structure)
    
    min_rows_per_label = {}
    if num_components > 0:
        # Iterate through the grid efficiently to find the first occurrence (min row) for each label
        rows, cols = np.where(labeled_grid > 0)
        for r, c in zip(rows, cols):
            label_id = labeled_grid[r, c]
            if label_id not in min_rows_per_label:
                min_rows_per_label[label_id] = r
                    
    return list(min_rows_per_label.values()) # Returns a list of min_rows, one for each component

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Transforms the input grid based on marker pixels (color 9).
    Extracts 5-row high slices associated with marker components, sorts them 
    by the marker's minimum row (descending), and concatenates horizontally.
    """
    input_np = np.array(input_grid, dtype=np.int8)
    h, w = input_np.shape

    # Handle empty input grid
    if h == 0 or w == 0:
        return [[]]

    # Identify marker color (fixed at 9 for this problem) and background color
    marker_color = 9
    background_color = get_background_color(input_np)

    # Find the minimum row for each marker component
    marker_component_min_rows = find_components_and_min_rows(input_np, marker_color)
    
    # If no markers found, return a 1x1 background grid as per interpretation
    if not marker_component_min_rows:
         # Check if grid contains only background
         if np.all(input_np == background_color):
              return [[int(background_color)]]
         else:
              # Or maybe return empty if no markers but other stuff exists?
              # Based on examples, seems like markers are required.
              # Returning 1x1 background seems safer.
              return [[int(background_color)]]

    extracted_regions = []
    # Track processed regions defined by (start_row, col_min, col_max) to avoid duplicates
    processed_regions_ids = set() 

    # Use unique min_rows associated with markers to define potential slice start rows
    unique_min_rows = sorted(list(set(marker_component_min_rows)))

    for m_min_r in unique_min_rows:
        
        # Define the row slice range (max 5 rows, respecting grid height)
        start_row = m_min_r
        end_row = min(start_row + 5, h) 
        
        # Skip if the start row is beyond the grid height
        if start_row >= h:
             continue
        
        # Select the relevant rows from the input grid
        rows_to_examine = input_np[start_row:end_row, :]
        
        # Create a mask for non-background, non-marker pixels within these rows
        pattern_mask = (rows_to_examine != background_color) & (rows_to_examine != marker_color)
        
        # Find the column indices where such pattern pixels exist
        pattern_cols_in_slice = np.where(pattern_mask)[1] # We only need column indices
        
        # If no pattern pixels found in these rows associated with this marker_min_row, skip
        if pattern_cols_in_slice.size == 0:
            continue 
            
        # Determine the horizontal extent (min/max columns) of the *pattern* in this slice
        p_min_c = np.min(pattern_cols_in_slice)
        p_max_c = np.max(pattern_cols_in_slice)
        
        # Define the region identifier to check if we already extracted this exact slice
        # Uses the actual data rows and the pattern's column bounds
        region_id = (start_row, end_row, p_min_c, p_max_c)
        if region_id in processed_regions_ids:
            continue # Skip duplicate region
        processed_regions_ids.add(region_id)

        # Extract the final slice using defined rows and calculated pattern columns
        # Note: We slice the original input_np, not rows_to_examine, to get the full slice data
        extracted_slice = input_np[start_row:end_row, p_min_c : p_max_c + 1]

        # Store the slice along with the marker row that triggered it (for sorting)
        # Ensure the slice is not empty before storing
        if extracted_slice.size > 0:
             extracted_regions.append({'trigger_row': m_min_r, 'slice': extracted_slice})

    # Sort the collected regions based on the marker row that triggered them, descending order
    extracted_regions.sort(key=lambda x: x['trigger_row'], reverse=True)

    # If no valid regions were extracted after filtering, return background grid
    if not extracted_regions:
         return [[int(background_color)]] 

    final_slices = [region['slice'] for region in extracted_regions]
    
    # Determine the target height (max height found among slices) for padding
    max_h = 0
    valid_heights = [s.shape[0] for s in final_slices if s.ndim == 2 and s.shape[0] > 0]
    if valid_heights:
        max_h = max(valid_heights)
    elif final_slices: # Handle case where maybe only 1D arrays resulted? Should not happen.
         pass # max_h remains 0

    # Pad slices shorter than max_h at the bottom with the background color
    padded_slices = []
    for s in final_slices:
         # Ensure it's a valid 2D array before padding
        if s.ndim == 2 and s.shape[0] > 0 and s.shape[1] > 0:
            if s.shape[0] < max_h:
                pad_h = max_h - s.shape[0]
                # Create padding array
                padding = np.full((pad_h, s.shape[1]), background_color, dtype=s.dtype)
                # Stack original slice on top of padding
                padded_s = np.vstack((s, padding))
                padded_slices.append(padded_s)
            elif s.shape[0] == max_h: # Only add if height matches max_h
                # Slice already has max height (or is the only slice)
                padded_slices.append(s)
            # else: slices taller than max_h? Should not happen if max_h is correct.
            # or slices with 0 height? Should be filtered by size > 0 check.

    # If after padding, no valid slices remain, return background
    if not padded_slices:
         # This might happen if all extracted slices had 0 height or width
         return [[int(background_color)]] 

    # Perform horizontal stacking (concatenation)
    try:
        # Ensure all arrays in padded_slices are 2D before hstack
        # This check might be redundant given previous filtering but adds safety
        arrays_to_stack = [arr for arr in padded_slices if arr.ndim == 2 and arr.shape[0] > 0 and arr.shape[1] > 0]
        if not arrays_to_stack:
             return [[int(background_color)]] # No valid arrays left to stack
        
        # Verify all arrays have the same height before stacking
        first_height = arrays_to_stack[0].shape[0]
        if not all(arr.shape[0] == first_height for arr in arrays_to_stack):
             # This indicates an error in padding or height calculation
             print(f"Error: Mismatched heights before hstack. Heights: {[arr.shape[0] for arr in arrays_to_stack]}")
             return [[int(background_color)]] 
             
        output_np = np.hstack(arrays_to_stack)
        
    except ValueError as e:
        # Catch potential errors during hstack (e.g., if somehow heights mismatch despite checks)
        print(f"Error during hstack: {e}")
        # Provide details for debugging
        print(f"Number of arrays to stack: {len(padded_slices)}")
        for i, arr in enumerate(padded_slices):
            print(f"  Slice {i} shape: {arr.shape}, dtype: {arr.dtype}")
            
        # Return a default error indicator or background grid
        return [[int(background_color)]]


    # Convert final numpy array back to list of lists
    return output_np.tolist()