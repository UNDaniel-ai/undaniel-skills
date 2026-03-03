#!/usr/bin/env python3
import argparse
import html
import mimetypes
import os
import sys
from datetime import datetime
from typing import Optional

from PySide6.QtCore import QDir, QModelIndex, QSortFilterProxyModel, Qt, QUrl
from PySide6.QtGui import QFontDatabase, QImageReader, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSplitter,
    QStackedWidget,
    QTreeView,
    QVBoxLayout,
    QWidget,
    QCheckBox,
    QFileSystemModel,
)

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_AVAILABLE = True
except Exception:
    QWebEngineView = None
    WEBENGINE_AVAILABLE = False

try:
    import markdown as md
    MARKDOWN_AVAILABLE = True
except Exception:
    md = None
    MARKDOWN_AVAILABLE = False

FILE_PREVIEW_LIMIT_BYTES = 2 * 1024 * 1024

HIDDEN_NAMES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".DS_Store",
}

MARKDOWN_EXTENSIONS = {".md", ".markdown"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tif", ".tiff"}


def _is_binary_file(path: str) -> bool:
    try:
        with open(path, "rb") as handle:
            sample = handle.read(8192)
        return b"\x00" in sample
    except Exception:
        return True


def _is_image_file(path: str) -> bool:
    ext = os.path.splitext(path)[1].lower()
    if ext in IMAGE_EXTENSIONS:
        return True
    mime, _ = mimetypes.guess_type(path)
    return bool(mime and mime.startswith("image/"))


class FileFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, hidden_names: set[str], parent=None):
        super().__init__(parent)
        self.hidden_names = hidden_names
        self.show_hidden = False

    def set_show_hidden(self, show_hidden: bool) -> None:
        self.show_hidden = show_hidden
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        index = self.sourceModel().index(source_row, 0, source_parent)
        name = self.sourceModel().fileName(index)
        if not self.show_hidden:
            if name.startswith(".") or name in self.hidden_names:
                return False
        return True


class ImagePreviewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap: Optional[QPixmap] = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.scroll_area.setWidget(self.image_label)

        self.info_label = QLabel("")
        self.info_label.setWordWrap(True)
        self.info_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        layout.addWidget(self.scroll_area, 1)
        layout.addWidget(self.info_label, 0)

    def set_image(self, pixmap: QPixmap, info_text: str) -> None:
        self._pixmap = pixmap
        self.info_label.setText(info_text)
        self._update_scaled()

    def clear(self, message: str) -> None:
        self._pixmap = None
        self.image_label.setPixmap(QPixmap())
        self.image_label.setText(message)
        self.info_label.setText("")

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._update_scaled()

    def _update_scaled(self) -> None:
        if not self._pixmap:
            return
        viewport_width = max(1, self.scroll_area.viewport().width())
        scaled = self._pixmap.scaledToWidth(viewport_width, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled)


