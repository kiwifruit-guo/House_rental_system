$(document).ready(function () {

    // 注册
    $('#registe-btn').on('click', function () {
        $('#registeform').bootstrapValidator({
            message: 'This value is not valid',
            fields: {
                username: {
                    message: 'The username is not valid',
                    validators: {
                        notEmpty: {
                            message: '用户名不能为空'
                        },
                        stringLength: {
                            min: 6,
                            max: 30,
                            message: '用户名长度必须在6到30位之间'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9_\.]+$/,
                            message: '用户名只能包含大写、小写、数字和下划线'
                        },
                        different: {
                            field: 'password',
                            message: '用户名不能与密码相同'
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {
                            message: '邮箱不能为空'
                        },
                        emailAddress: {
                            message: '无效的邮箱地址'
                        }
                    }
                },
                password: {
                    validators: {
                        notEmpty: {
                            message: '密码不能为空'
                        },
                        identical: {
                            field: 'confirmPassword',
                            message: '与确认密码不一致'
                        },
                        different: {
                            field: 'username',
                            message: '密码不能与用户名相同'
                        }
                    }
                },
                confirmPassword: {
                    validators: {
                        notEmpty: {
                            message: '确认密码不能为空'
                        },
                        identical: {
                            field: 'password',
                            message: '与密码不一致'
                        },
                        different: {
                            field: 'username',
                            message: '确认密码不能与用户名相同'
                        }
                    }
                }
            }
        });
        var validator = $('#registeform').data("bootstrapValidator"); //获取validator对象
        validator.validate(); //手动触发验证
        if (validator.isValid()) { //通过验证
            $.ajax({
                type: 'post',
                url: '/register',
                data: $('#registeform').serialize(),
                dataType: 'json',
                success: function (result) {
                    if (result['valid'] == '0') {
                        alert(result['msg'])
                        var validatorObj = $("#registeform").data('bootstrapValidator');
                        if (validatorObj) {
                            $("#registeform").data('bootstrapValidator').destroy(); //或者 validatorObj.destroy(); 都可以，销毁验证
                            $('#registeform').data('bootstrapValidator', null);
                        }
                    } else {
                        window.location.href = "/user/" + result['msg'];
                    }
                },

            })
        }
    });

    // 登录
    $('#login-btn').on('click', function () {
        $('#loginform').bootstrapValidator({
            message: 'This value is not valid',
            fields: {
                username: {
                    message: 'The username is not valid',
                    validators: {
                        notEmpty: {
                            message: '用户名不能为空'
                        },
                        stringLength: {
                            min: 6,
                            max: 30,
                            message: '用户名长度必须在6到30位之间'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9_\.]+$/,
                            message: '用户名只能包含大写、小写、数字和下划线'
                        }
                    }
                },
                password: {
                    validators: {
                        notEmpty: {
                            message: '密码不能为空'
                        },
                        different: {
                            field: 'username',
                            message: '密码不能与用户名相同'
                        }
                    }
                }
            }
        }); //验证配置
        var validator = $('#loginform').data("bootstrapValidator"); //获取validator对象
        validator.validate(); //手动触发验证
        if (validator.isValid()) { //通过验证
            $.ajax({
                type: 'post',
                url: '/login',
                data: $('#loginform').serialize(),
                dataType: 'json',
                success: function (result) {
                    if (result['valid'] == '0') {
                        alert(result['msg'])
                        var validatorObj = $("#loginform").data('bootstrapValidator');
                        if (validatorObj) {
                            $("#loginform").data('bootstrapValidator').destroy(); //或者 validatorObj.destroy(); 都可以，销毁验证
                            $('#loginform').data('bootstrapValidator', null);
                        }
                    } else {
                        href_str = "/user/" + result['msg'];

                        window.location.replace(href_str);
                    }
                },

            })
        }
    });
// 退出
$("#logout").on('click', function () {
    $.ajax({
        url: '/logout',
        type: 'get',
        dataType: 'json',
        success: function (res) {
            // 退出成功
            if (res["valid"] == '1') {
                alert(res["msg"]);
                window.location.href = '/';
            } else {
                // 退出失败
                alert(res["msg"]);
            }
        }
    })
});
});