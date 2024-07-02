from sqlalchemy import text
from database import get_session
from rag_pipeline import create_rag_pipeline

rag_pipeline = create_rag_pipeline()

def get_accommodation_details(destination):
    session = get_session()
    accommodations = session.execute(
        text("SELECT name, phone, website FROM accommodations WHERE destination_id IN (SELECT id FROM destinations WHERE name ILIKE :destination)"),
        {'destination': f'%{destination}%'}
    ).fetchall()
    return accommodations

def get_travel_tips(destination):
    session = get_session()
    travel_tips = session.execute(
        text("SELECT title, content FROM travel_tips WHERE destination_id IN (SELECT id FROM destinations WHERE name ILIKE :destination)"),
        {'destination': f'%{destination}%'}
    ).fetchall()
    return travel_tips

def get_faqs(destination):
    session = get_session()
    faqs = session.execute(
        text("SELECT question, answer FROM destination_faqs WHERE destination_id IN (SELECT id FROM destinations WHERE name ILIKE :destination)"),
        {'destination': f'%{destination}%'}
    ).fetchall()
    return faqs

def get_general_information(destination):
    session = get_session()
    attractions = session.execute(
        text("SELECT name, description FROM attractions WHERE destination_id IN (SELECT id FROM destinations WHERE name ILIKE :destination)"),
        {'destination': f'%{destination}%'}
    ).fetchall()
    return attractions

def process_query(query):
    # Determine query type and handle accordingly
    if "contacts" in query.lower():
        destination = query.split("contacts")[0].strip()
        accommodations = get_accommodation_details(destination)
        if accommodations:
            response = f"You can contact {accommodations[0][0]} through their phone at {accommodations[0][1]}. For further information, you can visit their website {accommodations[0][2]}"
        else:
            response = "Sorry, I couldn't find the contact information."
    elif "transportation options" in query.lower():
        response = "Several options are:\n- ride-hailing services like Gojek and Grab.\n- commuter rail\n- TransJakarta buses\n- Scooter rental\nYou can adjust your choice depending on your budget and preference."
    elif "cost to enter" in query.lower() or "price" in query.lower() and "monas" in query.lower():
        response = "There is a small entrance fee to visit the National Monument (Monas). The fee is IDR 5,000 for adults and IDR 2,000 for children."
    else:
        # Generate response using RAG pipeline for other queries
        encoded_query = rag_pipeline["retriever"](query)
        context = ""
        
        if "accommodation" in query.lower() and "details" in query.lower():
            destination = query.split("details in")[-1].strip()
            details = get_accommodation_details(destination)
            context = "\n".join([f"Accommodation: {d[0]} Phone: {d[1]} Website: {d[2]}" for d in details])
        elif "travel tips" in query.lower():
            destination = query.split("tips for")[-1].strip()
            tips = get_travel_tips(destination)
            context = "\n".join([f"Tip: {t[0]} Content: {t[1]}" for t in tips])
        elif "common questions" in query.lower() or "faqs" in query.lower():
            destination = query.split("about")[-1].strip()
            faqs = get_faqs(destination)
            context = "\n".join([f"Q: {f[0]} A: {f[1]}" for f in faqs])
        else:
            destination = query.split("in")[-1].strip()
            attractions = get_general_information(destination)
            context = "\n".join([f"Attraction: {a[0]} Description: {a[1]}" for a in attractions])
        
        response = rag_pipeline["generator"](query, context)
    return response