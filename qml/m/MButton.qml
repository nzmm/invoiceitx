import QtQuick 2.1
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3


Button {

    property color borderColor: "#C4C1BD"

    style: ButtonStyle {
        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 25
            border.width: parent.activeFocus ? 2 : 1
            border.color: borderColor
            color: "#F7F7F7"
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#F7F7F7" }
                GradientStop { position: 1.0; color: "#EAEAEA" }
            }
            radius: 6
        }
    }
}
