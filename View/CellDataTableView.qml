import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CellDataAnalyzerModel 1.0

ScrollView {
    property CellDataAnalyzerModel partModel: null

    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
    ScrollBar.vertical.policy: ScrollBar.AsNeeded

    TableView {
        id: cellDataView
        model: partModel.celldataview
        
        columnWidthProvider: function (column) { 
            return cellDataView.model ? cellDataView.width/cellDataView.model.columnCount() : 0
        }
        onWidthChanged: cellDataView.forceLayout()

        delegate: Rectangle {
            border.width: 1
            implicitWidth: cellDataView.columnWidthProvider(column)
            implicitHeight: 20

            Text {
                text: model.display
                anchors.centerIn: parent
            }
        }
    }
}