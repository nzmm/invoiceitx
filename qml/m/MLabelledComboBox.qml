import QtQuick 2.1
import QtQuick.Controls 1.3


Column {

    property alias label: _label
    property alias combo: _combo
    property alias borderColor: _combo.borderColor

    spacing: 5
    height: children[0].height + children[1].height + spacing

    Label {
        id: _label
        opacity: 0.5
    }
    MComboBox {
        id: _combo
        width: parent.width
    }
}
