import json, glob, sys
def load(pattern):
    recs = []
    for f in sorted(glob.glob(pattern)):
        for l in open(f, 'rb').read().decode('utf8', 'replace').splitlines():
            if l.startswith('{'):
                try: recs.append(json.loads(l))
                except Exception: pass
    return recs
