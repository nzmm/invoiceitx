import QtQuick 2.1
import QtQuick.Controls 1.3
import "m"


Item {
    id: salesView

    Rectangle {
        id: sidebar
        width: datePicker.width + 30
        anchors.top: parent.top
        anchors.bottom: parent.bottom

        color: "#3C3F41"

        Column {
            anchors.fill: parent
            anchors.margins: 15
            spacing: 15

            // MComboBox {
            //    id: outletSel
            //    width: parent.width
            //    model: vendor.outlets
            //    textRole: "name"
            // }
            Calendar {
                id: datePicker
                maximumDate: new Date() // current date

                onDoubleClicked: {
                    vendor.requestSalesForDate(
                        argv.getArgument("outlet"),
                        datePicker.selectedDate.toISOString()
                    )
                }
            }
            MButton {
                width: parent.width
                text: "Download sales for day"
                opacity: vendor.loadingSales ? 0.5 : 1

                onClicked: {
                    if (!vendor.loadingSales) {
                        vendor.requestSalesForDate(
                            argv.getArgument("outlet"),
                            datePicker.selectedDate.toISOString()
                        )
                    }
                }
            }
            Row {
                visible: vendor.loadingSales
                spacing: 4

                Throbber {
                    width: 22; height: 22
                    anchors.verticalCenter: parent.verticalCenter
                    running: parent.visible
                    invert: true
                }
                Label {
                    anchors.verticalCenter: parent.verticalCenter
                    text: "Downloading sales..."
                    color: "#fff"
                }
            }
        }
        MIconButton {
            text: glyphs.cog
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            anchors.margins: 15

            onClicked: { currentView = 'config' }
        }
    }
    Item {
        id: body
        anchors.left: sidebar.right
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom

        Column {
            id: filterCol

            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.margins: 15
            spacing: 5

            Label {
                text: "Filter sales"
                color: "#878787"
            }
            Row {
                spacing: 5

                MComboBox {
                    id: registerFilter
                    model: vendor.registers
                    textRole: "name"
                    width: 180

                    Connections {
                        target: vendor
                        onDomainChangeComplete: {
                            var i = argv.getArgument("register")
                            registerFilter.currentIndex = i
                        }
                    }
                    // Connections {
                    //     target: vendor.register
                    //     onRegisterChanged: {
                    //         registerFilter.currentIndex = vendor.registers.getIndex(vendor.register.id)
                    //     }
                    // }
                    onCurrentIndexChanged: {
                        vendor.sales.setRegisterFilter(registerFilter.currentIndex)
                    }
                }
                MTextField {
                    id: invoiceFilter
                    width: 140
                    placeholderText: "Invoice Number"

                    onTextChanged: {
                        vendor.sales.setInvoiceFilter(text)
                    }
                }
                MTextField {
                    id: amountFilter
                    width: 100
                    placeholderText: "Amount"

                    onTextChanged: {
                        vendor.sales.setAmountFilter(text)
                    }
                }
            }
        }
        Label {
            anchors.verticalCenter: filterCol.verticalCenter
            anchors.right: parent.right
            anchors.margins: 15
            anchors.verticalCenterOffset: height
            color: "#878787"
            text: "%1/%2".arg(vendor.sales.allVisible).arg(vendor.sales.allAvailable)
        }
        TableView {
            id: salesList

            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: filterCol.bottom
            anchors.bottom: parent.bottom
            anchors.margins: 15
            anchors.bottomMargin: 30

            model: vendor.sales

            onDoubleClicked: {
                vendor.saleReceipt.setSource(row)
                currentView = 'details'
            }

            TableViewColumn {
                role: "sent"
                title: ""
                width: 24
            }
            TableViewColumn {
                role: "invoice_number"
                title: "Invoice"
                width: 100
            }
            TableViewColumn {
                role: "total_payment"
                title: "Value"
                width: 100
            }
            TableViewColumn {
                role: "time"
                title: "Time"
                width: 100
            }
            TableViewColumn {
                role: "customer"
                title: "Customer"
                width: 100
            }
            TableViewColumn {
                role: "notes"
                title: "Notes"
                width: 400
            }
        }
        Label {
            anchors.left: parent.left
            anchors.top: salesList.bottom
            anchors.topMargin: 5
            anchors.leftMargin: 15
            text: "Value of displayed sales: <strong>$%1</strong>".arg(vendor.sales.displayedSalesValue.toFixed(2))
        }
    }
}
