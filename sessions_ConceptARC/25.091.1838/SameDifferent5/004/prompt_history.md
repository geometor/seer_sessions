
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 3 3 3 0 0 0
0 2 4 2 0 3 1 3 0 0 0
0 2 2 2 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 7 7 7
0 0 0 6 4 6 0 0 7 8 7
0 0 0 6 6 6 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 4 4 4 4 0
0 3 3 3 3 0 0 0 0 4 5 5 4 0
0 3 2 2 3 0 0 0 0 4 5 5 4 0
0 3 2 2 3 0 0 0 0 4 4 4 4 0
0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 0 8 7 7 8 0 0 0
0 0 0 0 0 0 0 8 7 7 8 0 0 0
0 0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 9 9 9 9 0 0 0 0 0 0 0 0
0 0 9 4 4 9 0 0 1 1 1 1 0 0
0 0 9 4 4 9 0 0 1 2 2 1 0 0
0 0 9 9 9 9 0 0 1 2 2 1 0 0
0 0 0 0 0 0 0 0 1 1 1 1 0 0
```


**output:**
```
2
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 3 7 3 0 0 5 5 5 0
0 3 7 3 0 0 5 7 5 0
0 3 3 3 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 4 4 3 0 0 0 0
0 0 3 3 3 3 0 0 0 0
```


**output:**
```
7
```

*   **Perception:** The task takes an input grid containing multiple distinct shapes, often resembling squares or rectangles, composed of non-white colors. Each shape typically has an outer "frame" of one color and an inner "center" area of another color. The output is a single color value (represented as a 1x1 grid). The relationship between the input and output appears to involve identifying a property common to multiple shapes within the input grid. Specifically, the output color corresponds to the color that appears most frequently as the "center" color within the identified shapes.

*   **Facts:**
    
```yaml
    task_type: property_identification
    input_features:
      - grid: 2D array of integers (colors)
      - background_color: white (0)
      - objects:
          - definition: Contiguous regions of non-white pixels, often forming a closed frame around a different non-white color.
          - properties:
              - frame_color: The color forming the outer boundary of the object.
              - center_color: The color enclosed within the frame. Multiple pixels of the same center color might exist.
    output_features:
      - grid: 1x1 array containing a single integer (color)
      - derivation: Represents the most frequently occurring 'center_color' among all identified objects in the input grid.
    relationship: Count the occurrences of each unique 'center_color' across all objects. The output color is the 'center_color' with the highest count.
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to identify distinct objects. An object consists of a contiguous block of non-white pixels where an outer frame of one color encloses an inner area (center) of a different non-white color. Ignore the white background pixels.
    2.  For each identified object, determine the color of the pixels forming the inner center.
    3.  Create a list of all center colors found across all objects.
    4.  Count the frequency of each unique color in the list of center colors.
    5.  Identify the color that has the highest frequency count.
    6.  The output is this most frequent center color.
