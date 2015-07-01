import QtQuick 2.1


Image {
    id: throbber
    property bool running: false
    property bool invert: false

    source: invert ? "icons/loading-light.png" : "icons/loading.png"

    NumberAnimation on rotation {
        running: throbber.running; from: 0; to: 360; loops: Animation.Infinite; duration: 1200
    }
}
