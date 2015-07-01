import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Dialogs 1.0
import "m"


Rectangle {
    property variant register: vendor.register

    id: configView
    color: "#FFE994"

    Rectangle {
        id: topbar
        color: "#3C3F41"
        height: 50
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top

        Row {
            id: navLeft
            spacing: 10
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter
            anchors.margins: 15

            MButton {
                text: "Back"

                onClicked: {
                    currentView = 'sales'
                }
            }
        }
        Row {
            id: navRight
            spacing: 10
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            anchors.margins: 15

            MButton {
                text: "Save"

                onClicked: {
                    var registerID = configRegister.model.getRegisterID(configRegister.currentIndex);

                    register.save(
                        registerID,
                        logo.source,
                        gst.field.text,
                        tradingName.field.text,
                        legalName.field.text,
                        postalAddress.area.text,
                        physicalAddress.area.text,
                        email.field.text,
                        emailServer.field.text,
                        emailUser.field.text,
                        emailPassword.field.text,
                        emailPort.field.text,
                        emailSecurity.combo.currentText,
                        phoneLandline.field.text,
                        phoneMobile.field.text,
                        paymentInstructions.area.text,
                        footerMessage.area.text
                    )
                }
            }
        }
    }
    ScrollView {
        id: config

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: topbar.bottom
        anchors.bottom: parent.bottom

        Item {
            x: 15; y: 15
            width: 850
            height: children[0].height

            Column {
                spacing: 12

                MComboBox {
                    id: configRegister
                    model: vendor.registers
                    textRole: "name"
                    width: 180

                    Connections {
                        target: vendor
                        onDomainChangeComplete: {
                            var i = argv.getArgument("register")
                            configRegister.currentIndex = i
                        }
                    }
                    Connections {
                        target: vendor.register
                        onRegisterChanged: {
                            configRegister.currentIndex = vendor.registers.getIndex(vendor.register.id)
                        }
                    }
                    onCurrentIndexChanged: {
                        register.setRegister(model.getRegisterID(currentIndex))
                    }
                }
                Label {
                    text: "Configure details to appear on customer invoices"
                    font.pointSize: 14
                    color: "#8E7950"
                }
                Item { width: 1; height: 12 }
                Row {
                    spacing: 15

                    Column {
                        spacing: 5

                        Label {
                            color: "#8E7950"
                            text: "Branding"
                        }
                        Rectangle {
                            width: 72; height: 72;
                            radius: 4
                            border.color: "#8E7950"
                            color: "#fff"

                            Image {
                                id: logo
                                source: register.logoPath
                                smooth: false
                                mipmap: true
                                anchors.fill: parent
                                anchors.margins: 2
                                fillMode: Image.PreserveAspectFit
                            }
                        }
                    }
                    Column {
                        anchors.verticalCenter: parent.verticalCenter
                        spacing: 5

                        MButton {
                            text: "Select image..."
                            borderColor: "#8E7950"
                            width: 184

                            onClicked: { fileDialog.visible = true }
                        }
                        Label {
                            id: logoPath
                            color: "#8E7950"
                            text: Qt.resolvedUrl(register.logoPath) ? register.logoPath : "No image set"
                            font.pointSize: 8
                            width: 500
                            elide: Text.ElideMiddle
                        }
                    }
                }
                MLabelledTextField {
                    id: tradingName
                    width: parent.width
                    borderColor: "#8E7950"
                    label.text: "Trading Name"
                    field.text: register.tradingName
                }
                MLabelledTextField {
                    id: legalName
                    width: parent.width
                    borderColor: "#8E7950"
                    label.text: "Legal Name"
                    field.text: register.legalName
                }
                MLabelledTextField {
                    id: gst
                    width: parent.width
                    borderColor: "#8E7950"
                    label.text: "GST Number"
                    field.text: register.taxID
                }
                MLabelledTextField {
                    id: email
                    width: parent.width
                    borderColor: "#8E7950"
                    label.text: "Email"
                    field.text: register.email
                }
                Row {
                    width: parent.width
                    height: children[0].height
                    spacing: 5

                    MLabelledTextField {
                        id: emailServer
                        width: (parent.width - 4*parent.spacing - 50)/3
                        borderColor: "#8E7950"
                        label.text: "SMTP Server"
                        field.text: register.emailServer
                    }
                    MLabelledTextField {
                        id: emailUser
                        width: (parent.width - 4*parent.spacing - 50)/3
                        borderColor: "#8E7950"
                        label.text: "Username"
                        field.text: register.emailUser
                    }
                    MLabelledTextField {
                        id: emailPassword
                        width: (parent.width - 4*parent.spacing - 200)/3
                        borderColor: "#8E7950"
                        label.text: "Password"
                        field.text: register.emailPassword
                        field.echoMode: TextInput.Password
                    }
                    MLabelledTextField {
                        id: emailPort
                        width: 50
                        borderColor: "#8E7950"
                        label.text: "Port"
                        field.text: register.emailPort
                    }
                    MLabelledComboBox {
                        id: emailSecurity
                        width: 50
                        borderColor: "#8E7950"
                        label.text: "Security"

                        combo.model: ListModel {
                            ListElement { name: "None" }
                            ListElement { name: "TLS" }
                            ListElement { name: "SSL" }
                        }
                        combo.textRole: "name"

                        Connections {
                            target: vendor.register
                            onRegisterChanged: {
                                var combo = emailSecurity.combo;
                                combo.currentIndex = combo.find(register.emailSecurity);
                            }
                        }
                    }
                }
                Row {
                    width: parent.width
                    height: children[0].height
                    spacing: 5

                    MLabelledTextField {
                        id: phoneLandline
                        width: (parent.width - parent.spacing) / 2
                        borderColor: "#8E7950"
                        label.text: "Landline"
                        field.text: register.phoneLandline
                    }
                    MLabelledTextField {
                        id: phoneMobile
                        width: (parent.width - parent.spacing) / 2
                        borderColor: "#8E7950"
                        label.text: "Mobile"
                        field.text: register.phoneMobile
                    }
                }
                MLabelledTextArea {
                    id: paymentInstructions
                    width: parent.width
                    area.height: 100
                    label.text: "Payment instructions"
                    area.text: register.paymentInstructions
                    visible: false
                }
                MLabelledTextArea {
                    id: footerMessage
                    width: parent.width
                    area.height: 100
                    label.text: "Footer message"
                    area.text: register.footerMessage
                }
                MLabelledTextArea {
                    id: physicalAddress
                    width: parent.width
                    area.height: 100
                    label.text: "Physical address"
                    area.text: register.physicalAddress
                }
                MLabelledTextArea {
                    id: postalAddress
                    width: parent.width
                    area.height: 100
                    label.text: "Postal address"
                    area.text: register.postalAddress
                }
                Item { width: 1; height: 30 }
            }
        }
    }

    FileDialog {
        id: fileDialog
        title: "Please choose an image"
        nameFilters: [ "Image files (*.jpg *.png)", "All files (*)" ]

        onAccepted: {
            logo.source = fileUrl
            logoPath.text = fileUrl.toString()
            Qt.quit()
        }
        onRejected: {
            console.log("Canceled")
            Qt.quit()
        }
    }
}
