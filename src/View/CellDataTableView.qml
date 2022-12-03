import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import OcvSocCellDataTable 1.0

TableView {
    property OcvSocCellDataTable viewModel: null
    id: table
    model: viewModel
    //leftMargin: rowsHeader.implicitWidth
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