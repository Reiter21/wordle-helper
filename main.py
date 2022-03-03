from cs50 import sql

db = sql.SQL("sqlite:///words.db")

query = "SELECT word FROM words WHERE word LIKE ? ?"

plug = ""
correct_letters = "_____"
incorrect_positions = set()
incorrect_letters = set()
potential_letters = set()

while True:
    word = input("Enter word entered: ")
    if len(word) != 5:
        print("invalid")
        break
    status = input("Input colors of every letter with corresonding letter [green: g, yellow: y, grey: w]: ")
    
    for i in range(5):
        if status[i] == 'g':
            tmp = list(correct_letters)
            tmp[i] = word[i]
            correct_letters = "".join(tmp)
        elif status[i] == 'y':
            tmp = ["_", "_", "_", "_", "_"]
            tmp[i] = word[i]
            incorrect_positions.add("".join(tmp))
            potential_letters.add(f"%{word[i]}%")
    for i in range(5):
        if status[i] == 'w':
            if not word[i] in correct_letters:
                incorrect_letters.add(f'%{word[i]}%')

    for letter in incorrect_letters:
        plug += f" AND NOT word LIKE '{letter}'"
    for pos in incorrect_positions:
        plug += f" AND NOT word LIKE '{pos}'"
    for letter in potential_letters:
        plug += f" AND word LIKE '{letter}'"

    matches = db.execute(f"SELECT word FROM words WHERE word LIKE '{correct_letters}'{plug} ORDER BY word;")

    for match in matches:
        print(match['WORD'])
