function broken_line_chart(data) {

    var salaru_line = echarts.init(document.getElementById('broken_line'), 'infographic');
    window.addEventListener('resize', function () {
        salaru_line.resize();
    });
    // data ==> {'3室2厅': [26, 28, 42, 26, 22, 28, 22, 26, 32, 17, 22], '2室1厅': [25, 28, 27, 40, 33, 29, 28, 37, 30, 28, 32], '2室2厅': [37, 37, 36, 47, 34, 32, 32, 37, 36, 29, 31], '1室1厅': [35, 47, 44, 47, 44, 44, 31, 32, 34, 34, 34]}

    var Data1 = data['3室2厅'];
    var Data2 = data['2室2厅'];
    var Data3 = data['2室1厅'];
    var Data4 = data['1室1厅'];
    var date_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14];

    var option = {
    tooltip: {
        trigger: 'axis',
    },

    grid: {
        containLabel: true,
        left: '3%',
        right: '4%',
        bottom: '3%',

    },

    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: date_list

    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name:'3室2厅',
            type:'line',
            data:Data1
        },
        {
            name:'2室2厅',
            type:'line',
            data:Data2
        },
        {
            name:'2室1厅',
            type:'line',

            data:Data3
        },
        {
            name:'1室1厅',
            type:'line',

            data:Data4
        }
    ]
};

    salaru_line.setOption(option, true);
}