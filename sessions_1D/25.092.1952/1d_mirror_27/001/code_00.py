import numpy as np

"""
The transformation rule operates on each row of the input grid independently.
For each row:
1. Identify the pivot element, which is the maroon (9) pixel. Assume there is exactly one pivot per row.
2. Create an output row of the same size, initialized with white (0) pixels.
3. Place the pivot (9) in the output row at the same column index it had in the input row.
4. Find the contiguous block of non-white pixels (the 'Object') located before the pivot in the input row. This object is the one immediately preceding the pivot, potentially separated by some white (0) pixels.
5. Identify the contiguous block of white (0) pixels (the 'Separator') located between the end of the Object and the pivot in the input row. The Separator's length can be zero if the Object is immediately adjacent to the pivot.
6. In the output row, place the Separator immediately after the pivot. Since the output is initialized to white, this step effectively reserves the space.
7. In the output row, place the Object immediately after the Separator. The Object retains its original color and length.
8. All other positions in the output row remain white (0).
9. Combine the processed rows to form the final output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output grid with the same shape as input, filled with white (0)
    output_np = np.zeros_like(input_np)

    # Process each row independently
    for r_idx in range(input_np.shape[0]):
        row = input_np[r_idx, :]
        output_row = output_np[r_idx, :]

        # 1. Find the pivot (maroon=9) index
        pivot_indices = np.where(row == 9)[0]
        
        # Assume exactly one pivot per row based on examples
        if len(pivot_indices) != 1:
             # If no pivot or multiple pivots, copy the row as is (or handle error)
             # For this task, examples suggest a single pivot is guaranteed.
             # If not found, let's copy the input row to be safe.
            output_np[r_idx, :] = row
            continue # Move to the next row
            
        pivot_index = pivot_indices[0]

        # 2. Place the pivot in the output row
        output_row[pivot_index] = 9

        # 3. Find the object (non-white block before pivot) and separator
        object_color = 0
        object_start = -1
        object_end = -1
        object_length = 0
        separator_length = 0

        # Scan backwards from the position just before the pivot
        current_index = pivot_index - 1
        
        # Scan backwards through any white pixels (separator)
        while current_index >= 0 and row[current_index] == 0:
            current_index -= 1
        
        # If we are still within the row bounds, we found the end of the object
        if current_index >= 0:
            object_end = current_index
            object_color = row[object_end] # Get the color of the object
            object_start = object_end
            
            # Scan backwards to find the start of the object (contiguous block of same color)
            while object_start > 0 and row[object_start - 1] == object_color:
                object_start -= 1
                
            # Calculate object length
            object_length = object_end - object_start + 1
            
            # Calculate separator length (number of white pixels between object end and pivot)
            separator_length = (pivot_index - 1) - object_end
            
        else:
             # No non-white object found before the pivot
             # Calculate separator length as all white pixels before pivot
             separator_length = pivot_index


        # 4. Determine placement indices in the output row
        # Separator starts immediately after the pivot
        separator_start_out = pivot_index + 1
        separator_end_out = separator_start_out + separator_length # exclusive index
        
        # Object starts immediately after the separator
        object_start_out = separator_end_out
        object_end_out = object_start_out + object_length # exclusive index

        # 5. Place the object in the output row (separator is already white)
        # Check if the object placement is within the bounds of the output row
        if object_length > 0 and object_start_out < len(output_row):
            # Calculate the actual end index considering row boundaries
            actual_object_end_out = min(object_end_out, len(output_row))
            # Place the object (or part of it that fits)
            output_row[object_start_out:actual_object_end_out] = object_color

    # Convert the final NumPy array back to a list of lists
    return output_np.tolist()
