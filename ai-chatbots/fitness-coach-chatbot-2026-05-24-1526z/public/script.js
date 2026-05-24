const messagesEl = document.querySelector('#messages');
const form = document.querySelector('#chatForm');
const input = document.querySelector('#userInput');
const button = document.querySelector('#sendButton');
const statusEl = document.querySelector('#status');

const history = [];

const demoReplies = [
  { match: ['workout', 'exercise'], text: 'Demo mode: try 3 rounds of squats, wall pushups, and brisk walking. Keep it easy enough to repeat tomorrow.' },
  { match: ['habit', 'routine'], text: 'Demo mode: attach one tiny habit to something you already do, like stretching for two minutes after brushing your teeth.' },
  { match: ['warmup'], text: 'Demo mode: do five minutes of gentle movement, then practice the first exercise slowly before adding effort.' },
  { match: ['recovery', 'rest', 'pain'], text: 'Demo mode: rest, hydrate, and reduce intensity. For pain or medical concerns, talk to a qualified professional.' }
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
  return `Demo mode: I would answer "${text}" with a simple beginner-safe plan, a warmup, and one recovery note.`;
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
addMessage('Fitness Coach is ready in browser demo mode. Ask for a beginner workout, habit plan, warmup, or recovery tip.', 'bot');
