# MARK LIV — FastAPI remote dashboard (cluster subset)
# The desktop PyQt HUD / mic / speakers are not part of this image.
FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --system --gid 1001 jarvis \
    && adduser --system --uid 1001 --ingroup jarvis --home /app jarvis \
    && mkdir -p /app/uploads /app/config \
    && chown -R jarvis:jarvis /app

COPY requirements-dashboard.txt /app/requirements-dashboard.txt
RUN pip install --no-cache-dir -r /app/requirements-dashboard.txt

COPY --chown=jarvis:jarvis dashboard /app/dashboard

USER jarvis
ENV JARVIS_K8S=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

EXPOSE 8000
CMD ["python", "-m", "dashboard.k8s_main"]
