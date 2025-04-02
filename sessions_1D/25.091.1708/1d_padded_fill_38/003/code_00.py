import numpy as np

"""
Transforms a 1D sequence based on the positions and spacing of a 'marker' color.

1.  Treats the input grid data as a single, one-dimensional sequence.
2.  Identifies the single non-white color ("marker color") present in the sequence.
3.  Finds all 0-based indices where the marker color appears.
4.  Forms pairs of consecutive marker indices `(start_index, end_index)`.
5.  Calculates the distance (`end_index - start_index`) for each pair.
6.  Selects only those pairs where the distance is strictly greater than 9.
7.  Creates a new output sequence, initialized with the background color (white, 0), 
    with a length exactly one less than the input sequence length.
8.  Iterates through the selected pairs in the order they were found:
    a. For the *first* selected pair `(s, e)`, it fills the output sequence 
       from index `s` up to and including index `e-1` with the marker color.
    b. For all *subsequent* selected pairs `(s, e)`, it fills the output sequence 
       from index `s+1` up to and including index `e` with the marker color.
9.  Returns the final output sequence as a list.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list or list of lists or np.ndarray): Input grid data.

    Returns:
        list: A 1D list representing the transformed output sequence.
    """
    # 1. Convert input to a flat 1D NumPy array
    try:
        input_sequence = np.array(input_grid, dtype=int).flatten()
    except ValueError: # Handle potentially inconsistent list depths if not rectangular
         # Fallback: flatten potentially jagged list
         flat_list = []
         q = list(input_grid)
         while q:
             item = q.pop(0)
             if isinstance(item, list):
                 q = item + q # Prepend items to maintain order
             else:
                 flat_list.append(item)
         input_sequence = np.array(flat_list, dtype=int)


    input_length = len(input_sequence)
    
    # Handle empty input
    if input_length == 0:
        return []
        
    output_length = input_length - 1
    # Handle input too short to produce meaningful output
    if output_length < 0:
         return []

    # 2. Identify marker color (first non-zero element)
    marker_color = 0
    for pixel in input_sequence:
        if pixel != 0:
            marker_color = pixel
            break

    # Handle case with no marker color or only background
    if marker_color == 0:
        return [0] * output_length

    # 3. Find marker indices
    marker_indices = np.where(input_sequence == marker_color)[0]

    # Handle case with fewer than 2 markers
    if len(marker_indices) < 2:
        return [0] * output_length

    # 4. Form pairs of consecutive indices
    marker_pairs = []
    for i in range(len(marker_indices) - 1):
        start_idx = marker_indices[i]
        end_idx = marker_indices[i+1]
        marker_pairs.append((start_idx, end_idx))

    # 5. Calculate distances
    # 6. Select pairs where distance > 9
    distance_threshold = 9
    selected_pairs = []
    for start_idx, end_idx in marker_pairs:
        distance = end_idx - start_idx
        if distance > distance_threshold:
            selected_pairs.append((start_idx, end_idx))

    # 7. Create output sequence initialized with background (0)
    output_sequence = np.zeros(output_length, dtype=int)

    # 8. Fill output sequence based on selected pairs
    is_first_selected_pair = True
    for start_idx, end_idx in selected_pairs:
        if is_first_selected_pair:
            # Rule for the first pair: fill [s, e-1]
            fill_start = start_idx
            fill_end = end_idx - 1
            is_first_selected_pair = False
        else:
            # Rule for subsequent pairs: fill [s+1, e]
            fill_start = start_idx + 1
            fill_end = end_idx

        # Ensure indices are within bounds of the output sequence
        # Use slicing for efficient filling, ensuring bounds are respected
        actual_fill_start = max(0, fill_start)
        actual_fill_end = min(output_length, fill_end + 1) # +1 because slice upper bound is exclusive
        
        if actual_fill_start < actual_fill_end: # Check if there's actually a range to fill
            output_sequence[actual_fill_start:actual_fill_end] = marker_color

    # 9. Return the result as a list
    return output_sequence.tolist()