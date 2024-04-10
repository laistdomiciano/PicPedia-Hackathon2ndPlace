# run with: python3 -W ignore: main.py
import wikipedia
import random
from PIL import Image
import requests
from io import BytesIO
import os
#import winsound
import warnings

#lostsound.Beep(432, 500)

#winsound.Beep(500, 432)

categories = {
    '1': ['Sport'],
    '2': ['Mass Media'],
    '3': ['Science']
}


def filter_images(starting_images):
    images_filter = []
    for image in starting_images:
        if ".png" in image[-4:] or ".jpg" in image[-4:]:
            images_filter.append(image)
    return images_filter


# Example usage:

def display_image_from_url(url):
    headers = {
        'User-Agent': 'My User Agent 1.0'
    }
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        # Loading
        print("\033[94mLoading image...\033[0m")
        try:
            # Open the image using Pillow
            image = Image.open(BytesIO(response.content))

            # Display the image
            image.show()
        except Image.UnidentifiedImageError:
            print(f"Failed to identify image from {url}. Please check the image format.")
    else:
        print(f"Failed to fetch image from {url}. Status code: {response.status_code}")


def choose_players_round():
    print("Please choose the number of players for this round:")
    players_round = int(input("Enter the number of players: "))
    if players_round > 0:
        print(f"You have selected {players_round} players for this round.")
        # Loading
        print("\033[94mLoading game...\033[0m")
        return players_round
    else:
        print("Players rounds should be more than Zero")
        return choose_players_round()


def choose_category():
    os.system('clear')
    print("Please choose a category by entering the number:")
    for number, name in categories.items():
        print(f"{number}. {name[0]}")
    choice = input("Enter your choice (1, 2, or 3): ").strip()

    if choice in categories:
        selected_category = categories[choice][0]
        print(f"You have selected {selected_category}.")
        # Loading
        print("\033[94mLoading game...\033[0m")
        return selected_category
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        return choose_category()


def game_setup():
    os.system('clear')
    print("Welcome to PicPedia!")
    print("""
     \033[1;36mWelcome to PicPedia, the ultimate test of your visual knowledge!\033[0m

     \033[1;33mHere's how to play:\033[0m

     \033[1;35mSelect Number of Players:\033[0m
     Choose the number of players joining this round. Gather your friends and get ready for some fun! 

     \033[1;35mChoose a Category:\033[0m
     Pick a category that interests you the most. We have three exciting categories to choose from: \033[1;32mSport\033[0m, \033[1;32mMass Media\033[0m, and \033[1;32mScience\033[0m.

     \033[1;35mEarn Points:\033[0m
     Each correct guess earns you a point. Try to score as high as you can to claim victory!

     \033[1;35mWho Will Win?\033[0m
     Compete with your friends over five rounds of image guessing. The player with the highest score at the end wins the game!
     """)
    players_round = choose_players_round()
    print(f"Number of Players: {players_round}")
    players_scores = {player + 1: 0 for player in range(players_round)}

    # loop on the players_round
    for player in range(1, players_round +1):
        score = 0  # score stars here
        selected_category = choose_category()
        print(f"Selected Category: {selected_category}")
        print(f"\nPlayer {player}, get ready to play!")
        print()

        links = get_ten_links_from_category(selected_category)
        right_links = links[0:5]
        wrong_links = links[5:10]

        assert links, "No links acquired"
        images = get_five_images_from_links(right_links)
        assert images, "No images acquired"

        # FOR I IN RANGE LEN
        for i in range(len(images)):
            # 5
            image = images[i]
            if image[-4:] == "svg":
                pass
            else:
                display_image_from_url(image)
                os.system('clear')
                print("What article is this picture from? ")
                right = {"article": right_links[i], "right": True}
                wrong = {"article": wrong_links[i], "right": False}
                my_list = [right, wrong]
                random.shuffle(my_list)
                [a, b] = my_list
                print(f" a.  {a['article']}")
                print(f" b.  {b['article']}")
                answer = input("What's the right answer? Enter a or b here: ")
                user_article = " "
                if answer == "a":
                    user_article = a["article"]
                elif answer == "b":
                    user_article = b["article"]
                else:
                    print("Invalid answer, choose a or b: ")
                if user_article == right["article"]:
                    print("\U0001F600 \033[92mCorrect!\033[0m")  # Happy emoji for correct answer
                    score += 1
                else:
                    print("\U0001F614 \033[91mWrong\033[0m")
                    #print(f"Your current score is {score}")  # print score
                input("\033[93mPress any key to continue to the next image..\033[0m")

        players_scores[player] = score
        print(f"Player {player}'s score after this round is {score}")

        print("\nFinal Scores: ")
        for player, score in players_scores.items():
            print(f"Player {player}: {score}")
def get_ten_links_from_category(selected_category):
    category_page = wikipedia.page(selected_category, auto_suggest=False)
    category_links = category_page.links
    random.shuffle(category_links)
    return category_links[:10]


def get_five_images_from_links(category_links):
    images = []
    for link in category_links:
        try:
            starting_images = wikipedia.page(link).images
            filtered_images = filter_images(starting_images)
            # to be fixed
            if not filtered_images:
                pass
            else:
                image = random.choice(filtered_images)
                images.append(image)
        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
            pass
    return images


#def turn_images_into_quiz(images):
    #2print(images)


def main():
    game_setup()


if __name__ == "__main__":
    main()