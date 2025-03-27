import numpy as np

# Define helper functions
def get_output_color(input_color):
    """
    Calculates the output color based on the input color using the rule:
    output_color = input_color + 5
    Applies only to colors 1 (blue), 2 (red), 3 (green), 4 (yellow).
    """
    if input_color in [1, 2, 3, 4]:
        return input_color + 5
    # Return None or raise an error if unexpected input color is found
    # Based on the problem description, only 1, 2, 3, 4 should be triggering colors.
    return None 

def find_non_separator_color(grid_block):
    """
    Finds the unique color in a grid block that is not white (0) or gray (5).
    Assumes exactly one such color exists per block based on task description.
    """
    # Flatten the block and find unique colors
    unique_colors = np.unique(grid_block)
    # Iterate through unique colors to find the trigger color
    for color in unique_colors:
        if color != 0 and color != 5:
            return color
    # Return None if no such color is found (should not happen based on task description)
    return None 

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Gray pixels (5) act as separators. Horizontal gray lines divide the grid
       into independent horizontal regions. Vertical gray lines divide these
       regions (or the whole grid) into vertical sections.
    2. Within each section (defined by separators and grid boundaries), locate
       the single pixel whose color is not white (0) or gray (5). Let this input
       color be C_in.
    3. Calculate the corresponding output color C_out = C_in + 5.
    4. Fill the entire section in the output grid with C_out, replacing all
       original pixels within that section except for the gray separator pixels (5),
       which are preserved.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize the output array as a copy of the input array.
    # This automatically preserves the gray separator lines (color 5).
    output_array = np.copy(input_array)

    # --- Identify Separators and Boundaries ---

    # Identify horizontal boundary rows. These are rows completely filled with gray (5).
    # Include implicit boundaries at the top (-1) and bottom (height).
    h_boundaries = [-1] 
    for r in range(height):
        if np.all(input_array[r, :] == 5):
            h_boundaries.append(r)
    h_boundaries.append(height)
    # Remove duplicates and sort, just in case
    h_boundaries = sorted(list(set(h_boundaries))) 

    # Identify vertical boundary columns. These are columns completely filled with gray (5).
    # Include implicit boundaries at the left (-1) and right (width).
    v_boundaries = [-1]
    for c in range(width):
        # Check if the column consists entirely of gray pixels
        if np.all(input_array[:, c] == 5):
             v_boundaries.append(c)
    v_boundaries.append(width)
    # Remove duplicates and sort
    v_boundaries = sorted(list(set(v_boundaries)))

    # --- Process Sections Defined by Boundaries ---

    # Iterate through each horizontal region defined by consecutive horizontal boundaries
    for i in range(len(h_boundaries) - 1):
        # Get the start and end row indices for the current region
        # r_start is the row index of the boundary above the region
        # r_end is the row index of the boundary below the region
        r_start = h_boundaries[i]
        r_end = h_boundaries[i+1]

        # Skip if the identified "region" is just the separator line itself
        if r_end == r_start + 1 and r_start != -1 :
             continue 

        # Iterate through each vertical section within the current horizontal region
        for j in range(len(v_boundaries) - 1):
            # Get the start and end column indices for the current section
            # c_start is the col index of the boundary left of the section
            # c_end is the col index of the boundary right of the section
            c_start = v_boundaries[j]
            c_end = v_boundaries[j+1]

            # Skip if the identified "section" is just the separator line itself
            if c_end == c_start + 1 and c_start != -1:
                 continue 

            # Define the actual coordinates of the block (section) within the grid
            # These are exclusive of the boundary lines themselves
            block_r_start = r_start + 1
            block_r_end = r_end
            block_c_start = c_start + 1
            block_c_end = c_end

            # Ensure the block has valid positive dimensions before proceeding
            if block_r_start >= block_r_end or block_c_start >= block_c_end:
                continue

            # Extract the subgrid corresponding to this block from the input array
            input_block = input_array[block_r_start:block_r_end, block_c_start:block_c_end]

            # Find the unique non-white (0), non-gray (5) color within this input block
            trigger_color = find_non_separator_color(input_block)

            # If a trigger color was found (it should always be found based on task)
            if trigger_color is not None:
                # Calculate the corresponding output color
                output_color = get_output_color(trigger_color)

                # Check if a valid output color was determined
                if output_color is not None:
                    # Fill the corresponding block in the output array
                    # Iterate through each cell within the block's boundaries
                    for r in range(block_r_start, block_r_end):
                        for c in range(block_c_start, block_c_end):
                            # Check if the cell in the output grid is NOT a gray separator
                            # We check output_array because it initially holds all separators
                            if output_array[r, c] != 5:
                                # Update the cell color to the calculated output color
                                output_array[r, c] = output_color

    # Convert the final numpy array back to a list of lists for the required output format
    return output_array.tolist()