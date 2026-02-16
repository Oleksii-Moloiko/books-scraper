import sqlite3
import matplotlib.pyplot as plt

DB = "my_books.db"

con = sqlite3.connect(DB)
cur = con.cursor()

# Графік 1: кількість книг по рейтингу
ratings = cur.execute("""
SELECT rating, COUNT(*)
FROM books
GROUP BY rating
ORDER BY rating
""").fetchall()

x = [r for r, _ in ratings]
y = [c for _, c in ratings]

plt.figure()
plt.bar(x, y)
plt.title("Books count by rating")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.savefig("rating_counts.png", dpi=150, bbox_inches="tight")


# Графік 2: розподіл цін (гістограма)
prices = [p[0] for p in cur.execute("SELECT price FROM books").fetchall()]

plt.figure()
plt.hist(prices, bins=30)
plt.title("Price distribution")
plt.xlabel("Price (£)")
plt.ylabel("Count")
plt.savefig("price_distribution.png", dpi=150, bbox_inches="tight")


con.close()
