# scripts/check_notifications.py
import run, pprint, traceback
from flask import url_for

app = run.app

print("BLUEPRINTS:")
pprint.pprint(sorted(app.blueprints.keys()))

print("\nENDPOINTS:")
pprint.pprint(sorted(r.endpoint for r in app.url_map.iter_rules()))

print("\nTRY BUILDING url_for('notifications.index'):")
ctx = app.test_request_context()
ctx.push()
try:
    print(url_for('notifications.index'))
except Exception as e:
    print("BUILDERR", type(e).__name__, e)
    traceback.print_exc()
finally:
    ctx.pop()