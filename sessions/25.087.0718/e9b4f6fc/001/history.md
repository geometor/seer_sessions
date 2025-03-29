
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 0 0 0
0 0 0 0 8 8 4 8 8 8 0 0 0
0 0 0 0 8 4 4 4 8 8 0 0 0
0 0 0 0 8 3 4 3 8 8 0 0 0
0 0 0 0 8 3 3 3 8 8 0 0 0
0 0 0 0 8 8 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8 8 8 8 8 8
8 8 1 8 8 8
8 1 1 1 8 8
8 2 1 2 8 8
8 2 2 2 8 8
8 8 8 8 8 8
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 0 4 5 0 0
0 3 5 5 5 5 3 3 0 0 0 0 0
0 3 3 1 1 5 3 3 0 0 0 0 0
0 3 8 1 1 3 3 3 0 0 0 0 0
0 3 8 8 8 8 3 3 0 0 0 0 0
0 3 3 3 3 3 3 3 0 0 0 0 0
0 3 3 3 3 3 3 3 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3
3 4 4 4 4 3 3
3 3 2 2 4 3 3
3 6 2 2 3 3 3
3 6 6 6 6 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0
0 0 8 8 2 4 8 8 8 0 0 0 0
0 0 8 2 2 4 4 4 8 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8 8 8 8 8 8 8
8 8 3 1 8 8 8
8 3 3 1 1 1 8
8 8 8 8 8 8 8
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 4 1 0 0 0 0 0 0 0 0
0 8 8 4 1 0 0 0 0 0 0 0 0
0 8 8 1 1 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 2 2 1
3 3 2 1
3 3 1 1
1 1 1 1
```

*   **Perception:** The input grids contain multiple distinct objects (contiguous blocks of non-white color) scattered on a white background. One specific object in each input appears to be the target for transformation. This target object is characterized by having a solid, single-color border enclosing an inner pattern. The other objects in the input are ignored. The output grid is a cropped version of the input, containing only the target object. The colors within the interior of the target object are transformed based on a rule that depends on the color of the object's border. The border color itself remains unchanged in the output.

*   **Facts:**
    
```yaml
    task_elements:
      - Input Grid: Contains multiple distinct objects on a white background.
      - Output Grid: Contains a single object derived from the input.
      - Objects: Contiguous areas of non-white pixels.
      - Target Object: A specific object in the input characterized by a uniform, single-pixel-thick (or thicker) border enclosing an interior region.
      - Border: The outermost layer of pixels of the target object, having a single, uniform color (Border Color).
      - Interior: The pixels enclosed by the border within the target object.
      - Ignored Objects: All objects in the input grid other than the target object.
    properties:
      - Target object has a unique Border Color (BC).
      - Target object has an interior pattern potentially containing multiple colors.
      - Output grid dimensions match the bounding box of the target object.
    actions:
      - Identify the target object with a uniform border.
      - Extract the target object (including border and interior).
      - Determine the Border Color (BC).
      - Transform the colors of the interior pixels based on the Border Color (BC).
      - Keep the border pixels' color unchanged.
    relationships:
      - The output is a transformed version of the target object from the input.
      - The color transformation rule for the interior depends solely on the Border Color (BC) of the target object.
      - Specific color mappings observed:
        - If BC=Azure(8): Red(2)<->Green(3), Blue(1)<->Yellow(4).
        - If BC=Green(3): Blue(1)->Red(2), Gray(5)->Yellow(4), Azure(8)->Magenta(6).
        - If BC=Blue(1): Yellow(4)->Red(2), Azure(8)->Green(3).
        - Other interior colors, including pixels matching BC but inside the border, remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct objects (contiguous non-white areas) in the input grid.
    2.  Find the unique object that possesses a solid, uniform-colored border completely enclosing an interior area. This is the "target object". Determine its "Border Color" (BC).
    3.  Determine the bounding box of the target object. The output grid will have the dimensions of this bounding box.
    4.  Create the output grid by copying the target object (border and interior) into it.
    5.  Iterate through each pixel location within the bounding box of the target object in the output grid.
    6.  For each pixel, check if it belongs to the interior of the target object (i.e., it is not part of the uniform-colored border).
    7.  If the pixel is part of the interior:
        a.  Get its original color (OC) from the corresponding position in the input grid's target object.
        b.  Apply a color transformation based on the Border Color (BC):
            i.  If BC is Azure (8): Swap Red (2) with Green (3), and swap Blue (1) with Yellow (4). (If OC is 2, change to 3; if 3, change to 2; if 1, change to 4; if 4, change to 1).
            ii. If BC is Green (3): Change Blue (1) to Red (2); change Gray (5) to Yellow (4); change Azure (8) to Magenta (6).
            iii.If BC is Blue (1): Change Yellow (4) to Red (2); change Azure (8) to Green (3).
            iv. If the original color (OC) is not involved in the transformations defined for the specific BC, or if OC is the same as BC, leave the pixel's color unchanged (it remains OC).
    8.  If the pixel is part of the border (its color is BC and it forms the enclosing border), leave its color unchanged (it remains BC).
    9.  The resulting grid is the final output.
