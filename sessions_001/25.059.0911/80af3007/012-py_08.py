"""
1.  **Identify Gray Objects:** Examine the input grid and identify the three distinct gray (color 5) objects.  There are three shape types: a "cross" shape, a "T" shape, and an "I" shape.

2.  **Determine Vertical Order:** Sort the three gray objects based on their vertical position in the input grid. The object that appears *lowest* in the input grid will be considered the "middle" object. The object appearing highest is the "top" object.

3.  **Create Output Grid:** Create a 9x9 output grid filled with black (color 0).

4.  **Replicate and Arrange:** Replicate the objects based on the "middle object", placing the copies in the following positions on the 9x9 grid. The layout is always this grid:
