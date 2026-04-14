FROM python:3.11-slim

# ── Sistema base ──────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-21-jre-headless \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Java requerido por PySpark
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# ── Python: dependencias del proyecto ────────────────────────────────────────
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# ── dbt: perfil preconfigurado para DuckDB ────────────────────────────────────
RUN mkdir -p /root/.dbt
COPY profiles.yml /root/.dbt/profiles.yml

# ── Directorios de trabajo ────────────────────────────────────────────────────
WORKDIR /workspace
RUN mkdir -p /workspace/data/raw \
             /workspace/data/warehouse \
             /workspace/notebooks \
             /workspace/scripts \
             /workspace/sql \
             /workspace/dbt_project

# ── Jupyter: configuración mínima ─────────────────────────────────────────────
RUN jupyter lab --generate-config && \
    echo "c.ServerApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_lab_config.py && \
    echo "c.ServerApp.allow_root = True" >> /root/.jupyter/jupyter_lab_config.py && \
    echo "c.ServerApp.open_browser = False" >> /root/.jupyter/jupyter_lab_config.py && \
    echo "c.ServerApp.token = ''" >> /root/.jupyter/jupyter_lab_config.py && \
    echo "c.ServerApp.password = ''" >> /root/.jupyter/jupyter_lab_config.py

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
