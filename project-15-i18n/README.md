# #15 i18n extraction

Views route every user-facing string through `t()` (`app/views.py`);
`app/locale/en.json` is complete, `es.json` is deliberately partial to
exercise fallback. `tools/check.py` is the CI guard: any `t()` key missing
from `en.json` fails the build.

```sh
source .venv/bin/activate
python tools/check.py              # keys used=3 missing=0
python -m pytest tests/ -q         # 8 passed
```
