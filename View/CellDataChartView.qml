import QtQuick
import QtQuick.Controls
import QtCharts
import CellDataAnalyzerModel 1.0

Rectangle {
    property CellDataAnalyzerModel partModel: null

    ChartView {
        id: cellDataChartView
        x: 0
        y: 0
        width: parent.width
        height: parent.height
        antialiasing: true

        ValueAxis {
            id: axisX
            min: 2.5
            max: 4.5
        }

        ValueAxis {
            id: axisY
            min: -0.1
            max: 1.1
        }

        Connections {
            target: partModel.cellDataGraph
            function onSeriesAdded(value) { 
                var series = cellDataChartView.createSeries(ChartView.SeriesTypeSpline, value.fileinfo.filepath, axisX, axisY)
                value.data.forEach(entry => {
                    var p = entry.point
                    series.append(p.x, p.y)
                });
            }
            function onSeriesCleared() {
                cellDataChartView.removeAllSeries();
            }
        }
    }
}