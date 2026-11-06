"""Run the integration tests and retain their output for this exact ROM (v5.0)."""
from pathlib import Path
import subprocess,sys,os,json,hashlib,shutil

root=Path(__file__).resolve().parents[1]
work=root/'work'
env=os.environ.copy()
env['PYTHONIOENCODING']='utf-8'
env['PYTHONUTF8']='1'
env['PYTHONPATH']=str(work)+(os.pathsep+env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
node=shutil.which(os.environ.get('NODE_BINARY','node'))
if not node: raise SystemExit('Node.js no está disponible en PATH.')
groups=[('Tito services and maps','test-v4-tito.py',True,'v4-tito-tests.json',48),
        ('Tito rendered directions','test-v42-tito-directions.py',True,'v42-tito-directions-tests.json',4),
        ('All Ulex routes and sandbox Items','test-v42-fixes.py',False,'v42-fixes-tests.json',17),
        ('Ulex battles and sandbox UI','test-v4-root-ui.py',False,'v41-root-ui-tests.json',27),
        ('Battle calculations and storage','test-v4-battle.py',True,'v4-battle-tests.json',11),
        ('Real battle UI and capture','test-v4-battle-ui.py',True,'v41-battle-ui-tests.json',4),
        ('Randomizer core','test-v4-randomizer.cjs',False,'v4-randomizer-tests.json',9),
        ('Offline randomizer UI','test-v4-randomizer-ui.cjs',False,'v4-randomizer-ui-tests.json',4),
        ('v4.3 changes (Fly, Map Card, marts, League supplies, candies, bag)','test-v43-changes.py',False,'v43-changes-tests.json',14),
        ('v4.4 interface (level cap, move icons, exp bar, Tito idle)','test-v44-changes.py',False,'v44-changes-tests.json',4),
        ('v5.0 routines (infinite items, hatching, Super League picker, 10-step eggs)','test-v45-routines.py',False,'v45-routines-tests.json',14),
        ('v5.0 story and world (Ulex warning, Joy, Elm, other protagonist, Super League, data)','test-v45-story.py',False,'v45-story-tests.json',28),
        ('v5.3 sandbox HMs and mart stones (data and routines)','test-v53-routines.py',False,'v53-routines-tests.json',5),
        ('v5.4 beta-tester fixes (Choice lock text, sprite list on connections)','test-v54-fixes.py',False,'v54-fixes-tests.json',5),
        ('v5.5 routines (evolution by level, level floor, moves of their own type, Fairy moves for Tito, Poison moves)','test-v55-routines.py',False,'v55-routines-tests.json',35),
        ('v5.5 story (the other protagonist runs up from behind, TMs are not used up)','test-v55-story.py',False,'v55-story-tests.json',6),
        ('v5.6 routines (modern moves and TMs, Tito reminder for all species, trade partners list, Ulex without lock)','test-v56-routines.py',False,'v56-routines-tests.json',18),
        ('v5.6 story (the other protagonist leaves and vanishes)','test-v56-story.py',False,'v56-story-tests.json',2),
        ('v5.6 Tito TRUEQUES on the real map UI','test-v56-tito-ui.py',False,'v56-tito-ui-tests.json',7),
        ('v5.7 story (Super League prize with a full party, Dark Lugia back picture)','test-v57-story.py',False,'v57-story-tests.json',6),
        ('v5.0 story and world played as a girl (Gold ambushes, Cristal does not)','test-v45-story.py',False,'v45-story-girl-tests.json',28,{'PLAYER_GENDER':'1'}),
        ('v5.5 story played as a girl (Gold runs up from behind)','test-v55-story.py',False,'v55-story-girl-tests.json',6,{'PLAYER_GENDER':'1'}),
        ('v5.6 story played as a girl','test-v56-story.py',False,'v56-story-girl-tests.json',2,{'PLAYER_GENDER':'1'}),
        ('v5.7 story played as a girl','test-v57-story.py',False,'v57-story-girl-tests.json',6,{'PLAYER_GENDER':'1'})]
reports=[]
for title,script,rom_arg,report,expected,*extra in groups:
    executable=str(node) if script.endswith('.cjs') else sys.executable
    args=[executable,str(work/script)]
    if rom_arg:args.append('work/source/pokecristal.gbc')
    process=subprocess.run(args,cwd=root,env={**env,**(extra[0] if extra else {})},capture_output=True,text=True,encoding='utf8',errors='replace',timeout=1500)
    (work/('v50-'+Path(report).stem+'.log')).write_text(process.stdout+'\n'+process.stderr,encoding='utf8')
    if process.returncode:
        print(process.stdout,process.stderr);raise SystemExit(process.returncode)
    result=json.loads((work/report).read_text(encoding='utf8'))
    assert result['passed']==expected,(title,result)
    reports.append({'name':title,'report':report,'passed':expected})
    print('PASS',title,expected,flush=True)
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
summary={'version':'5.7','fecha':'2026-11-06','normal_sha256':digest(work/'source/pokecristal.gbc'),
         'sandbox_sha256':digest(work/'source/pokecristal_debug.gbc'),'passed':sum(g['passed'] for g in reports),
         'groups':reports,'limitaciones':['No equivale a una campaña completa.',
         'Se omite la introducción en las pruebas de interfaz; en Ruta 17 se desactiva la gravedad solo en el montaje de prueba.',
         'Las pruebas de combate de Ulex aumentan el daño para recorrer sus equipos; no evalúan el equilibrio completo.',
         'Los combates de las pruebas de la v5.0 (Elm, emboscadas, Meseta Añil, sala de Azul) se juegan con un Mewtwo de estadísticas infladas; el combate contra el campeón de la Superliga no se juega entero: se comprueba su recompensa con un atajo.']}
(work/'v50-validation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
