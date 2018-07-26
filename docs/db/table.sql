-- 交易日期日历
DROP TABLE IF EXISTS `stock_trade_calendar`;
create table `stock_trade_calendar` (
`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
`date` date NOT NULL COMMENT '日期',
`is_open` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '是否是交易日，1：是；0：否',
PRIMARY KEY (`id`),
UNIQUE KEY `uk_date` (`date`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='股票交易日期日历';

-- 股票信息基本数据表
DROP TABLE IF EXISTS `stock_base`;
create table `stock_base` (
`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
`code` varchar(10) NOT NULL COMMENT '股票6位编码',
`type` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '类型，1：股票；2：指数',
`name` varchar(25) NOT NULL COMMENT '股票名称',
`time_to_market` date NOT NULL COMMENT '上市日期',
`status` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '交易状态，1：正常；2：停牌；3：退市',
`gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录最近一次修改时间',
`gmt_create` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
PRIMARY KEY (`id`),
UNIQUE KEY `uk_code_type` (`code`, `type`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='股票基本数据表';

-- 股票每日交易信息数据表
DROP TABLE IF EXISTS `stock_trade_daily`;
create table `stock_trade_daily`(
`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
`code` varchar(10) NOT NULL COMMENT '股票6位编码',
`open` float(7,3) NOT NULL COMMENT '开盘价',
`high` float(7,3) NOT NULL COMMENT '最高价',
`low` float(7,3) NOT NULL COMMENT '最低价',
`close` float(7,3) NOT NULL COMMENT '收盘价',
`volume` int(11) unsigned NOT NULL COMMENT '成交量',
`amount` bigint(20) unsigned NOT NULL DEFAULT 0 COMMENT '成交额',
`turn_over_ratio` float(7,3) NOT NULL DEFAULT 0.0 COMMENT '换手率',
`increase` float(7,3) NOT NULL DEFAULT 0.0 COMMENT '股票涨幅',
`amplitude` float(7,3) NOT NULL DEFAULT 0.0 COMMENT '股票振幅',
`trade_date` date NOT NULL COMMENT '交易日期',
`gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录最近一次修改时间',
`gmt_create` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
PRIMARY KEY (`id`),
UNIQUE KEY `uk_code_trade_date` (`code`, `trade_date`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='股票每日交易信息数据表';
-- index
create index idx_trade_date on stock_trade_daily(`trade_date`);