import QtQuick 2.1
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3


ComboBox {
    property color borderColor: "#C4C1BD"

    style: ComboBoxStyle {
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
            radius: 3

            Label {
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: -3
                renderType: Text.QtRendering
                font.family: "FontAwesome"
                font.pointSize: 10
                anchors.right: parent.right
                anchors.margins: 8
                text: "\uf0dd"
                color: "#2B2B2B"
                style: Text.Raised
                styleColor: "#fff"
            }
        }
    }
}
