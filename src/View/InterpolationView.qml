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
    }
}