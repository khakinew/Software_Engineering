from flask import Flask, render_template, request, jsonify
from zhipuai import ZhipuAI
import time

app = Flask(__name__)

client = ZhipuAI(api_key="a1c47777fabe9ee3ef60aa4f238551ba.9ABk513Zrrjw5PqC")

# Store conversation history in memory (for demo purposes)
# In production, you'd want to use a database or session storage
conversations = {}


def get_chat_response(messages):
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=messages,
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
        tools=[{"type": "web_search", "web_search": {"search_result": True}}],
        stream=False,  # Changed to False for simpler implementation
    )
    return response.choices[0].message.content


@app.route('/')
def home():
    # Generate a unique session ID for each visitor
    session_id = str(int(time.time()))
    conversations[session_id] = [
        {
            "role": "system",
            "content": "你是一个智能鱼塘的管理助手，你的任务是为用户提供专业、准确、有见地的建议。"
        }
    ]
    return render_template('index.html', session_id=session_id)


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data['message']
    session_id = data['session_id']

    if not session_id or session_id not in conversations:
        return jsonify({"error": "Invalid session"}), 400

    # Add user message to conversation history
    conversations[session_id].append({"role": "user", "content": user_input})

    # Get assistant response
    assistant_response = get_chat_response(conversations[session_id])

    # Add assistant response to conversation history
    conversations[session_id].append({"role": "assistant", "content": assistant_response})

    return jsonify({"response": assistant_response})


if __name__ == '__main__':
    app.run(debug=True,
            port=2222)