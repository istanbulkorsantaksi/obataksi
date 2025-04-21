
from flask import Flask, request, jsonify, render_template_string
import openai

app = Flask(__name__)

# SAHTE API ANAHTARI - GERÇEK BAĞLANTI KURMAZ, SADECE TEST İÇİN
openai.api_key = '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'

erdem_prompt = """
Sen İstanbul'da korsan taksicilik yapan sert bir şoförsün. Adın Erdem.
Ağzın biraz bozuk, ama saygısız değilsin. Trip atmayı, laf sokmayı seversin.
Cümlelerin kısa, dobra ve mizah dolu. Sanki trafikte sinirli bir adam gibi konuş.
"""

@app.route("/")
def index():
    return render_template_string(html_page)

@app.route("/erdem-chat", methods=["POST"])
def erdem_chat():
    try:
        user_message = request.json.get("message", "")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": erdem_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=200
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"Erdem: Bağlantı yok. ({str(e)})"})

html_page = '''
<!DOCTYPE html>
<html lang="tr">
<head><meta charset="UTF-8"><title>Şoför Erdem</title></head>
<body style="background:#111;color:#eee;font-family:monospace;padding:40px;text-align:center;">
<h1>🧔 Şoför Erdem</h1>
<p>Yaz bakalım bir şeyler, belki sinirlenmez.</p>
<div id="chatBox" style="max-width:600px;margin:20px auto;background:#222;padding:20px;border-radius:10px;text-align:left;"></div>
<input id="userInput" placeholder="Mesaj yaz..." style="padding:10px;width:60%;" />
<button onclick="sendMessage()" style="padding:10px 20px;background:#f44;color:white;">Gönder</button>
<script>
async function sendMessage() {
  const input = document.getElementById("userInput");
  const chatBox = document.getElementById("chatBox");
  const msg = input.value.trim();
  if (!msg) return;

  chatBox.innerHTML += '<div style="text-align:right;color:#4cf;">Sen: ' + msg + '</div>';
  input.value = "";

  const res = await fetch("/erdem-chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg })
  });

  const data = await res.json();
  chatBox.innerHTML += '<div style="text-align:left;color:#fc3;">Erdem: ' + data.response + '</div>';
  chatBox.scrollTop = chatBox.scrollHeight;
}
</script>
</body>
</html>
'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
