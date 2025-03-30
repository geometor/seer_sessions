import numpy as np
from scipy.ndimage import label, generate_binary_structure

"""
This transformation identifies distinct connected objects of green pixels (value 3)
in the input grid using 8-way adjacency. If two or more such objects exist,
it draws straight lines (using Bresenham's algorithm) between every pair of 
pixels (p1, p2) where p1 belongs to one object and p2 belongs to a different 
object. All pixels lying on these lines are colored green in the output grid. 
The original green pixels are preserved. If there are zero or one green objects 
in the input, the output grid is identical to the input grid.

Note: This rule is derived primarily from examples train_1 and train_3. 
Example train_2, which contains only one object, exhibits a different output 
pattern not fully explained by this rule. This implementation follows the 
rule derived from the multi-object examples.
"""

def bresenham_line(r0, c0, r1, c1):
    """
    Generates pixel coordinates for a line segment between (r0, c0) and (r1, c1)
    using Bresenham's line algorithm.
    
    Args:
        r0, c0: Coordinates of the starting point.
        r1, c1: Coordinates of the ending point.
        
    Returns:
        A list of (row, col) tuples representing the pixels on the line segment.
    """
    points = []
    dr = abs(r1 - r0)
    dc = abs(c1 - c0)
    # Determine step direction
    sr = 1 if r0 < r1 else -1
    sc = 1 if c0 < c1 else -1
    # Initialize error term
    err = dr - dc

    # Current position starts at (r0, c0)
    cr, cc = r0, c0 

    while True:
        points.append((cr, cc))
        # Stop when the end point is reached
        if cr == r1 and cc == c1:
            break
        
        # Calculate error adjustments for next step
        e2 = 2 * err
        if e2 > -dc: # Check if step in row direction is needed
            err -= dc
            cr += sr
        if e2 < dr:  # Check if step in column direction is needed
            err += dr
            cc += sc
            
    return points

def find_objects(grid, target_color):
    """
    Identifies connected components (objects) of a specified color in a grid.
    Uses 8-way connectivity (pixels touching sides or corners are connected).
    
    Args:
        grid: The input numpy array grid.
        target_color: The integer color value to find objects of.
        
    Returns:
        A list of sets. Each set contains the (row, col) tuples of pixels 
        belonging to one distinct connected object. Returns an empty list if
        no objects are found.
    """
    # Create a binary mask where target_color pixels are True
    binary_grid = (grid == target_color)
    
    # Define the connectivity structure (8-way)
    # [[True, True, True],
    #  [True, True, True],
    #  [True, True, True]]
    structure = generate_binary_structure(rank=2, connectivity=2) 
    
    # Label the connected components in the binary grid
    # labeled_grid assigns a unique integer ID (starting from 1) to each component
    # num_labels is the total number of components found
    labeled_grid, num_labels = label(binary_grid, structure=structure)
    
    objects = []
    if num_labels > 0:
        # Extract the coordinates for each labeled component
        # np.argwhere returns an array of [row, col] pairs for each label
        # We iterate from label 1 up to num_labels
        object_coords = [np.argwhere(labeled_grid == i) for i in range(1, num_labels + 1)]
        
        # Convert the coordinates for each object into a set of (row, col) tuples
        objects = [set(map(tuple, coords)) for coords in object_coords]
        
    return objects

def transform(input_grid):
    """
    Applies the transformation rule: finds green objects and draws lines between
    pixels of different objects if multiple objects exist.
    
    Args:
        input_grid: A numpy array representing the input grid.
        
    Returns:
        A numpy array representing the output grid after applying the transformation.
    """
    
    # Define the color of interest
    green_color = 3
    
    # Find all distinct connected green objects
    objects = find_objects(input_grid, green_color)
    num_objects = len(objects)
    
    # Initialize the output grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # --- Transformation Logic ---
    
    # Only proceed if there are 2 or more objects
    if num_objects >= 2:
        
        # Iterate through all unique pairs of distinct objects
        # Example: If objects are [O1, O2, O3], pairs are (O1, O2), (O1, O3), (O2, O3)
        for i in range(num_objects):
            for j in range(i + 1, num_objects):
                # Get the sets of pixels for the two objects in the current pair
                object1_pixels = objects[i]
                object2_pixels = objects[j]
                
                # Iterate through every pixel p1 in the first object
                for p1 in object1_pixels:
                    # Iterate through every pixel p2 in the second object
                    for p2 in object2_pixels:
                        # Get coordinates for the pair of pixels
                        r1, c1 = p1
                        r2, c2 = p2
                        
                        # Calculate the pixels forming the line segment between p1 and p2
                        line_pixels = bresenham_line(r1, c1, r2, c2)
                        
                        # Color each pixel on the calculated line segment green
                        for r, c in line_pixels:
                            # Ensure coordinates are within grid bounds (safety check)
                            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                                output_grid[r, c] = green_color
                                
    # If num_objects is 0 or 1, no lines are drawn between objects,
    # so the output_grid remains the initial copy of input_grid.
    
    return output_grid