-- List locations
SELECT DISTINCT location FROM weather_data;

-- Used to List daily forecasts and get avg temperatures
SELECT * FROM weather_data ORDER BY date_time;


-- Used to get Top n locations
SELECT location, AVG(?) AS avg_metric
FROM weather_data
GROUP BY location
ORDER BY avg_metric DESC
LIMIT ?;