class MdFileViewer(QMainWindow):
    def __init__(self, root_path: str, initial_file: Optional[str], show_hidden: bool):
        super().__init__()
        self.setWindowTitle("MD File Viewer")
        self.resize(1200, 800)

        self.assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
        self.base_url = QUrl.fromLocalFile(self.assets_dir + os.sep)

        self.root_path = root_path

        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        top_bar = QHBoxLayout()
        self.root_edit = QLineEdit()
        self.root_edit.setReadOnly(True)
        self.root_edit.setText(self.root_path)

        self.choose_button = QPushButton("Choose Folder")
        self.choose_button.clicked.connect(self._choose_folder)

        self.open_button = QPushButton("Open File")
        self.open_button.clicked.connect(self._choose_file)

        self.hidden_checkbox = QCheckBox("Show hidden")
        self.hidden_checkbox.setChecked(show_hidden)
        self.hidden_checkbox.stateChanged.connect(self._toggle_hidden)

        top_bar.addWidget(QLabel("Root:"))
        top_bar.addWidget(self.root_edit, 1)
        top_bar.addWidget(self.choose_button)
        top_bar.addWidget(self.open_button)
        top_bar.addWidget(self.hidden_checkbox)

        splitter = QSplitter(Qt.Horizontal)

        self.file_model = QFileSystemModel()
        self.file_model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)
        self.file_model.setRootPath(self.root_path)

        self.file_proxy = FileFilterProxyModel(HIDDEN_NAMES)
        self.file_proxy.setSourceModel(self.file_model)
        self.file_proxy.set_show_hidden(show_hidden)

        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_proxy)
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setEditTriggers(QTreeView.NoEditTriggers)
        self.file_tree.hideColumn(1)
        self.file_tree.hideColumn(2)
        self.file_tree.hideColumn(3)
        self.file_tree.selectionModel().selectionChanged.connect(self._on_file_selected)

        splitter.addWidget(self.file_tree)

        self.preview_stack = QStackedWidget()

        self.text_view = QPlainTextEdit()
        self.text_view.setReadOnly(True)
        self.text_view.setLineWrapMode(QPlainTextEdit.NoWrap)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.text_view.setFont(fixed_font)

        self.image_view = ImagePreviewWidget()

        self.text_view_index = self.preview_stack.addWidget(self.text_view)
        self.image_view_index = self.preview_stack.addWidget(self.image_view)

        if WEBENGINE_AVAILABLE:
            self.markdown_view = QWebEngineView()
            self.markdown_view_index = self.preview_stack.addWidget(self.markdown_view)
        else:
            self.markdown_view = None
            self.markdown_view_index = self.text_view_index

        splitter.addWidget(self.preview_stack)
        splitter.setSizes([300, 900])

        main_layout.addLayout(top_bar)
        main_layout.addWidget(splitter, 1)
        self.setCentralWidget(central)

        self._set_root(self.root_path)

        if initial_file:
            self._reveal_file(initial_file)
        else:
            self._show_message("Select a file to preview.")

    def _choose_folder(self) -> None:
        selected = QFileDialog.getExistingDirectory(self, "Choose Root Folder", self.root_path)
        if selected:
            self._set_root(selected)

    def _choose_file(self) -> None:
        selected, _ = QFileDialog.getOpenFileName(self, "Open File", self.root_path)
        if selected:
            self._reveal_file(selected)

    def _toggle_hidden(self) -> None:
        self.file_proxy.set_show_hidden(self.hidden_checkbox.isChecked())

    def _set_root(self, path: str) -> None:
        self.root_path = path
        self.root_edit.setText(path)
        self.file_model.setRootPath(path)
        root_index = self.file_model.index(path)
        proxy_index = self.file_proxy.mapFromSource(root_index)
        self.file_tree.setRootIndex(proxy_index)

    def _reveal_file(self, path: str) -> None:
        if not os.path.exists(path):
            self._show_message("File not found: " + path)
            return

        if os.path.isdir(path):
            self._set_root(path)
            return

        file_dir = os.path.dirname(path)
        if os.path.abspath(file_dir) != os.path.abspath(self.root_path):
            if not os.path.commonpath([os.path.abspath(path), os.path.abspath(self.root_path)]) == os.path.abspath(self.root_path):
                self._set_root(file_dir)

        index = self.file_model.index(path)
        proxy_index = self.file_proxy.mapFromSource(index)
        if proxy_index.isValid():
            self.file_tree.setCurrentIndex(proxy_index)
            self.file_tree.scrollTo(proxy_index)
        self._load_file_preview(path)

    def _on_file_selected(self, *_):
        indexes = self.file_tree.selectionModel().selectedIndexes()
        if not indexes:
            return
        source_index = self.file_proxy.mapToSource(indexes[0])
        path = self.file_model.filePath(source_index)
        self._load_file_preview(path)

    def _load_file_preview(self, path: str) -> None:
        if os.path.isdir(path):
            self._show_message("Select a file to preview.")
            return

        if not os.path.exists(path):
            self._show_message("File not found: " + path)
            return

        if _is_image_file(path):
            self._load_image_preview(path)
            return

        if _is_binary_file(path):
            self._show_message("Binary file preview is not supported.")
            return

        try:
            size = os.path.getsize(path)
        except Exception:
            self._show_message("Unable to read file size.")
            return

        if size > FILE_PREVIEW_LIMIT_BYTES:
            self._show_message("File is too large to preview (over 2MB).")
            return

        try:
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                content = handle.read()
        except Exception:
            self._show_message("Unable to read file.")
            return

        ext = os.path.splitext(path)[1].lower()
        if ext in MARKDOWN_EXTENSIONS:
            self._set_markdown_content(content)
        else:
            self._set_text_content(content)

    def _load_image_preview(self, path: str) -> None:
        reader = QImageReader(path)
        if not reader.canRead():
            self._show_message("Image preview is not supported for this file.")
            return

        image = reader.read()
        if image.isNull():
            self._show_message("Failed to load image.")
            return

        pixmap = QPixmap.fromImage(image)

        try:
            stat = os.stat(path)
            size_bytes = stat.st_size
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            size_bytes = 0
            modified = "Unknown"

        info = (
            f"Path: {path}\n"
            f"Dimensions: {image.width()} x {image.height()}\n"
            f"Size: {size_bytes} bytes\n"
            f"Modified: {modified}"
        )

        self.image_view.set_image(pixmap, info)
        self.preview_stack.setCurrentIndex(self.image_view_index)

    def _set_markdown_content(self, markdown_text: str) -> None:
        if self.markdown_view:
            html_text = self._render_markdown_html(markdown_text)
            self.markdown_view.setHtml(html_text, self.base_url)
            self.preview_stack.setCurrentIndex(self.markdown_view_index)
            return

        if not WEBENGINE_AVAILABLE:
            note = "(QtWebEngine not available. Showing raw markdown.)\n\n"
        else:
            note = ""
        self._set_text_content(note + markdown_text)

    def _set_text_content(self, text: str) -> None:
        self.text_view.setPlainText(text)
        self.preview_stack.setCurrentIndex(self.text_view_index)

    def _show_message(self, message: str) -> None:
        self._set_text_content(message)

    def _render_markdown_html(self, markdown_text: str) -> str:
        if MARKDOWN_AVAILABLE:
            body_html = md.markdown(markdown_text, extensions=["fenced_code", "tables"])
        else:
            body_html = "<pre>" + html.escape(markdown_text) + "</pre>"
        return self._build_html(body_html, include_mermaid=True)

    def _build_html(self, body_html: str, include_mermaid: bool) -> str:
        style = """
<style>
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 16px; color: #e6e6e6; background: #1e1e1e; }
pre, code { background: #2b2b2b; padding: 8px; border-radius: 4px; white-space: pre-wrap; }
table { border-collapse: collapse; }
th, td { border: 1px solid #444; padding: 6px; }
</style>
"""
        mermaid_script = ""
        if include_mermaid and os.path.exists(os.path.join(self.assets_dir, "vendor", "mermaid.min.js")):
            mermaid_script = """
<script src="vendor/mermaid.min.js"></script>
<script>
  const blocks = document.querySelectorAll("pre code.language-mermaid, pre code.mermaid");
  blocks.forEach((block) => {
    const container = document.createElement("div");
    container.className = "mermaid";
    container.textContent = block.textContent;
    const pre = block.parentElement;
    if (pre && pre.parentElement) {
      pre.parentElement.replaceChild(container, pre);
    }
  });
  if (window.mermaid) {
    mermaid.initialize({ startOnLoad: false, theme: "dark" });
    mermaid.run();
  }
</script>
"""
        return f"<!doctype html><html><head><meta charset='utf-8'>{style}</head><body>{body_html}{mermaid_script}</body></html>"


def _resolve_root_path(path: Optional[str]) -> str:
    if path:
        return os.path.abspath(path)
    return os.path.abspath(os.getcwd())


def main() -> int:
    parser = argparse.ArgumentParser(description="Popup viewer for Markdown, Mermaid, images, and text files.")
    parser.add_argument("--root", help="Root directory for file browser (default: cwd)")
    parser.add_argument("--file", help="File path to open on launch")
    parser.add_argument("--show-hidden", action="store_true", help="Show hidden files by default")
    args = parser.parse_args()

    root_path = _resolve_root_path(args.root)
    initial_file = os.path.abspath(args.file) if args.file else None

    app = QApplication(sys.argv)
    viewer = MdFileViewer(root_path, initial_file, args.show_hidden)
    viewer.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
