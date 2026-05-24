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
  { match: ['beat', 'idea'], text: 'Demo mode: try 92 BPM with dusty drums, a two-note bass pulse, and a chopped vocal texture for movement.' },
  { match: ['drum', 'kick', 'snare'], text: 'Demo mode: place the kick on 1 and the and of 3, snare on 2 and 4, then add quiet ghost hats for swing.' },
  { match: ['bass'], text: 'Demo mode: keep the bass simple: root note, octave jump, short rest, then a slide into the next chord.' },
  { match: ['mix', 'master'], text: 'Demo mode: lower everything, make the kick and vocal lead clear, then use gentle saturation instead of too much volume.' }
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
  statusEl.textContent = isBusy ? 'producing' : apiKey ? 'real AI ready' : 'demo ready';
  statusEl.classList.toggle('busy', isBusy);
}

function getDemoReply(text) {
  const clean = text.toLowerCase();
  const hit = demoReplies.find((reply) => reply.match.some((word) => clean.includes(word)));
  if (hit) return hit.text;
  return `Demo mode: I would shape "${text}" into a beat by choosing tempo, drum pocket, bass movement, and one memorable texture.`;
}

keyForm.addEventListener('submit', (event) => {
  event.preventDefault();
  apiKey = apiKeyInput.value.trim();
  if (!apiKey) return;
  sessionStorage.setItem('openai_api_key', apiKey);
  apiKeyInput.value = '';
  refreshKeyState();
  addMessage('API key saved for this browser session. Real AI mode is ready after Vercel deployment; demo mode still works anytime.', 'bot');
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

addMessage('Beat Producer is ready in browser demo mode. Ask for beat ideas, drums, basslines, song sections, or mix notes.', 'bot');
refreshKeyState();
