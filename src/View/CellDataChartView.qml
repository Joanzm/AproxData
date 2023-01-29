import QtQuick
import QtQuick.Controls
import QtCharts
import QDataGraph 1.0

Item {
    property QDataGraph viewModel: null

    Rectangle {
        anchors.fill: parent
        color: "#DFDFDF"

        ChartView {
            id: cellDataChartView
            anchors.fill: parent
            anchors.margins: 0
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
                target: viewModel
                function onSeriesAdded(key, value) { 

                    var series = cellDataChartView.createSeries(ChartView.SeriesTypeSpline, key, axisX, axisY);

                    value.forEach(entry => {
                        series.append(entry[0], entry[1]);
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
}