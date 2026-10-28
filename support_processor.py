import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Step 5: Securely load environment variables from .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

# Step 1: Create Sample Tickets (Mix of billing, bug, questions, tones)
tickets = [
    {
        "id": "TICK-001",
        "customer": "rohith p s",
        "text": "I was charged twice for my monthly subscription this month! Please refund the extra charge immediately."
    },
    {
        "id": "TICK-002",
        "customer": "tony stark",
        "text": "Every time I click the 'Export to CSV' button on the dashboard, the page goes completely blank and throws a 500 error."
    },
    {
        "id": "TICK-003",
        "customer": "steve rogers ",
        "text": "Hi team, what are your standard support hours over the upcoming weekend holidays?"
    },
    {
        "id": "TICK-004",
        "customer": "bruce banner",
        "text": "My team cannot log into the workspace since this morning. It says password incorrect even after resetting it twice."
    },
    {
        "id": "TICK-005",
        "customer": "henry cavil",
        "text": "Can we upgrade our current plan to include custom branding options? Let me know the steps."
    }
]

def classify_ticket(ticket_text):
    """Sends ticket text to Gemini and requests structured JSON output."""
    prompt = f"""
    Analyze the following support ticket and classify it. You must return ONLY a valid JSON object with these exact keys:
    - "category": (e.g., "Billing", "Technical Bug", "Account Access", "General Question", "Feature Request")
    - "urgency": ("Low", "Medium", "High", "Critical")
    - "suggested_action": (A short, actionable sentence on what support staff should do)

    Support Ticket:
    "{ticket_text}"
    """
    
    # Step 3: Parse and Handle Errors with try/except
    try:
        
       
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',  # <-- Ultra-reliable model
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json"
            ),
        )
       
        
        
        # Parse the JSON response returned by the model
        result_data = json.loads(response.text)
        return {
            "success": True,
            "category": result_data.get("category", "Uncategorized"),
            "urgency": result_data.get("urgency", "Medium"),
            "suggested_action": result_data.get("suggested_action", "Review manually.")
        }
        
    except json.JSONDecodeError:
        return {
            "success": False,
            "category": "Parsing Error",
            "urgency": "Medium",
            "suggested_action": "Malformed JSON returned by model; manual review required."
        }
    except Exception as e:
        return {
            "success": False,
            "category": "API Error",
            "urgency": "High",
            "suggested_action": f"API or network failure: {str(e)}"
        }

def main():
    print("=" * 60)
    print("🤖 AI Support Desk Ticket Processor Starting...")
    print("=" * 60)
    
    processed_results = []
    category_counts = {}
    urgency_counts = {}
    
    for ticket in tickets:
        print(f"\nProcessing {ticket['id']} from {ticket['customer']}...")
        classification = classify_ticket(ticket["text"])
        
        # Combine original ticket data with LLM classification
        processed_ticket = {**ticket, **classification}
        processed_results.append(processed_ticket)
        
        # Track counts for Step 4 summary
        cat = classification["category"]
        urg = classification["urgency"]
        
        category_counts[cat] = category_counts.get(cat, 0) + 1
        urgency_counts[urg] = urgency_counts.get(urg, 0) + 1
        
        print(f"  -> Category: {cat} | Urgency: {urg}")
        print(f"  -> Action: {classification['suggested_action']}")

    # Save structured results to a JSON file
    output_filename = "processed_tickets.json"
    with open(output_filename, "w") as f:
        json.dump(processed_results, f, indent=4)
    print(f"\n📁 Results saved successfully to {output_filename}")

    # Step 4: Generate and Print Summary
    print("\n" + "=" * 60)
    print("📊 TICKET PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Total Tickets Processed: {len(tickets)}")
    
    print("\nBreakdown by Category:")
    for cat, count in category_counts.items():
        print(f"  - {cat}: {count}")
        
    print("\nBreakdown by Urgency:")
    for urg, count in urgency_counts.items():
        print(f"  - {urg}: {count}")
    print("=" * 60)

if __name__ == "__main__":
    main()