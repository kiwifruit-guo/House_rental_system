// function getdata1(data) {
//     var center1 = echarts.init(document.getElementById('f_line'), 'infographic');
//     window.addEventListener('resize', function () {
//         center1.resize();
//     });
//
//     var myRegression = ecStat.regression('linear', data);
//
//     myRegression.points.sort(function (a, b) {
//         return a[0] - b[0];
//     });
//
//     option = {
//         title: {
//             subtext: '根据最近的房价，预测价格走势',
//             left: 'center',
//         },
//
//         tooltip: {
//             trigger: 'axis',
//             axisPointer: {
//                 type: 'cross'
//             }
//         },
//
//         grid: {
//             show: true,//是否显示直角坐标系的网格,true显示，false不显示
//             left: '13%',//grid组件离容器左侧的距离
//             containLabel: false,//grid 区域是否包含坐标轴的刻度标签，在无法确定坐标轴标签的宽度，容器有比较小无法预留较多空间的时候，可以设为 true 防止标签溢出容器。
//
//         },
//
//
//         xAxis: {
//             type: 'value',
//             height: '100px',
//             splitLine: {
//                 lineStyle: {
//                     type: 'dashed'
//                 }
//             },
//         },
//         yAxis: {
//             type: 'value',
//             min: 1.5,
//             splitLine: {
//                 lineStyle: {
//                     type: 'dashed'
//                 }
//             },
//         },
//         series: [{
//             name: '分散值(实际值)',
//             type: 'scatter',
//             label: {
//                 emphasis: {
//                     show: true,
//                     position: 'left',
//                     textStyle: {
//                         color: 'blue',
//                         fontSize: 12
//                     }
//                 }
//             },
//             data: data
//         }, {
//             name: '线性值(预测值)',
//             type: 'line',
//             showSymbol: false,
//             data: myRegression.points,
//             markPoint: {
//                 itemStyle: {
//                     normal: {
//                         color: 'transparent'
//                     }
//                 },
//                 label: {
//                     normal: {
//                         show: true,
//                         position: 'left',
//                         formatter: myRegression.expression,
//                         textStyle: {
//                             color: '#333',
//                             fontSize: 12
//                         }
//                     }
//                 },
//                 data: [{
//                     coord: myRegression.points[myRegression.points.length - 1]
//                 }]
//             }
//         }]
//     };
//     center1.setOption(option, true);
//
// }
function getdata1(data) {
    var myChart = echarts.init(document.getElementById('pie'));

    window.addEventListener('resize', function () {
        myChart.resize();
    });

    var option = {
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)",
        },

        series:[{

            name: '户型的占比',

            type: 'pie',

            radius: ['10%', '50%'],
            center: ['50%', '50%'],

            labelLine: {

                normal: {
                    show: true
                },
                // 选中后加重表现
                emphasis: {
                    show: true
                }
            },
            // 饼状图的内部名字
            label: {
                normal: {
                    show: true
                },
                emphasis: {
                    show: true
                }
            },
            //
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            },
            data: data,
        }]
    };

    myChart.setOption(option);
}