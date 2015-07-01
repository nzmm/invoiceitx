import QtQuick 2.1
import QtQuick.Controls 1.3


Column {

    property alias label: _label
    property alias field: _field
    property alias borderColor: _field.borderColor

    spacing: 5

    Label {
        id: _label
        opacity: 0.5
    }
    MTextField {
        id: _field
        width: parent.width
    }
}
