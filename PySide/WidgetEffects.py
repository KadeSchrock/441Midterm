from PySide6 import QtWidgets, QtGui

'''
This module contains helper functions that apply visual effects to widgets
'''
def add_shadow(widget: QtWidgets.QWidget, blur: int = 18, offset_y: int = 4, opacity: int = 90) -> None:
    # Create a shadow effect for the widget
    shadow: QtWidgets.QGraphicsDropShadowEffect = QtWidgets.QGraphicsDropShadowEffect(widget)

    # How soft and spread out the shadow appears
    shadow.setBlurRadius(blur)

    # Move the shadow slightly downwards
    shadow.setOffset(0, offset_y)

    # Set the shadow color and transparency
    color: QtGui.QColor = QtGui.QColor("#000000")
    color.setAlpha(opacity)
    shadow.setColor(color)

    # Apply the effect to the widget
    widget.setGraphicsEffect(shadow)
