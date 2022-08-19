import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CellDataAnalyzerModel 1.0

ScrollView {
    property CellDataAnalyzerModel partModel: null

    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
    ScrollBar.vertical.policy: ScrollBar.AsNeeded

    TableView {
        id: table
        model: partModel.cellDataTable
        
        columnWidthProvider: function (column) { 
            return table.model ? table.width/table.model.columnCount() : 0
        }
        onWidthChanged: table.forceLayout()

        delegate: Rectangle {
            border.width: 1
            implicitWidth: table.columnWidthProvider(column)
            implicitHeight: 20

            Text {
                text: model.display
                anchors.centerIn: parent
            }
        }
    }
}