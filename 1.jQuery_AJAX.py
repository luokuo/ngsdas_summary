用Ajax的好处是省去form表单的整个页面的刷新，Ajax采用的是局部刷新，效率更高，用户体验更好

Ajax是通过两个data来完成的数据传输，djax当中的参数data是传给后台的数据，success中的data是后台传给前端的数据，
只要搞清楚这两个data就明白了ajax。剩下的就是固定的格式和不同的方法啦

1.当选择不同的下拉菜单是刷新出不同的内容：
	监听id为id_Panel的下拉菜单；
	对这个变量进行change
<select name="Panel" required="" id="id_Panel">
  <option value="" selected="">---------</option>

  <option value="1">NovoPM</option>

  <option value="2">诺禾新筛</option>

  <option value="3">NovoPM2.0</option>

</select>

    <script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
    <script>
        $(function () {
            var change1 = $("#id_Panel").change(function () {

                $.ajax({
                    url: '{% url 'get_field' %}',
                    type: 'GET',
                    data: {'panel': change1.val()},#这个data是要传给后台的数据
                    success: function (data) { #这个data是后台传给前端的数据
                        if (data) {

                            $("#message").html(data);
                        } else {
                            alert('添加失败')
                        }
                    }

                })
            });


        })
    </script>

2.登陆中用到的Ajax：点击事件，当用户点击id为btn的提交按钮时发生数据的传输，注意每个标签中的name为什么，
  那么后端request.POST.get（）或request.GET.get（）里对应的内容就是什么
  比如：前端<input id="password" type="password" name="pwd" class="pass_input" placeholder="请输入密码">
		后端password = request.POST.get('pwd')

<input  type="submit" name="" value="登录" class="input_submit" id="btn">
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
				#post请求$.post('路径',传给后台的参数,对后台数据处理的函数function(data){})
                $.post('{% url 'login' %}', params, function (data) {
                    if (data.res == 1) {
                        // 跳转页面
                        location.href = data.next_url;
                    } else if (data.res == 2) {
                        alert("用户未激活");
                        alert(data.ip_surplus)
                    } else if (data.res == 0) {
                        alert("用户名或者密码错误,剩余登陆次数为:" + data.ip_surplus);
                    } else if (data.res == 3) {
                        alert("数据不完整,剩余登陆次数为:" + data.ip_surplus);
                    }else if (data.res == 4) {
                        var min = parseInt(data.outtime/60);
                        var sec = (data.outtime%60);
                        if (min == 0) {
                            alert('登陆错误次数超过十次,休息休息!请'+ sec +'秒之后再来');
                        }else {
                            alert('登陆错误次数超过十次,休息休息!请'+ min +'分'+ sec +'秒之后再来');
                        }
                    }
                })
            });
        })
    </script>
	
	
总结：
1.Ajax最主要的是搞清楚两个data，另外弄清楚不管是点击事件还是change等都是对前端的标签发生的，里面包含着对后端传输的参数
2.在jQuery中AJAX的写法有3种，$.ajax，$.post，$.get这三种。
  其中$.post和$.get是简易写法，高层的实现，在调用他们的时候，会运行底层封装好的$.ajax。
        $(function () {
            var change1 = $("标签").事件(function () {
				var 参数1；
				var 参数2；
				......
				};
				==================
				方式一：
				$.ajax({
					url:"",    //请求的url地址
					dataType:"json",   //返回格式为json
					async:true,//请求是否异步，默认为异步，这也是ajax重要特性
					data:{"id":"value"},    //参数值,键值对
					type:"GET",   //请求方式
					beforeSend:function(){
						//请求前的处理
					},
					success:function(req){
						//请求成功时处理
					},
					complete:function(){
						//请求完成的处理
					},
					error:function(){
						//请求出错处理
					}
				});
				=======================
				方式二
				 $.get("url",{传递到后端参数},function(传递到前端的参数data){逻辑处理});
				 $.post("url",{传递到后端参数},function(传递到前端的参数data){逻辑处理});
				=======================
			})
		)

3.jQuery的事件有很多，可随便百度，常用的click,change,keydown,keyup,keypress,mouse事件等
	可参考：http://www.w3school.com.cn/jquery/jquery_ref_events.asp
			https://blog.csdn.net/ziwutong88/article/details/53701531
			https://blog.csdn.net/tanga842428/article/details/52432026
	

