
STOCK_INFO='select today_close,trade_volume ,trade_date,UNIX_TIMESTAMP(trade_date),lowest_price  from market_data where stock_code="#stockcode"  and trade_date >= DATE_SUB(CURDATE(), INTERVAL 10 MONTH) AND trade_date < CURDATE()  ORDER BY trade_date  asc  '
STOCK_MARKET='select TURNOVER_D,PCT_CHANGE_D,BetaHS300Index,AlphaHS300Index,TurnoverValueTW,TurnoverVolumeTW,ChangePCTTW,RangePCTTW,TurnoverRateTW,RangePCTRM,AvgPriceRM,ChangePCTR3M,TurnoverRateR3M,ChangePCTR12M from stock_performance sp where secucode="#stockcode"  order by sp.TradingDay  desc limit 1'
STOCK_LATEST='select  FORMAT(today_open,2), FORMAT(today_close,2), FORMAT(highest_price,2), FORMAT(lowest_price,2),date_format(trade_date,"%Y-%m-%d")  from market_data where stock_code="#stockcode" order by  trade_date desc limit 1'
STOCK_MARKET_HA='select today_open,today_close,highest_price,lowest_price,trade_volume from market_data where stock_code="#stockcode"  and trade_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND trade_date < CURDATE()  ORDER BY trade_date  asc  '

