import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import CellEntries 1.0
import CellDataAnalyzerModel 1.0
import AbcCellData 1.0
import OcvSocCellData 1.0

ColumnLayout {
    property CellDataAnalyzerModel partModel: null

    Keys.onPressed: (event) => { 
        if (event.key == Qt.Key_F5) 
            partModel.reload_single_element_by_index(_lv.currentIndex)
    }

    ScrollView {
        Layout.leftMargin: 10
        Layout.fillHeight: true
        Layout.fillWidth: true

        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        ScrollBar.vertical.policy: ScrollBar.AsNeeded

        ListView {
            id: _lv
            spacing: 5
            model: partModel.model
            currentIndex: partModel.model.selectedIndex
            delegate: Item {
                id: _lvItem
                width: ListView.view.width
                height: 45

                MouseArea {
                    id: _itemArea
                    anchors.fill: parent
                    onClicked: partModel.model.selectedIndex = index
                    hoverEnabled: true

                    Rectangle {
                        id: _lvRectangle
                        color: _itemArea.containsMouse ? !_lvItem.ListView.isCurrentItem ? "#DFDFDF" : "Transparent" : "Transparent"
                        anchors.leftMargin: 20
                        width: _lvItem.width
                        height: _lvItem.height

                        Grid {
                            anchors.verticalCenter: _lvRectangle.verticalCenter
                            verticalItemAlignment: Grid.AlignVCenter

                            rows: 2
                            spacing: 1

                            Text { 
                                text: model.celldata.fileinfo.filename
                            }

                            Grid {
                                verticalItemAlignment: Grid.AlignVCenter
                                horizontalItemAlignment: Grid.AlignHCenter
                                columns: 3
                                spacing: 2
                                Text { 
                                    text: model.celldata.state_str
                                    color: {
                                        if (model.celldata.state_int == 0) {
                                            return "gray";
                                        }
                                        else if (model.celldata.state_int == 1) {
                                            return "orange";
                                        }
                                        else if (model.celldata.state_int == 3) {
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

                                    ToolTip.visible: _errMouseArea.containsMouse && model.celldata.state_int == 3 
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
                                    ToolTip.text: model.celldata.fileinfo.strDisplay
                                }
                                Text {
                                    text: "(Reload on F5)"
                                    visible: _lvItem.ListView.isCurrentItem && partModel.worker_finished
                                }
                            }
                        }
                    }
                }
            }

            highlight: Rectangle { color: "lightsteelblue"; radius: 2 }
        }
    }

    Button {
        id: loadButton
        Layout.alignment: "AlignBottom"
        Layout.fillWidth: true
        text: "Load"
        enabled: partModel.worker_finished
        onClicked: {
            fileDialog.visible = true
        }
    }
}