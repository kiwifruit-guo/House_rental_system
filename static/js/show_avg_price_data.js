function avg_price_chart(data) {

    var salaru_line = echarts.init(document.getElementById('avg_price_line'));
    window.addEventListener('resize', function () {
        salaru_line.resize();
    });
    // var XData=['东方凤雅台', '仙桐御景', '仙湖山庄二期', '仙湖枫景家园', '兰亭国际公寓', '华景园御庭轩', '合正锦园一期', '名骏豪庭', '广岭家园', '新世界四季御园', '新世界鹿茵翠地', '桐景花园', '聚宝华府', '金色年华家园', '鸿景翠峰', '鹏兴花园一期', '鹏兴花园三期', '鹏兴花园二期', '鹏兴花园六期', '鹏莲花园'];
    // var yData=[1, 1, 1, 3, 1, 1, 1, 3, 4, 1, 1, 1, 2, 2, 1, 2, 1, 8, 1, 1];
    // {'name_list_x': name_list, 'num_list_y': num_list}
    var XData = data['name_list_x'];
    var yData = data['price_list_y'];

    var dataMin = parseInt(Math.min.apply(null, yData)/2);

    var option = {
        backgroundColor: "#fff",
        grid: {
            height:'200px'
        },
        xAxis: {
            axisTick: {
                show: false
            },
            splitLine: {
                show: false
            },
            splitArea: {
                show: false
            },
            data: XData,
            axisLabel: {
                formatter: function (value) {
                    var ret = ""; //拼接加\n返回的类目项
                    var maxLength = 1; //每项显示文字个数
                    var valLength = value.length; //X轴类目项的文字个数
                    var rowN = Math.ceil(valLength / maxLength); //类目项需要换行的行数
                    if (rowN > 1) //如果类目项的文字大于3,
                    {
                        for (var i = 0; i < rowN; i++) {
                            var temp = ""; //每次截取的字符串
                            var start = i * maxLength; //开始截取的位置
                            var end = start + maxLength; //结束截取的位置
                            //这里也可以加一个是否是最后一行的判断，但是不加也没有影响，那就不加吧
                            temp = value.substring(start, end) + "\n";
                            ret += temp; //凭借最终的字符串
                        }
                        return ret;
                    } else {
                        return value;
                    }
                },
                interval: 0,
                fontSize: 11,
                fontWeight: 100,
                textStyle: {
                    color: '#555',

                }
            },
            axisLine: {
                lineStyle: {
                    color: '#4d4d4d'
                }
            }
        },
        yAxis: {
            axisTick: {
                show: false
            },
            splitLine: {
                show: false
            },
            splitArea: {
                show: false
            },
            min: dataMin,
            axisLabel: {
                textStyle: {
                    color: '#9faeb5',
                    fontSize: 16,
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#4d4d4d'
                }
            }
        },
        "tooltip": {
            "trigger": "item",
            "textStyle": {
                "fontSize": 12
            },
            "formatter": "{b0}: {c0}元/㎡"
        },
        series: [{
            type: "bar",
            itemStyle: {
                normal: {
                    color: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: '#00d386' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: '#0076fc' // 100% 处的颜色
                        }],
                        globalCoord: false // 缺省为 false
                    },
                    barBorderRadius: 15,
                }
            },
            // barWidth: 7,
            data: yData
        }
        ]
    };

    salaru_line.setOption(option, true);
}