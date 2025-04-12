import numpy as np

"""
The transformation identifies horizontal bars (contiguous segments of non-white, non-azure colors) located above the lowest row containing azure (8) pixels (the 'floor') in the input grid. 
These bars are then sorted primarily by length (longest first) and secondarily by their original row index (highest row first, i.e., closer to the top, for ties in length). 
The sorted bars are then placed in the output grid, stacked vertically upwards starting from the row immediately above the floor. 
Each bar is aligned to the right edge of the grid. The floor row itself is copied directly from the input to the output. The rest of the output grid remains white (0).
"""

def find_floor_row(input_array: np.ndarray) -> int:
    """
    Finds the index of the lowest row containing at least one azure (8) pixel.

    Args:
        input_array: The input grid as a numpy array.

    Returns:
        The row index of the floor, or -1 if no azure pixel is found.
    """
    height = input_array.shape[0]
    for r in range(height - 1, -1, -1):
        if 8 in input_array[r, :]:
            return r
    return -1 # Should not happen based on problem description

def find_bars_above_floor(input_array: np.ndarray, floor_row_index: int) -> list[tuple[int, int, int]]:
    """
    Finds all horizontal bars (contiguous segments of the same color, not white or azure) 
    in the rows above the floor line.

    Args:
        input_array: The input grid as a numpy array.
        floor_row_index: The row index of the azure floor.

    Returns:
        A list of tuples, where each tuple represents a bar: (color, length, row_index).
    """
    bars = []
    height, width = input_array.shape
    
    # Determine the upper limit for scanning (either floor row or grid top if no floor)
    scan_limit_row = floor_row_index if floor_row_index != -1 else 0 
    
    # Scan rows above the floor
    for r in range(scan_limit_row):
        c = 0
        while c < width:
            color = input_array[r, c]
            # Check if it's a bar color (not white 0 or azure 8)
            if color != 0 and color != 8:
                # Found the start of a potential bar
                start_c = c
                bar_color = color
                # Find the end of the bar
                while c < width and input_array[r, c] == bar_color:
                    c += 1
                length = c - start_c
                bars.append((bar_color, length, r))
                # Continue scanning from the end of the found bar (already incremented c)
            else:
                # Not a bar color, move to the next column
                c += 1
    return bars

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Transforms the input grid by identifying bars, sorting them by length (desc) 
    and original row (asc for ties), and stacking them right-aligned above the floor.
    
    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output grid with white (0)
    output_array = np.zeros_like(input_array)

    # Find the floor row index
    floor_row_index = find_floor_row(input_array)

    # Copy the floor line to the output grid if found
    if floor_row_index != -1:
         output_array[floor_row_index, :] = input_array[floor_row_index, :]
    # else: # Assume floor always exists based on examples

    # Identify all bars above the floor
    bars = find_bars_above_floor(input_array, floor_row_index)

    # Sort bars: primary key = length descending (-length), secondary key = row index ascending
    sorted_bars = sorted(bars, key=lambda x: (-x[1], x[2]))

    # Place the sorted bars onto the output grid, right-aligned, stacking upwards
    # Start placing just above the floor, or from the bottom if no floor (though floor is expected)
    current_placement_row = (floor_row_index - 1) if floor_row_index != -1 else (height - 1)
        
    for bar_color, bar_length, original_row_idx in sorted_bars:
        # Check if there's space left to place the bar
        if current_placement_row < 0:
            break # Stop if we run out of space at the top
            
        # Calculate start column for right alignment
        start_col = width - bar_length
        end_col = width # Slicing goes up to, but does not include, end_col
        
        # Place the bar
        # Ensure start_col is not negative if bar_length > width (shouldn't happen in ARC)
        start_col = max(0, start_col) 
        output_array[current_placement_row, start_col:end_col] = bar_color
        
        # Move placement row up for the next bar
        current_placement_row -= 1

    # Convert back to list of lists for the final output format
    output_grid = output_array.tolist()
    
    return output_grid