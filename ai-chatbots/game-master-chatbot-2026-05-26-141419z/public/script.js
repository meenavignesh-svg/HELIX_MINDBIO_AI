const messagesEl = document.querySelector('#messages');
    const keyForm = document.querySelector('#keyForm');
    const apiKeyInput = document.querySelector('#apiKeyInput');
    const form = document.querySelector('#chatForm');
    const input = document.querySelector('#userInput');
    const button = document.querySelector('#sendButton');
    const statusEl = document.querySelector('#status');
    const history = [];
    const demoReplies = [
  {
    "match": [
      "quest"
    ],
    "text": "Demo mode: a missing map points to a locked observatory where the stars changed overnight."
  },
  {
    "match": [
      "puzzle"
    ],
    "text": "Demo mode: make the answer visible in the room, but require players to connect two clues."
  },
  {
    "match": [
      "encounter"
    ],
    "text": "Demo mode: add a goal besides fighting, a terrain twist, and a reason to negotiate."
  }
];
    let apiKey = sessionStorage.getItem('openai_api_key') || '';

    function addMessage(text, sender) {
      const bubble = document.createElement('div');
      bubble.className = `message ${sender}`;
      bubble.textContent = text;
      messagesEl.appendChild(bubble);
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }
    function setBusy(isBusy) { button.disabled = isBusy; input.disabled = isBusy; statusEl.textContent = isBusy ? "rolling" : apiKey ? 'real AI ready' : 'demo ready'; }
    function demoReply(text) {
      const clean = text.toLowerCase();
      const hit = demoReplies.find((reply) => reply.match.some((word) => clean.includes(word)));
      return hit ? hit.text : `Demo mode: I would turn "${text}" into a practical next step in the Game Master style.`;
    }
    keyForm.addEventListener('submit', (event) => {
      event.preventDefault();
      apiKey = apiKeyInput.value.trim();
      if (!apiKey) return;
      sessionStorage.setItem('openai_api_key', apiKey);
      apiKeyInput.value = '';
      statusEl.textContent = 'real AI ready';
      addMessage('API key saved for this browser session. Real AI mode is ready after Vercel deployment.', 'bot');
    });
    async function sendMessage(text) {
      history.push({ role: 'user', content: text });
      setBusy(true);
      if (!apiKey) {
        setTimeout(() => { const reply = demoReply(text); history.push({ role: 'assistant', content: reply }); addMessage(reply, 'bot'); setBusy(false); }, 250);
        return;
      }
      try {
        const response = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` }, body: JSON.stringify({ messages: history }) });
        if (!response.ok) throw new Error('fallback');
        const data = await response.json();
        const reply = data.reply || demoReply(text);
        history.push({ role: 'assistant', content: reply });
        addMessage(reply, 'bot');
      } catch {
        const reply = demoReply(text);
        history.push({ role: 'assistant', content: reply });
        addMessage(reply, 'bot');
      } finally { setBusy(false); }
    }
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const text = input.value.trim();
      if (!text) return;
      addMessage(text, 'user');
      input.value = '';
      sendMessage(text);
    });
    addMessage("Game Master is ready in browser demo mode. Ask for quests, characters, puzzles, or encounter ideas.", 'bot');
