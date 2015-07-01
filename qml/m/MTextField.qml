import QtQuick 2.1
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3


TextField {
    property color borderColor: "#C4C1BD"

    style: TextFieldStyle {
        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 25
            border.width: parent.activeFocus ? 2 : 1
            border.color: borderColor
            radius: 3
        }
    }
}
