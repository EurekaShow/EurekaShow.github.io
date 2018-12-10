# mybatis中使用in查询
  
  ## 第一种写法
  哈哈，这种写法比较傻，只是为了和第二种写法比对展示foreach属性特征。

  ```conf
  ## 调用
# http://127.0.0.1:12222/areaclass/findBykeys?classIds=1&classIds=2&classIds=3

## mybatis xml配置

  <select id="getByBusinessId" resultType="com.cloud.bo.AreaClass">
    SELECT * FROM bd_area_class_big_level WHERE
    <foreach collection="classIds" index="index" item="id" open="(" separator="OR" close=")">
      class_id = #{id}
    </foreach>
  </select>

## 输出sql
 # SELECT * FROM bd_area_class_big_level WHERE ( class_id = ? OR class_id = ? OR class_id = ? ) 
```

## 第二种写法
```conf
## 调用
# http://127.0.0.1:12222/areaclass/findBykeys?classIds=1&classIds=2&classIds=3

## mybatis xml配置

   <select id="getByBusinessId" resultType="com.cloud.bo.AreaClass">
    SELECT * FROM bd_area_class_big_level WHERE class_id in
    <foreach collection="classIds" index="index" item="id" open="(" separator="," close=")">
      #{id}
    </foreach>
  </select>

## 输出sql
# SELECT * FROM bd_area_class_big_level WHERE class_id in ( ? , ? , ? )
```

## 第三种写法
```conf
## 调用
# http://127.0.0.1:12222/areaclass/findBykeys?ids=1,2,3

## mybatis xml配置

   <select id="getByBusinessId" resultType="com.cloud.bo.AreaClass">
    SELECT * FROM area_class WHERE class_id in ${ids}
  </select>

## 输出sql
# select * from area_class WHERE id in (1,2,3) 
  ```