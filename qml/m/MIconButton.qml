import QtQuick 2.1
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3


Button {
    property variant glyphs: _g
    MGlyphs { id: _g }

    style: ButtonStyle {
        background: Rectangle {
            implicitWidth: 36
            implicitHeight: 25
            border.width: parent.activeFocus ? 2 : 1
            border.color: "#3A3D3E"
            color: "#F7F7F7"
            gradient: Gradient {
                GradientStop { position: 0.0; color: "#F7F7F7" }
                GradientStop { position: 1.0; color: "#EAEAEA" }
            }
            radius: 6
        }
        label: MIcon {
            text: control.text
        }
    }
}
