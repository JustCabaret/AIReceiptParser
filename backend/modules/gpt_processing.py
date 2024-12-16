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
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract JSON response
    content = response.choices[0].message.content

    try:
        # Validate if content is a valid JSON
        json_data = json.loads(content[content.find("{"):content.rfind("}") + 1])
    except json.JSONDecodeError:
        raise ValueError("A resposta do GPT não contém um JSON válido.")

    return json_data
