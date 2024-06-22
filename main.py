import sqlite3
import openai

# Set your OpenAI API key
openai.api_key = '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'

def get_diet_recommendations(condition):
    conn = sqlite3.connect('diet_recommendations.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT foods.name, foods.calories, foods.protein, foods.fat, foods.carbs
    FROM foods
    JOIN diet_recommendations ON foods.id = diet_recommendations.food_id
    JOIN health_conditions ON health_conditions.id = diet_recommendations.condition_id
    WHERE health_conditions.condition = ?
    ''', (condition,))

    recommendations = cursor.fetchall()
    conn.close()

    if not recommendations:
        return "No recommendations found for this condition."

    recommendations_str = "\n".join([f"{name}: {calories} kcal, {protein}g protein, {fat}g fat, {carbs}g carbs" for name, calories, protein, fat, carbs in recommendations])
    return recommendations_str

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

def main():
    user_input = input("Enter your health condition: ")
    recommendations = get_diet_recommendations(user_input)
    print(f"Diet recommendations for {user_input}:\n{recommendations}")

    gpt_response = chat_with_gpt(f"Provide a brief summary for diet recommendations for {user_input}. The recommendations are as follows:\n{recommendations}")
    print(f"Summary from GPT:\n{gpt_response}")

if __name__ == "__main__":
    main()
