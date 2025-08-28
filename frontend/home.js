const API_BASE = '/api/';
let categoryChart;

function showMessage(text, type = 'success') {
  const box = document.getElementById('message');
  box.textContent = text;
  box.className = `message ${type}`;
  box.classList.remove('hidden');
  setTimeout(() => box.classList.add('hidden'), 3000);
}

async function login(e) {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  const response = await fetch(API_BASE + 'auth/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access', data.access);
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
    document.getElementById('logout').classList.remove('hidden');
    document.getElementById('admin-link').classList.remove('hidden');
    await loadExpenses();
    await showSummary();
    await showByCategory();
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
  document.getElementById('admin-link').classList.add('hidden');
  if (categoryChart) categoryChart.destroy();
  showMessage('Logged out', 'success');
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

function getReportParams() {
  const params = new URLSearchParams();
  const from = document.getElementById('report-from').value;
  const to = document.getElementById('report-to').value;
  if (from) params.append('date_from', from);
  if (to) params.append('date_to', to);
  const query = params.toString();
  return query ? `?${query}` : '';
}

async function showSummary() {
  const res = await fetch(API_BASE + 'reports/summary/' + getReportParams(), {
    headers: { Authorization: `Bearer ${localStorage.getItem('access')}` },
  });
  if (res.ok) {
    const data = await res.json();
    document.getElementById('summary-output').textContent =
      `Income: ${data.income_total}, Expense: ${data.expense_total}, Balance: ${data.balance}`;
  } else {
    showMessage('Failed to load summary', 'error');
  }
}

async function showByCategory() {
  const res = await fetch(API_BASE + 'reports/by-category/' + getReportParams(), {
    headers: { Authorization: `Bearer ${localStorage.getItem('access')}` },
  });
  if (res.ok) {
    const data = await res.json();
    const table = document.getElementById('by-category-table');
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    data.forEach((row) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${row.category}</td><td>${row.income}</td><td>${row.expense}</td>`;
      tbody.appendChild(tr);
    });
    table.classList.remove('hidden');
    renderCategoryChart(data);
  } else {
    showMessage('Failed to load report', 'error');
  }
}

function renderCategoryChart(data) {
  const ctx = document.getElementById('category-chart').getContext('2d');
  const labels = data.map((row) => row.category);
  const values = data.map((row) => row.expense);
  const colors = labels.map(
    (_, i) => `hsl(${(i * 60) % 360},70%,60%)`
  );
  if (categoryChart) categoryChart.destroy();
  categoryChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels,
      datasets: [
        {
          data: values,
          backgroundColor: colors,
        },
      ],
    },
  });
}

function exportCSV() {
  const url = API_BASE + 'exports/expenses.csv' + getReportParams();
  window.open(url, '_blank');
}

document.getElementById('login-form').addEventListener('submit', login);
document.getElementById('logout').addEventListener('click', logout);
document.getElementById('summary-btn').addEventListener('click', showSummary);
document.getElementById('by-category-btn').addEventListener('click', showByCategory);
document.getElementById('export-btn').addEventListener('click', exportCSV);

if (localStorage.getItem('access')) {
  document.getElementById('login-section').classList.add('hidden');
  document.getElementById('app').classList.remove('hidden');
  document.getElementById('logout').classList.remove('hidden');
  document.getElementById('admin-link').classList.remove('hidden');
  loadExpenses();
  showSummary();
  showByCategory();
}
