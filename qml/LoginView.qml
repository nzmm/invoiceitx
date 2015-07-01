import QtQuick 2.1
import QtQuick.Controls 1.3
import "m"


Rectangle {
    property bool loggedIn: vendor.loggedIn
    property bool authError: vendor.authError

    onLoggedInChanged: {
        if (loggedIn) {
            currentView = 'sales'
        } else {
            currentView = 'login'
            password.text = ""
            signIn.visible = true
        }
    }
    onAuthErrorChanged: {
        if (authError) {
            password.text = ""
            signIn.visible = true
        }
    }

    color: "#3C3F41"

    Column {
        id: signIn

        width: 300
        anchors.centerIn: parent
        spacing: 6

        Rectangle {
            visible: vendor.authError.length > 0

            width: parent.width
            height: err.height + 24

            color: "#FF3847"
            radius: 8

            Label {
                id: err
                text: vendor.authError
                anchors.centerIn: parent
                width: parent.width - 36
                wrapMode: Text.WrapAnywhere
                maximumLineCount: 5
                elide: Text.ElideRight
            }
        }

        Item {
            // spacer
            width: 1; height: 12
        }

        Label {
            text: "Shop Name"
            color: "#fff"
        }

        MTextField {
            id: shopName
            width: parent.width
            font.pixelSize: 20
            text: argv.getArgument("domain")
            height: 32
            focus: true

            Component.onCompleted: { selectAll() }

            onFocusChanged: {
                if(focus) { selectAll() }
            }
        }

        Label {
            text: "Username"
            color: "#fff"
        }

        MTextField {
            id: username
            width: parent.width
            height: 32
            text: argv.getArgument("user")

            onFocusChanged: {
                if(focus) { selectAll() }
            }
        }

        Label {
            text: "Password"
            color: "#fff"
        }

        MTextField {
            id: password
            width: parent.width
            echoMode: TextInput.Password
            height: 32
            text: argv.getArgument("pass")

            onFocusChanged: {
                if(focus) { selectAll() }
            }
        }

        Item {
            // spacer
            width: 1; height: 8
        }

        MButton {
            anchors.right: parent.right
            text: "Sign In"

            onClicked: {
                // login() performs simple validation of supplied args...
                // does not mean login was successful just that args look ok
                var validInputs = vendor.login(shopName.text, username.text, password.text)
                if (validInputs) {
                    parent.visible = false
                }
            }
        }
    }

    Row {
        visible: !signIn.visible
        width: 300
        anchors.centerIn: parent
        spacing: 4

        Throbber {
            width: 22; height: 22
            anchors.verticalCenter: parent.verticalCenter
            running: parent.visible
            invert: true
        }

        Label {
            anchors.verticalCenter: parent.verticalCenter
            text: "Signing in to %1...".arg(shopName.text)
            color: "#fff"
        }
    }
}
