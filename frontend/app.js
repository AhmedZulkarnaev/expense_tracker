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
    const tbody = document.querySelector('#categories-table tbody');
    tbody.innerHTML = '';
    data.forEach((cat) => {
      const option = document.createElement('option');
      option.value = cat.id;
      option.textContent = cat.name;
      select.appendChild(option);

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${cat.id}</td>
        <td>${cat.name}</td>
        <td>
          <button class="edit-category" data-id="${cat.id}" data-name="${cat.name}">Edit</button>
          <button class="delete-category" data-id="${cat.id}">Delete</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  }
}

async function addCategory(e) {
  e.preventDefault();
  const name = document.getElementById('category-name').value;
  const response = await fetch(API_BASE + 'categories/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access')}`,
    },
    body: JSON.stringify({ name }),
  });
  if (response.ok) {
    document.getElementById('category-form').reset();
    await loadCategories();
    showMessage('Category added');
  } else {
    showMessage('Failed to add category', 'error');
  }
}

async function editCategory(id, currentName) {
  const name = prompt('Category name', currentName);
  if (name === null) return;
  const response = await fetch(API_BASE + `categories/${id}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access')}`,
    },
    body: JSON.stringify({ name }),
  });
  if (response.ok) {
    await loadCategories();
    showMessage('Category updated');
  } else {
    showMessage('Failed to update category', 'error');
  }
}

async function deleteCategory(id) {
  if (!confirm('Delete category?')) return;
  const response = await fetch(API_BASE + `categories/${id}/`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${localStorage.getItem('access')}` },
  });
  if (response.ok) {
    await loadCategories();
    showMessage('Category deleted');
  } else {
    showMessage('Failed to delete category', 'error');
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
        <td>
          <button class="edit-expense" data-id="${exp.id}">Edit</button>
          <button class="delete-expense" data-id="${exp.id}">Delete</button>
        </td>
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

async function editExpense(id) {
  const detail = await fetch(API_BASE + `expenses/${id}/`, {
    headers: { Authorization: `Bearer ${localStorage.getItem('access')}` },
  });
  if (!detail.ok) {
    showMessage('Failed to load expense', 'error');
    return;
  }
  const exp = await detail.json();
  const description = prompt('Description', exp.description || '');
  if (description === null) return;
  const amount = prompt('Amount', exp.amount);
  if (amount === null) return;
  const category_id = prompt('Category ID', exp.category ? exp.category.id : '');
  if (category_id === null) return;
  const date = prompt('Date', exp.date);
  if (date === null) return;

  const response = await fetch(API_BASE + `expenses/${id}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access')}`,
    },
    body: JSON.stringify({ description, amount, category_id, date }),
  });
  if (response.ok) {
    await loadExpenses();
    showMessage('Expense updated');
  } else {
    showMessage('Failed to update expense', 'error');
  }
}

async function deleteExpense(id) {
  if (!confirm('Delete expense?')) return;
  const response = await fetch(API_BASE + `expenses/${id}/`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${localStorage.getItem('access')}` },
  });
  if (response.ok) {
    await loadExpenses();
    showMessage('Expense deleted');
  } else {
    showMessage('Failed to delete expense', 'error');
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
  } else {
    showMessage('Failed to load report', 'error');
  }
}

function exportCSV() {
  const url = API_BASE + 'exports/expenses.csv' + getReportParams();
  window.open(url, '_blank');
}

document.getElementById('login-form').addEventListener('submit', login);
document.getElementById('expense-form').addEventListener('submit', addExpense);
document.getElementById('logout').addEventListener('click', logout);
document.getElementById('category-form').addEventListener('submit', addCategory);
document.getElementById('categories-table').addEventListener('click', (e) => {
  if (e.target.classList.contains('edit-category')) {
    editCategory(e.target.dataset.id, e.target.dataset.name);
  } else if (e.target.classList.contains('delete-category')) {
    deleteCategory(e.target.dataset.id);
  }
});

document.getElementById('expenses-table').addEventListener('click', (e) => {
  if (e.target.classList.contains('edit-expense')) {
    editExpense(e.target.dataset.id);
  } else if (e.target.classList.contains('delete-expense')) {
    deleteExpense(e.target.dataset.id);
  }
});

document.getElementById('summary-btn').addEventListener('click', showSummary);
document.getElementById('by-category-btn').addEventListener('click', showByCategory);
document.getElementById('export-btn').addEventListener('click', exportCSV);

if (localStorage.getItem('access')) {
  document.getElementById('login-section').classList.add('hidden');
  document.getElementById('app').classList.remove('hidden');
  document.getElementById('logout').classList.remove('hidden');
  loadCategories();
  loadExpenses();
}
