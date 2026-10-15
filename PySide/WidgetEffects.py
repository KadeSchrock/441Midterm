from PySide6 import QtWidgets, QtGui


def add_shadow(widget, blur=18, offset_y=4, opacity=90):
    # Create a shadow effect for the widget
    shadow = QtWidgets.QGraphicsDropShadowEffect(widget)

    # How soft and spread out the shadow appears
    shadow.setBlurRadius(blur)

    # Move the shadow slightly downwards
    shadow.setOffset(0, offset_y)

    # Set the shadow color and transparency
    color = QtGui.QColor("#000000")
    color.setAlpha(opacity)
    shadow.setColor(color)

    # Apply the effect to the widget
    widget.setGraphicsEffect(shadow)
