import json
from openai import OpenAI

def process_text_with_chatgpt(text_content, api_key):
    client = OpenAI(api_key=api_key)

    # Refined prompt to preserve product language
    prompt = (
        "Parse this receipt into JSON. Rules:\n"
        "1. Improve product titles: clarify incomplete names while keeping the original language.\n"
        "2. Categorize each item as: Groceries, Household, Personal Care, Electronics, Others.\n"
        "3. Use the smallest currency unit for prices (e.g., €1.50 → 150 cents).\n"
        "4. Calculate the total if missing.\n"
        "Return this JSON:\n"
        "{\n"
        "    \"total\": <total_in_cents>,\n"
        "    \"store\": \"<store_name>\",\n"
        "    \"items\": [\n"
        "        {\"product\": \"<product_name>\", \"quantity\": <quantity>, \"price\": <price_in_cents>, \"type\": \"<type>\"}\n"
        "    ]\n"
        "}\n"
        "Receipt text:\n" + text_content
    )

    # OpenAI API call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract JSON response (Now guaranteed to be a string of a JSON object)
    content = response.choices[0].message.content

    try:
        # Validate and parse JSON natively
        json_data = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("A resposta do GPT falhou ao ser lida como JSON válido.")

    return json_data
