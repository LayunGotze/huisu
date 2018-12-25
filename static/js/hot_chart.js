/**
 * Created by gaoyunchu on 18/12/25.
 */

//  根据时间绘制热度曲线函数
function draw_chart(data, container_id, chart_name) {
    //绘制热度和情感值曲线
    //data是返回数据，container_id是要绘制的DIV标签的id,chart_name是表格名称
    var chart = null;
    var color_sentiment = "#D32361";
    var color_heat = "#1D6DBE";
    var color_zeroLine = "#DC143C";
    var item_distance = 200;
    var chart = null;
    var hot_max = data['max_value'];
    var hot_min = data['min_value'];
    chart = Highcharts.chart(container_id, {
        chart: {
            zoomType: 'x'
        },
        title: {
            text: chart_name
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                millisecond: '%H:%M:%S.%L',
                second: '%H:%M:%S',
                minute: '%H:%M',
                hour: '%H:%M',
                day: '%m-%d',
                week: '%m-%d',
                month: '%Y-%m',
                year: '%Y'
            }
        },
        tooltip: {
            dateTimeLabelFormats: {
                millisecond: '%H:%M:%S.%L',
                second: '%H:%M:%S',
                minute: '%H:%M',
                hour: '%H:%M',
                day: '%Y-%m-%d',
                week: '%m-%d',
                month: '%Y-%m',
                year: '%Y'
            }
        },
        yAxis: [
            {//热度值
                gridLineWidth: 0,//去掉 Y 轴的参照横线
                max: hot_max, //设置最大值
                min: hot_min,//设置最大值
                startOnTick: false,//曲线起始允许不在刻度线上
                endOnTick: false,//曲线终止允许不在刻度线上
                opposite: true,  //该曲线参考轴在右侧
                title: { // y 轴的title
                    text: ''
                },
                labels: {  //刻度线字符的颜色
                    style: {
                        color: color_heat
                    }
                }
            }
        ],
        legend: {
            enabled: true
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },
        series: [{
            type: 'area',
            name: '热度',
            data: data["hot"],
            yAxis: 0,
            selected: true
        },
        ]
    });
}