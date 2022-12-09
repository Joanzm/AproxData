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
            z: 2
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
                        text: viewModel.headerData(modelData, Qt.Horizontal)
                    }
                }
            }
        }

        delegate: Rectangle {
            border.width: 1
            implicitWidth: table.columnWidthProvider(column)
            implicitHeight: 20

            Text {
                anchors.centerIn: parent
                text: model.display
            }
        }

        ScrollIndicator.horizontal: ScrollIndicator { }
        ScrollIndicator.vertical: ScrollIndicator { }
    }
}