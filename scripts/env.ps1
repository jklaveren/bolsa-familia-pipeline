# Variaveis de ambiente necessarias para rodar PySpark localmente no Windows.
# Uso: . .\scripts\env.ps1

$env:JAVA_HOME = "C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot"
$env:HADOOP_HOME = "C:\hadoop"
$env:PATH = "$env:JAVA_HOME\bin;$env:HADOOP_HOME\bin;$env:PATH"
$env:PYSPARK_PYTHON = "C:\DataBricks\.venv\Scripts\python.exe"
$env:PYSPARK_DRIVER_PYTHON = "C:\DataBricks\.venv\Scripts\python.exe"
$env:PYTHONPATH = "C:\DataBricks;$env:PYTHONPATH"
