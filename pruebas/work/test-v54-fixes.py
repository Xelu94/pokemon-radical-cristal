"""v5.4 fixes found by the beta testers, played in the emulator: the Choice-item lock text no longer resets the console,
and crossing a map connection on foot keeps every NPC's graphics (sprite list rebuilt before the objects are created).
Runs the testers' reproduction scripts (work/beta54, written by the Gold beta tester) and checks their output."""
import json
import os
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
env = {**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1', 'BETA_ROOT': str(root)}
(root / 'shots').mkdir(exist_ok=True)
tests = []


def run(script):
    p = subprocess.run([sys.executable, '-W', 'ignore', str(root / 'work/beta54' / script)], cwd=root, env=env,
                       capture_output=True, text=True, encoding='utf8', errors='replace', timeout=900)
    return [l for l in (p.stdout + p.stderr).splitlines() if 'INFO' not in l]


def check(name, condition):
    assert condition, name
    tests.append({'name': name, 'passed': True})
    print('PASS', name, flush=True)


out = run('repro_choice_crash.py')
check('choosing another move with a Choice Band, Specs or Scarf prints the lock text and does not reset the console',
      sum('lock text shown (ok)' in l for l in out) == 3 and not any('CRASH' in l for l in out))
out = run('repro_bug001.py')
check('after walking Route 29 to New Bark Town and closing the bag the Teacher keeps her own graphics',
      [l for l in out if l.startswith(('control', 'bug'))] and all(l.rstrip().endswith('[]') for l in out if l.startswith(('control', 'bug'))))
out = run('repro_bug002.py')
check('the Route 29 Ulex-warning dude walks without background tiles in his sprite when arriving from New Bark Town',
      any(l.startswith('bad samples 0') for l in out))
out = run('repro_silver.py')
check('Silver and the Guide Gent keep their graphics after the first fight when arriving in Cherrygrove from Route 29',
      sum(l.rstrip().endswith('[[]]') for l in out) == 2)
learn = (root / 'work/source/engine/pokemon/learn.asm').read_text(encoding='utf8')
check('the forget-a-move menu no longer refuses HM moves (HMs are bag tools, random moves may be HM moves)',
      'IsHMMove' not in learn and 'MoveCantForgetHMText' not in learn)
Path('work/v54-fixes-tests.json').write_text(json.dumps({'passed': len(tests), 'tests': tests}), encoding='utf8')
