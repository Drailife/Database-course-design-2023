# Database-course-design-2023

## 个人信息

学校：北京交通大学

学号：20281239

姓名：戴斌斌 

专业：物联网2001班 

时间：2023.6.1

项目链接：https://github.com/Drailife/Database-course-design-2023.git

## 说明

数据库系统设计-2023

一个点餐系统，功能基本完备，

**前端**: 主要使用boost strap框架 + jquery库

**后端**： flask + python

**数据库**： MySql

分配唯一的管理员账号，顾客账号和商家账号支持注册

**账号** ： admin@gmail.com	

**密码** ：admin

可按照用户安装和说明手册来使用本系统

![](https://drailife.oss-cn-beijing.aliyuncs.com/img/202306181147702.png)

## 管理员界面

![](https://drailife.oss-cn-beijing.aliyuncs.com/img/202306181148514.png)



## 商家界面

![](https://drailife.oss-cn-beijing.aliyuncs.com/img/202306181151269.png)



## 用户界面

![](https://drailife.oss-cn-beijing.aliyuncs.com/img/202306181152543.png)



## 源代码列表及说明

所用的到的代码和脚本如下所示：

├────__init__.py                       //设置环境变量地址

├────app.py                          //项目入口文件

├────backup.exe                       //数据库恢复exe文件

├────backup.vbs                       //数据库恢复脚本文件

├────BluePrints/                       //蓝图文件夹

│  ├────__init__.py                 //设置环境变量地址

│  ├────InfoShow.py                //在管理员页面显示数据

│  ├────Login.py                  //登录功能实现

│  ├────Res_Operate.py             //餐厅用户功能实现

│  ├────Update.py                 //管理员更新数据操作实现

│  └────User_Operate.py            //顾客用户操作实现

├────config.py                        //flask的配置文件

├────exts.py                          //插件文件的设置

├────README.md                    //文件介绍

├────SqlFIle/                         //SQL文件夹

│  ├────backup.sql                 //数据库恢复的sql文件

│  ├────Create.sql                  //数据库表创建的文件

│  ├────Delete.sql                  //用于删除表数据

│  ├────Query.sql                  //用于查询表数据

│  └────视图-存储过程-触发器.sql    //存储视图存储过程触发器

├────SQLModel.py                    //ORM映射模型的表

├────static/                           //静态文件

│  ├────img/                      //图片文件

│  └────js/                        //js文件

│  │  ├────bootstrap.min.js       //bootstrap框架

│  │  ├────bootstrap.min.js.map   

│  │  └────jquery-3.6.4.min.js    //jquery库

└────templates/                       //html的文件

│  ├────0_base.html                //网站基本框架   

│  ├────10_orders_detail.html        //订单详情表数据

│  ├────11_my_restaurant.html       //餐厅用户展示

│  ├────12_User_Purchase_From_Res.html //购物车展示

│  ├────1_index.html               //开始界面

│  ├────2_setting.html              //设置界面

│  ├────4_user.html                //用户界面

│  ├────5_user_log.html             //用户日志表数据

│  ├────6_Restaurant.html           //餐厅表数据

│  ├────7_foods.html               //食品表数据

│  ├────8_foods_price.html          //食品价格表数据

│  ├────9_orders.html               //订单表数据

├────20281239戴斌斌_数据库系统原理课程设计/                       //系统设计说明文件夹

│  ├────1.系统规划与可行性分析报告.docx

│  ├────2.需求规格说明书.docx	 

│  ├────3.系统详细设计说明书.docx

│  ├────4.用户安装与使用手册.docx

│  ├────5.系统设计总结.docx

│  └────6.课程总结与建议.docx

