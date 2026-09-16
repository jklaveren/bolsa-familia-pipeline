#!/usr/bin/env bash
# Variaveis de ambiente necessarias para rodar PySpark localmente no Windows.
# Uso: source scripts/env.sh

export JAVA_HOME="C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot"
export HADOOP_HOME="C:\hadoop"
export PATH="$JAVA_HOME/bin:$HADOOP_HOME/bin:$PATH"
export PYSPARK_PYTHON="C:\DataBricks\.venv\Scripts\python.exe"
export PYSPARK_DRIVER_PYTHON="C:\DataBricks\.venv\Scripts\python.exe"
export PYTHONPATH="C:\DataBricks:$PYTHONPATH"
