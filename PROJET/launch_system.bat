@echo off
echo ========================================
echo   Multi-Source Analytics System
echo   Apache Kafka + Spark Streaming
echo ========================================
echo.

echo Etape 1: Demarrage Zookeeper...
start "Zookeeper" cmd /k "scripts\start_zookeeper.bat"
timeout /t 10

echo Etape 2: Demarrage Kafka...
start "Kafka" cmd /k "scripts\start_kafka.bat"
timeout /t 15

echo Etape 3: Creation des topics...
call scripts\create_topics.bat

echo Etape 4: Demarrage Spark Master...
start "Spark Master" cmd /k "scripts\start_spark_master.bat"
timeout /t 10

echo Etape 5: Demarrage Spark Worker...
start "Spark Worker" cmd /k "scripts\start_spark_worker.bat"
timeout /t 5

echo.
echo ========================================
echo   Systeme demarre avec succes!
echo ========================================
echo.
echo Services disponibles:
echo - Kafka: localhost:9092
echo - Spark Master: localhost:7077
echo - Spark UI: http://localhost:8080
echo - MongoDB: localhost:27017
echo.
echo Pour demarrer les producteurs:
echo   python kafka_producers.py
echo.
echo Pour demarrer le consumer Spark:
echo   python spark_streaming_consumer.py
echo.
echo Pour le dashboard:
echo   streamlit run dashboard_3d_realtime.py
echo.
pause
