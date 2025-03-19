import numpy as np

# Example Data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 7],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 7],
                            [0, 0, 0, 0, 0, 7],
                            [0, 0, 0, 0, 0, 7],
                            [0, 0, 0, 0, 0, 7],
                            [0, 0, 0, 0, 0, 7]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 5, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 6, 6, 6],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[5, 5, 0, 0, 0, 6, 6, 6],
                            [5, 5, 0, 0, 0, 6, 6, 6],
                            [5, 5, 0, 0, 0, 6, 6, 6],
                            [5, 5, 0, 0, 0, 6, 6, 6],
                            [5, 5, 0, 0, 0, 6, 6, 6]]),
    },
    {
       "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 4, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 3, 0, 0, 0, 0, 8, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 3, 0, 4, 0, 0, 8, 0],
                           [0, 0, 3, 0, 4, 0, 0, 8, 0],
                           [0, 0, 3, 0, 4, 0, 0, 8, 0],
                           [0, 0, 3, 0, 4, 0, 0, 8, 0],
                           [0, 0, 3, 0, 4, 0, 0, 8, 0]]),
    },
]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find non-zero pixels
    nonzero_pixels = get_nonzero_pixels(input_grid)

    # Expand horizontally
    expanded_grid = expand_horizontally(input_grid, nonzero_pixels)
    
    # expand vertically
    output_grid = expand_vertically(input_grid, expanded_grid)

    return output_grid

def get_nonzero_pixels(grid):
    """Finds the coordinates of all non-zero pixels in a grid."""
    pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                pixels.append((r, c, grid[r, c]))
    return pixels

def expand_horizontally(grid, pixels):
    """Expands pixels horizontally to the maximum extent."""
    expanded_grid = np.zeros_like(grid)
    for r, c, color in pixels:
        # Find leftmost boundary
        left = c
        while left > 0 and grid[r, left - 1] == 0:
            left -= 1

        # Find rightmost boundary
        right = c
        while right < grid.shape[1] - 1 and grid[r, right + 1] == 0:
            right += 1

        # Fill horizontally
        expanded_grid[r, left:right+1] = color
    return expanded_grid
    

def expand_vertically(input_grid, expanded_grid):
    """Expands blocks vertically based on some complex rule."""
    final_grid = np.copy(expanded_grid)
    
    pixels = get_nonzero_pixels(input_grid)
    if not pixels:
        return final_grid

    #find top and bottom edges of each colour
    color_extents = {}
    for r,c, color in pixels:
        if color not in color_extents:
            color_extents[color] = {'top':input_grid.shape[0], 'bottom':-1, 'left':input_grid.shape[1], 'right': -1}
        color_extents[color]['top'] = min(color_extents[color]['top'], r)
        color_extents[color]['bottom'] = max(color_extents[color]['bottom'], r)
        color_extents[color]['left'] = min(color_extents[color]['left'], c)
        color_extents[color]['right'] = max(color_extents[color]['right'], c)

    # expand each object vertically, up to existing edges
    for color in color_extents:
        top_edge = color_extents[color]['top']
        bottom_edge = color_extents[color]['bottom']
        
        leftmost = color_extents[color]['left']
        rightmost = color_extents[color]['right']
      
        # find horizontal extent in expanded grid
        for r in range(input_grid.shape[0]):
            if expanded_grid[r, leftmost] == color:
              left_edge = r
              while left_edge > 0 and expanded_grid[left_edge-1, leftmost] == color:
                  left_edge-=1
            if expanded_grid[r, rightmost] == color:    
              right_edge = r
              while right_edge < input_grid.shape[0] -1 and expanded_grid[right_edge+1,rightmost] == color:
                right_edge+=1

        # expand the color within its boundaries
        for r in range(input_grid.shape[0]):
            if expanded_grid[r, leftmost] == color:
                # find connected regions of the color
                top = r
                while top > 0 and expanded_grid[top-1, leftmost] == color:
                    top-=1
                bottom = r
                while bottom < input_grid.shape[0]-1 and expanded_grid[bottom+1, leftmost] == color:
                    bottom+=1

                #find new top
                new_top = top
                while new_top > 0 and expanded_grid[new_top-1, leftmost] == 0:
                    new_top -= 1
                if new_top < top_edge:
                  new_top = top_edge
                new_bottom = bottom
                while new_bottom < input_grid.shape[0]-1 and expanded_grid[new_bottom+1, leftmost] == 0:
                    new_bottom +=1
                #fill the section, if it contains original colored pixel
                for rr in range(top, bottom+1):
                  final_grid[new_top:new_bottom+1,:] = np.where(expanded_grid[rr:rr+1,:]==color, color, final_grid[new_top:new_bottom+1,:])
    return final_grid

for i, example in enumerate(examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    print(f"  Input:\n{input_grid}")
    print(f"  Expected Output:\n{expected_output}")
    print(f"  Predicted Output:\n{predicted_output}")
    print(f"  Match: {np.array_equal(predicted_output, expected_output)}")
    print("-" * 20)
