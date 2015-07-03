import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3
import "m"


Item {
    property variant receipt: vendor.saleReceipt

    function save() {
        savedHint.visible = false;
        receipt.saveCustomerDetails(
            customerName.text,
            customerEmail.text,
            saleComment.area.text
        );

        var model = productList.model,
            i,
            l = model.rowCount();

        for (i=0; i<l; i++) {
            receipt.saveLineNote(i, model.lineNote(i));
        }
        savedHint.visible = true;
    }

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

            Label {
                id: savedHint

                anchors.verticalCenter: parent.verticalCenter
                text: "Saved :)"
                color: "#F2F1F0"
                visible: false

                onVisibleChanged: {
                    if (visible) {
                        timeout.restart()
                    }
                }

                Timer {
                    id: timeout
                    interval: 10000;
                    running: false;
                    repeat: false;
                    onTriggered: {
                        parent.visible = false
                    }
                }
            }
            MButton {
                text: receipt.saving ? "Saving..." : "Save"
                opacity: receipt.saving ? 0.5 : 1

                onClicked: {
                    if (!receipt.saving) {
                        save()
                    }
                }
            }
            MButton {
                text: "Show PDF"
                opacity: receipt.saving ? 0.5 : 1

                onClicked: {
                    if (!receipt.saving) {
                        save();
                        receipt.generatePDF();
                    }
                }
            }
            MButton {
                text: "Email PDF"
                opacity: receipt.saving || customerEmail.text !== "" ? 1 : 0.5
                onClicked: {
                    if (!receipt.saving) {
                        save();
                        receipt.emailPDF();
                    }
                }
            }
        }
    }

    Item {
        id: details

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: topbar.bottom
        anchors.bottom: parent.bottom
        anchors.margins: 15

        Column {
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: Math.min(1024, parent.width)
            spacing: 30

            Column {
                spacing: 10

                Label {
                    text: "%1 - %2".arg(receipt.invoiceNumber).arg(receipt.saleDate)
                    color: "#7A7A7A"

                    MGlyphicon {
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.right
                        anchors.leftMargin: 15
                        glyph: glyphs.check
                        bgColor: "#319231"
                        visible: receipt.sent
                    }
                }
                Label {
                    text: receipt.note
                    color: "#878787"
                    font.italic: true
                }
                Row {
                    spacing: 5

                    MTextField {
                        id: customerName
                        placeholderText: "Customer Name"
                        width: 200
                        text: receipt.customerName
                        borderColor: "#C4C1BD"
                    }
                    MTextField {
                        id: customerEmail
                        placeholderText: "Customer Email"
                        width: 300
                        text: receipt.customerEmail
                        borderColor: "#C4C1BD"
                    }
                }
                MLabelledTextArea {
                    id: saleComment
                    area.height: 40
                    area.width: 505
                    label.text: "Sale Comment"
                    area.text: receipt.comment
                }
            }
            TableView {
                id: productList

                width: parent.width
                height: 200
                model: receipt.saleProducts

                itemDelegate: Item {
                    Loader {
                        anchors.fill: parent
                        sourceComponent: styleData.column == 6 ? noteCell : labelCell

                        onLoaded: { item.styleData = styleData }
                    }
                }

                Component {
                    id: labelCell

                    Label {
                        property variant styleData

                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.leftMargin: 4
                        elide: Text.ElideMiddle
                        color: styleData.textColor

                        text: {
                            switch(styleData.column) {
                                case 3:
                                case 4:
                                case 5:
                                    try {
                                        return styleData.value.toFixed(2)
                                    } catch(e) {
                                        return styleData.value
                                    }
                                default:
                                    return styleData.value
                            }
                        }
                    }
                }
                Component {
                    id: noteCell

                    TextField {
                        property variant styleData

                        y: 3
                        width: parent.width
                        text: styleData.value
                        textColor: styleData.textColor

                        style: TextFieldStyle {
                            background: Item {}
                        }

                        onTextChanged: {
                            productList.model.updateLineNote(
                                styleData.row,
                                text
                            )
                        }
                    }
                }

                TableViewColumn {
                    title: "#"
                    width: 40
                }
                TableViewColumn {
                    title: "Item name"
                    role: "name"
                    width: 250
                }
                TableViewColumn {
                    title: "Quantity"
                    role: "quantity"
                    width: 100
                }
                TableViewColumn {
                    title: "Price"
                    role: "price"
                    width: 100
                }
                TableViewColumn {
                    title: "%1 ($)".arg(receipt.taxName)
                    role: "tax"
                    width: 100
                }
                TableViewColumn {
                    title: "Total"
                    role: "total"
                    width: 100
                }
                TableViewColumn {
                    title: "Line Notes"
                    role: "note"
                    width: 500
                }
            }
            Item {
                width: parent.width
                height: totals.height

                Row {
                    width: parent.width * 0.5
                    spacing: 15

                    Rectangle {
                        height: totals.height; width: height;
                        radius: 4
                        border.color: "#8E7950"
                        color: "#fff"

                        Image {
                            source: vendor.register.logoPath
                            smooth: false
                            mipmap: true
                            anchors.fill: parent
                            anchors.margins: 2
                            fillMode: Image.PreserveAspectFit
                        }
                    }
                    Column {
                        spacing: 5

                        Label {
                            text: "%1 t/a ".arg(vendor.register.legalName)
                            font.pointSize: 7
                            visible: vendor.register.legalName !== ""
                        }
                        Label {
                            text: vendor.register.tradingName
                            font.pointSize: 15
                            font.bold: true
                        }
                        Label {
                            text: vendor.register.physicalAddress
                            font.pointSize: 7
                        }
                    }
                }
                Item {
                    id: totals

                    width: 250
                    height: 100
                    anchors.right: parent.right
                    anchors.margins: 15

                    Row {
                        anchors.fill: parent

                        Column {
                            spacing: 5
                            width: parent.width * 0.4

                            Label {
                                x: 3
                                text: "Subtotal"
                                color: "#3C3F41"
                            }
                            Label {
                                x: 3
                                text: "%1 %2%".arg(receipt.taxName).arg(receipt.taxRate * 100)
                                color: "#3C3F41"
                            }
                            Rectangle { height: 1; width: parent.width; color: '#000' }
                            Label {
                                x: 3
                                text: "TOTAL NZD"
                                color: "#3C3F41"
                            }
                            Rectangle { height: 2; width: parent.width; color: '#000' }
                            Column {
                                x: 3

                                Repeater {
                                    model: receipt.salePayments

                                    Label {
                                        text: "%1".arg(name)
                                        color: "#1E90FF"
                                    }
                                }
                            }
                            Rectangle { height: 1; width: parent.width; color: '#000' }
                            Label {
                                x: 3
                                text: "Amount Due"
                                color: "#3C3F41"
                            }
                            Rectangle { height: 2; width: parent.width; color: '#000' }
                        }
                        Column {
                            spacing: 5
                            width: parent.width * 0.6
                            clip: true

                            Label {
                                text: "%1".arg(receipt.subtotal.toFixed(2))
                                color: "#3C3F41"
                                anchors.right: parent.right
                                anchors.rightMargin: 3
                            }
                            Label {
                                text: "%1".arg(receipt.taxComponent.toFixed(2))
                                color: "#3C3F41"
                                anchors.right: parent.right
                                anchors.rightMargin: 3
                            }
                            Rectangle { height: 1; width: parent.width; color: '#000' }
                            Label {
                                text: "%1".arg(receipt.total.toFixed(2))
                                color: "#3C3F41"
                                font.bold: true
                                anchors.right: parent.right
                                anchors.rightMargin: 3
                            }
                            Rectangle { height: 2; width: parent.width; color: '#000' }
                            Column {
                                anchors.right: parent.right
                                anchors.rightMargin: 3

                                Repeater {
                                    model: receipt.salePayments

                                    Label {
                                        text: "(%1)".arg(amount.toFixed(2))
                                        color: "#1E90FF"
                                    }
                                }
                            }
                            Rectangle { height: 1; width: parent.width; color: '#000' }
                            Label {
                                text: "%1".arg(receipt.toPay.toFixed(2))
                                color: "#3C3F41"
                                anchors.right: parent.right
                                anchors.rightMargin: 3
                            }
                            Rectangle { height: 2; width: parent.width; color: '#000' }
                        }
                    }
                }
            }
        }
    }
    Label {
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.margins: 15
        font.pointSize: 7
        text: receipt.transactionID
    }
}
