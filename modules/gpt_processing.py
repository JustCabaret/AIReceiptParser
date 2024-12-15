from openai import OpenAI

def process_text_with_chatgpt(text_content, api_key):
    client = OpenAI(api_key=api_key)

    # Refined prompt to preserve product language
    prompt = """
    Parse the receipt and return a JSON. Tasks:
    1. Keep product names in the receipt's language, improving formatting (fix capitalization, expand abbreviations).
    2. Categorize each product into types in English (e.g., Grocery, Household, Leisure).
    3. Return prices in the smallest currency unit (e.g., €1.50 → 150 cents).
    4. Calculate the total if missing.
    5. Return only this JSON:
    {
        "total": <total_in_cents>,
        "store": "<store_name>",
        "items": [
            {"product": "<product_name>", "quantity": <quantity>, "price": <price_in_cents>, "type": "<type_in_english>"}
        ]
    }
    Receipt text:
    """ + text_content

    # OpenAI API call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract JSON response
    content = response.choices[0].message.content
    json_data = content[content.find("{"):content.rfind("}") + 1]
    return json_data