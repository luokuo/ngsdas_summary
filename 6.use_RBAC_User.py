RBAC和ngsdas项目衔接问题解决方法及总结
参考：https://stackoverflow.com/questions/8043881/django-admin-manytomanyfield#   （这个是我们最后参考的链接）
https://www.cnblogs.com/ccorz/p/Django-zi-ding-yi-yong-hu-ren-zheng-xi-tong-zhi-zi.html    （这个两种方法全部都介绍了）

1.遇到的问题
	我们项目并不需要用户注册这一功能，在admin后台添加用户即可，但是在将RBAC模块嵌入到项目过程中，将User注册到admin时，role这一字段
	并不能在admin进行操作，即无法给用户添加角色

2.解决思路和方案
	第一种：重写django自带的User模块，这种是改变了django的模块，需要附带一系列的修改，其中认证权限这块也需要重写
		在逻辑处理上当调用重写的User，需要调用django.contrib.auth.get_user_model()这一模块，
		在定义model时，外键关系上的调用先要在settings.py中定义常量AUTH_USER_MODEL = 'rbac.User'，再在调用时用settings.AUTH_USER_MODEL
		充当User
		刚开始是用的此种方法，但在调用时出现问题，并且用户认证authenticate这一块始终是None，到此为止，并未在深入去研究
	第二种：使用django自带的User模块，因为user和role是多对多的关系，我们在这个基础之上再添加一张表UserProfile，它们之间的关系为
		User--OneToOneField--UserProfile--ManyToManyField--Role--ManyToManyField--User
		即我们将多对多的关系关联在了UserProfile表中，而UserProfile又和User是一对一的关系，从而在不改变原有User模块的基础上进行扩展
		需要注意admin.py模块在注册User先要解除默认的注册，再定义新的UserProfileInline继承StackedInline，然后定义CustomUserAdmin继承
		UserAdmin，在CustomUserAdmin类中inlines = [UserProfileInline]，最后在重新注册即可
		最后有admin.py中内容
		
3.需要提一下的事 
	3.1 RBAC模块嵌入到项目中来后，数据库迁移，先生成rbac的迁移脚本，再生成ngsweb的迁移脚本，最后生成表
	3.2 初始化权限init_permission（）方法中，permission_item_list = user_obj.roles.values(...).distinct()改为
		permission_item_list = user_obj.userprofile.roles.values(...).distinct()
		因为user和role之间多了userprofile表
	3.3 init_permission（）方法在用户登陆成功之前做初始化，其它时候不做操作

		
admin.py内容如下：
====================================================
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin import StackedInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Menu, Permission, Role, UserProfile

# Register your models here.
admin.site.unregister(User)

class RoleAdmin(ModelAdmin):
	pass


class UserProfileInline(StackedInline):
	model = UserProfile
	filter_horizontal = ('roles',)


class CustomUserAdmin(UserAdmin):
	# save_on_top = True
	inlines = [UserProfileInline]


admin.site.register(Menu)
admin.site.register(Permission)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Role,RoleAdmin)