import db_operations as d
from db_config import DATABASE_PATH

print("DB path:", DATABASE_PATH)

# Old call style (8 positional args, no machine_id) must still work
old_id = d.save_prediction("M", 300.0, 310.0, 1500, 40.0, 100, 0, "No failure predicted")
print("old-style save:", old_id)

# Call with machine_id
new_id = d.save_prediction("M", 300.0, 310.0, 1500, 40.0, 100, 1,
                           "Failure predicted", "MCH-002")
print("with machine_id:", new_id)

print("machines:", len(d.get_machines()))
print("latest for MCH-002:", d.get_machine("MCH-002")["latest_prediction"])
print("history rows:", len(d.get_predictions()))

# Only if you added alerts / confidence:
# a = d.save_alert("MCH-002", new_id, "Test alert"); print("alert:", a)
# print("alerts:", d.get_alerts())
# d.save_prediction(..., "MCH-002", confidence=0.95)

