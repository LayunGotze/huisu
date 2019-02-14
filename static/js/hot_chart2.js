//Created by gaoyunchu on 19/2/14
//根据数据绘制echarts时间热度折线图
function draw_hot_charts(id, title, data) {
    var timeline_chart = echarts.init(document.getElementById(id));
    var timeline_option = {
        title: {
            text: title
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: data['legend']
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: data['time']
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: data['data']
    };
    timeline_chart.setOption(timeline_option);
}