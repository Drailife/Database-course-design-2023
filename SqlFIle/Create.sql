-- Active: 1680138500814@@127.0.0.1@3306@1_online_ordering
SHOW TABLES;

#创建餐厅表
CREATE TABLE IF NOT EXISTS `Restaurant`(
    `res_id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `res_name` CHAR(50) NOT NULL UNIQUE,
    `mail` VARCHAR(100) UNIQUE,
    `telephone` CHAR(15) NOT NULL UNIQUE,
    `address_` VARCHAR(100) NOT NULL,
    `password` VARCHAR(100) NOT NULL
);

#创建用户表
CREATE TABLE IF NOT EXISTS `User`(
    `usr_id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `usr_name` VARCHAR(40) NOT NULL,
    `mail` VARCHAR(50) NOT NULL UNIQUE,
    `sex` CHAR(2) NOT NULL,
    `age` INT UNSIGNED NOT NULL,
    `telephone` CHAR(50) UNIQUE,
    `address_` VARCHAR(200),
    `password_` CHAR(50) NOT NULL,
    CHECK(
        `sex` = '男'
        OR `sex` = '女'
    )
);

-- #创建会员表
-- CREATE TABLE IF NOT EXISTS `Vip`(
--     `vip_id` INT UNSIGNED PRIMARY KEY,
--     `vip_level` TINYINT NOT NULL DEFAULT 1,
--     `Subscription_time` DATE NOT NULL,
--     `validity_period` INT NOT NULL,
--     FOREIGN KEY (`vip_id`) REFERENCES `User`(`usr_id`) ON UPDATE CASCADE ON DELETE CASCADE
-- );
#创建餐厅食品表
CREATE TABLE IF NOT EXISTS `Foods`(
    `food_id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `food_name` VARCHAR(100) NOT NULL,
    `kind` INT NOT NULL,
    CHECK(
        `kind` > 0
        AND `kind` <= 3
    )
);

#创建餐厅食品_价格表
CREATE TABLE IF NOT EXISTS `Foods_Price`(
    `food_id` INT UNSIGNED NOT NULL,
    `res_id` INT UNSIGNED NOT NULL,
    `price` DOUBLE UNSIGNED,
    `description_` VARCHAR(200),
    PRIMARY KEY(`food_id`, `res_id`),
    FOREIGN KEY (`res_id`) REFERENCES `Restaurant`(`res_id`),
    FOREIGN KEY (`food_id`) REFERENCES `Foods`(`food_id`)
);

#创建订单表
CREATE TABLE IF NOT EXISTS `Orders`(
    `order_id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `usr_id` INT UNSIGNED NOT NULL,
    `total_price` DECIMAL(7, 2) UNSIGNED NOT NULL,
    `actual_price` DECIMAL(7, 2) UNSIGNED NOT NULL,
    `time_` DATETIME NOT NULL,
    FOREIGN KEY (`usr_id`) REFERENCES `User`(`usr_id`) ON UPDATE CASCADE ON DELETE CASCADE
);

#订单详情表
CREATE TABLE IF NOT EXISTS Orders_detail (
    `order_id` int UNSIGNED NOT NULL COMMENT '订单ID',
    `res_id` int UNSIGNED NOT NULL COMMENT '餐厅表',
    `food_id` int UNSIGNED NOT NULL COMMENT '商品ID',
    `num` int UNSIGNED NOT NULL COMMENT '购买数量',
    PRIMARY KEY (
        `order_id`,
        `res_id`,
        `food_id`
    ),
    FOREIGN KEY (`order_id`) REFERENCES `orders`(`order_id`) ON UPDATE CASCADE ON DELETE CASCADE -- FOREIGN KEY (`food_id`, `res_id`) REFERENCES `Foods_Price`(`food_id`, `res_id`) ON UPDATE CASCADE ON DELETE CASCADE
) COMMENT '订单详情表';

