import numpy as np

"""
Identifies solid rectangular blocks of non-white colors in the input grid. 
For each block that has a height and width greater than 2, it changes the color 
of the interior pixels (excluding the 1-pixel border) to azure (8). 
Pixels belonging to the border, the background (white, 0), or blocks too small 
to have an interior remain unchanged.
"""

def find_solid_rectangles(grid):
    """
    Finds solid rectangular blocks of non-white colors using Breadth-First Search (BFS).
    
    Args:
        grid (np.array): The input grid.
        
    Returns:
        list: A list of tuples, where each tuple represents a found solid rectangle
              and contains (color, r_min, c_min, r_max, c_max).
              - color: The color of the rectangle.
              - r_min, c_min: Coordinates of the top-left corner.
              - r_max, c_max: Coordinates of the bottom-right corner.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool) # Keep track of visited pixels
    rectangles = [] # List to store properties of found rectangles

    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # If pixel is non-white (not 0) and hasn't been visited yet, start BFS
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c] # Get the color of the potential object
                q = [(r, c)] # Initialize queue for BFS with the starting pixel
                visited[r, c] = True # Mark starting pixel as visited
                pixels = set([(r, c)]) # Set to store all pixels belonging to this object
                
                # Initialize bounding box for the current object
                r_min, c_min = r, c
                r_max, c_max = r, c

                # Perform BFS to find all connected pixels of the same color
                head = 0
                while head < len(q):
                    row, col = q[head]
                    head += 1
                    
                    # Update bounding box coordinates
                    r_min = min(r_min, row)
                    c_min = min(c_min, col)
                    r_max = max(r_max, row)
                    c_max = max(c_max, col)

                    # Explore neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check if neighbor is within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                           # Check if neighbor has the same color and hasn't been visited
                           if not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True # Mark neighbor as visited
                                q.append((nr, nc)) # Add neighbor to the queue
                                pixels.add((nr, nc)) # Add neighbor to the set of object pixels

                # After BFS, check if the identified object is a solid rectangle
                rect_height = r_max - r_min + 1
                rect_width = c_max - c_min + 1
                is_solid_rectangle = True
                
                # Condition 1: The number of pixels found must equal the area of the bounding box
                if len(pixels) != rect_height * rect_width:
                    is_solid_rectangle = False
                else:
                    # Condition 2: Verify all pixels within the bounding box actually match the color
                    # This confirms the shape is solid and rectangular.
                    for row_idx in range(r_min, r_max + 1):
                        for col_idx in range(c_min, c_max + 1):
                            if grid[row_idx, col_idx] != color:
                                is_solid_rectangle = False
                                break
                        if not is_solid_rectangle:
                            break
                
                # If it's confirmed to be a solid rectangle, add its properties to the list
                if is_solid_rectangle:
                    rectangles.append((color, r_min, c_min, r_max, c_max))
                    # Make sure all pixels within this confirmed rectangle are marked visited
                    # This prevents issues if BFS somehow didn't cover every pixel within the bounds,
                    # although the len(pixels) check should handle this.
                    visited[r_min:r_max+1, c_min:c_max+1] = True
                           
    return rectangles


def transform(input_grid):
    """
    Transforms the input grid by changing the color of the interior pixels 
    of solid rectangular blocks (with height > 2 and width > 2) to azure (8).

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid
    output_array = np.copy(input_array)
    
    # Find all solid rectangular objects in the input grid
    solid_rects = find_solid_rectangles(input_array)
    
    # Define the color to use for filling the interior
    fill_color = 8 # azure

    # Process each found solid rectangle
    for _color, r_min, c_min, r_max, c_max in solid_rects:
        # Calculate the height and width of the rectangle
        height = r_max - r_min + 1
        width = c_max - c_min + 1
        
        # Check if the rectangle is large enough to have an interior region
        # An interior exists only if height > 2 and width > 2
        if height > 2 and width > 2:
            # Determine the slice indices for the interior region
            # The interior starts one pixel in from each border
            interior_r_start = r_min + 1
            interior_r_end = r_max # NumPy slice upper bound is exclusive
            interior_c_start = c_min + 1
            interior_c_end = c_max # NumPy slice upper bound is exclusive
            
            # Update the output array by setting the interior pixels to the fill color
            output_array[interior_r_start:interior_r_end, interior_c_start:interior_c_end] = fill_color
            
    # Convert the resulting NumPy array back to a list of lists format
    output_grid = output_array.tolist()
    
    return output_grid
