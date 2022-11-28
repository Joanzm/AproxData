import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CellDataAnalyzerModel 1.0

ListView {
    property CellDataAnalyzerModel viewModel: null
    id: barCtrl
    width: 80

    model: ListModel {
        ListElement {
            tabName: qsTr("Data")
            iconPath: qsTr("555 3264")
        }
        ListElement {
            tabName: qsTr("Interpolation")
            iconPath: qsTr("555 8426")
        }
    }
    orientation: ListView.Vertical

    delegate: Item {
        id: barCtrlItem
        width: parent.width
        height: 30
        Text {
            width: barCtrlItem.width
            height: barCtrlItem.height
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter

            text: model.tabName
        }
        MouseArea {
            width: barCtrlItem.width
            height: barCtrlItem.height
            onClicked: barCtrl.currentIndex = index
        }
    }
    highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
}