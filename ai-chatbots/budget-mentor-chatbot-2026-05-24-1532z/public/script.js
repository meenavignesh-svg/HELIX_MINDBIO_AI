const messagesEl = document.querySelector('#messages');
const keyForm = document.querySelector('#keyForm');
const apiKeyInput = document.querySelector('#apiKeyInput');
const form = document.querySelector('#chatForm');
const input = document.querySelector('#userInput');
const button = document.querySelector('#sendButton');
const statusEl = document.querySelector('#status');

const history = [];
let apiKey = sessionStorage.getItem('openai_api_key') || '';

const demoReplies = [
  { match: ['budget', 'spend'], text: 'Demo mode: split spending into needs, wants, savings, and surprise costs. Start by tracking only three categories for one week.' },
  { match: ['save', 'saving'], text: 'Demo mode: choose one goal, one amount, and one automatic habit. Small repeatable savings beats heroic one-time effort.' },
  { match: ['debt', 'loan'], text: 'Demo mode: list balances, rates, and minimum payments. Then compare avalanche versus snowball payoff styles.' },
  { match: ['goal', 'plan'], text: 'Demo mode: make the goal measurable: amount, deadline, monthly target, and what you will reduce to fund it.' }
];

function addMessage(text, sender, extraClass = '') {
  const bubble = document.createElement('div');
  bubble.className = `message ${sender} ${extraClass}`.trim();
  bubble.textContent = text;
  messagesEl.appendChild(bubble);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function refreshKeyState() {
  statusEl.textContent = apiKey ? 'real AI ready' : 'demo ready';
  input.disabled = false;
  button.disabled = false;
}

function setBusy(isBusy) {
  button.disabled = isBusy;
  input.disabled = isBusy;
  statusEl.textContent = isBusy ? 'planning' : apiKey ? 'real AI ready' : 'demo ready';
  statusEl.classList.toggle('busy', isBusy);
}

function getDemoReply(text) {
  const clean = text.toLowerCase();
  const hit = demoReplies.find((reply) => reply.match.some((word) => clean.includes(word)));
  if (hit) return hit.text;
  return `Demo mode: I would turn "${text}" into a simple money plan with a goal, a category, and one next action.`;
}

keyForm.addEventListener('submit', (event) => {
  event.preventDefault();
  apiKey = apiKeyInput.value.trim();
  if (!apiKey) return;
  sessionStorage.setItem('openai_api_key', apiKey);
  apiKeyInput.value = '';
  refreshKeyState();
  addMessage('API key saved for this browser session. Real AI mode is ready; demo mode still works if the deployment is not connected.', 'bot');
  input.focus();
});

async function sendMessage(text) {
  history.push({ role: 'user', content: text });
  setBusy(true);

  if (!apiKey) {
    window.setTimeout(() => {
      const reply = getDemoReply(text);
      history.push({ role: 'assistant', content: reply });
      addMessage(reply, 'bot');
      setBusy(false);
      input.focus();
    }, 250);
    return;
  }

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({ messages: history })
    });

    if (!response.ok) throw new Error('Demo fallback');
    const data = await response.json();
    const reply = data.reply || getDemoReply(text);
    history.push({ role: 'assistant', content: reply });
    addMessage(reply, 'bot');
  } catch {
    const reply = getDemoReply(text);
    history.push({ role: 'assistant', content: reply });
    addMessage(reply, 'bot');
  } finally {
    setBusy(false);
    input.focus();
  }
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, 'user');
  input.value = '';
  sendMessage(text);
});

addMessage('Budget Mentor is ready in browser demo mode. Enter an OpenAI API key for real AI mode, or just chat now for the built-in demo.', 'bot');
refreshKeyState();
