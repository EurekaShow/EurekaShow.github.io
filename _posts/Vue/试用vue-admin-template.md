# 试用 vue-admin-template

>要前沿要生态，要快，GitHub上找template。找到了Github上star最多的一家， [GitHub - PanJiaChen/vue-element-admin: A magical vue admin](https://github.com/PanJiaChen/vue-element-admin)， 但是大牛作者推荐大家不要直接在这个项目的基础上进行二次开发，而是选用他的基础版本：[GitHub - PanJiaChen/vue-admin-template: a vue2.0 minimal admin template](https://github.com/PanJiaChen/vue-admin-template)，在该项目基础上进行二次开发，同时可以参考vue-element-admin项目的效果，有需要用的组件就直接搬过来用。template项目中集成了： Element UI & axios & iconfont & permission control & lint。 vue-element-admin项目的预览地址： vue-element-admin ，遵从作者的告诫，只取直接真正需要的。

## 克隆并编译项目

```bash
git clone https://github.com/PanJiaChen/vue-admin-template.git
## 修改成想要的名字
mv vue-admin-template dashboard
npm install
npm run dev
```

## 浏览模板项目代码

熟悉使用vue脚手架生成项目的结构的话，对admin-template的结构就很清晰了。src下的目录结构：

```c
.
├── App.vue //入口
├── api // 各种接口
├── assets // 图片等资源
├── components // 各种公共组件，非公共组件在各自view下维护
├── icons //svg icon
├── main.js //入口
├── permission.js //认证入口
├── router // 路由表
├── store // 存储
├── styles // 各种样式
├── utils // 公共工具，非公共工具，在各自view下维护
└── views // 各种layout
```

### 增加百度地图页面

- 1. index.html 引入百度地图接口
```js
<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=youapikey"></script>
```

- 2. 添加BMap到webpack.base.conf.js文件中
```js
  externals: {
    "BMap": "BMap"
  },
```
添加后应该是：
```js
  entry: {
    app: './src/main.js'
  },
  externals: {
    "BMap": "BMap"
  },
```

- 3. router/index.js中增加新页面路由，我们定位为menu3
```js
    {
        path: 'menu3',
        component: () => import('@/views/nested/menu3/index'),
        meta: { title: 'menu3' }
      }
```

- 4. 在nested目录下增加menu3，并增加index.vue文件。

```html
<template>
  <div class="con" style="width:100%; height:100%;position: absolute;">
    <div id="container" style="width:100%; height:100%;position: absolute;border:1px solid gray"/>
  </div>
</template>

<script>
export default {
  name: '',
  data() {
    return {
    }
  },
  mounted() {
    const map = new window.BMap.Map('container', {
      enableMapClick: false,
      mapType: window.BMAP_HYBRID_MAP
    })
    const point = new window.BMap.Point(116.4035, 39.915)
    map.setCurrentCity('上海') // 设置地图显示的城市 此项是必须设置的,因为要使用三维图
    map.centerAndZoom(point, 15) // 初始化地图,设置中心点坐标和地图级别。
    map.addControl(new window.BMap.MapTypeControl()) // 添加地图类型控件
    map.centerAndZoom(new window.BMap.Point(105.403119, 38.028658), 5) // 初始化地图,设置中心点坐标和地图级别
    map.enableScrollWheelZoom(true) // 开启鼠标滚轮缩放
    map.disableDoubleClickZoom(true) // 禁用双击
  }
}

</script>

```

- 5. 查看页面效果，点击menu3看看卫星地图是否出现？
