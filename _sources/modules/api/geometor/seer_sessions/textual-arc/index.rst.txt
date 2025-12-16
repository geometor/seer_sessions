geometor.seer_sessions.textual-arc
==================================

.. py:module:: geometor.seer_sessions.textual-arc


Attributes
----------

.. autoapisummary::

   geometor.seer_sessions.textual-arc.COLOR_PALETTE
   geometor.seer_sessions.textual-arc.GRID_DATA
   geometor.seer_sessions.textual-arc.app


Classes
-------

.. autoapisummary::

   geometor.seer_sessions.textual-arc.BaseGrid
   geometor.seer_sessions.textual-arc.ImageGrid
   geometor.seer_sessions.textual-arc.UnicodeBlockGrid
   geometor.seer_sessions.textual-arc.HalfBlockGrid
   geometor.seer_sessions.textual-arc.ARCGridApp


Module Contents
---------------

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


   Grid rendered using an image-based approach via rich-pixels (requires PIL and rich-pixels).


   .. py:method:: on_mount()


   .. py:method:: on_resize(event)

      Regenerate the image when the widget is resized to adjust scaling.



.. py:class:: UnicodeBlockGrid(grid, **kwargs)

   Bases: :py:obj:`BaseGrid`


   Grid rendered using colored Unicode blocks (using colored spaces or block characters).


   .. py:method:: render()

      Get a rich renderable for the widget's content.

      :returns: A rich renderable.



.. py:class:: HalfBlockGrid(grid, **kwargs)

   Bases: :py:obj:`BaseGrid`


   Grid rendered by combining two rows into one using half-block characters.


   .. py:method:: render()

      Get a rich renderable for the widget's content.

      :returns: A rich renderable.



.. py:class:: ARCGridApp(driver_class: Type[textual.driver.Driver] | None = None, css_path: textual._path.CSSPathType | None = None, watch_css: bool = False, ansi_color: bool = False)

   Bases: :py:obj:`textual.app.App`


   Textual Application to display the ARC-style grid with switchable rendering modes.


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

      Callback when a mode switch button is pressed.



.. py:data:: app

