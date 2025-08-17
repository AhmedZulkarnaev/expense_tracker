const API_BASE = '/api/';

function showMessage(text, type = 'success') {
  const box = document.getElementById('message');
  box.textContent = text;
  box.className = `message ${type}`;
  box.classList.remove('hidden');
  setTimeout(() => box.classList.add('hidden'), 3000);
}

async function login(e) {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  const response = await fetch(API_BASE + 'auth/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access', data.access);
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
    document.getElementById('logout').classList.remove('hidden');
    await loadCategories();
    await loadExpenses();
    showMessage('Logged in', 'success');
  } else {
    showMessage('Login failed', 'error');
  }
}

function logout() {
  localStorage.removeItem('access');
  document.getElementById('app').classList.add('hidden');
  document.getElementById('login-section').classList.remove('hidden');
  document.getElementById('logout').classList.add('hidden');
  showMessage('Logged out', 'success');
}

async function loadCategories() {
  const response = await fetch(API_BASE + 'categories/', {
    headers: { Authorization: `Bearer ${localStorage.getItem('access')}` },
  });
  if (response.ok) {
    const data = await response.json();
    const select = document.getElementById('category');
    select.innerHTML = '';
    data.forEach((cat) => {
      const option = document.createElement('option');
      option.value = cat.id;
      option.textContent = cat.name;
      select.appendChild(option);
    });
  }
}

async function loadExpenses() {
  const response = await fetch(API_BASE + 'expenses/', {
    headers: { Authorization: `Bearer ${localStorage.getItem('access')}` },
  });
  if (response.ok) {
    const data = await response.json();
    const tbody = document.querySelector('#expenses-table tbody');
    tbody.innerHTML = '';
    data.forEach((exp) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${exp.description || ''}</td>
        <td>${exp.amount}</td>
        <td>${exp.category ? exp.category.name : ''}</td>
        <td>${exp.date}</td>
      `;
      tbody.appendChild(tr);
    });
  }
}

async function addExpense(e) {
  e.preventDefault();
  const payload = {
    description: document.getElementById('description').value,
    amount: document.getElementById('amount').value,
    category_id: document.getElementById('category').value,
    date: document.getElementById('date').value,
  };

  const response = await fetch(API_BASE + 'expenses/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access')}`,
    },
    body: JSON.stringify(payload),
  });
  if (response.ok) {
    document.getElementById('expense-form').reset();
    await loadExpenses();
    showMessage('Expense added', 'success');
  } else {
    showMessage('Failed to add expense', 'error');
  }
}

document.getElementById('login-form').addEventListener('submit', login);
document.getElementById('expense-form').addEventListener('submit', addExpense);
document.getElementById('logout').addEventListener('click', logout);

if (localStorage.getItem('access')) {
  document.getElementById('login-section').classList.add('hidden');
  document.getElementById('app').classList.remove('hidden');
  document.getElementById('logout').classList.remove('hidden');
  loadCategories();
  loadExpenses();
}
