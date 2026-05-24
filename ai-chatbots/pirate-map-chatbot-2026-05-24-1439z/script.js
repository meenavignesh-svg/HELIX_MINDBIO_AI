const messages = document.querySelector('#messages');
const form = document.querySelector('#chatForm');
const input = document.querySelector('#userInput');

const replies = [
  {
    match: ['hello', 'hi', 'hey'],
    text: 'Ahoy. The map is open and the compass is steady.'
  },
  {
    match: ['map', 'read', 'clue'],
    text: 'The map says to follow the oldest clue first, then check what changed after sunset.'
  },
  {
    match: ['treasure', 'gold', 'chest'],
    text: 'Treasure rarely sits where the big X is obvious. Look for the note hidden beside the route.'
  },
  {
    match: ['storm', 'warning', 'danger'],
    text: 'Storm warning: slow down, save your work, and do not trust any link with a suspicious sail.'
  },
  {
    match: ['help', 'navigate', 'route'],
    text: 'Set a goal, mark the blockers, and sail one small step at a time. That is how maps become journeys.'
  }
];

function addMessage(text, sender) {
  const bubble = document.createElement('div');
  bubble.className = `message ${sender}`;
  bubble.textContent = text;
  messages.appendChild(bubble);
  messages.scrollTop = messages.scrollHeight;
}

function getBotReply(text) {
  const clean = text.toLowerCase();
  const hit = replies.find((reply) => reply.match.some((word) => clean.includes(word)));

  if (hit) return hit.text;

  return `I marked "${text}" on the chart. The next move is to compare it with the nearest clue.`;
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, 'user');
  input.value = '';

  window.setTimeout(() => {
    addMessage(getBotReply(text), 'bot');
  }, 350);
});

addMessage('The route is ready. What clue should we follow first?', 'bot');
