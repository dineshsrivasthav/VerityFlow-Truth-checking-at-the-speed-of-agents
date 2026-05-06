import json
from pprint import pprint 
from datetime import date, datetime

from article_assurance.api import AssuranceService


with open("input_json.json") as f:
    payload = json.load(f)

service = AssuranceService()

result = service.assess(payload)
pprint(result)



class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.strftime('%Y-%m-%d')  # Customize format as needed
        return super().default(obj)

# Save with custom encoder
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False, cls=DateTimeEncoder)

print("File saved successfully!")