import QtQuick 2.4
import QtQuick.Controls 1.3

import ArgV 1.0
import Vend 1.0


Rectangle {
    id: root
    width: 900
    height: 650
    color: "#F8F8F8"

    property string currentView: argv.getArgument("initview")

    ArgParser { id: argv }
    Vendor { id: vendor }
    FontLoader { source: "fonts/fontawesome.ttf" }

    SaleListView {
        visible: currentView == 'sales'
        anchors.fill: parent
    }
    SaleReceiptView {
        visible: currentView == 'details'
        anchors.fill: parent
    }
    ConfigView {
        visible: currentView == 'config'
        anchors.fill: parent
    }
    LoginView {
        visible: currentView == 'login'
        anchors.fill: parent
    }
}
