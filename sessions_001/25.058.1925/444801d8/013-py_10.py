import numpy as np

def get_objects(grid, color):
    """
    Find connected regions of a specific color.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))

        return region

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                objects.append(dfs(row, col))
    return objects

def get_outline(grid, object_pixels):
    """
    Find the outline pixels of an object.
    """
    outline = set()
    for row, col in object_pixels:
        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for n_row, n_col in neighbors:
            if 0 <= n_row < grid.shape[0] and 0 <= n_col < grid.shape[1] and grid[n_row, n_col] != 1:
                outline.add((n_row, n_col))
    return list(outline)

def transform(input_grid, example_index):
    # Initialize output grid with the same dimensions and background color
    output_grid = np.copy(input_grid)
    print(f"Example {example_index}:")

    # Find blue objects
    blue_objects = get_objects(input_grid, 1)

    # Sort blue objects by topmost row coordinate
    blue_objects.sort(key=lambda obj: min(pixel[0] for pixel in obj))

    # Get outlines
    outlines = []
    for obj in blue_objects:
        outlines.append(get_outline(input_grid,obj))

    # added background detection
    # Find the most frequent color
    colors, counts = np.unique(input_grid, return_counts=True)
    background_color_index = np.argmax(counts)
    background_color = colors[background_color_index]   

    print(f"  Detected background color: {background_color}")
    print(f"  Number of blue objects: {len(blue_objects)}")

    if len(blue_objects) >= 1:
        # Topmost blue object: replace outline with red (2) if original is not blue (1) or background (0)
        top_outline = outlines[0]
        print(f"  Top object outline size: {len(top_outline)}")
        for row, col in top_outline:
            if  input_grid[row, col] !=background_color :
                output_grid[row,col] = 2

    if len(blue_objects) >= 2:
        # Bottommost blue object, replace outline with Green (3)
        bottom_outline = outlines[-1]
        print(f"  Bottom object outline size: {len(bottom_outline)}")

        for row, col in bottom_outline:
            if input_grid[row, col] !=background_color :
                # check for overlap
                skip = False
                for top_row, top_col in top_outline:
                    if (row,col) == (top_row, top_col):
                        skip = True
                if not skip: 
                    output_grid[row, col] = 3


    return output_grid


# Example Usage (replace with your actual training data)
training_examples = [
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 1, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 2, 1, 2, 0, 0, 0],
              [0, 0, 0, 2, 1, 2, 0, 0, 0],
              [0, 0, 0, 2, 1, 2, 0, 0, 0],
              [0, 0, 0, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]])),

    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 1, 1, 1, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 2, 1, 2, 0, 0, 0],
              [0, 0, 0, 2, 1, 2, 0, 0, 0],
              [0, 0, 0, 2, 1, 2, 0, 0, 0],
              [0, 0, 0, 2, 1, 2, 0, 0, 0],
              [0, 0, 0, 3, 1, 3, 0, 0, 0],
              [0, 0, 0, 0, 3, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]])),

    (np.array([[7, 7, 7, 7, 7, 7, 7, 7, 7],
              [7, 7, 7, 7, 7, 7, 7, 7, 7],
              [7, 7, 7, 7, 7, 7, 7, 7, 7],
              [7, 7, 7, 7, 7, 7, 7, 7, 7],
              [7, 7, 7, 7, 1, 7, 7, 7, 7],
              [7, 7, 7, 1, 1, 1, 7, 7, 7],
              [7, 7, 7, 7, 1, 7, 7, 7, 7],
              [7, 7, 7, 7, 7, 7, 7, 7, 7],
              [7, 7, 7, 7, 7, 7, 7, 7, 7]]),
     np.array([[7, 7, 7, 7, 7, 7, 7, 7, 7],
              [7, 7, 7, 7, 2, 7, 7, 7, 7],
              [7, 7, 7, 2, 1, 2, 7, 7, 7],
              [7, 7, 7, 2, 1, 2, 7, 7, 7],
              [7, 7, 7, 2, 1, 2, 7, 7, 7],
              [7, 7, 7, 2, 1, 2, 7, 7, 7],
              [7, 7, 7, 3, 1, 3, 7, 7, 7],
              [7, 7, 7, 0, 3, 0, 7, 7, 7],
              [7, 7, 7, 7, 7, 7, 7, 7, 7]])),
    (np.array([[8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 1, 8, 8],
                [8, 8, 8, 8, 8, 1, 8, 8],
                [8, 8, 8, 8, 8, 1, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 1, 8, 8, 8, 8, 8],
                [8, 8, 1, 8, 8, 8, 8, 8],
                [8, 8, 1, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8]]),
     np.array([[8, 8, 8, 8, 8, 2, 8, 8],
                [8, 8, 8, 8, 8, 1, 8, 8],
                [8, 8, 8, 8, 8, 1, 8, 8],
                [8, 8, 8, 8, 8, 1, 8, 8],
                [8, 8, 8, 8, 8, 3, 8, 8],
                [8, 8, 1, 8, 8, 8, 8, 8],
                [8, 8, 1, 8, 8, 8, 8, 8],
                [8, 8, 1, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8]]))
]

for i, (input_grid, expected_output) in enumerate(training_examples):
    predicted_output = transform(input_grid, i + 1)
    print(f"equal: {np.array_equal(expected_output,predicted_output)}")