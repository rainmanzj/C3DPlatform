## Feature
### 属性
* #### Guid
	GUID
* #### Placement
	方位:位置+旋转
* #### Label
	标签
* #### Texture
	纹理
* #### Group
	组别，如果不存在则返回None

### 方法
* #### addProperty(name, type, group = "", value = None)
	增加属性
* #### show()
	显示
* #### hide()
	隐藏
* #### update()
	刷新
* #### delete()
	删除
* #### setTexture(tex)
	设置纹理
	tex --- 纹理文件路径
* #### clearTexture()
	清空纹理