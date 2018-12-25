/**
 * Created by gaoyunchu on 18/12/25.
 */
function draw_rank_chart(data, container_id, chart_name, key_name, value_name) {
    //绘制热度和情感值曲线
    //data是返回数据，container_id是要绘制的DIV标签的id,chart_name是表格名称
    //key_name是data的键名称,value_name是data的值名称
    var chart = null;
    var color_sentiment = "#D32361";
    var color_heat = "#1D6DBE";
    var color_zeroLine = "#DC143C";
    var item_distance = 200;
    var chart = null;
    chart = Highcharts.chart(container_id, {
        chart: {
            type: 'line'
        },
        title: {
            text: chart_name
        },
        xAxis: {
            categories: data[key_name]
        },
        tooltip: {
        },
        yAxis: [
            {//热度值
                gridLineWidth: 0,//去掉 Y 轴的参照横线
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
            name: '人物热度',
            data: data[value_name],
            yAxis: 0,
            selected: true
        },
        ]
    });
}