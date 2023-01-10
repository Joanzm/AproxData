import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import OcvSocInterpolation 1.0

Item {
    property OcvSocInterpolation viewModel: null

    Rectangle {
        anchors.fill: parent
        color: "black"

        ScrollView {
            anchors.fill: parent
            anchors.margins: 2

            TextArea {
                id: lookUpTextField            
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