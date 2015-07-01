import QtQuick 2.1
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3


TextArea {
    property color borderColor

    style: TextAreaStyle {
        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 25
            border.width: parent.activeFocus ? 2 : 1
            border.color: borderColor ? borderColor : "#3A3D3E99"
            radius: 3
        }
    }
}
