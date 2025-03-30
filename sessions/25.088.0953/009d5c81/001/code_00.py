import numpy as np

# Define color constants
WHITE = 0
BLUE = 1
RED = 2
GREEN = 3
# YELLOW = 4 # Not used in this logic
# GRAY = 5 # Not used in this logic
# MAGENTA = 6 # Not used in this logic
ORANGE = 7
AZURE = 8
# MAROON = 9 # Not used in this logic

# Define the canonical shapes found in the examples, represented by 1s on a 0 background
# Shape 1 ('+') maps to Red (2)
PLUS_SHAPE = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
], dtype=np.uint8)

# Shape 2 ('Weird Cross') maps to Green (3)
# Found in examples 2 and 5
WEIRD_CROSS_SHAPE = np.array([
    [1, 0, 1],
    [0, 1, 0],
    [1, 1, 1]
], dtype=np.uint8)

# Shape 3 ('Weird L') maps to Orange (7)
# Found in example 4
WEIRD_L_SHAPE = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [0, 1, 0]
], dtype=np.uint8)

def _find_pixels(grid, color):
    """Finds the coordinates of all pixels of a given color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None # No pixels of this color found
    return list(zip(rows, cols))

def _extract_shape_pattern(grid, color):
    """
    Extracts the pattern of a given color as a minimal bounding box grid.
    The pattern is represented by 1s on a background of 0s.
    Returns the pattern grid (numpy array) or None if no pixels of the color are found.
    """
    # Find all coordinates of the specified color
    coords = _find_pixels(grid, color)
    if not coords:
        return None # No pattern found

    # Determine the bounding box of the pattern
    rows, cols = zip(*coords)
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    # Calculate the dimensions of the minimal grid containing the pattern
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Create an empty grid (filled with 0s) for the pattern
    pattern_grid = np.zeros((height, width), dtype=np.uint8)

    # Populate the pattern grid with 1s at the relative coordinates of the colored pixels
    for r, c in coords:
        relative_r = r - min_r
        relative_c = c - min_c
        pattern_grid[relative_r, relative_c] = 1 # Use 1 to represent the shape

    return pattern_grid


def _get_target_color_from_shape(blue_shape_pattern):
    """
    Determines the target color (Red, Green, or Orange) based on the
    provided blue shape pattern grid.
    Raises ValueError if the shape is not recognized or not found.
    """
    if blue_shape_pattern is None:
        raise ValueError("No blue shape pattern found in the input grid.")

    # Compare the extracted shape with the known canonical shapes
    if blue_shape_pattern.shape == PLUS_SHAPE.shape and np.array_equal(blue_shape_pattern, PLUS_SHAPE):
        return RED
    elif blue_shape_pattern.shape == WEIRD_CROSS_SHAPE.shape and np.array_equal(blue_shape_pattern, WEIRD_CROSS_SHAPE):
        return GREEN
    elif blue_shape_pattern.shape == WEIRD_L_SHAPE.shape and np.array_equal(blue_shape_pattern, WEIRD_L_SHAPE):
        return ORANGE
    else:
        # This case should ideally not happen with valid ARC task inputs following the observed pattern
        raise ValueError(f"Unknown blue shape pattern encountered:\n{blue_shape_pattern}")


def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Identifies a pattern of blue (1) pixels.
    2. Determines the specific shape of the blue pattern by comparing it to known templates ('+', 'Weird Cross', 'Weird L').
    3. Maps the identified blue shape to a target color: '+' maps to Red(2), 'Weird Cross' maps to Green(3), 'Weird L' maps to Orange(7).
    4. Creates an output grid by:
       a. Replacing all azure (8) pixels in the input grid with the determined target color.
       b. Replacing all blue (1) pixels in the input grid with the background color (white=0).
       c. Keeping all other pixels (background white=0) the same.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_array = np.array(input_grid, dtype=np.uint8)

    # --- Step 1 & 2: Identify blue shape ---
    # Extract the minimal grid containing the blue pattern, represented by 1s
    blue_shape_pattern = _extract_shape_pattern(input_array, BLUE)

    # --- Step 3: Map shape to target color ---
    # Determine the target color based on the identified blue shape
    # This will raise a ValueError if the shape is missing or not recognized
    target_color = _get_target_color_from_shape(blue_shape_pattern)

    # --- Step 4: Create output grid ---
    # Initialize output grid as a copy of the input
    output_array = input_array.copy()

    # 4a. Recolor Azure Pixels: Find all azure pixels and change them to the target color
    output_array[input_array == AZURE] = target_color

    # 4b. Remove Blue Pixels: Find all blue pixels and change them to the background color
    output_array[input_array == BLUE] = WHITE

    # 4c. Other pixels (white=0) remain unchanged as they were copied initially.

    # Convert the resulting numpy array back to a list of lists for the standard ARC output format
    output_grid = output_array.tolist()

    return output_grid