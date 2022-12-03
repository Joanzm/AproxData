import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import OcvSocDataViewModel 1.0
import CellEntries 1.0
import AbcData 1.0
import OcvSocCellData 1.0

ColumnLayout {
    property OcvSocDataViewModel viewModel: null

    Keys.onPressed: (event) => { 
        if (event.key == Qt.Key_F5) 
            viewModel.reloadSingleElementByIndex(_lv.currentIndex)
    }

    ListView {
        Layout.fillHeight: true
        Layout.fillWidth: true

        id: _lv
        model: viewModel
        currentIndex: viewModel.selectedIndex

        highlightResizeDuration: 0
        highlightResizeVelocity: -1 

        delegate: Item {
            id: _lvItem
            width: ListView.view.width
            height: 45

            MouseArea {
                id: _itemArea
                anchors.fill: parent
                onClicked: viewModel.selectedIndex = index
                hoverEnabled: true

                Rectangle {
                    id: _lvRectangle
                    color: _itemArea.containsMouse ? !_lvItem.ListView.isCurrentItem ? "#DFDFDF" : "Transparent" : "Transparent"
                    width: _lvItem.width
                    height: _lvItem.height

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 10
                        anchors.rightMargin: 10

                        Grid {
                            Layout.fillWidth: true

                            spacing: 1
                            rows: 2
                            verticalItemAlignment: Grid.AlignVCenter

                            Text { 
                                text: model.celldata.fileInfo.fileName
                            }

                            Grid {
                                verticalItemAlignment: Grid.AlignVCenter
                                horizontalItemAlignment: Grid.AlignHCenter
                                spacing: 2
                                columns: 3

                                Text { 
                                    text: model.celldata.stateStr
                                    color: {
                                        if (model.celldata.stateInt == 0) {
                                            return "gray";
                                        }
                                        else if (model.celldata.stateInt == 1) {
                                            return "orange";
                                        }
                                        else if (model.celldata.stateInt == 3) {
                                            return "red";
                                        }
                                        else {
                                            return "green";
                                        }
                                    }

                                    MouseArea {
                                        id: _errMouseArea
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        propagateComposedEvents: true
                                    }

                                    ToolTip.visible: _errMouseArea.containsMouse && model.celldata.stateInt == 3 
                                    ToolTip.text: model.celldata.exceptionMessage
                                }

                                Text {
                                    id: _infoText
                                    text: " _i_ "
                                    color: _infoMouseArea.containsMouse ? "green" : "black"

                                    MouseArea {
                                        id: _infoMouseArea
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        propagateComposedEvents: true
                                    }

                                    ToolTip.visible: _infoMouseArea.containsMouse
                                    ToolTip.text: model.celldata.fileInfo.strDisplay
                                }

                                Text {
                                    text: "(Reload on F5)"
                                    visible: _lvItem.ListView.isCurrentItem && viewModel.runnerFinished
                                }
                            }
                        }

                        Button {
                            Layout.maximumWidth: 25
                            Layout.minimumWidth: 25

                            text: "X"
                            enabled: viewModel.runnerFinished
                            onClicked: {
                                viewModel.removeData(index)
                            }
                        }
                    }
                }
            }
        }

        highlight: Rectangle { color: "lightsteelblue"; radius: 2 }
        ScrollIndicator.horizontal: ScrollIndicator { }
        ScrollIndicator.vertical: ScrollIndicator { }
    }

    RowLayout {
        Layout.alignment: "AlignBottom"
        Layout.fillWidth: true

        Button {
            Layout.fillWidth: true

            id: loadButton
            text: "Load"
            enabled: viewModel.runnerFinished
            onClicked: {
                xlsFileDialog.visible = true
            }

            FileDialog {
                id: xlsFileDialog
                title: "Please choose a file"
                nameFilters: "XLS Files (*.xls)"
                fileMode: "OpenFiles"
                onAccepted: {
                    viewModel.loadElements(xlsFileDialog.selectedFiles)
                }
            }
        }

        Button {
            Layout.fillWidth: true

            id: clearButton
            text: "Clear"
            enabled: viewModel.runnerFinished && viewModel.hasData
            onClicked: {
                if (viewModel.hasData) {
                    yesNoClearDialog.visible = true
                }  
            }

            Dialog {
                id: yesNoClearDialog
                title: qsTr("Clear data")
                modal: true
                standardButtons: Dialog.Yes | Dialog.No

                Text {
                    text: "Do you really want to clear the current loaded data?"
                }

                onAccepted: {
                    viewModel.clearData()
                }
            }
        }
    }
}