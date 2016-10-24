/*
 Navicat Premium Data Transfer

 Source Server         : javalocal
 Source Server Type    : MySQL
 Source Server Version : 50629
 Source Host           : 172.16.2.41
 Source Database       : 55haitao_dev

 Target Server Type    : MySQL
 Target Server Version : 50629
 File Encoding         : utf-8

 Date: 10/13/2016 15:30:02 PM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `sfm_order` 订单表
-- ----------------------------
DROP TABLE IF EXISTS `sfm_order`;
CREATE TABLE `sfm_order` (
  `id` int(10) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '自增id',
  `order_id` varchar(11) NOT NULL COMMENT '订单号',

  `state_id` int(10) COMMENT '订单状态0未支付订单，1已付款代发货，2已发货，3交易成功，4订单取消，',
  `weight` float(10) COMMENT '订单重量',
  `ship_amount` decimal COMMENT '运费价格',
  `products_amount` decimal COMMENT '商品总价',
  `manual_amount` decimal COMMENT '人工干预',
  `amount` decimal COMMENT '订单总价 ship_amount + products_amount + manual_amount',
  `ctime` int(11) COMMENT '下单时间',
  `overtime` int(11) COMMENT '订单过期时间',
  `user_note` varchar(200) COMMENT '消费者备注',
  `admin_note` varchar(200) COMMENT '管理员备注',
  `user_id` varchar(32) COMMENT '用户id',
  `address_id` int(10) COMMENT '订单收获地址id',
  -- `pay_id` int(10) COMMENT '订单支付id',
  'logistics_id' int(10) COMMENT '物流信息id',
  UNIQUE KEY `order_id` (`order_id`) COMMENT '订单索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

SET FOREIGN_KEY_CHECKS = 1;