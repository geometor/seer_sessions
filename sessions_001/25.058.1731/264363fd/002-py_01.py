"""
1.  **Identify Objects:** Find all colored rectangles and smaller colored shapes within the azure background.
2.  **Locate Point Reflection Centers:** Identify the pixel locations of the center of the crosses. and yellow pixels inside large rectangles.
3. **Point reflect objects:** Point reflect color of cross center in yellow pixel inside the larger rectangle. If there are two such yellow pixels, point reflect color of cross center with the center of the rectangle.
4. **Point reflect objects:** Reflect other single colored dots in the center of the cross, if the dot is inside the big rectangle.
5. Point reflect colors of the rectangle which includes the center cross in the other yellow dot, if the dot is outside the rectangle.
"""

import numpy as np

def find_objects(grid, background_color=8):
    """Finds contiguous objects of the same color, excluding the background."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)
        dfs(row+1, col+1, color, object_pixels)
        dfs(row+1, col-1, color, object_pixels)
        dfs(row-1, col+1, color, object_pixels)
        dfs(row-1, col-1, color, object_pixels)


    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != background_color:
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                if object_pixels:
                    objects.append(object_pixels)
    return objects

def find_center(object_pixels):
    """Calculates the center of a set of pixels."""
    rows = [p[0] for p in object_pixels]
    cols = [p[1] for p in object_pixels]
    if not rows or not cols:
      return None, None
    center_row = int(round(np.mean(rows)))
    center_col = int(round(np.mean(cols)))
    return center_row, center_col

def point_reflect(point, center):
    """Reflects a point across a center point."""
    return 2 * center[0] - point[0], 2 * center[1] - point[1]

def is_inside(point, rectangle_pixels):
    """ checks if the point is inside. """
    rows = [p[0] for p in rectangle_pixels]
    cols = [p[1] for p in rectangle_pixels]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row <= point[0] <= max_row and min_col <= point[1] <= max_col
    
def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # Find crosses and rectangles
    crosses = []
    rectangles = []
    single_dots = []

    for obj in objects:
        center_row, center_col = find_center(obj)

        rows = [p[0] for p in obj]
        cols = [p[1] for p in obj]

        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)

        width = max_col - min_col + 1
        height = max_row - min_row + 1
            
        if len(obj) > 4 and width>2 and height>2:
            rectangles.append(obj)

        elif len(obj) > 1 and len(obj)<=9 : #cross object size
             crosses.append((obj,(center_row, center_col)))

        elif len(obj) == 1:
          single_dots.append(obj[0])



    # Perform reflections
    for cross_obj, cross_center in crosses:
        cross_color = input_grid[cross_center]
        
        rect_cont_cross = None
        for rect in rectangles:
            if is_inside(cross_center,rect):
               rect_cont_cross = rect
               break

        yellow_dots_inside = [dot for dot in single_dots if input_grid[dot]==4 and is_inside(dot,rect_cont_cross)  ]
        yellow_dots_outside = [dot for dot in single_dots if input_grid[dot] == 4 and not is_inside(dot, rect_cont_cross)]
        #Point reflect objects
        if len(yellow_dots_inside)>0:
             reflected_color_point = point_reflect(cross_center, yellow_dots_inside[0])
             if 0 <= reflected_color_point[0] < output_grid.shape[0] and 0 <= reflected_color_point[1] < output_grid.shape[1]:
                   output_grid[reflected_color_point] = cross_color

        #Point reflect objects: single dots
        for dot in single_dots:
           if is_inside(dot,rect_cont_cross):
               reflected_dot = point_reflect(dot,cross_center)
               if 0 <= reflected_dot[0] < output_grid.shape[0] and 0 <= reflected_dot[1] < output_grid.shape[1]:
                    output_grid[reflected_dot] = input_grid[dot]
        
        if len(yellow_dots_outside)>0:
            reflected_color_rect = point_reflect(find_center(rect_cont_cross),yellow_dots_outside[0] )
            for point in rect_cont_cross:
               reflected_point = point_reflect(point, yellow_dots_outside[0])
               if 0 <= reflected_point[0] < output_grid.shape[0] and 0 <= reflected_point[1] < output_grid.shape[1]:
                  output_grid[reflected_point]= input_grid[point]

    return output_grid