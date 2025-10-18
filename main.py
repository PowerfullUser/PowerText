# File: main.py
# Purpose: Main application logic for PowerText – a feature-rich text editor

# Copyright 2025 Toshan

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Libraries required to be imported
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtPrintSupport import QPrinter

import sys
import os

# Information of the text editor
name = 'PowerText'
version = 1
default_font = 'Calibri'
default_font_size = 12
display_name = name + ' ' + str(version)

# Main Class
class PowerText(QMainWindow):
    # Initializing main function
    def __init__(self, *args, **kwargs):
        # Making a super connection with PowerText()
        super(PowerText, self).__init__(*args, **kwargs)

        # Tabular System
        self.center = QTabWidget()
        self.center.setDocumentMode(True)
        self.center.tabBarDoubleClicked.connect(self.text_editor_tab)
        self.center.tabCloseRequested.connect(lambda: self.center.removeTab(self.center.currentIndex()))
        self.center.setTabsClosable(True)
        self.center.setMovable(True)
        self.center.setStatusTip('Tabular System')
        self.setCentralWidget(self.center)

        # Status Bar
        self.status_bar = QStatusBar()
        self.status_bar.setStatusTip('Status Bar')
        self.setStatusBar(self.status_bar)

        # Functions to Run
        self.text_editor_tab()
        self.navigations()
        self.center.currentChanged.connect(self.font_changed)

        # A variable to recall paths from previously opened or saved files
        self.path = {}

    # Text Editor Tab
    def text_editor_tab(self):
        # Text Editor
        self.text_editor = QTextEdit()
        self.text_editor.setStatusTip('Workspace No. ' + str(1 + self.center.currentIndex()))
        self.text_editor.setFont(QFont(default_font, default_font_size))
        self.center.addTab(self.text_editor, 'New Workspace')

    # Navigations
    def navigations(self):
        # Navigations Toolbar
        self.navigations_toolbar = QToolBar('Navigations Bar', self)
        self.navigations_toolbar.setIconSize(QSize(30, 30))

        # New Workspace Action
        self.new_workspace = QAction(QIcon('Icons/new-tab.png'), 'New Workspace', self)
        self.new_workspace.setStatusTip('Add a new workspace')
        self.new_workspace.triggered.connect(self.text_editor_tab)

        # New Document Action
        self.new = QAction(QIcon('Icons/add-file.png'), 'New', self)
        self.new.triggered.connect(self.new_document)
        self.new.setStatusTip('Make a new document within the desired workspace')

        # Open Document
        self.open = QAction(QIcon('Icons/arrow.png'), 'Open', self)
        self.open.triggered.connect(self.open_document)
        self.open.setStatusTip('Open a document within the desired workspace')

        # Save
        self.save = QAction(QIcon('Icons/save.png'), 'Save', self)
        self.save.triggered.connect(self.save_document)

        # Save As
        self.save_as = QAction(QIcon('Icons/save-as.png'), 'Save As', self)
        self.save_as.triggered.connect(self.save_as_document)
        self.save_as.setStatusTip('Save the document in the desired workspace')

        # Save As PDF
        self.saveas_pdf = QAction(QIcon('Icons/file.png'), 'Save As PDF', self)
        self.saveas_pdf.triggered.connect(self.save_as_pdf)
        self.saveas_pdf.setStatusTip('Save the document in the desired workspace as PDF')

        # Font Box
        self.font_box = QFontComboBox()
        self.font_box.setStatusTip('Change the font of your selected text')
        self.font_box.setCurrentFont(QFont(default_font))
        self.font_box.currentFontChanged.connect(self.font_selection)

        # Font Size Adjuster
        self.font_size = QSpinBox()
        self.font_size.setStatusTip('Change the size of your selected text')
        self.font_size.setMinimum(8)
        self.font_size.setMaximum(96)
        self.font_size.valueChanged.connect(self.font_size_selection)
        self.font_size.setValue(default_font_size)

        # Bold
        self.bold = QAction(QIcon('Icons/bold.png'), 'Bold', self)
        self.bold.setStatusTip('Make the selected text Bold')
        self.bold.triggered.connect(self.bold_function)
        self.bold.setCheckable(True)
        self.bold.setChecked(False)

        # Italic
        self.italic = QAction(QIcon('Icons/text.png'), 'Italic', self)
        self.italic.setStatusTip('Make the selected text Italic')
        self.italic.triggered.connect(self.italic_function)
        self.italic.setCheckable(True)
        self.italic.setChecked(False)

        # Underline
        self.underline = QAction(QIcon('Icons/underline.png'), 'Underline', self)
        self.underline.setStatusTip('Make the selected text Underlined')
        self.underline.triggered.connect(self.underline_function)
        self.underline.setCheckable(True)
        self.underline.setChecked(False)

        # Strikethrough
        self.strikethrough = QAction(QIcon('Icons/strikethrough.png'), 'Strikethrough', self)
        self.strikethrough.setStatusTip('Make the selected text be Striked Out')
        self.strikethrough.triggered.connect(self.strikethrough_function)
        self.strikethrough.setCheckable(True)
        self.strikethrough.setChecked(False)

        # Insert Image Function
        self.insert_image = QAction(QIcon('Icons/image.png'), 'Insert Image', self)
        self.insert_image.setStatusTip('Insert an Image onto the document')
        self.insert_image.triggered.connect(self.insert_image_function)

        # Insert Table Function
        self.insert_table = QAction(QIcon('Icons/cells.png'), 'Insert Table', self)
        self.insert_table.setStatusTip('Insert a Table onto the document')
        self.insert_table.triggered.connect(self.insert_table_function)

        # Align to the Left
        left_align = QAction(QIcon('Icons/left-align.png'), 'Left Alignment', self)
        left_align.triggered.connect(self.left_align_function)
        left_align.setStatusTip('Align the selected text towards the left')

        # Align to the Right
        right_align = QAction(QIcon('Icons/right-justification.png'), 'Right Alignment', self)
        right_align.triggered.connect(self.right_align_function)
        right_align.setStatusTip('Align the selected text towards the right')

        # Align to the Center
        center_align = QAction(QIcon('Icons/text-center.png'), 'Center Alignment', self)
        center_align.triggered.connect(self.center_align_function)
        center_align.setStatusTip('Align the selected text towards the center')

        # Justified Alignment
        justify_align = QAction(QIcon('Icons/justified.png'), 'Justify Alignment', self)
        justify_align.triggered.connect(self.justify_align_function)
        justify_align.setStatusTip('Align the selected text as justified')

        # Numbered List
        number_list = QAction(QIcon('Icons/prioritize.png'), 'Number List', self)
        number_list.triggered.connect(self.number_list)
        number_list.setStatusTip('Make a list of numbers')

        # Bullet List
        bullet_list = QAction(QIcon('Icons/menu.png'), 'Bullet Points List', self)
        bullet_list.triggered.connect(self.bullet_list)
        bullet_list.setStatusTip('Make a list of bullet points')

        # Highlight Text Function
        self.highlight_text = QAction(QIcon('Icons/highlighter.png'), 'Highlight Text', self)
        self.highlight_text.setStatusTip('Highlight Selected Text')
        self.highlight_text.triggered.connect(self.highlight_text_function)

        # Text Colour Function
        self.text_colour = QAction(QIcon('Icons/color.png'), 'Highlight Text', self)
        self.text_colour.setStatusTip('Colour Selected Text')
        self.text_colour.triggered.connect(self.text_colour_function)

        # Adding the following actions made previously
        self.navigations_toolbar.addAction(self.new_workspace)
        self.navigations_toolbar.addSeparator()
        self.navigations_toolbar.addActions([self.new, self.open, self.save, self.save_as, self.saveas_pdf])
        self.navigations_toolbar.addSeparator()
        self.navigations_toolbar.addWidget(self.font_box)
        self.navigations_toolbar.addWidget(self.font_size)
        self.navigations_toolbar.addSeparator()
        self.navigations_toolbar.addActions([self.bold, self.italic, self.underline, self.strikethrough])
        self.navigations_toolbar.addSeparator()
        self.navigations_toolbar.addActions([self.highlight_text, self.text_colour])
        self.navigations_toolbar.addSeparator()
        self.navigations_toolbar.addActions([left_align, right_align, center_align, justify_align])
        self.navigations_toolbar.addSeparator()
        self.navigations_toolbar.addActions([number_list, bullet_list])
        self.navigations_toolbar.addSeparator()
        self.navigations_toolbar.addActions([self.insert_image, self.insert_table])

        self.addToolBar(self.navigations_toolbar)

    # Defining new document
    def new_document(self):
        index = self.center.currentIndex()
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            current_editor.clear()
            self.center.setTabText(index, 'New Workspace')
            if index in self.path:
                del self.path[index]

    # Defining open document
    def open_document(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Document (*.txt);;PowerText Document (*.ptxt);;All Files (*.*)')

        if path:
            try:
                file_to_read = open(path, 'r', encoding='utf-8').read()
                current_editor = self.center.currentWidget()
                self.path[self.center.currentIndex()] = path

                if isinstance(current_editor, QTextEdit):
                    self.center.setTabText(self.center.currentIndex(), 'File: ' + str(os.path.basename(path)))
                    current_editor.setText(file_to_read)
            except Exception as e:
                QMessageBox.warning(self, f'Unable to open document due to:\n{e}')
        else:
            pass
    
    # Defining save as function
    def save_as_document(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save File As', '', 'Text File (*.txt);;PowerText Document(*.ptxt);;All Files (*.*)')

        if path:
            try:
                self.path[self.center.currentIndex()] = path
                current_editor = self.center.currentWidget()

                if isinstance(current_editor, QTextEdit):
                    with open(path, 'w', encoding='utf-8') as f:
                        if path.endswith('.txt'):
                            f.write(current_editor.toPlainText())
                            self.center.setTabText(self.center.currentIndex(), 'File: ' + os.path.basename(path))
                        else:
                            f.write(current_editor.toHtml())
                            self.center.setTabText(self.center.currentIndex(), 'File: ' + os.path.basename(path))
            except Exception as e:
                QMessageBox.warning(self, f'Unable to save document due to:\n{e}')
        else:
            pass

    # Defining Save Function
    def save_document(self):
        index = self.center.currentIndex()
        path = self.path.get(index)

        if not path:
            self.save_as_document()
            return

        try:
            current_editor = self.center.currentWidget()

            if isinstance(current_editor, QTextEdit):
                with open(path, 'w', encoding='utf-8') as f:
                    if path.endswith('.txt'):
                        f.write(current_editor.toPlainText())
                    else:
                        f.write(current_editor.toHtml())
                self.center.setTabText(index, os.path.basename(path))
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Unable to save document due to:\n{e}")

    # Defining Save As PDF Document function
    def save_as_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export as PDF", "", "PDF Files (*.pdf);;All Files (*)")

        if path:
            if not path.endswith('.pdf'):
                path += '.pdf'

            printer = QPrinter()
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(path)

            current_editor = self.center.currentWidget()

            if isinstance(current_editor, QTextEdit):
                current_editor.document().print(printer)
                QMessageBox.information(self, "Export Successful", f"Document exported as PDF:\n{path}")

    # Defining Font Selection
    def font_selection(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            font = self.font_box.currentFont()
            current_editor.setCurrentFont(font)

    # Defining Font Size Selection
    def font_size_selection(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            current_editor.setFontPointSize(float(self.font_size.value()))

    # Defining Updating of Font when tab is switched
    def font_changed(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            self.font_box.setCurrentFont(current_editor.font())
            self.font_size.setValue(int(current_editor.fontPointSize()))

    # Defining the Bold Function
    def bold_function(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            cursor = current_editor.textCursor()
            fmt = cursor.charFormat()
            
            if self.bold.isChecked() == True:
                fmt.setFontWeight(QFont.Weight.Bold)
            else:
                fmt.setFontWeight(QFont.Weight.Normal)

            cursor.mergeCharFormat(fmt)

    # Defining the Italic Function
    def italic_function(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            cursor = current_editor.textCursor()
            fmt = cursor.charFormat()
            
            if self.italic.isChecked() == True:
                fmt.setFontItalic(True)
            else:
                fmt.setFontItalic(False)

            cursor.mergeCharFormat(fmt)

    # Defining the Underline Function
    def underline_function(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            cursor = current_editor.textCursor()
            fmt = cursor.charFormat()
            
            if self.underline.isChecked() == True:
                fmt.setFontUnderline(True)
            else:
                fmt.setFontUnderline(False)

            cursor.mergeCharFormat(fmt)

    # Defining a Strikethrough Function
    def strikethrough_function(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            cursor = current_editor.textCursor()
            fmt = cursor.charFormat()
            
            if self.strikethrough.isChecked() == True:
                fmt.setFontStrikeOut(True)
            else:
                fmt.setFontStrikeOut(False)

            cursor.mergeCharFormat(fmt)

    # Deifining of Insert Image Function
    def insert_image_function(self):
        path, _ = QFileDialog.getOpenFileName(self, "Insert Image", "", "Image Files (*.png *.jpg *.bmp *.gif);;All Files (*)")

        width, ok = QInputDialog.getInt(self, 'Image Width' ,'Type the width of the image in pixels', 300, 1, 2000)

        height, ok2 = QInputDialog.getInt(self, 'Image Width' ,'Type the width of the image in pixels', 300, 1, 2000)


        if path and ok and ok2:
            current_editor = self.center.currentWidget()

            if isinstance(current_editor, QTextEdit):
                cursor = current_editor.textCursor()
                image = QTextImageFormat()
                image.setName(path)
                image.setWidth(width)
                image.setHeight(height)
                cursor.insertImage(image)

    # Defining the function of inserting tables
    def insert_table_function(self):
        current_editor = self.center.currentWidget()   

        if isinstance(current_editor, QTextEdit):
            rows, ok = QInputDialog.getInt(self, 'Rows of Table', 'Put the number of required number of rows for the table.', 10, 1, 1000)
            columns, ok2 = QInputDialog.getInt(self, 'Columns of Table', 'Put the number of required number of columns for the table.', 10, 1, 1000)
            
            if ok and ok2:
                cursor = current_editor.textCursor()
                cursor.insertTable(rows, columns)

    # Defining Right Alignment Function
    def right_align_function(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            cursor = current_editor.textCursor()
            block_format = cursor.blockFormat()
            block_format.setAlignment(Qt.AlignmentFlag.AlignRight)
            cursor.setBlockFormat(block_format)

    # Defining Left Alignment Function
    def left_align_function(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            cursor = current_editor.textCursor()
            block_format = cursor.blockFormat()
            block_format.setAlignment(Qt.AlignmentFlag.AlignLeft)
            cursor.setBlockFormat(block_format)

    # Defining Center Alignment Function
    def center_align_function(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            cursor = current_editor.textCursor()
            block_format = cursor.blockFormat()
            block_format.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cursor.setBlockFormat(block_format)
    
    # Defining Justify Alignment Function
    def justify_align_function(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            cursor = current_editor.textCursor()
            block_format = cursor.blockFormat()
            block_format.setAlignment(Qt.AlignmentFlag.AlignJustify)
            cursor.setBlockFormat(block_format)

    # Defining numbered list
    def number_list(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            cursor = current_editor.textCursor()
            list_format = QTextListFormat()
            list_format.setStyle(QTextListFormat.Style.ListDecimal)
            cursor.createList(list_format)

    # Defining Bullet Point list
    def bullet_list(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            cursor = current_editor.textCursor()
            list_format = QTextListFormat()
            list_format.setStyle(QTextListFormat.Style.ListCircle)
            cursor.createList(list_format)

    # Defining Highlight Text Function
    def highlight_text_function(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            colour_dialog = QColorDialog.getColor(Qt.GlobalColor.yellow, self, 'Select Highlighting Colour')

            if colour_dialog.isValid():
                cursor = current_editor.textCursor()
                highlighter = QTextCharFormat()
                highlighter.setBackground(colour_dialog)
                cursor.mergeCharFormat(highlighter)
            else:
                pass

    # Defining Text Colour Function
    def text_colour_function(self):
        current_editor = self.center.currentWidget()

        if isinstance(current_editor, QTextEdit):
            colour_dialog = QColorDialog.getColor(Qt.GlobalColor.black, self, 'Select Highlighting Colour')

            if colour_dialog.isValid():
                cursor = current_editor.textCursor()
                highlighter = QTextCharFormat()
                highlighter.setForeground(colour_dialog)
                cursor.mergeCharFormat(highlighter)
            else:
                pass


# Using QApplication as a base for PowerText() to run
app = QApplication(sys.argv)
app.setApplicationName(name)
app.setApplicationDisplayName(display_name)
app.setWindowIcon(QIcon('Icons/ApplicationIcon.ico'))
window = PowerText()
window.show()
window.setGeometry(100, 100, 1000, 600)
app.exec()

