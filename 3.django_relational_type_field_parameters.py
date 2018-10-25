django关系类型字段，参考地址：http://www.liujiangblog.com/course/django/96
django2.0之后外键字段必须要有on_delete参数
ForeignKey
1.当一个被外键关联的对象被删除时，django将模仿on_delete参数定义的SQL约束执行相应操作
该参数可选的值都内置在django.db.models中：

CASCADE:将定义有外键的模型对象同时删除
PROTECT:组织上面的删除操作，弹出ProtectedError异常
SET_NULL:将外江字段设为null，只有当字段设置了null=true时，方可使用该值。
SET_DEFAULT:将外键字段设为默认值，只有当字段设置default参数是才能使用
DO_NOTHING:什么也不做
SET():设置为一个传递给SET()的值或者一个回调函数的返回值

2.limit_choices_to该参数用于限制外键所能关联的对象，只能用与django的ModelForm(django的表单模块)和admin后台
其值可以是一个字典，Q对象或者一个返回字典或Q对象的函数调用
staff_member = models.ForeignKey(
	User,
	on_delete=models.CASCADE,
	limit_choices_to={'is_staff':True},
)
----------------
def limit_pub_date_choices():
	return {'pub_date__lte':datetime.date.utcnow()}
limit_choices_to = limit_pub_date_choices

3.related_name用于关联对象反向引用模型的名称，如果你不想为外键设置一个反向关联名称，
可以将这个参数设置为'+'或者以'+'结尾

4.related_query_name反向关联查询名，用于从目标模型反向过滤模型对象的名称
class Tag(models.Model):
	article = models.ForeignKey(
		Article,
		on_delete = models.CASCADE,
		related_name = 'tags',
		related_query_name = 'tag',
	)
	name = models.CharField(max_length=255)
	
Article.objects.filter(tag__name='important')

5.to_field这个参数可以关联到指定的字段上，但是该字段必须具有unique=True唯一属性

6.db_constraint默认情况这个参数为True，表示遵循数据库约束，如果设为False，那么将无法保证数据的完整性和
合法性，一般在历史遗留的不合法数据，正在分割数据库的时候用到False