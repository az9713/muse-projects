FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir pytest \
 && python -m pytest project-1-migration/python-sample/tests -q \
 && python -m pytest project-2-coldstart/python/tests -q \
 && python -m pytest project-3-test-swarm/python/tests -q \
 && python -m pytest project-4-polyglot/tests -q \
 && python -m pytest project-5-docs-to-code/tests -q \
 && python -m pytest project-6-bughunt/python/tests -q
CMD ["python", "-m", "pytest", "project-1-migration/python-sample/tests", "-q"]
