import pandas as pd


def helper(choice):
    if choice == "movie":
        df = pd.read_csv("data/movie_ids.csv")
    elif choice == "book":
        df = pd.read_csv("data/book_ids.csv")
    elif choice == "music":
        df = pd.read_csv("data/music_ids.csv")
    else:
        return

    print("Press press q to quit")
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    for row in range(1682):
        if len(df.iloc[row]["mood"]) != 2:
            continue

        print("ID: " + str(df.iloc[row]["id"]) + "  Name:  " + df.iloc[row]["name"])
        print("Mood:  0: Angry, 1: Disgusted, 2: Fearful, 3: Happy, 4: Neutral, 5: Sad, 6: Surprised")

        inp = input("-  ")
        if inp == 'q':
            df.to_csv('data/movie_ids.csv', index=False)
            return

        inp = list(inp)
        mood = list()
        for emotion in inp:
            mood.append(emotion_dict[int(emotion)])
        df.at[row, "mood"] = mood
        print(mood)


helper("movie")  # movie, book, music
