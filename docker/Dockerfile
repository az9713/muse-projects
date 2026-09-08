FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir pytest \
 && python project-11-log-dashboard/gen_logs.py && python project-11-log-dashboard/analyze.py \
 && python project-16-rehearsal/rehearse.py \
 && python project-17-perf/bench.py && python project-17-perf/gate.py --update-baseline && python project-17-perf/trend.py \
 && python -m pytest project-1-migration/python-sample/tests -q \
 && python -m pytest project-2-coldstart/python/tests -q \
 && python -m pytest project-3-test-swarm/python/tests -q \
 && python -m pytest project-4-polyglot/tests -q \
 && python -m pytest project-5-docs-to-code/tests -q \
 && python -m pytest project-6-bughunt/python/tests -q \
 && python -m pytest project-8-strict-typing/tests -q \
 && python -m pytest project-9-traffic-sdk/tests -q \
 && python -m pytest project-10-upgrade/tests -q \
 && python -m pytest project-11-log-dashboard/tests -q \
 && python -m pytest project-12-config-drift/tests -q \
 && python -m pytest project-13-deadcode/tests -q \
 && python -m pytest project-14-fuzz/tests -q \
 && python -m pytest project-15-i18n/tests -q \
 && python -m pytest project-16-rehearsal/tests -q \
 && python -m pytest project-17-perf/tests -q
CMD ["python", "-m", "pytest", "project-1-migration/python-sample/tests", "-q"]
