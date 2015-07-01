import QtQuick 2.1
import QtQuick.Controls 1.3


Column {

    property alias label: _label
    property alias area: _area

    spacing: 5
    height: children[0].height + children[1].height + spacing

    Label {
        id: _label
        color: "#878787"
    }
    TextArea {
        id: _area
        width: parent.width
    }
}
