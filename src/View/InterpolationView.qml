import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import OcvSocInterpolation 1.0

RowLayout {
    property OcvSocInterpolation viewModel: null
    id: interpolationView
    
    ColumnLayout {
        anchors.topMargin: 100
        anchors.leftMargin: 100
        Layout.preferredHeight: 50
        Layout.preferredWidth: 50
        spacing: 5

        Text {
            text: "Interpolation: Here you can analyze the loaded data and create look up tables for algorithm implementation :)"
        }

        Text {
            text: "Lower:"
        }

        TextField {

        }

        Text {
            text: "Higher:"
        }

        TextField {

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