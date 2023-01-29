import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CellDataAnalyzerViewModel 1.0

ColumnLayout {
    property CellDataAnalyzerViewModel partModel: null

    Text {
        text: partModel.selectedValue == null ? "" : qsTr("Filepath: ") + partModel.selectedValue.fileInfo.filepath
    }
    Text {
        text: partModel.selectedValue == null ? "" : qsTr("Filesize: ") + partModel.selectedValue.fileInfo.fileSize + qsTr(" KB")
    }
    Text {
        text: partModel.selectedValue == null ? "" : qsTr("Create date: ") + partModel.selectedValue.fileInfo.createDate
    }
    Text {
        text: partModel.selectedValue == null ? "" : qsTr("Last edit date: ") + partModel.selectedValue.fileInfo.lastEditDate
    }
}