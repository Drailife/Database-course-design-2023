-- Active: 1680138500814@@127.0.0.1@3306@1_online_ordering
#创建视图
# 用与呈现给用户点餐页面的视图，包含餐厅以及食物的详细信息。
DROP VIEW IF EXISTS Foods_available_for_purchase;

CREATE VIEW `Foods_available_for_purchase` AS
SELECT
    res_name,
    food_name,
    price,
    kind,
    description_
FROM
    `restaurant` AS r,
    `foods_price` AS fp,
    `foods` AS f
WHERE
    r.res_id = fp.res_id
    AND fp.food_id = f.food_id;

DROP VIEW IF EXISTS My_Orders_Detail_Info;

#创建一个视图显示订单详情，目的是将id换为name
CREATE VIEW `My_Orders_Detail_Info` AS
SELECT
    od.order_id,
    r.res_name,
    f.food_name,
    od.num
FROM
    `orders_detail` od,
    `restaurant` r,
    `foods` f
WHERE
    od.res_id = r.res_id
    AND od.food_id = f.food_id;

SELECT
    *
FROM
    My_Orders_Detail_Info;

DROP VIEW IF EXISTS Orders_Detail_By_Usr_Id;

#定义一个视图显示用户的订单细则
CREATE VIEW `Orders_Detail_By_Usr_Id` AS
SELECT
    u.usr_name,
    o.order_id,
    r.res_name,
    f.food_name,
    od.num,
    o.time_
FROM
    `user` u,
    `restaurant` r,
    `foods` f,
    `orders_detail` od,
    `orders` o
WHERE
    u.usr_id = o.usr_id
    AND o.order_id = od.order_id
    AND od.res_id = r.res_id
    AND od.food_id = f.food_id
ORDER BY
    o.order_id;

-- DROP VIEW Orders_Detail_By_Usr_Id;
SELECT
    *
FROM
    Orders_Detail_By_Usr_Id;

DROP VIEW IF EXISTS ALL_FOODS_INFO;

#定义一个视图来显示商家所有的餐品信息,用到res表和foods表
CREATE VIEW `ALL_FOODS_INFO` AS
SELECT
    -- r.res_id,
    r.res_name,
    fp.food_id,
    f.food_name,
    fp.price,
    fp.description_
FROM
    `restaurant` r,
    `foods` f,
    `FOODS_PRICE` fp
WHERE
    r.res_id = fp.res_id
    AND f.food_id = fp.food_id;

SELECT
    *
FROM
    `ALL_FOODS_INFO`;

DELIMITER $ $ #定义一个存储过程，用于添加商品到购物车
CREATE PROCEDURE IF NOT EXISTS `ADDTOSHOPCART`(
    IN `USR_ID_` INT,
    IN `RES_NAME_` VARCHAR(100),
    IN `FOOD_NAME_` VARCHAR(100),
    IN `PRICE_` DECIMAL(7, 2)
) BEGIN DECLARE `flag_have_food` INT DEFAULT 0;

SELECT
    COUNT(*) INTO `flag_have_food`
FROM
    `shopping_cart`
WHERE
    usr_id = `USR_ID_`
    AND res_name = `RES_NAME_`
    AND food_name = `FOOD_NAME_`;

IF `flag_have_food` = 0 THEN
INSERT INTO
    `shopping_cart` VALUE(usr_id_, res_name_, food_name_, 1, price_);

ELSE
UPDATE
    `shopping_cart`
SET
    `num` = `num` + 1,
    `total_price` = `total_price` + `price_`
WHERE
    usr_id = `usr_id_`
    AND res_name = `res_name_`
    AND food_name = `food_name_`;

END IF;

SELECT
    res_name,
    food_name,
    num,
    total_price
FROM
    shopping_cart
WHERE
    usr_id = `usr_id_`;

END;

$ $ DELIMITER;

-- DROP PROCEDURE `ADDTOSHOPCART`;
SELECT
    *
FROM
    shopping_cart;

-- TRUNCATE shopping_cart;
#定义一个存储过程用于提交购物车的下单请求
#向orders表中添加数据
#以及添加对应的orders_detail中数据
DELIMITER $ $ #1
CREATE PROCEDURE IF NOT EXISTS `PURCHASE_FROM_SHOPPING_CURT`(
    IN `USR_ID_` INT,
    IN `TOTAL_PRICE_` DECIMAL(7, 2),
    IN `ACTUAL_PRICE_` DECIMAL(7, 2)
) BEGIN
INSERT INTO
    `orders` VALUE(
        NULL,
        `USR_ID_`,
        `TOTAL_PRICE_`,
        `ACTUAL_PRICE_`,
        NOW()
    );

END;

-- #重置密码
CREATE PROCEDURE IF NOT EXISTS `RESET_PASSWORD`(
    IN `TARGET_ID` INT,
    IN `NEW_PASSWORD` VARCHAR(255)
) BEGIN
UPDATE
    `user`
SET
    `password_` = `new_password`
WHERE
    `usr_id` = `target_id`;

END;

-- $ $ DELIMITER;
-- DROP PROCEDURE IF EXISTS `PURCHASE_FROM_SHOPPING_CURT`;
-- CALL `PURCHASE_FROM_SHOPPING_CURT`(2, '1.2', '11.2');
SELECT
    *
FROM
    orders;

SELECT
    LAST_INSERT_ID();

CREATE TRIGGER IF NOT EXISTS `TIGGER_DELETE_USER`
AFTER
    DELETE ON `USER` FOR EACH ROW BEGIN
INSERT INTO
    `User_Operate_logs` VALUE(
        NULL,
        "delete",
        NOW(),
        OLD.usr_id
    );

END;

-- DROP TRIGGER TIGGER_DELETE_USER;
CREATE TRIGGER IF NOT EXISTS `TIGGER_INSERT_USER`
AFTER
INSERT
    ON `USER` FOR EACH ROW BEGIN
INSERT INTO
    `User_Operate_logs` VALUE(
        NULL,
        'insert',
        NOW(),
        NEW.usr_id
    );

END;

CREATE TRIGGER IF NOT EXISTS `TIGGER_UPDATE_USER`
AFTER
UPDATE
    ON `USER` FOR EACH ROW BEGIN
INSERT INTO
    `User_Operate_logs` VALUE(
        NULL,
        'update',
        NOW(),
        OLD.usr_id
    );

END;