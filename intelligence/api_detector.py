import re

API_PATTERNS = [
    r"@app\.get\(\"(.*?)\"\)",
    r"@app\.post\(\"(.*?)\"\)",
    r"app\.get\(\"(.*?)\"\)",
    r"app\.post\(\"(.*?)\"\)"
]

def detect_apis(files):

    apis = []

    for f in files:

        try:
            content = open(f,"r",errors="ignore").read()

            for p in API_PATTERNS:

                matches = re.findall(p,content)

                for m in matches:
                    apis.append(m)

        except:
            pass

    return apis