import numpy as np

"""
Transforms a 1D input sequence based on the positions of a 'marker' color.

1.  Treats the input grid data as a single, one-dimensional sequence.
2.  Identifies the single non-white 'marker color'.
3.  Finds all indices where the marker color appears.
4.  Forms pairs of consecutive marker indices and calculates the distance between them.
5.  Selects pairs where the distance is greater than a threshold (9 in the examples).
6.  Creates an output sequence of length (input_length - 1), initialized with white (0).
7.  Fills segments of the output sequence with the marker color based on the selected pairs:
    - For the first selected pair (start_idx, end_idx), fills indices [start_idx, end_idx - 1].
    - For subsequent pairs, fills indices [start_idx - 1, end_idx - 1].
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid. 
                                     Expected to be treated as a 1D sequence.

    Returns:
        list: A 1D list representing the transformed output sequence.
    """
    # 1. Treat input as a 1D sequence
    # Assuming input_grid might be a list of lists (e.g., [[...]]) or just a list [...]
    if isinstance(input_grid[0], list):
         input_sequence = np.array(input_grid).flatten().tolist()
    else:
         # If it's already flat (like in the provided examples)
         input_sequence = list(input_grid) 

    input_length = len(input_sequence)
    if input_length == 0:
        return []

    # 2. Identify marker color (first non-zero color)
    marker_color = 0
    for pixel in input_sequence:
        if pixel != 0:
            marker_color = pixel
            break
    
    # Handle case with no marker color or only background
    if marker_color == 0:
        return [0] * (input_length - 1) if input_length > 0 else []


    # 3. Find marker indices
    marker_indices = [i for i, pixel in enumerate(input_sequence) if pixel == marker_color]

    if len(marker_indices) < 2:
        # Not enough markers to form pairs
        return [0] * (input_length - 1) if input_length > 0 else []

    # 4. Form pairs and calculate distances
    marker_pairs = []
    distances = []
    for i in range(len(marker_indices) - 1):
        start_idx = marker_indices[i]
        end_idx = marker_indices[i+1]
        distance = end_idx - start_idx
        marker_pairs.append((start_idx, end_idx))
        distances.append(distance)

    # 5. Select pairs based on distance threshold (> 9)
    distance_threshold = 9
    selected_pairs = [pair for pair, dist in zip(marker_pairs, distances) if dist > distance_threshold]

    # 6. Create output sequence (length N-1) initialized with background (0)
    output_length = input_length - 1
    output_sequence = [0] * output_length

    # 7. Fill output sequence based on selected pairs
    is_first_pair = True
    for start_idx, end_idx in selected_pairs:
        if is_first_pair:
            # Rule for the first pair: fill [start_idx, end_idx - 1]
            fill_start = start_idx
            fill_end = end_idx - 1 
            is_first_pair = False
        else:
            # Rule for subsequent pairs: fill [start_idx - 1, end_idx - 1]
            fill_start = start_idx - 1
            fill_end = end_idx - 1
        
        # Ensure indices are within bounds of the output sequence
        fill_start = max(0, fill_start)
        fill_end = min(output_length -1 , fill_end)

        # Fill the segment
        for i in range(fill_start, fill_end + 1):
             # Add check to prevent index out of bounds if fill_end was capped
             if i < output_length:
                 output_sequence[i] = marker_color

    return output_sequence