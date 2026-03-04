# name: YOUR NAME HERE
# date:
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 0 (out of 5) -- if I don't change this, I agree to get 0 points.

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Movies')

def create_movie():
    """
    Prompt user for a Movie Title.
    Add the movie to the database with the title and an empty Ratings list.
    """
    title = input("Enter movie title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return

    try:
        table.put_item(
            Item={
                "Title": title,
                "Ratings": []
            }
        )
        print(f"Created movie: {title}")
    except Exception as e:
        print(f"Error creating movie: {e}")

def print_all_movies():
    """Scan the entire Movies table and print each item."""
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No movies found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} movie(s):\n")
    for movie in items:
        print_movie(movie)

def print_movie(movie):
    """Print a single movie's details in a readable format."""
    title = movie.get("Title", "Unknown Title")
    year = movie.get("Year", "Unknown Year")
    runtime = movie.get("Runtime (mins)", "Unknown Runtime")
    ratings = movie.get("Ratings", "No ratings")

    
    print(f"  Title : {title}")
    print(f"  Year  : {year}")
    print(f"  Ratings: {ratings}")
    print(f"  Runtime: {runtime}")
    print()

def update_rating():
    """
    Prompt user for a Movie Title.
    Prompt user for a rating (integer).
    Append the rating to the movie's Ratings list in the database.
    """
    title = input("Enter movie title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return
    
    try:
        response = table.get_item(Key={"Title": title})
        if "Item" not in response:
            print(f"Movie '{title}' not found.")
            return
    except Exception as e:
        print(f"Error fetching movie: {e}")
        return

    rating_text = input("Enter rating (integer): ").strip()
    try:
        rating = int(rating_text)
    except ValueError:
        print("Rating must be an integer.")
        return

    try:
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(Ratings, :r)",
            ExpressionAttributeValues={
                ":r": [rating]
            },
        )
        print(f"Added rating {rating} to {title}.")
    except Exception as e:
        print(f"Error updating rating: {e}")

def delete_movie():
    """
    Prompt user for a Movie Title.
    Delete that item from the database.
    """
    print("deleting movie")

def query_movie():
    """
    Prompt user for a Movie Title.
    Print out the average of all ratings in the movie's Ratings list.
    """
    print("query movie")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to QUERY a movie's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
