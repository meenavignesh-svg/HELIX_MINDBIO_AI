const messagesEl = document.querySelector('#messages');
const form = document.querySelector('#chatForm');
const input = document.querySelector('#userInput');
const button = document.querySelector('#sendButton');
const statusEl = document.querySelector('#status');

const history = [];

const demoReplies = [
  { match: ['itinerary', 'plan'], text: 'Demo mode: split the day into one main attraction, one relaxed meal, one flexible stop, and a simple way back.' },
  { match: ['pack', 'packing'], text: 'Demo mode: pack by layers: documents, clothes, chargers, medicines, hygiene, and one comfort item.' },
  { match: ['budget', 'cost'], text: 'Demo mode: separate transport, stay, food, tickets, local travel, and buffer money. The buffer saves the trip.' },
  { match: ['compare', 'destination'], text: 'Demo mode: compare weather, travel time, cost, safety, activities, and how tired you want to be.' }
];

function addMessage(text, sender, extraClass = '') {
  const bubble = document.createElement('div');
  bubble.className = `message ${sender} ${extraClass}`.trim();
  bubble.textContent = text;
  messagesEl.appendChild(bubble);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function setBusy(isBusy) {
  button.disabled = isBusy;
  input.disabled = isBusy;
  statusEl.textContent = isBusy ? 'planning' : 'demo ready';
  statusEl.classList.toggle('busy', isBusy);
}

function getDemoReply(text) {
  const clean = text.toLowerCase();
  const hit = demoReplies.find((reply) => reply.match.some((word) => clean.includes(word)));
  if (hit) return hit.text;
  return `Demo mode: I would turn "${text}" into a travel plan by asking dates, budget, pace, and must-see priorities.`;
}

async function sendMessage(text) {
  history.push({ role: 'user', content: text });
  setBusy(true);

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: history })
    });

    if (!response.ok) throw new Error('Demo fallback');
    const data = await response.json();
    const reply = data.reply || getDemoReply(text);
    history.push({ role: 'assistant', content: reply });
    addMessage(reply, 'bot');
  } catch {
    window.setTimeout(() => {
      const reply = getDemoReply(text);
      history.push({ role: 'assistant', content: reply });
      addMessage(reply, 'bot');
    }, 250);
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

statusEl.textContent = 'demo ready';
addMessage('Travel Planner is ready in browser demo mode. Ask for an itinerary, packing list, budget plan, or destination comparison.', 'bot');
