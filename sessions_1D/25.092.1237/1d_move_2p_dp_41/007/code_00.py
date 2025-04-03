"""
Transforms a 1D input grid by rearranging specific segments based on object identification.
1. Identify the 'Main Object': The first contiguous sequence of identical pixels whose color is neither white (0) nor green (3).
2. Identify the 'Anchor Pixel': The first pixel with the color green (3) that appears *after* the Main Object.
3. Identify the 'Separator Pixels': The sequence of pixels located directly between the end of the 'Main Object' and the 'Anchor Pixel'.
4. Identify the 'Prefix Pixels': Any pixels before the 'Main Object'.
5. Identify the 'Anchor and Suffix Pixels': The Anchor Pixel and any pixels after it.
6. Construct the output grid by concatenating these components in the order: Prefix + Separators + Main Object + Anchor/Suffix.
"""

# No external libraries like numpy are needed for this specific logic

def _find_main_object(row):
    """
    Finds the start index, end index (exclusive), and color of the main object.
    The main object is the first contiguous block of identical pixels 
    whose color is not 0 (white) and not 3 (green).
    
    Args:
        row (list): The 1D list of pixels.

    Returns:
        tuple: (start_index, end_index, color) or (None, None, None) if not found.
    """
    n = len(row)
    start_index = -1
    end_index = -1
    color = -1

    # Find the start of the main object
    for i in range(n):
        pixel = row[i]
        if pixel != 0 and pixel != 3:
            start_index = i
            color = pixel
            break
            
    if start_index == -1:
        return None, None, None # Main object not found

    # Find the end of the main object
    for i in range(start_index, n):
        if row[i] != color:
            end_index = i # End index is exclusive
            break
    else: # If the loop completed, the object goes to the end
        end_index = n
        
    return start_index, end_index, color

def _find_anchor(row, search_start_index):
    """
    Finds the index of the first anchor pixel (3) starting from a specific index.

    Args:
        row (list): The 1D list of pixels.
        search_start_index (int): The index from where to start searching.

    Returns:
        int: The index of the anchor pixel, or None if not found.
    """
    n = len(row)
    for i in range(search_start_index, n):
        if row[i] == 3:
            return i
    return None # Anchor pixel not found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list containing a single list representing the 1D grid. 
                           Example: [[0, 2, 2, 0, 0, 3, 0]]

    Returns:
        list: A list containing the transformed 1D grid, or the original grid if
              the required pattern (main object followed by anchor) is not found.
    """
    
    # --- Input Validation and Extraction ---
    # Check if input is a list containing exactly one element which is also a list
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Invalid format, return original grid as per robustness principle
        return input_grid 

    # Extract the 1D row
    grid_1d = input_grid[0]
    
    # Handle empty row case
    if not grid_1d:
        return [[]] 

    # --- Find Objects/Segments ---
    # Find the main object using the helper function
    main_start, main_end, _ = _find_main_object(grid_1d)

    # If main object not found, the pattern doesn't match, return original grid
    if main_start is None:
        return input_grid

    # Find the anchor pixel using the helper function, searching only *after* the main object ends
    anchor_index = _find_anchor(grid_1d, main_end)
    
    # If anchor pixel not found after the main object, the pattern doesn't match, return original grid
    if anchor_index is None:
        return input_grid

    # --- Extract Segments using list slicing based on the found indices ---
    # 1. Prefix: Pixels before the main object starts
    prefix_pixels = grid_1d[:main_start]
    
    # 2. Main Object: The pixels of the main object itself
    main_object_pixels = grid_1d[main_start:main_end]
    
    # 3. Separator: Pixels between the end of the main object and the start of the anchor
    separator_pixels = grid_1d[main_end:anchor_index]
    
    # 4. Anchor and Suffix: The anchor pixel and all pixels after it
    anchor_and_suffix_pixels = grid_1d[anchor_index:]

    # --- Construct Output ---
    # Concatenate the segments in the specified new order: Prefix + Separator + Main Object + Anchor/Suffix
    output_1d = prefix_pixels + separator_pixels + main_object_pixels + anchor_and_suffix_pixels
    
    # Format the output row into the required structure: [[...]]
    output_grid = [output_1d]
    
    return output_grid