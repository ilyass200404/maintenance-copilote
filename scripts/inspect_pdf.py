from pypdf import PdfReader

dbook="data/manuals/prusa3d_manual.pdf"
pg=[71,72]
vides=0
rd=PdfReader(dbook)
print("-- Nombre de pages :", len(rd.pages))
for p in rd.pages:
    t=rd.extract_text()
    if t is None:
        t=""
    t=t.strip()
    if len(t) < 50:
        vides+=1
print("-- Pages quasi vides :", vides)

for n in pg:
    if n<=len(rd.pages):
        print(f"\n--- Page {n} ---")
        print((rd.pages[n-1].extract_text()or"")[:600])
        print("\n")