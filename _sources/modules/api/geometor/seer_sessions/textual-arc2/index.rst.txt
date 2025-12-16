geometor.seer_sessions.textual-arc2
===================================

.. py:module:: geometor.seer_sessions.textual-arc2

.. autoapi-nested-parse::

   Filename: textual_arc_grid_with_lines.py
   Description: A Textual app that displays ARC-style colored grids with grid lines separating the cells.
   It demonstrates several rendering methods (image-based, Unicode block, and half-block) with grid lines.



Attributes
----------

.. autoapisummary::

   geometor.seer_sessions.textual-arc2.GRID_LINE_COLOR
   geometor.seer_sessions.textual-arc2.GRID_LINE_WIDTH
   geometor.seer_sessions.textual-arc2.COLOR_PALETTE
   geometor.seer_sessions.textual-arc2.GRID_DATA
   geometor.seer_sessions.textual-arc2.app


Classes
-------

.. autoapisummary::

   geometor.seer_sessions.textual-arc2.BaseGrid
   geometor.seer_sessions.textual-arc2.ImageGrid
   geometor.seer_sessions.textual-arc2.UnicodeBlockGrid
   geometor.seer_sessions.textual-arc2.SplitBlockGrid
   geometor.seer_sessions.textual-arc2.BoxDrawingGrid
   geometor.seer_sessions.textual-arc2.SquareCharGrid
   geometor.seer_sessions.textual-arc2.HalfBlockGrid
   geometor.seer_sessions.textual-arc2.ARCGridApp


Module Contents
---------------

.. py:data:: GRID_LINE_COLOR
   :value: 'black'


.. py:data:: GRID_LINE_WIDTH
   :value: 1


.. py:data:: COLOR_PALETTE

.. py:data:: GRID_DATA
   :value: [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 2, 2, 2, 2, 2, 2, 2, 2, 1], [1, 2, 3, 3, 3, 3, 3, 3, 2, 1],...


.. py:class:: BaseGrid(grid, **kwargs)

   Bases: :py:obj:`textual.widgets.Static`


   Base widget class for rendering the colored grid.


   .. py:attribute:: grid


   .. py:attribute:: rows


   .. py:attribute:: cols


.. py:class:: ImageGrid(grid, **kwargs)

   Bases: :py:obj:`BaseGrid`


   Grid rendered using an image-based approach via rich-pixels.
   This mode creates a PIL image with grid lines separating the cells.


   .. py:method:: on_mount()


   .. py:method:: on_resize(event)

      Regenerate the image on resize so that cell sizes scale with available space.



.. py:class:: UnicodeBlockGrid(grid, **kwargs)

   Bases: :py:obj:`BaseGrid`


   Grid rendered using colored Unicode blocks.
   This version inserts extra spaces with background styling to simulate grid lines.


   .. py:method:: render()

      Get a rich renderable for the widget's content.

      :returns: A rich renderable.



.. py:class:: SplitBlockGrid(grid, **kwargs)

   Bases: :py:obj:`BaseGrid`


   New Unicode rendering mode.

   For each grid cell, render:
     • A full block ("█") with the cell's fill color.
     • A vertical split block ("▌") styled with foreground = fill color and background = grid line color.

   This results in two characters per cell that show the cell color and a vertical separator.


   .. py:method:: render()

      Get a rich renderable for the widget's content.

      :returns: A rich renderable.



.. py:class:: BoxDrawingGrid(grid, **kwargs)

   Bases: :py:obj:`BaseGrid`


   A grid rendered with box-drawing characters to show horizontal and vertical lines clearly.
   Each cell is rendered as a box of text with a colored background.


   .. py:method:: render()

      Get a rich renderable for the widget's content.

      :returns: A rich renderable.



.. py:class:: SquareCharGrid(grid, **kwargs)

   Bases: :py:obj:`BaseGrid`


   Renders each grid cell as a single Unicode square character (default: '■'),
   styled with the cell's fill color.

   You can switch the character to something else (e.g. '⬛', '◼', '▣') if desired.


   .. py:attribute:: SQUARE_CHAR
      :value: '■'



   .. py:method:: render()

      Get a rich renderable for the widget's content.

      :returns: A rich renderable.



.. py:class:: HalfBlockGrid(grid, **kwargs)

   Bases: :py:obj:`BaseGrid`


   Grid rendered using half-block characters (▀) to combine two rows.
   This version also adds grid lines.


   .. py:method:: render()

      Get a rich renderable for the widget's content.

      :returns: A rich renderable.



.. py:class:: ARCGridApp(driver_class: Type[textual.driver.Driver] | None = None, css_path: textual._path.CSSPathType | None = None, watch_css: bool = False, ansi_color: bool = False)

   Bases: :py:obj:`textual.app.App`


   The base class for Textual Applications.


   .. py:attribute:: CSS
      :value: Multiline-String

      .. raw:: html

         <details><summary>Show Value</summary>

      .. code-block:: python

         """
             Screen {
                 align: center middle;
             }
             """

      .. raw:: html

         </details>



      Inline CSS, useful for quick scripts. This is loaded after CSS_PATH,
      and therefore takes priority in the event of a specificity clash.


   .. py:method:: compose() -> textual.app.ComposeResult

      Yield child widgets for a container.

      This method should be implemented in a subclass.



   .. py:method:: on_button_pressed(event: textual.widgets.Button.Pressed) -> None

      Switch the active rendering mode based on button presses.



.. py:data:: app

