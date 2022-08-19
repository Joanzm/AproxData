import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import CellEntries 1.0
import CellDataAnalyzerModel 1.0
import AbcCellData 1.0
import OcvSocCellData 1.0
// import Graphing 1.0

ApplicationWindow {
    id: page
    visible: true
    width: 1200; height: 800
    title: "Cell Data Analyzer"
    property QtObject mainmodel: CellDataAnalyzerModel{ }

    menuBar: MenuBar {
        enabled: mainmodel.dataParser.workerFinished
        Menu {
            title: qsTr("Datei")
            MenuItem {
                text: qsTr("&Open")
                onTriggered: fileDialog.visible = true            
            }
            MenuItem {
                text: qsTr("Exit")               
                onTriggered: Qt.quit();
            }
        }
        Menu {
            title: qsTr("View")
            MenuItem {
                text: qsTr("Show all data in table")
                checkable: true
                checked: mainmodel.cellDataTable.viewAll
                onCheckedChanged: mainmodel.cellDataTable.viewAll = !mainmodel.cellDataTable.viewAll
            }
            MenuItem {
                text: qsTr("Show all graphs")
                checkable: true
                checked: mainmodel.cellDataGraph.viewAll
                onCheckedChanged: mainmodel.cellDataGraph.viewAll = !mainmodel.cellDataGraph.viewAll
            }
        }
    }

    GridLayout {
        anchors.fill: parent
        rows: 2; columns: 2
        rowSpacing: 2; columnSpacing: 2

        FileListView {
            partModel: mainmodel
            Layout.minimumWidth: 100; Layout.minimumHeight: 100
            Layout.preferredWidth: 50; Layout.preferredHeight: 80
            Layout.fillWidth: true; Layout.fillHeight: true
        }

        CellDataTableView {
            partModel: mainmodel
            Layout.minimumWidth: 100; Layout.minimumHeight: 100
            Layout.preferredWidth: 80; Layout.preferredHeight: 80
            Layout.fillWidth: true; Layout.fillHeight: true
        }

        // FileInfoView {
        //     partModel: mainmodel
        //     Layout.minimumWidth: 100; Layout.minimumHeight: 65
        //     Layout.preferredWidth: 100; Layout.preferredHeight: 50
        //     Layout.fillWidth: true; Layout.fillHeight: true
        // }

        CellDataChartView {
            partModel: mainmodel
            Layout.minimumWidth: 100; Layout.minimumHeight: 85
            Layout.preferredWidth: 80; Layout.preferredHeight: 80
            Layout.columnSpan: 2
            Layout.fillWidth: true; Layout.fillHeight: true
        }
    }

    FileDialog {
        id: fileDialog
        title: "Please choose a file"
        nameFilters: "XLS Files (*.xls)"
        fileMode: "OpenFiles"
        onAccepted: {
            mainmodel.dataParser.loadElements(fileDialog.selectedFiles)
        }
    }
}