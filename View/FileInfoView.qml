import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CellDataAnalyzerModel 1.0

ColumnLayout {
    property CellDataAnalyzerModel partModel: null

    Text {
        text: partModel.selectedValue == null ? "" : qsTr("Filepath: ") + partModel.selectedValue.fileinfo.filepath
    }
    Text {
        text: partModel.selectedValue == null ? "" : qsTr("Filesize: ") + partModel.selectedValue.fileinfo.file_size + qsTr(" KB")
    }
    Text {
        text: partModel.selectedValue == null ? "" : qsTr("Create date: ") + partModel.selectedValue.fileinfo.create_date
    }
    Text {
        text: partModel.selectedValue == null ? "" : qsTr("Last edit date: ") + partModel.selectedValue.fileinfo.last_edit_date
    }
}