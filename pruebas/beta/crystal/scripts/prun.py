"""Generic parallel runner with per-job timeout (a hung emulator is reported as HANG, not allowed to block the batch).
usage: py -3.12 scripts/prun.py <worker.py> <jobs.json> <out.jsonl> [procs=3] [timeout=300]
  jobs.json: list of arg-lists (strings); each is passed as argv to `py -3.12 -W ignore worker.py ...`
  The worker must print one line 'RESULT {json}' (anything else is ignored). Env (PLAYER_GENDER...) is inherited.
Never exceed 3 procs (shared machine).
"""
import sys, json, subprocess, time, threading, os, queue

worker, jobs_file, out_file = sys.argv[1:4]
procs = min(3, int(sys.argv[4])) if len(sys.argv) > 4 else 3
timeout = int(sys.argv[5]) if len(sys.argv) > 5 else 300
jobs = json.load(open(jobs_file, encoding='utf8'))
q = queue.Queue()
for j in jobs:
    q.put(j)
lock = threading.Lock()
out = open(out_file, 'w', encoding='utf8')
stats = {'done': 0, 'hang': 0, 'err': 0}


def run():
    while True:
        try:
            job = q.get_nowait()
        except queue.Empty:
            return
        cmd = ['py', '-3.12', '-W', 'ignore', worker] + [str(a) for a in job]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf8', errors='replace')
        res = None
        try:
            txt, _ = p.communicate(timeout=timeout)
            for line in txt.splitlines():
                if line.startswith('RESULT '):
                    res = json.loads(line[7:])
            if res is None:
                res = {'job': job, 'error': 'no RESULT; tail=' + txt[-400:]}
                stats['err'] += 1
        except subprocess.TimeoutExpired:
            subprocess.run(['taskkill', '/F', '/T', '/PID', str(p.pid)], capture_output=True)
            res = {'job': job, 'hang': True}
            stats['hang'] += 1
        res.setdefault('job', job)
        with lock:
            out.write(json.dumps(res, ensure_ascii=False) + '\n'); out.flush()
            stats['done'] += 1


ts = [threading.Thread(target=run) for _ in range(procs)]
t0 = time.time()
for t in ts: t.start()
for t in ts: t.join()
print('jobs', len(jobs), stats, 'seconds', int(time.time() - t0))
