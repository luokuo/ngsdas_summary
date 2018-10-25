之前做的登陆是每刷新一次才显示最新剩余时间，我们在此基础之上做了动态生成倒计时，
实时查看剩余时间，当剩余时间为0时提示可重新登陆
在views.py中登陆的get请求要传到前端参数：
{'username': username, 'checked': checked, 'outtime': outtime, 'minu': minu, 'seco': seco})
这样下面的js才能获取到。
根据前端传来的过期时间来判断是否要有倒计时，当过期时间大于等于0时，则进入倒计时



    <script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
    <script>
        $(function () {
            var change1 = $("#btn").click(function () {
                var username = $('#username').val();
                var pwd = $('#password').val();
                var remember = $('input[name="remember"]').prop('checked');
                var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();

                var params = {
                    username: username,
                    pwd: pwd,
                    remember: remember,
                    csrfmiddlewaretoken: csrfmiddlewaretoken
                };

                $.post('{% url 'login' %}', params, function (data) {

                    if (data.res == 1) {
                        // 跳转页面
                        location.href = data.next_url;
                    } else if (data.res == 2) {
                        var msg2 = "用户未激活,剩余登陆次数为:" + data.ip_surplus;
                        $("#msg").html(msg2);
                    } else if (data.res == 0) {
                        var msg0 = "用户名或者密码错误,剩余登陆次数为:" + data.ip_surplus;
                        $("#msg").html(msg0);
                    } else if (data.res == 3) {
                        var msg3 = "数据不完整,剩余登陆次数为:" + data.ip_surplus;
                        $("#msg").html(msg3);
                    } else if (data.res == 4) {
                        if (data.outtime == 1800) {
                            $("#msg").html('登陆错误次数过多!请30分钟之后登陆');
                            location.reload();
                        }
                    }
                })
            });


        })
    </script>
    {% if outtime >= 0 %}

        <script type="text/javascript">
            var timer = null;
            window.onload = function () {
                //定义倒计时的时间(倒计时30分钟59秒)
                var minutes = {{ minu }};
                var seconds = {{ seco }};

                function show() {
                    //判断时间到了没
                    {#		if(seconds==0&&minutes==0){#}
                    {#			clearInterval(timer);//清除定时器#}
                    {#			document.getElementById("msg").innerHTML = '时间到,您可以继续登陆';#}
                    {#			return;#}
                    {#		}#}
                    seconds--;
                    if (seconds < 0) {
                        seconds = 59;
                        minutes--;
                    }
                    minutes = (minutes + "").length == 1 ? "0" + minutes : minutes;//(minutes+"")是将其数据类型转换成字符串类型
                    seconds = (seconds + "").length == 1 ? "0" + seconds : seconds;
                    if (minutes == 0) {
                        document.getElementById("msg").innerHTML = '登陆错误次数过多!请' + seconds + '秒之后再登陆';
                        if (seconds == 0) {
                            clearInterval(timer);
                            document.getElementById("msg").innerHTML = '时间到,您可以继续登陆';
                            return;
                        }
                    } else {
                        document.getElementById("msg").innerHTML = '登陆错误次数过多!请' + minutes + '分' + seconds + '秒之后再登陆'
                    }

                }

                //开启定时器
                timer = setInterval(show, 1000);
            }
        </script>

