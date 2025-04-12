import copy

def find_largest_msb(grid: list[list[int]], digit: int) -> tuple[tuple[int, int] | None, int]:
    """
    Finds the largest monochromatic square block (MSB) of a given digit.

    Args:
        grid: The input grid (list of lists of integers).
        digit: The digit to search for (0, 1, or 2).

    Returns:
        A tuple containing:
        - The top-left coordinate (row, col) of the first largest MSB found
          (in reading order), or None if no MSB of size >= 2x2 exists.
        - The size (side length N) of the largest MSB found, or 0 if none exists.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    max_size = 0
    best_coord = None

    # Iterate possible sizes from largest possible down to 2
    for size in range(min(rows, cols), 1, -1):
        found_at_this_size = False
        # Iterate through possible top-left corners
        for r in range(rows - size + 1):
            for c in range(cols - size + 1):
                is_msb = True
                # Check if the square block is monochromatic
                for i in range(r, r + size):
                    for j in range(c, c + size):
                        if grid[i][j] != digit:
                            is_msb = False
                            break
                    if not is_msb:
                        break
                
                if is_msb:
                    # Found an MSB of the current size
                    if size > max_size:
                        # This is the largest size found so far
                        max_size = size
                        best_coord = (r, c)
                        found_at_this_size = True
                    elif size == max_size and best_coord is None:
                        # This is the first block of the current max size found
                         best_coord = (r,c)
                         found_at_this_size = True
                    # Only need the first one for a given size if it's the max size found so far
                    # For subsequent blocks of the *same* max size, we keep the first coordinate found
        # If we found the largest possible size, no need to check smaller sizes
        if found_at_this_size and size == max_size:
             break # optimization: we found the largest size

    return best_coord, max_size


def find_first_msb_of_size(grid: list[list[int]], digit: int, size: int) -> tuple[int, int] | None:
    """
    Finds the first monochromatic square block (MSB) of a given digit and exact size.

    Args:
        grid: The input grid.
        digit: The digit to search for.
        size: The exact side length N of the square block to find.

    Returns:
        The top-left coordinate (row, col) of the first MSB found
        (in reading order), or None if no such block exists.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    if size < 2 or size > min(rows, cols):
        return None

    # Iterate through possible top-left corners in reading order
    for r in range(rows - size + 1):
        for c in range(cols - size + 1):
            is_msb = True
            # Check if the square block is monochromatic and of the target size
            for i in range(r, r + size):
                for j in range(c, c + size):
                    if grid[i][j] != digit:
                        is_msb = False
                        break
                if not is_msb:
                    break
            
            if is_msb:
                # Found the first MSB of the required size
                return (r, c)
                
    return None # No MSB of the specified size found

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the following rules:

    Default Rule:
    - Change all '0's to '1's.
    - Change all '2's to '0's.
    - '1's and '3's remain unchanged.

    Exception Condition:
    - If the largest monochromatic square block (MSB) of '0's (size N0 >= 2)
      and the largest MSB of '2's (size N2 >= 2) both exist AND have the
      exact same size (N0 = N2 = N), then the following overrides apply:
        1. The '0's within the N x N 0-MSB change to '1's (as per default).
        2. The '2's within the N x N 2-MSB remain '2's (overriding default).
        3. The first N x N MSB of '1's found (in reading order) changes
           to a block of '0's (overriding default).
        4. All other digits outside these specific blocks follow the default rule.
    """
    
    # Find the largest MSBs for 0 and 2
    coord0, N0 = find_largest_msb(input_grid, 0)
    coord2, N2 = find_largest_msb(input_grid, 2)

    # Initialize output grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    rows = len(output_grid)
    cols = len(output_grid[0]) if rows > 0 else 0

    # Check if the exception condition is met
    exception_applies = (N0 >= 2 and N2 >= 2 and N0 == N2)
    
    if exception_applies:
        N = N0 # The common size
        # Find the first MSB of '1's with size N
        coord1_special = find_first_msb_of_size(input_grid, 1, N)

        # Apply transformations considering the exception
        for r in range(rows):
            for c in range(cols):
                # Check if cell is within the 2-MSB
                is_in_L2_MSB = (coord2 is not None and 
                                r >= coord2[0] and r < coord2[0] + N and 
                                c >= coord2[1] and c < coord2[1] + N)
                
                # Check if cell is within the special 1-MSB
                is_in_L1_special = (coord1_special is not None and 
                                      r >= coord1_special[0] and r < coord1_special[0] + N and 
                                      c >= coord1_special[1] and c < coord1_special[1] + N)

                if is_in_L2_MSB:
                    # Rule 2: 2s in the 2-MSB remain 2
                    output_grid[r][c] = 2 
                elif is_in_L1_special:
                     # Rule 3: 1s in the special 1-MSB become 0
                    output_grid[r][c] = 0
                else:
                    # Apply default rules for cells outside the exception blocks
                    if input_grid[r][c] == 0:
                        output_grid[r][c] = 1
                    elif input_grid[r][c] == 2:
                        output_grid[r][c] = 0
                    # else: 1s and 3s remain as copied initially
                        
    else:
        # Apply default transformations globally
        for r in range(rows):
            for c in range(cols):
                if input_grid[r][c] == 0:
                    output_grid[r][c] = 1
                elif input_grid[r][c] == 2:
                    output_grid[r][c] = 0
                # else: 1s and 3s remain as copied initially

    return output_grid