import json
with open("knowledgebase.json", "r") as json_file:
    destinations = json.load(json_file)
weathers = ['Cold','Mild','Tropical','Hot','Temperate','Varies','any']
Purpose = ['Tourism and Relaxation','Fun','Adventure','Religious','Exploration','Leisure','any']
# print(len(destinations))
# print(destinations['San Francisco'])
def recommend_destination(destinations, weathers, Purpose):
    name = input('Your Good name: ')
    print(f"Hello {name}!, Welcome to Bharatiye Travel advisory system!")
    print("Select Weather for travel site:")
    for i, weather in enumerate(weathers):
        print(f"{i + 1}. {weather}")

    n = int(input("Enter your choice for Weather from above options: "))
    climate = weathers[n - 1]
    print("Select Purpose of travel:")
    for i, purpose in enumerate(Purpose):
        print(f"{i + 1}. {purpose}")

    m = int(input("Enter your choice for purpose of your travel from above options: "))
    purpose = Purpose[m - 1]
    peoples = int(input('Number of peoples going to travel: '))
    budget = int(input("Enter your total budget for travel: "))
    activity = input('Activities: ')
    rating = float(input('Enter minimum user rating: '))

    final_destinations = []
    for dest, info in destinations.items():
        if (climate.lower() == 'any' or info['Climate'].lower() == climate.lower()) \
                and (purpose.lower() == 'any' or info['Purpose'].lower() == purpose.lower()) \
                and (info['Budget']*peoples <= budget) and (activity.lower() == 'any' or activity.lower() in [act.lower() for act in info["Activities"]]) \
                and (rating <= info['User Rating']):
            final_destinations.append((dest, info))
    
    return final_destinations

def add_new_destination(destinations):
    print("Add a New Destination:")
    name = input("Enter the destination name: ")
    
    if name in destinations:
        print(f"{name} already exists in the destinations.")
        return

    location = input("Enter the location: ")
    climate = input("Enter the climate: ")
    activities = input("Enter activities (comma-separated): ").split(',')
    user_rating = float(input("Enter user rating (0.0 - 10.0): "))
    budget = int(input("Enter budget for one person: "))
    purpose = input("Enter purpose: ")
    duration_preferred = input("Enter duration preferred: ")

    feedback = []
    user = input("Enter your name for feedback: ")
    comment = input("Enter your comment: ")
    feedback.append({"User": user, "Rating": user_rating, "Comment": comment})

    destinations[name] = {
        "Location": location,
        "Climate": climate,
        "Activities": activities,
        "User Rating": user_rating,
        "Feedback": feedback,
        "Budget": budget,
        "Purpose": purpose,
        "Duration Preferred": duration_preferred,
    }
    with open("knowledgebase.json", "w") as json_file:
        json.dump(destinations, json_file)
    print(f"{name} has been added to the destinations.")

def add_feedback(destinations):
    print("Add Feedback to a Destination:")
    name = input("Enter the name of the destination to add feedback to: ")

    if name not in destinations:
        print(f"{name} does not exist in the destinations.")
        return

    user = input("Enter your name: ")
    rating = float(input("Enter your rating (0.0 - 10.0): "))
    comment = input("Enter your comment: ")

    destinations[name]["Feedback"].append({"User": user, "Rating": rating, "Comment": comment})
    with open("knowledgebase.json", "w") as json_file:
        json.dump(destinations, json_file)
    print("Feedback has been added to the destination.")
def check_feedback(destinations):
    print("Check Feedback for a Destination:")
    name = input("Enter the name of the destination to check feedback for: ")

    if name not in destinations:
        print(f"{name} does not exist in the destinations.")
        return

    feedback_list = destinations[name]["Feedback"]

    if not feedback_list:
        print(f"No feedback available for {name}.")
    else:
        print(f"Feedback for {name}:")
        for feedback in feedback_list:
            print(f"User: {feedback['User']}, Rating: {feedback['Rating']}, Comment: {feedback['Comment']}")
def main():
    final_destinations = recommend_destination(destinations, weathers, Purpose)
    
    if not final_destinations:
        print("Sorry, no matching destinations found based on your preferences.")
    else:
        final_destinations.sort(key=lambda x: x[1]["User Rating"], reverse=True)
        print("Recommended destinations based on your preferences:")
        for i, (destination, info) in enumerate(final_destinations):
            print(f"{i + 1}. {destination} ({info['Location']})")
            print(f"Weather: {info['Climate']}")
            print(f"Activities: {', '.join(info['Activities'])}")
            print(f"User Rating: {info['User Rating']}")
            print(f"Budget : {info['Budget']}")
            print(f"Duration Preferred: {info['Duration Preferred']}")
            print(f"Feedback:")
            for feedback in info['Feedback']:
                print(f"- User: {feedback['User']}, Rating: {feedback['Rating']}, Comment: {feedback['Comment']}")
            print()

if __name__ == "__main__":
    
    while True:
        print('''Welcome to Our Advisory System:-
1. Recommend Destinantion
2. Add new destination
3. Add feedback for a destinantion
4. Check feedback for a existing destination
5. exit''')
        n = int(input('Enter your choice: '))
        if n==1:
            main()
        elif n==2:
            add_new_destination(destinations)
        elif n==3:
            add_feedback(destinations)
        elif n==4:
            check_feedback(destinations)
        elif n==5:
            print('Thank you for using our Travel advisory system!!')
            break