from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Set your OpenAI API key
client = OpenAI(
    api_key=st.secrets["openai"]["OPENAI_API_KEY"]
)


def generate_itinerary(input_data):
    """Generate a personalized travel itinerary"""
    prompt = f"""You are an expert AI travel assistant tasked with creating a highly personalized travel itinerary. Carefully analyze the following user details and preferences to craft a unique experience that perfectly matches their needs:

USER PROFILE:
1. Trip Overview: {input_data['description']}
2. Available Budget: {input_data['budget']} INR (unless specified otherwise)
3. Trip Duration: {input_data['duration']} days
4. Destination: {input_data['destination']}
5. Primary Purpose: {input_data['purpose']}

PERSONAL PREFERENCES:
1. Travel Style: {input_data['preferences']}
2. Dietary Requirements: {input_data['dietary']}
3. Special Interests: {input_data['interests']}
4. Physical Considerations: {input_data['walking']}
5. Accommodation Style: {input_data['accommodation']}

PERSONALIZATION REQUIREMENTS:
1. All activities must directly align with stated preferences and interests
2. Daily budget allocation should respect total budget constraints
3. Activity intensity should match walking tolerance
4. Meal suggestions must accommodate dietary requirements
5. Accommodation recommendations should match stated preferences and budget
6: Make sure everything in the trip matches with th description of trip overview given.

CREATE A DAY-BY-DAY ITINERARY WITH:

For Each Day:
MORNING (Time: XX:XX - XX:XX)
- Primary activity matching user interests
- Breakfast recommendation (considering dietary needs)
- Transportation details
- Cost breakdown

AFTERNOON (Time: XX:XX - XX:XX)
- Activities aligned with preferences
- Lunch suggestion (matching dietary requirements)
- Transportation between locations
- Cost breakdown

EVENING (Time: XX:XX - XX:XX)
- Evening activity matching interests
- Dinner recommendation (dietary-appropriate)
- Transportation details
- Cost breakdown

DAILY ESSENTIALS:
1. Accommodation Details:
   - Recommended stay matching preferences
   - Approximate cost per night
   - Location benefits
   - Amenities aligned with needs

2. Transportation:
   - Best methods between activities
   - Estimated costs
   - Time considerations
   - Accessibility notes

3. Activity Mix:
   - 70% activities matching specific interests
   - 30% complementary experiences
   - Balance between popular and hidden gems
   - Attention to physical comfort level

4. Meal Planning:
   - All restaurants pre-screened for dietary requirements
   - Mix of local and familiar options
   - Price range within daily budget
   - Special dietary accommodations

5. Daily Budget Tracking:
   - Activity costs
   - Meal estimates
   - Transportation expenses
   - Running total against overall budget

Local Insights:
1. Weather considerations for the season
2. Cultural etiquette relevant to activities
3. Safety tips for the specific areas
4. Local customs to be aware of
5. Special events during visit dates

FORMAT REQUIREMENTS:
1. Clear day-by-day breakdown for each n number of days
2. Specific timings for all activities
3. Precise cost estimates in INR
4. Alternative suggestions for flexibility
5. Clear transportation instructions
6. Emergency contact information
7. Booking requirements where necessary

Remember: This itinerary must feel exclusively crafted for this specific user. Every suggestion should tie back to their stated preferences, interests, and requirements. Avoid generic recommendations that don't align with their profile."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert AI Travel Assistant with comprehensive knowledge of global destinations, travel planning, and cultural insights. Your mission is to create highly personalized travel experiences while maintaining a natural, conversational approach with users"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def main():
    st.title("🌍 Travel Planner")
    st.markdown("### Plan Your Perfect Trip")

    # Basic trip details
    description = st.text_area("Tell us about your dream trip", 
        help="Describe what kind of experience you're looking for")
    
    col1, col2 = st.columns(2)
    with col1:
        budget = st.text_input("Budget")
        duration = st.text_input("Duration (days)")
        destination = st.text_input("Destination")
        purpose = st.text_input("Purpose of trip")
        preferences = st.text_input("Travel preferences")

    with col2:
        dietary = st.text_input("Dietary preferences (if any)")
        interests = st.text_input("Specific interests (if any)")
        walking = st.text_input("Walking tolerance (if any)")
        accommodation = st.text_input("Accommodation preference (if any)")

    if st.button("Create Travel Plan"):
        # Check required fields
        required_fields = {
            'description': description,
            'budget': budget,
            'duration': duration,
            'destination': destination,
            'purpose': purpose
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        
        if missing_fields:
            st.error(f"Please fill in these required fields: {', '.join(missing_fields)}")
            return

        # Collect all inputs
        input_data = {
            'description': description,
            'budget': budget,
            'duration': duration,
            'destination': destination,
            'purpose': purpose,
            'preferences': preferences,
            'dietary': dietary or "No specific requirements",
            'interests': interests or "No specific interests",
            'walking': walking or "No specific requirements",
            'accommodation': accommodation or "No specific preference"
        }

        # Generate itinerary
        with st.spinner("Creating your travel plan..."):
            itinerary = generate_itinerary(input_data)
            st.markdown("### ✨ Your Travel Itinerary")
            st.markdown(itinerary)
            

if __name__ == "__main__":
    main()