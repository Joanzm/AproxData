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

                var series = cellDataChartView.createSeries(ChartView.SeriesTypeSpline, value.fileinfo.filepath, axisX, axisY);

                value.data.forEach(entry => {
                    var p = entry.point
                    series.append(p.x, p.y);
                });

                //Calculate graph min and max value for axis
                var xMin = Number.POSITIVE_INFINITY;
                var yMin = Number.POSITIVE_INFINITY;
                var xMax = Number.NEGATIVE_INFINITY;
                var yMax = Number.NEGATIVE_INFINITY;
                for (var i=0;i<cellDataChartView.count;i++){
                    series = cellDataChartView.series(i);

                    var minPoint = series.at(0);
                    if (minPoint.x < xMin){
                        xMin = minPoint.x;
                    }
                    if (minPoint.y < yMin){
                        yMin = minPoint.y;
                    }

                    var maxPoint = series.at(series.count - 1);
                    if (maxPoint.x > xMax){
                        xMax = maxPoint.x;
                    }
                    if (maxPoint.y > yMax){
                        yMax = maxPoint.y;
                    }
                }

                // Calulate extra space for graph between graph and axis
                var graphXSpacing = (xMax - xMin) / 20;
                var graphYSpacing = (yMax - yMin) / 20;
                axisX.min = xMin - graphXSpacing;
                axisY.min = yMin - graphYSpacing;
                axisX.max = xMax + graphXSpacing;
                axisY.max = yMax + graphYSpacing;
            }
            function onSeriesCleared() {
                cellDataChartView.removeAllSeries();
            }
        }
    }
}