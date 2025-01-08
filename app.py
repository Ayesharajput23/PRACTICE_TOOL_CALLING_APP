from langchain_core.tools import tool
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
import streamlit as st

GOOGLE_API_KEY = "AIzaSyDlGuiJOqQePVsQEu5gWiftb74RDGvcq-c"
@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b."""
    print("function is called")
    return a * b
@tool(parse_docstring=True)
def get_latest_news(topic: str) -> str:
    """
    Fetches the latest news for a given topic.

    Args:
        topic (str): The topic to search for news articles.

    Returns:
        str: A formatted string containing the tool name, the latest news titles, and their respective links.

    Example:
        get_latest_news("Technology")
    """
    api_key = "e9c6d47717ab4738b733f4a8e15f9375"  # Replace with your actual API key
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get('articles'):
            articles = data['articles']
            result = f"Tool used: get_latest_news\n get_latest_news tool is used \nHere are the latest news articles related to {topic}:\n"

            for article in articles[:10]:  # Limiting to 5 articles
                title = article['title']
                url = article['url']
                result += f"- {title}: {url}\n"

            return result
        else:
            return f"Error: Could not fetch news for {topic}. Reason: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error: Unable to fetch news. Details: {str(e)}"

@tool(parse_docstring=True)
def get_movie_details(movie_name: str) -> str:
    """
    Fetches detailed information about a movie using its name.

    Args:
        movie_name (str): The name of the movie.

    Returns:
        str: A detailed summary of the movie, including title, year, genre, director, plot, and rating.

    Raises:
        Exception: If the movie is not found or the API request fails.
    """
    import requests

    api_key = "31f29fd0"  # Replace with your OMDB API key
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "True":
            title = data.get("Title", "N/A")
            year = data.get("Year", "N/A")
            genre = data.get("Genre", "N/A")
            director = data.get("Director", "N/A")
            plot = data.get("Plot", "N/A")
            imdb_rating = data.get("imdbRating", "N/A")

            return (
                f"Tool used: get_movie_details\n"
                f"Movie Details:\n"
                f"- Title: {title}\n"
                f"- Year: {year}\n"
                f"- Genre: {genre}\n"
                f"- Director: {director}\n"
                f"- Plot: {plot}\n"
                f"- IMDb Rating: {imdb_rating}/10"
            )
        else:
            return f"Tool used: get_movie_details\nMovie not found: {movie_name}"
    except Exception as e:
        return f"Tool used: get_movie_details\nError fetching movie details: {str(e)}"
@tool(parse_docstring=True)
def get_recipe(dish_name: str) -> str:
    """Fetches a recipe for a given dish name using the Spoonacular API.

    Args:
        dish_name (str): The name of the dish for which the recipe is to be fetched.

    Returns:
        str: The recipe with ingredients and instructions.
    """
    try:
        api_key = '716e3a77f3e841669be0a6974ff05b9b'  # Replace with your Spoonacular API key
        url = f"https://api.spoonacular.com/recipes/complexSearch?query={dish_name}&apiKey={api_key}&number=1"
        response = requests.get(url)
        data = response.json()

        if data.get('results'):
            recipe_id = data['results'][0]['id']
            recipe_title = data['results'][0]['title']
            
            # Fetch detailed recipe information
            details_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}"
            details_response = requests.get(details_url)
            details_data = details_response.json()
            
            ingredients = details_data.get('extendedIngredients', [])
            instructions = details_data.get('instructions', 'No instructions available.')

            # Create the recipe text
            recipe_text = f"Recipe for {recipe_title}:\n\nIngredients:\n"
            for ingredient in ingredients:
                recipe_text += f"- {ingredient['original']}\n"
            
            recipe_text += f"\nInstructions:\n{instructions}"
            
            return f"Tool used: get_recipe\n{recipe_text}"
        else:
            return f"Error: Could not find a recipe for {dish_name}. Try another dish name."
    except Exception as e:
        return f"Error: Unable to fetch recipe. Details: {str(e)}"
@tool
def get_distance(location1: str, location2: str) -> str:
    """
    Calculates the distance between two locations using the OpenCage Geocoder API.

    This function uses the OpenCage Geocoder API to get the geographic coordinates (latitude and longitude) 
    of the provided locations, then computes the distance between the two points using the Haversine formula.

    Args:
        location1 (str): The first location (e.g., "New York").
        location2 (str): The second location (e.g., "Los Angeles").

    Returns:
        str: A message containing the calculated distance in kilometers between the two locations.

    Raises:
        Exception: If either location is invalid or the API requests fail.
    """
    
    api_key = "52420d959f5749cfbd67a5258d590195"  # Replace with your OpenCage API key
    
    # Geocode the origin location
    url1 = f"https://api.opencagedata.com/geocode/v1/json?q={location1}&key={api_key}"
    response1 = requests.get(url1)
    
    # Geocode the destination location
    url2 = f"https://api.opencagedata.com/geocode/v1/json?q={location2}&key={api_key}"
    response2 = requests.get(url2)
    
    # Check if both responses are successful
    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.json()
        data2 = response2.json()

        # Extract latitude and longitude for both locations
        lat1, lon1 = data1['results'][0]['geometry']['lat'], data1['results'][0]['geometry']['lng']
        lat2, lon2 = data2['results'][0]['geometry']['lat'], data2['results'][0]['geometry']['lng']

        # Calculate the distance using the Haversine formula
        from math import radians, sin, cos, sqrt, atan2
        
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        # Radius of the Earth in kilometers
        radius = 6371.0
        
        # Calculate the distance
        distance = radius * c
        
        return f"Tool used: get_distance\n get_distance tool is used to find The distance between {location1} and {location2} is {distance:.2f} km."
    
    else:
        return f"Error: Could not calculate the distance. Check if both locations are valid.\nTool used: get_distance"
@tool
def get_stock_price(symbol: str) -> str:
    """Fetches the current stock price of a company based on its stock symbol using the Polygon API.

    Args:
        symbol (str): The stock symbol of the company (e.g., 'AAPL' for Apple, 'GOOGL' for Google).

    Returns:
        str: A message containing the current stock price of the company.

    Raises:
        HTTPError: If the HTTP request to the stock API fails (e.g., 404 or 500 status).
        RequestException: If there is an issue with the request itself (e.g., connection error).
        Exception: For any other unexpected errors during the execution of the function.

    """
    api_key =  "2bx0DyQuypHfwohF46294_29KpFtMKzt"  # Replace this with your actual secret API key from Polygon
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev"  # Polygon endpoint for previous close price

    try:
        # Send a GET request with the API key
        response = requests.get(url, params={'apiKey': api_key})
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

        # Assuming the data contains 'close' in the response for the last closing price
        data = response.json()
        price = data.get('results', [{}])[0].get('c')  # 'c' is the closing price

        if price:
            return f"Tool used: get_stock_price\n get_stock_price tool is used to find The current price of {symbol} is ${price}"
        else:
            return f"Error: Could not retrieve stock data for {symbol}.\nTool used: get_stock_price"

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}\nTool used: get_stock_price"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}\nTool used: get_stock_price"
    except Exception as err:
        return f"An unexpected error occurred: {err}\nTool used: get_stock_price"

@tool(parse_docstring=True)
def get_ip_address() -> str:
    """Fetches the user's public IP address.

    Args:
        None

    Returns:
        str: A message containing the user's public IP address.
    """
    try:
        ip = requests.get('https://api.ipify.org').text
        return f"get_ip_address tool is used to find Your public IP address is {ip}."
    except Exception as e:
        return f"Error: Unable to fetch IP address. Details: {str(e)}"
    


tools = [multiply,get_latest_news,get_movie_details,get_recipe,get_distance,get_stock_price,get_ip_address]

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash-exp" , api_key=GOOGLE_API_KEY)

agent = initialize_agent(tools, llm , agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION )


# Frontend

st.title("Practice Tool Calling App")
user_input = st.text_input("Ask anything")

if st.button("Submit"):
    result = agent.invoke(user_input)
    st.write(result["output"])