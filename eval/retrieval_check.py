from copilot.search import get_store
from copilot import config

CASES=[
    ("Que faire si Z endstop not hit ?",{20}),
    ("Erreur de câblage du capteur de filament, que vérifier ?",{20,72}),
    ("Que se passe-t-il en cas de coupure de courant pendant l'impression ?",{40}),
    ("Que signifie l'erreur MINTEMP et à quelle température se déclenche-t-elle ?",{81}),
    ("Comment vérifier que les courroies X et Y sont bien tendues ?",{79,80}),
    ("L'imprimante ne lit pas ma carte SD, que faire ?",{79}),
    ("Quelles températures de buse et de plateau pour imprimer en PETG ?",{60,61}),
    ("Le filament ne passe plus du tout dans la buse, comment la déboucher ?",{73,74}),
    ("Le ventilateur de l'extrudeur affiche une erreur, que vérifier ?",{69,70,82}),
    ("Quelle est la différence entre le mode Normal et le mode Stealth ?",{33}),
]

store=get_store()
score1=score2=0
p=0
for q, expected in CASES:
    docs=store.similarity_search(q,k=config.TOP_K)
    pages=[]
    for d in docs:
        pages.append(d.metadata["page"])
    first_res_ok=pages[0] in expected
    ok_any=any(p in expected for p in pages)
    score1+=first_res_ok
    score2+=ok_any
    p+=1
    print(f"{'[OK]' if ok_any else '[NONOK]'}{f' Q{p} : '}{q}\n--> attendu {sorted(expected)} vs obtenu {pages}")

print(f"\nScore première position : {score1}/{len(CASES)} | Score top-{config.TOP_K} : {score2}/{len(CASES)}")