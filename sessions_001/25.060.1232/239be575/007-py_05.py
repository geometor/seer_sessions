import numpy as np

def _is_solid_rectangle(grid, color):
    """Checks if a grid contains a solid rectangle of the given color."""
    rows, cols = grid.shape
    rects = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                # Found a starting pixel. Check for rectangle.
                for height in range(1, rows - r + 1):
                    for width in range(1, cols - c + 1):
                        sub_grid = grid[r:r+height, c:c+width]
                        if np.all(sub_grid == color):
                          rects.append( (height, width) )
    return rects

def analyze_example(input_grid, output_grid):
    red_count = np.sum(input_grid == 2)
    azure_count = np.sum(input_grid == 8)
    red_rectangles = _is_solid_rectangle(input_grid, 2)
    output_value = output_grid[0, 0]

    print(f"  Red Count: {red_count}")
    print(f"  Azure Count: {azure_count}")
    print(f"  Red Rectangles: {red_rectangles}")
    print(f"  Output Value: {output_value}")
    print("-" * 20)
    
def transform(input_grid):
    # Count the number of red (2) pixels.
    red_count = np.sum(input_grid == 2)
    
    # Count the number of azure (8) pixels.
    azure_count = np.sum(input_grid == 8)
    
    # Check for solid red rectangle
    height, width, is_rectangle = _is_solid_rectangle(input_grid, 2)

    # Calculate output based on the new rule
    if is_rectangle and azure_count > 0:
        if height >= 3 and width >= 2 :
          result = 5
        else:
          result = abs(red_count - azure_count)
    elif azure_count == 0 and red_count > 0:
        result = abs(red_count - azure_count)          
    else:
        result = 0

    
    # Create a 1x1 output grid.
    output_grid = np.array([[result]])
    
    return output_grid

# Provided training examples (replace with actual data)
examples = [
    (np.array([[8, 8, 8, 8, 8, 8, 8, 8, 2, 2, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8]]), np.array([[5]])),
    (np.array([[2, 2, 8, 8, 8, 2, 8, 2, 8, 8, 2, 2, 8, 8, 8, 2, 2, 2, 8, 8]]), np.array([[0]])),
    (np.array([[8, 2, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]), np.array([[0]])),
    (np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 2, 2, 2]]), np.array([[0]])),
    (np.array([[2, 8, 8, 2, 8, 8, 2, 2, 8, 8, 2, 2, 2, 2, 8, 8, 8, 8, 8, 8]]), np.array([[0]])),
]
#train_set_transformed = [(transform(inp), out) for inp, out in task['train']]

for i, (input_grid, output_grid) in enumerate(examples):
    print(f"Example {i + 1}:")
    analyze_example(input_grid, output_grid)
    #print(f"  Predicted: {transform(input_grid)[0,0]}")
