from datetime import datetime, timedelta

t = datetime.now()
yesterday = t - timedelta(days=1)
tomorrow = t + timedelta(days=1)

print("Today: ", t.strftime("%x"))
print("Yesterday: ", yesterday.strftime("%x"))
print("Tomorrow: ", tomorrow.strftime("%x"))