参考链接：https://blog.csdn.net/Ayhan_huang/article/details/78094570?locationNum=9&fps=1
参考git源码：https://github.com/Ayhan-Huang/RBAC

1.概述
RBAC(Role-Based Access Control,基于角色的访问控制)，通过角色绑定权限，
然后给用户划分角色。在web应用中，可以将权限理解为url，一个权限对应一个url。

2.设计表结构
基于上述分析，在设计表关系时，起码要有4张表：用户，角色，权限，菜单：
用户可以绑定多个角色，从而实现灵活的权限组合 ：用户和角色，多对多关系
每个角色下，绑定多个权限，一个权限也可以属于多个角色：角色和权限，多对多关系
一个权限附属在一个菜单下，一个菜单下可以有多个权限：菜单和权限：多对一关系
一个菜单下可能有多个子菜单，也可能有一个父菜单：菜单和菜单是自引用关系
其中角色和权限、用户和角色，是两个多对多关系，由Django自动生成另外两种关联表。因此一共会产生6张表，用来实现权限管理。

3.权限的初始化和验证
因为Http是无状态协议，我们只能通过session会话管理，将请求之间需要”记住“的信息保存在session中。
用户登录成功后，可以从数据库中取出该用户角色下对应的权限信息，并将这些信息写入session中。

*******************
因为每次发送请求都会经过中间件，所以为了避免每次访问一个url就要调用下后面的菜单结构，所以我们直接在初始化session的时候将菜单
结构定下来，就不在菜单显示的时候做处理啦
*******************

3.1提取用户权限信息，并写入session,注意此时我们已经把菜单的结构写入到了session中----init_permission.py
可以在项目的settings中指定session保存权限信息的key
3.2检查用户权限，控制访问---中间件
说明：
有些访问不需要权限，或者在测试时，我们可以在settings中配置一个白名单；
将登录的url写入settings中，增强可移植性；
url本质是正则表达式，在匹配用户请求的url是否在其权限范围内时，需要作严格匹配，这个也可以在settings中配置
中间件定义完成后，加入settings中的MIDDLEWARE列表中最后面（加到前面可能还没有session信息）

4.菜单显示
用户登录后，应该根据其权限，显示其可以操作的菜单。前面我们我们已经将用户的权限和菜单信息保存在了request.session中，
因此如何从中提取信息，并将其渲染成页面显示的菜单，就是接下来要解决的问题。
提取信息很简单，因为在用户登录后调用init_permission初始化权限时，
已经将权限和菜单信息进行了初步处理，并写入了session，这里只需要通过key将信息取出来即可。
4.1自定义标签
我们通过自定义标签来实现：
它接收request参数，从中提取session保存的权限和菜单数据（菜单数据在初始化权限时已经做了结构化处理）；
将数据渲染为html字符串。
注意：自定义标签需要用到定义标签的装饰器，但先要注册：register = template.Library()，
因为我们用简单便签就可以，所以用@register.simple_tag
4.2渲染菜单
多级菜单需要用到递归
主要还是拼串


总结：项目结构
RBAC/
	app01/
		models.py
		views.py #用户登陆逻辑处理，在登陆时会初始化用户权限
	permission/ #项目名
		settings.py #导入中间件，定义session键，url白名单，登陆的url（增强可移植性），匹配用户请求的url做严格匹配（REGEX_URL = r'^{url}$'）
		url.py
	rbac/
		middleware/
			rbac.py #检查用户的url请求是否在其权限范围内
		service/
			init_permission.py #初始化用户权限，菜单数据结构化处理，写入session中
		templatetags/
			__init__.py
			custom_tag.py #自定义标签，渲染菜单
			

代码所在位置：E:\django模块\RBAC


