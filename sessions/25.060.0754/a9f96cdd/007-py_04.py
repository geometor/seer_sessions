import numpy as np

def find_2x2_squares(grid):
    """Finds all 2x2 squares of the same color in the grid."""
    squares = []
    for r in range(grid.shape[0] - 1):
        for c in range(grid.shape[1] - 1):
            subgrid = grid[r:r+2, c:c+2]
            if np.all(subgrid == subgrid[0, 0]):
                squares.append((r, c, subgrid[0, 0]))  # (row, col, color)
    return squares

def analyze_example(input_grid, output_grid):
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    squares = find_2x2_squares(input_grid)
    output_color = output_grid[0,0] if output_shape == (3,3) else None
    
    print(f"Input Shape: {input_shape}")
    print(f"Output Shape: {output_shape}")
    print(f"Detected 2x2 Squares: {squares}")
    print(f"Output Color: {output_color}")

    # Check if the output color matches any of the found squares
    color_match = False
    for _,_, color in squares:
        if color == output_color:
            color_match = True
            break
    print(f"Output Color Matches a 2x2 Square: {color_match}")
    print("---")
    
# Example data (replace with your actual example data)
examples = [
    (np.array([[0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0],
              [0,0,0,1,1,0,0],
              [0,0,0,1,1,0,0],
              [0,0,0,0,0,0,0]]),
    np.array([[1,1,1],
              [1,1,1],
              [1,1,1]])),

    (np.array([[0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,1,1,0,0],
              [0,0,1,1,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0]]),
    np.array([[1,1,1],
              [1,1,1],
              [1,1,1]])),

    (np.array([[0,0,0,0,0],
              [0,0,0,0,0],
              [0,1,1,0,0],
              [0,1,1,0,0],
              [0,0,0,0,0]]),
    np.array([[1,1,1],
              [1,1,1],
              [1,1,1]])),

    (np.array([[5,5,5,5,0],
              [5,5,5,5,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0]]),
    np.array([[0,0,0],
              [0,0,0],
              [0,0,0]])),
     (np.array([[0,0,0,0,0,0],
              [0,2,2,0,0,0],
              [0,2,2,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,4,4],
              [0,0,0,0,4,4]]),
    np.array([[2,2,2],
              [2,2,2],
              [2,2,2]])),
    (np.array([[0,8,8,0,0,0],
             [0,8,8,0,0,0],
             [0,0,0,0,6,6],
             [0,0,0,0,6,6],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0]]),
    np.array([[8,8,8],
              [8,8,8],
              [8,8,8]]))
]

for input_grid, output_grid in examples:
    analyze_example(input_grid, output_grid)