```python
import numpy as np
from collections import Counter

"""
Identify distinct objects in the input grid. An object is defined by a center 
pixel (or pixels) of one color completely surrounded (8 neighbors) by pixels 
of a single, different, non-white color (the frame color). Count the occurrences 
of each unique center color found across all such objects. The output is a 1x1 
grid containing the center color that occurs most frequently. In case of a tie 
in frequency, the color with the highest numerical value is chosen.
"""

def find_center_colors(input_grid):
    """
    Finds all pixels that act as a center of a framed object.
    A center pixel is a non-white pixel surrounded on all 8 sides
    by pixels of the same, different, non-white color.

    Args:
        input_grid (np.array): The input grid.

    Returns:
        list: A list of center colors found.
    """
    center_colors = []
    height, width = input_grid.shape

    # Iterate through pixels that can potentially be centers (not on the border)
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            center_color = input_grid[r, c]

            # Skip white pixels
            if center_color == 0:
                continue

            # Get the 8 neighbors
            neighbors = [
                input_grid[r - 1, c - 1], input_grid[r - 1, c], input_grid[r - 1, c + 1],
                input_grid[r, c - 1],                         input_grid[r, c + 1],
                input_grid[r + 1, c - 1], input_grid[r + 1, c], input_grid[r + 1, c + 1]
            ]

            # Check if all neighbors are the same, non-white color
            first_neighbor_color = neighbors[0]
            if first_neighbor_color == 0:  # Frame cannot be white
                continue

            all_same_frame = True
            for neighbor_color in neighbors:
                if neighbor_color != first_neighbor_color:
                    all_same_frame = False
                    break
            
            # Check if the frame color is different from the center color
            if all_same_frame and first_neighbor_color != center_color:
                # This pixel is a center pixel
                center_colors.append(center_color)
                
    return center_colors

def transform(input_grid):
    """
    Transforms the input grid based on the identified rule.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 1x1 numpy array representing the output grid.
    """
    # Find all center colors in the input grid
    center_colors = find_center_colors(input_grid)

    # Handle the case where no center colors are found (though unlikely based on examples)
    if not center_colors:
        # Default behavior might need refinement based on more examples or ARC rules.
        # Returning white as a placeholder.
        return np.array([[0]], dtype=int) 

    # Count the frequency of each center color
    color_counts = Counter(center_colors)

    # Find the maximum frequency
    max_freq = 0
    if color_counts:
         max_freq = max(color_counts.values())

    # Find all colors with the maximum frequency (handle ties)
    most_frequent_colors = [color for color, count in color_counts.items() if count == max_freq]

    # Select the color with the highest numerical value in case of a tie
    output_color = 0 # Default to white if list is somehow empty
    if most_frequent_colors:
        output_color = max(most_frequent_colors)

    # Create the 1x1 output grid
    output_grid = np.array([[output_color]], dtype=int)

    return output_grid
```
```python
import numpy as np
from collections import Counter, deque

"""
Identify distinct contiguous non-white regions (blobs) in the input grid. 
For each blob, determine if it consists of exactly two non-white colors where 
one color (the center color) is topologically enclosed by the other color (the 
frame color). A color is considered enclosed if all its pixels within the blob 
only have neighbors (8-connectivity) that are either the background color (0), 
the frame color, or the center color itself. Collect all identified center 
colors from all such valid frame/center blobs. The final output is a 1x1 grid 
containing the center color that appears most frequently across all identified 
blobs. If there is a tie in frequency, the color with the highest numerical 
value is chosen.
"""

def get_neighbors(r, c, height, width, connectivity=8):
    """
    Gets valid neighbor coordinates for a given pixel.

    Args:
        r (int): Row index of the pixel.
        c (int): Column index of the pixel.
        height (int): Grid height.
        width (int): Grid width.
        connectivity (int): 4 or 8 for neighbor connectivity.

    Returns:
        list: A list of (row, col) tuples for valid neighbors.
    """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue # Skip self
            if connectivity == 4 and abs(dr) + abs(dc) != 1: continue # Skip diagonals for 4-connectivity
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_blobs(grid):
    """
    Finds all distinct contiguous regions (blobs) of non-white pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list where each element is a list of (row, col) tuples 
              representing the coordinates of a single blob.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    blobs = []

    for r in range(height):
        for c in range(width):
            # Start BFS from a non-white, unvisited pixel
            if grid[r, c] != 0 and not visited[r, c]:
                current_blob_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_blob_coords.append((curr_r, curr_c))
                    
                    # Explore neighbors (using 8-connectivity for blob definition)
                    for nr, nc in get_neighbors(curr_r, curr_c, height, width, connectivity=8):
                        if grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if current_blob_coords:
                     blobs.append(current_blob_coords)
    return blobs

def analyze_blob_for_center(blob_coords, grid):
    """
    Analyzes a blob to find if it has a frame/center structure and returns the center color.

    Args:
        blob_coords (list): List of (row, col) tuples for the blob pixels.
        grid (np.array): The input grid.

    Returns:
        int or None: The center color if found, otherwise None.
    """
    if not blob_coords:
        return None

    height, width = grid.shape
    blob_colors = set()
    pixel_map = {} # color -> list of coords
    
    # Collect colors and their pixel locations within the blob
    for r, c in blob_coords:
        color = grid[r, c]
        if color != 0: # Ignore background if somehow included (shouldn't happen with find_blobs)
            blob_colors.add(color)
            if color not in pixel_map:
                pixel_map[color] = []
            pixel_map[color].append((r,c))

    # A valid frame/center blob must have exactly two non-white colors
    non_white_colors = list(blob_colors)
    if len(non_white_colors) != 2:
        return None 

    c1, c2 = non_white_colors[0], non_white_colors[1]
    c1_pixels = pixel_map[c1]
    c2_pixels = pixel_map[c2]
    
    # Helper to check if a color is enclosed by the other within the blob context
    def is_topologically_enclosed(center_candidate_pixels, center_candidate_color, frame_candidate_color):
        for r, c in center_candidate_pixels:
            # Check all 8 neighbors
            for nr, nc in get_neighbors(r, c, height, width, connectivity=8):
                neighbor_color = grid[nr, nc]
                # A neighbor is invalid if it's NOT background, NOT the center color itself, and NOT the frame color
                if neighbor_color != 0 and neighbor_color != center_candidate_color and neighbor_color != frame_candidate_color:
                    return False # Found a neighbor that breaks the enclosure rule
        return True # All neighbors of all center pixels are valid

    # Check if c1 is enclosed by c2
    c1_is_center = is_topologically_enclosed(c1_pixels, c1, c2)
    # Check if c2 is enclosed by c1
    c2_is_center = is_topologically_enclosed(c2_pixels, c2, c1)

    # Return the center color if exactly one color is enclosed by the other
    if c1_is_center and not c2_is_center:
        return c1 
    elif c2_is_center and not c1_is_center:
        return c2
    else:
        # Ambiguous or invalid structure (e.g., adjacent, neither enclosed, or both somehow seem enclosed)
        return None


def transform(input_grid):
    """
    Transforms the input grid by finding frame/center objects, identifying 
    their center colors, and returning the most frequent center color.

    Args:
        input_grid (np.array): The 2D input grid.

    Returns:
        np.array: A 1x1 grid containing the most frequent center color.
    """
    
    # Step 1: Find all distinct non-white blobs
    blobs = find_blobs(input_grid)
    
    # Step 2: Analyze each blob to identify center colors
    center_colors_found = []
    for blob_coords in blobs:
        center_color = analyze_blob_for_center(blob_coords, input_grid)
        if center_color is not None:
            center_colors_found.append(center_color)

    # Step 3: Count frequencies of center colors
    output_color = 0 # Default to white if no center colors found
    if center_colors_found:
        color_counts = Counter(center_colors_found)
        
        # Step 4: Find the maximum frequency
        max_freq = 0
        if color_counts: # Ensure counter is not empty
             max_freq = max(color_counts.values())

        # Step 5: Find all colors with the maximum frequency (handle ties)
        most_frequent_colors = [color for color, count in color_counts.items() if count == max_freq]

        # Step 6: Select the color with the highest numerical value in case of a tie
        if most_frequent_colors:
            output_color = max(most_frequent_colors)

    # Step 7: Create the 1x1 output grid
    output_grid = np.array([[output_color]], dtype=int)

    return output_grid
```
