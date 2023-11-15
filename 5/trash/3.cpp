#include <QApplication>
#include <QMainWindow>
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCharts/QValueAxis>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QMainWindow mainWindow;

    QLineSeries *series1 = new QLineSeries();
    QLineSeries *series2 = new QLineSeries();
    QLineSeries *series3 = new QLineSeries();

    QChart *chart1 = new QChart();
    QChart *chart2 = new QChart();
    QChart *chart3 = new QChart();

    QChartView *chartView1 = new QChartView(chart1);
    QChartView *chartView2 = new QChartView(chart2);
    QChartView *chartView3 = new QChartView(chart3);

    for (int i = 0; i < 10; ++i) {
        series1->append(i, i);
        series2->append(i, i*2);
        series3->append(i, i*3);
    }

    QVBoxLayout *layout = new QVBoxLayout();
    layout->addWidget(chartView1);
    layout->addWidget(chartView2);
    layout->addWidget(chartView3);

    QWidget *widget = new QWidget();
    widget->setLayout(layout);

    mainWindow.setCentralWidget(widget);

    mainWindow.show();

    return app.exec();
}
