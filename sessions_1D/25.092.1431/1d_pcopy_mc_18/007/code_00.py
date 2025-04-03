import copy

"""
Transforms a 1D input list of pixels based on the following rule:
1.  Create a copy of the input list to serve as the initial output list.
2.  Scan the original input list from the second element (index 1) to the second-to-last element (index width-2).
3.  Identify any non-white pixel (value > 0) that is immediately surrounded by white pixels (value 0) on both its left and right sides in the input list. Such a pixel is called an "isolated single pixel".
4.  For each isolated single pixel found at index `i` with color `c` in the input list, modify the output list by setting the elements at indices `i-1`, `i`, and `i+1` to the color `c`.
5.  Pixels in the output list that are not part of such a 3-pixel expansion retain their original copied value from the input list.
6.  Return the final modified output list.
"""

def transform(input_list):
    """
    Applies the expansion transformation to isolated single pixels in a 1D list.

    Args:
        input_list (list[int]): A 1D list of integers representing the pixel row.

    Returns:
        list[int]: The transformed 1D list.
    """
    # Check if the input is a list
    if not isinstance(input_list, list):
        raise TypeError("Input must be a list of integers.")
        
    # Check if all elements are integers (optional, but good practice)
    if not all(isinstance(item, int) for item in input_list):
         raise TypeError("All elements in the input list must be integers.")

    width = len(input_list)

    # Handle edge cases: lists too short to have isolated pixels
    if width < 3:
        return copy.deepcopy(input_list) # Return a copy, no changes possible

    # Initialize output_list as a deep copy of the input_list.
    # Modifications will be made to this copy based on analysis of the original input_list.
    output_list = copy.deepcopy(input_list)

    # Iterate through the input list to find isolated single pixels.
    # We only need to check indices from 1 up to width - 2 (exclusive).
    # Pixels at index 0 and width-1 cannot be surrounded by two neighbors.
    for i in range(1, width - 1):
        # Get the color of the current pixel and its immediate neighbors from the original input list.
        current_pixel_color = input_list[i]
        left_neighbor_color = input_list[i-1]
        right_neighbor_color = input_list[i+1]

        # Check for the isolated single pixel condition:
        # 1. Current pixel is non-white (color != 0)
        # 2. Left neighbor is white (color == 0)
        # 3. Right neighbor is white (color == 0)
        if current_pixel_color != 0 and left_neighbor_color == 0 and right_neighbor_color == 0:
            # If it's an isolated single pixel, perform the expansion in the output_list.
            # Set the left neighbor, the pixel itself, and the right neighbor in the output_list
            # to the color of the isolated pixel found in the input_list.
            output_list[i-1] = current_pixel_color
            output_list[i]   = current_pixel_color
            output_list[i+1] = current_pixel_color

    # Return the modified output_list.
    return output_list