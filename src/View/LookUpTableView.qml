import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import OcvSocInterpolation 1.0

Rectangle {
    property OcvSocInterpolation viewModel: null
    color: "white"

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