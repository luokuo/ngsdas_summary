如果ip不存在redis中：
	在redis中创建ip
	判断用户的登陆状态：
		0--用户或密码错误
		1--登陆成功，并且将redis中的ip清除
		2--用户未激活
		3--数据不完整
		4--同一ip错误登陆次数超过十次，限制30分钟之后再允许登陆

如果ip在redis中：
	如果ip在redis中对应的值小于9：
		0--用户或密码错误
		1--登陆成功，并且将redis中的ip清除
		2--用户未激活
		3--数据不完整
		4--同一ip错误登陆次数超过十次，限制30分钟之后再允许登陆
	如果ip在redis中对应的值等于9：
		设置ip的过期时间为30分钟，并且显示剩余过期时间
	如果ip在redis中对应的值大于9：
		显示剩余过期时间
		-------
		讨论：是否限制ip登陆上限
		假如登陆20次，则将其限制24小时不能登陆
		-------
		
注意点：
1.django-redis中技术点：选用数据库的字符串数据结构
	conn = get_redis_connection('default') #连接django-redis
	conn.set(userip,0) #创建userip=1的键值对,实际数据库中是以byte字节码的形式存在，bytes(userip, encoding='utf8')
	conn.incr(userip) #自增长1
	conn.get(userip) #获取userip的值
	conn.expire(userip,1800) #设置userip过期时间为半小时，其中expire单位为秒，pexpire单位为毫秒
	过期时间也可在创建时设置，根据需求来定：conn.set(userip,0,ex=1800) #ex单位是秒，px单位是毫秒
	conn.ttl(userip) #查看剩余过期时间
	参考：
		redis中可以使用expire命令设置一个键的生存时间，到时间后redis会自动删除它 
		expire 设置生存时间（单位/秒） 
		pexpire 设置生存时间(单位/毫秒) 
		ttl/pttl 查看键的剩余生存时间 
		persist 取消生存时间 
		expireat [key] unix时间戳1351858600 
		pexpireat [key] unix时间戳(毫秒)1351858700000
	应用场景：本次应用为限制登陆错误次数之后限制ip的30分钟
		限时的优惠活动 
		网站数据缓存（对于一些需要定时更新的数据） 
		限制网站访客访问频率（例如：1分钟最多访问10次）
	
2.清除redis中的ip记录是通过conn.expire(userip,0)即当用户登陆成功则将对应的ip在redis中的过期时间设置为0，达到删除效果。
