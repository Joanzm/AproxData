import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import AbcVmInterpolation 1.0

Item {
    property AbcVmInterpolation viewModel: null

    Rectangle {
        anchors.fill: parent
        color: "black"

        ScrollView {
            anchors.fill: parent
            anchors.margins: 2

            TextArea {
                id: lookUpTextField   
                readOnly: true         
                Connections {
                    target: viewModel
                    function onSelectedRowChanged(value) {
                        lookUpTextField.text = viewModel.lookUpTable
                    }
                }
            }
        }
    }
}