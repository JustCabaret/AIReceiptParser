import json
from openai import OpenAI

def process_text_with_chatgpt(text_content, api_key):
    client = OpenAI(api_key=api_key)

    # Refined prompt to preserve product language
    prompt = (
        "Parse the receipt and return a JSON. Tasks:\n"
        "1. Keep product names in the receipt's language, improving formatting (fix capitalization, expand abbreviations).\n"
        "2. Categorize each product into types in English (e.g., Grocery, Household, Leisure).\n"
        "3. Return prices in the smallest currency unit (e.g., €1.50 → 150 cents).\n"
        "4. Calculate the total if missing.\n"
        "5. Return only this JSON:\n"
        "{\n"
        "    \"total\": <total_in_cents>,\n"
        "    \"store\": \"<store_name>\",\n"
        "    \"items\": [\n"
        "        {\"product\": \"<product_name>\", \"quantity\": <quantity>, \"price\": <price_in_cents>, \"type\": \"<type_in_english>\"}\n"
        "    ]\n"
        "}"
        "Receipt text:\n" + text_content
    )

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

    # Save JSON to a file
    with open("receipt_data.json", "w", encoding="utf-8") as file:
        file.write(json_data)

    # Load the JSON to format it properly in the console
    formatted_json = json.loads(json_data)
    print(json.dumps(formatted_json, indent=4, ensure_ascii=False))

    return json_data
