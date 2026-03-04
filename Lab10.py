import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Games')

def create_game():
    """
    Prompt user for a Game Title.
    Add the game to the database with the title and an empty Developer list.
    """
    title = input("Enter game title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return

    try:
        table.put_item(
            Item={
                "Title": title,
                "Developer": []
            }
        )
        print(f"Created game: {title}")
    except Exception as e:
        print(f"Error creating game: {e}")

def print_all_games():
    """Scan the entire games table and print each item."""
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No games found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} game(s):\n")
    for game in items:
        print_game(game)

def print_game(game):
    """Print a single game's details in a readable format."""
    title = game.get("Title", "Unknown Title")
    developers = game.get("Developer", "No developers")

    
    print(f"  Title : {title}")
    print(f"  Developer: {developers}")
    print()

def update_developer():
    """
    Prompt user for a game Title.
    Prompt user for a developer name.
    Append the developer to the game's Developer list in the database.
    """
    title = input("Enter game title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return
    
    try:
        response = table.get_item(Key={"Title": title})
        if "Item" not in response:
            print(f"game '{title}' not found.")
            return
    except Exception as e:
        print(f"Error fetching game: {e}")
        return

    developer = input("Enter developer name: ").strip()
    if not developer:
        print("Developer name cannot be empty.")
        return

    try:
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Developer = list_append(Developer, :d)",
            ExpressionAttributeValues={
                ":d": [developer]
            },
        )
        print(f"Added developer {developer} to {title}.")
    except Exception as e:
        print(f"Error updating developer: {e}")
        return


def delete_game():
    """
    Prompt user for a game Title.
    Delete that item from the database.
    """
    title = input("Enter game title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return
    
    try:
        response = table.get_item(Key={"Title": title})
        if "Item" not in response:
            print(f"game '{title}' not found.")
            return
    except Exception as e:
        print(f"Error fetching game: {e}")
        return

    try:
        table.delete_item(
            Key={"Title": title},
            ConditionExpression="attribute_exists(Title)"
        )
        print(f"Deleted game: {title}")
    except Exception as e:
        print(f"Error deleting game: {e}")

def query_game():
    """
    Prompt user for a game Title.
    Print out the developer(s) for that game.
    """
    title = input("Enter game title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return

    try:
        response = table.get_item(Key={"Title": title})
        game = response.get("Item")

        if not game:
            print(f"game '{title}' not found.")
            return

        developers = game.get("Developer", [])
        if not developers:
            print(f"game '{title}' has no developer listed yet.")
            return

        print(f"Developer(s) for '{title}': {developers}")
    except Exception as e:
        print(f"Error querying game: {e}")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new game")
    print("Press R: to READ all games")
    print("Press U: to UPDATE a game (add a review)")
    print("Press D: to DELETE a game")
    print("Press Q: to QUERY a game's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_game()
        elif input_char.upper() == "R":
            print_all_games()
        elif input_char.upper() == "U":
            update_developer()
        elif input_char.upper() == "D":
            delete_game()
        elif input_char.upper() == "Q":
            query_game()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
