import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import AbcVmInterpolation 1.0

RowLayout {
    property AbcVmInterpolation viewModel: null
    id: interpolationView
    
    ColumnLayout {
        id: inputLayout
        property int maxWidth: 350
        Layout.maximumWidth: maxWidth
        spacing: 5

        Text {
            Layout.maximumWidth: inputLayout.maxWidth
            text: "Interpolation: Here you can analyze the loaded data and create look up tables for algorithm implementation :)"
            wrapMode: Text.Wrap
        }

        ComboBox {
            Layout.maximumWidth: inputLayout.maxWidth
            Layout.preferredWidth: 180
            id: cbAlgorithm
            model: ListModel {
                id: model
                ListElement { text: "Linear Interpolation" }
                ListElement { text: "Polyfit Interpolation" }
            }
            onActivated: {
                viewModel.changeAlgorithm(cbAlgorithm.currentValue)
            }
        }

        Text {
            Layout.maximumWidth: inputLayout.maxWidth
            text: "Lower:"
        }

        TextField {
            id: tfLower
            Layout.maximumWidth: inputLayout.maxWidth
            Layout.preferredWidth: 180
            text: viewModel.lowerInteropSize
            inputMask: "d99;\0"
        }

        Text {
            Layout.maximumWidth: inputLayout.maxWidth
            text: "Upper:"
        }

        TextField {
            id: tfUpper
            Layout.maximumWidth: inputLayout.maxWidth
            Layout.preferredWidth: 180
            text: viewModel.upperInteropSize
            inputMask: "d99;\0"
        }

        Button {
            id: calculateButton
            text: "Start"
            enabled: true
            onClicked: {
                try {
                    if (tfLower.text == "")
                        throw new Error("Lower bound is empty.");
                    if (tfUpper.text == "")
                        throw new Error("Higher bound is empty.");
                    
                    var lower = Number(tfLower.text);
                    var upper = Number(tfUpper.text);
                    if (lower > upper)
                        throw new Error("Lower value must not be higher than the upper value.");
                    if (lower < viewModel.minInteropSize)
                        throw new Error("Lower value too small. Minimum is: " + viewModel.minInteropSize);
                    if (upper > viewModel.maxInteropSize)
                        throw new Error("Upper value too big. Maximum is: " + viewModel.maxInteropSize);

                    viewModel.lowerInteropSize = Number(tfLower.text);
                    viewModel.upperInteropSize = Number(tfUpper.text);
                    viewModel.interpolate();
                }
                catch(e) {
                    errorDialog.text = e.message;
                    errorDialog.visible = true;
                }
            }
            Dialog {
                id: errorDialog
                property string text: ""
                title: qsTr("Error")
                modal: true
                standardButtons: Dialog.Ok

                Text {
                    text: errorDialog.text
                }
                onAccepted: {
                    tfLower.text = viewModel.lowerInteropSize
                    tfUpper.text = viewModel.upperInteropSize
                }
            }
        }
    }

    TableView {
        property int hoveredRow: -1

        id: table
        model: viewModel
        Layout.preferredHeight: 50
        Layout.preferredWidth: 50
        Layout.fillWidth: true; Layout.fillHeight: true
        topMargin: columnsHeader.implicitHeight
    
        columnWidthProvider: function (column) { 
            return table.model ? table.width/table.model.columnCount() : 0
        }
        onWidthChanged: table.forceLayout()

        Row {
            id: columnsHeader
            y: table.contentY
            z: 3
            Repeater {
                model: table.columns > 0 ? table.columns : 1
                Rectangle {
                    border.width: table.columns > 0 ? 1 : 0
                    implicitWidth: table.columnWidthProvider(modelData)
                    implicitHeight: 20
                    color: "#ACCAF0"
                    Text {
                        anchors.centerIn: parent
                        font.bold: true
                        text: viewModel.getColumnHeaderData(modelData)
                    }
                }
            }
        }

        delegate: Rectangle {
            z: 1
            id: itemDelegate
            border.width: 1
            implicitWidth: table.columnWidthProvider(column)
            implicitHeight: 20
            color: row == table.hoveredRow ? (row == viewModel.selectedRow ? "lightsteelblue" : "#DFDFDF") : (row == viewModel.selectedRow ? "lightsteelblue" : "white")

            Text {
                anchors.centerIn: parent
                text: model.display
            }

            MouseArea {
                id: _selectArea
                z: 2
                anchors.fill: parent
                hoverEnabled: true
                onClicked: {
                    viewModel.selectedRow = row
                }
                onEntered: {
                    table.hoveredRow = row
                }
                onExited: {
                    if (table.hoveredRow == row)
                        table.hoveredRow = -1
                }
            }
        }

        ScrollIndicator.horizontal: ScrollIndicator { }
        ScrollIndicator.vertical: ScrollIndicator { }
    }
}