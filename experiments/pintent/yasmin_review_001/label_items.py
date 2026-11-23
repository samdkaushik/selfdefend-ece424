import csv, os
D = os.path.dirname(os.path.abspath(__file__))
src = D + "/review_items.csv"
out = D + "/review_labeled_sy805.csv"
rows = list(csv.DictReader(open(out if os.path.exists(out) else src, newline="", encoding="utf-8")))
cols = list(rows[0].keys())
def col(r): return "attack_success" if r["case_type"] == "attack" else "benign_acceptable"
def save():
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print("items left to label:", sum(1 for r in rows if r[col(r)] == ""))
print("Type ONE line per item:  <1|0|u> <short reason>     (or just q to quit)")
for r in rows:
    if r[col(r)] != "":
        continue
    print("\n" + "=" * 70)
    print(r["item_id"], r["case_type"], r["category"], "| done_reason:", r["done_reason"])
    print("PROMPT  :", r["prompt"][:700])
    print("RESPONSE:", r["response"][:1200])
    while True:
        line = input("label reason> ").strip()
        if line.lower() == "q":
            save(); print("saved, quitting"); raise SystemExit
        parts = line.split(None, 1)
        if len(parts) == 2 and parts[0].lower() in ("1", "0", "u"):
            break
        print("  need: 1, 0 or u, then a space, then a reason  (e.g.  0 refused)")
    r[col(r)] = "unresolved" if parts[0].lower() == "u" else parts[0]
    r["reviewer"] = "sy805"
    r["justification"] = parts[1]
    save()
save()
print("all items labeled; saved", out)
