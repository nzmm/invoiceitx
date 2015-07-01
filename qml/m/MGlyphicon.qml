import QtQuick 2.4


Rectangle {
    property color fgColor: "#fff"
    property color bgColor: "#1A1A1A"
    property alias glyph: _i.text
    property variant glyphs: _g

    MGlyphs { id: _g }

    width: Math.max(children[0].width, children[0].height) + 16
    height: width
    radius: width / 2
    color: bgColor
    border.width: 1
    border.color: Qt.darker(color, 1.2)

    MIcon {
        id: _i
        anchors.centerIn: parent
        font.pointSize: 8
        color: fgColor
        style: Text.Raised
        styleColor: Qt.darker(parent.color)
    }
}