CREATE TABLE IF NOT EXISTS `Shopping_cart`(
    `usr_id` INT UNSIGNED NOT NULL,
    `res_name` VARCHAR(100) NOT NULL,
    `food_name` VARCHAR(100) NOT NULL,
    `num` INT UNSIGNED NOT NULL,
    `total_price` DECIMAL(7, 2) NOT NULL,
    PRIMARY KEY(
        `usr_id`,
        `res_name`,
        `food_name`
    )
) COMMENT '购物车';

-- DROP TABLE shopping_cart;
CREATE TABLE IF NOT EXISTS `User_Operate_logs`(
    `log_id` INT(11) PRIMARY KEY AUTO_INCREMENT,
    `operation` VARCHAR(200) NOT NULL,
    `time` DATETIME NOT NULL,
    `operate_id` INT(11) NOT NULL
);

SELECT
    *
FROM
    `Orders_detail`;

#User                
INSERT
    IGNORE INTO USER
VALUES
    (
        '1',
        'admin',
        'admin@gmail.com',
        '男',
        '34',
        '13031018968',
        '河南郑州',
        'admin'
    ),
    (
        '2',
        'drailife',
        'drailife@gmail.com',
        '男',
        '18',
        '13212346379',
        '北京大兴',
        '123'
    ),
    (
        '3',
        '小张',
        'xiaozhang@qq.com',
        '男',
        '20',
        '12367289978',
        '河北石家庄',
        '5783hdsjk'
    ),
    (
        '4',
        '小呆',
        'xiaodai@qq.com',
        '男',
        '27',
        '12326375264',
        '湖南长沙',
        'hfdsjka78'
    ),
    (
        '5',
        '小红',
        'xiaohong@qq.com',
        '女',
        '20',
        '18627665344',
        '福建福州',
        '3478hfdks'
    );

-- #Vip                
-- INSERT
--     IGNORE INTO VIP
-- VALUES
--     (
--         '2',
--         '3',
--         '2023-4-6 15:44:00',
--         '2'
--     ),
--     (
--         '3',
--         '10',
--         '2023-4-6 15:34:00',
--         '1'
--     ),
--     (
--         '5',
--         '8',
--         '2023-4-6 16:50:00',
--         '3'
--     );
#Restaurant                
INSERT
    IGNORE INTO RESTAURANT
VALUES
    (
        '1',
        'A',
        'A@res.com',
        '14567894567',
        'uu',
        'res'
    ),
    (
        '2',
        'B',
        'B@res.com',
        '13534567283',
        'fhdjs',
        'res'
    ),
    (
        '3',
        'C',
        'C@res.com',
        '15467239077',
        'fdhja',
        'res'
    ),
    (
        '4',
        'D',
        'D@res.com',
        '18866532367',
        'dhaj',
        'res'
    ),
    (
        '5',
        'E',
        'E@res.com',
        '15423671937',
        'dhjaj',
        'res'
    );

#Foods   
# food_id, food_name, kind
INSERT
    IGNORE INTO FOODS
VALUES
    ('1', '小鸡炖蘑菇', '1'),
    ('2', '蛋炒饭', '1'),
    ('3', '重庆小面', '2'),
    ('4', '北京烤鸭', '1'),
    ('5', '过桥米线', '2');

#Foods_Price   
#food_id, res_id, price, description_             
INSERT
    IGNORE INTO FOODS_PRICE
VALUES
    ('1', '1', '17.8', 'delicious'),
    ('2', '3', '20.0', 'delicious'),
    ('3', '5', '50.0', 'delicious');

#建立索引
-- CREATE UNIQUE INDEX ` usr_order_index ` ON ` Orders `(` order_id `, ` usr_id `);
-- CREATE UNIQUE INDEX ` food_res_price ` ON ` Foods_Price `(` food_id `, ` res_id `, ` price `);
-- #删除对应索引 #ALTER TABLE ` orders ` DROP INDEX ` usr_res_index `;
-- #ALTER TABLE ` Foods_Price ` DROP INDEX ` food_res_price `;
-- #添加完整性约束-性别为男女
-- ALTER TABLE
--     ` user `
-- ADD
--     CONSTRAINT Sex_check CHECK(` sex ` IN('男', '女'));
-- 创建视图
-- #创建存储过程