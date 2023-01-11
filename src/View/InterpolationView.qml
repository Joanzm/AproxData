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
            Layout.maximumWidth: inputLayout.maxWidth
            Layout.preferredWidth: 180
        }

        Text {
            Layout.maximumWidth: inputLayout.maxWidth
            text: "Higher:"
        }

        TextField {
            Layout.maximumWidth: inputLayout.maxWidth
            Layout.preferredWidth: 180
        }

        Button {
            id: calculateButton
            text: "Start"
            enabled: true
            onClicked: {
                viewModel.interpolate()
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

        /*MouseArea {
            id: _tableArea
            z: 100
            anchors.fill: parent
            hoverEnabled: true
            onExited: {
                console.log(table.currentRow)
                table.hoveredRow = -1
            }
        }*/

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