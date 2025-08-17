const API_BASE = '/api/';

function showMessage(text, type = 'success') {
  const box = document.getElementById('message');
  box.textContent = text;
  box.className = `message ${type}`;
  box.classList.remove('hidden');
  setTimeout(() => box.classList.add('hidden'), 3000);
}

async function register(e) {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  if (password.length < 8) {
    showMessage('Password must be at least 8 characters', 'error');
    return;
  }

  const response = await fetch(API_BASE + 'auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, username, password }),
  });

  if (response.ok) {
    showMessage('Registration successful', 'success');
    setTimeout(() => { window.location.href = 'index.html'; }, 1000);
  } else {
    showMessage('Registration failed', 'error');
  }
}

document.getElementById('register-form').addEventListener('submit', register);
