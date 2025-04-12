import numpy as np

"""
The transformation takes an input grid containing horizontal bars of various colors above a solid azure floor line at the bottom. 
It identifies these bars, sorts them by their original vertical position (lowest first), and then stacks them vertically upwards starting from the row just above the azure floor. 
Crucially, each bar is aligned to the right edge of the grid in the output. The azure floor remains in its original position. The rest of the grid is white.
"""

def find_bars(input_grid: np.ndarray, floor_row_index: int) -> list[tuple[int, int, int]]:
    """
    Finds all horizontal bars (contiguous segments of the same color, not white or azure) 
    above the floor line.

    Args:
        input_grid: The input grid as a numpy array.
        floor_row_index: The row index of the azure floor.

    Returns:
        A list of tuples, where each tuple represents a bar: (color, length, row_index).
    """
    bars = []
    height, width = input_grid.shape
    
    # Scan rows above the floor
    for r in range(floor_row_index):
        c = 0
        while c < width:
            color = input_grid[r, c]
            # Check if it's a bar color (not white 0 or azure 8)
            if color != 0 and color != 8:
                # Found the start of a potential bar
                start_c = c
                bar_color = color
                # Find the end of the bar
                while c < width and input_grid[r, c] == bar_color:
                    c += 1
                length = c - start_c
                bars.append((bar_color, length, r))
                # Continue scanning from the end of the found bar
            else:
                # Not a bar color, move to the next column
                c += 1
    return bars

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Rearranges horizontal bars from the input grid by stacking them vertically 
    from bottom to top (based on original position), right-aligned, 
    above a fixed azure floor line.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output grid with white (0)
    output_array = np.zeros_like(input_array)

    # Find the azure floor line (assuming it's solid and at the bottom)
    floor_row_index = -1
    for r in range(height - 1, -1, -1):
        if np.all(input_array[r, :] == 8):
            floor_row_index = r
            break
        # Handle cases where floor might not be solid, find first row containing 8
        elif 8 in input_array[r, :]: 
             # Check if it's the actual floor by seeing if it spans the width or is the lowest row with 8
             is_floor = True
             for c_check in range(width):
                 # Allow for white padding around the floor as seen in examples
                 if input_array[r, c_check] != 8 and input_array[r, c_check] != 0:
                     is_floor = False
                     break
             if is_floor and 8 in input_array[r,:]: # Ensure there's at least one 8
                floor_row_index = r
                break


    if floor_row_index == -1:
        # Fallback or error handling if no azure floor is found
        # For this specific problem, assume the floor always exists.
        # If it might not, we'd return the input or an empty grid, depending on requirements.
        # Let's assume it's the last row if no solid '8' row is found but 8 exists somewhere
        # For robustnes lets find the lowest row containing an 8
        for r in range(height - 1, -1, -1):
            if 8 in input_array[r,:]:
                floor_row_index = r
                break
        # If still -1, it means no 8 exists at all, which contradicts the problem description
        # For now, we proceed assuming floor_row_index is valid based on examples.


    # Copy the floor line to the output grid
    if floor_row_index != -1:
         output_array[floor_row_index, :] = input_array[floor_row_index, :]
    else:
         # If no floor was found even with fallbacks, maybe return input?
         # Based on problem, floor is guaranteed.
         pass 

    # Identify all bars above the floor
    bars = find_bars(input_array, floor_row_index if floor_row_index != -1 else height)

    # Sort bars by original row index (descending order - lowest bar first)
    # Bars with higher row index were lower on the screen
    sorted_bars = sorted(bars, key=lambda x: x[2], reverse=True)

    # Place the sorted bars onto the output grid, right-aligned, stacking upwards
    if floor_row_index != -1:
        current_placement_row = floor_row_index - 1
    else:
        # If no floor, stack from bottom
        current_placement_row = height - 1
        
    for bar_color, bar_length, _ in sorted_bars:
        if current_placement_row < 0:
            # Stop if we run out of space at the top
            break 
            
        # Calculate start column for right alignment
        start_col = width - bar_length
        end_col = width
        
        # Place the bar
        output_array[current_placement_row, start_col:end_col] = bar_color
        
        # Move placement row up for the next bar
        current_placement_row -= 1

    # Convert back to list of lists for the final output
    output_grid = output_array.tolist()
    
    return output_grid