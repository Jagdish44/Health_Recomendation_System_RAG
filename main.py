from flask import Flask, request, jsonify
import sqlite3
import openai

# Initialize the Flask application
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = 'sk-proj-XPF0fIquEv9wskgJrIc7T3BlbkFJhI84ga8D92IXeIbFKnFu'

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

@app.route('/recommendations', methods=['POST'])
def recommendations():
    data = request.get_json()
    condition = data.get('condition')
    if not condition:
        return jsonify({'error': 'Condition is required'}), 400

    recommendations = get_diet_recommendations(condition)
    gpt_response = chat_with_gpt(f"Provide a brief summary for diet recommendations for {condition}. The recommendations are as follows:\n{recommendations}")
    
    return jsonify({'recommendations': recommendations, 'gpt_response': gpt_response})

if __name__ == '__main__':
    app.run(debug=True)
