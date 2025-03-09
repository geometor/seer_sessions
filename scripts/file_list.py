import os
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Static
from rich.syntax import Syntax
from textual.screen import Screen
from textual import log


def get_py_files(folder):
    files = []
    for file in os.listdir(folder):
        if file.endswith(".py"):
            path = os.path.join(folder, file)
            size = os.path.getsize(path) / 1024  # KB
            with open(path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            files.append((file, f"{size:.2f}", lines))
    return files


class FileViewScreen(Screen):
    def __init__(self, filepath: str):
        super().__init__()
        self.filepath = filepath

    def compose(self) -> ComposeResult:
        #  with open(self.filepath, 'r', encoding='utf-8') as f:
            #  content = f.read()
        #  yield Syntax(content)
        syntax = Syntax.from_path(
            self.filepath,
            line_numbers=True,
            word_wrap=False,
            indent_guides=True,
        )
        yield Static(syntax)


class FileListApp(App):
    CSS = """
    DataTable {height: 100%;}
    Static {padding: 1;}
    """

    def compose(self) -> ComposeResult:
        self.table = DataTable()
        self.table.add_columns("Filename", "Size (KB)", "Lines of Code")
        yield self.table

    def on_mount(self):
        folder = "."  # current folder, change as needed
        self.file_info = get_py_files(folder)
        for file_data in self.file_info:
            self.table.add_row(*map(str, file_data))

        self.table.cursor_type = "row"
        self.table.focus()

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        row = self.table.get_row(event.row_key)
        selected_filename = row[0]
        log(f"{event.row_key=}")
        filepath = os.path.join('.', selected_filename)
        log(f"{filepath=}")
        self.push_screen(FileViewScreen(filepath))


if __name__ == "__main__":
    app = FileListApp()
    app.run()

