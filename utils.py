from collections import Counter

def stampa_risultati(tickets, risultati, titolo, tempo):
    print("\n" + "=" * 90)
    print(f"{titolo}".center(90))
    print("=" * 90)

    print(f"{'ID':<5} {'CATEGORIA':<15} MESSAGGIO")
    print("-" * 90)

    for t, r in zip(tickets, risultati):
        msg = (t.messaggio[:55] + "...") if len(t.messaggio) > 55 else t.messaggio
        print(f"{t.id:<5} {r.upper():<15} {msg}")

    print("-" * 90)

    print("\n📊 RIEPILOGO")
    print("-" * 40)

    conteggio = Counter(risultati)

    for categoria, n in conteggio.most_common():
        barra = "█" * n
        print(f"{categoria:<15} {n:<3} {barra}")

    print("-" * 40)
    print(f"⏱ Tempo totale: {tempo}s")
    print("=" * 90 + "\n")