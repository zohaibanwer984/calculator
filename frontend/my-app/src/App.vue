<template>
  <div>
    <h1>Calculator History</h1>

    <input v-model.number="form.value_1" placeholder="value_1" />

    <select v-model="form.operator">
      <option value="+">+</option>
      <option value="-">-</option>
      <option value="*">*</option>
      <option value="/">/</option>
    </select>

    <input v-model.number="form.value_2" placeholder="value_2" />

    <input :value="result" placeholder="result" readonly />

    <button @click="save" :disabled="loading">
      {{ loading ? 'Saving...' : 'Save' }}
    </button>

    <p v-if="msg">{{ msg }}</p>

    <table v-if="rows.length" border="1">
      <thead>
        <tr>
          <th>Expression</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in rows" :key="r.id">
          <td>
            {{ r.value_1 }} {{ r.operator }} {{ r.value_2 }} = {{ r.value_3 }}
          </td>
          <td>
            <button @click="del(r.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>No records yet.</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const API = 'http://127.0.0.1:8000/api/history/'

const rows = ref([])
const loading = ref(false)
const msg = ref('')

const form = ref({
  value_1: null,
  value_2: null,
  operator: '+',
})

const result = computed(() => {
  const v1 = form.value.value_1
  const v2 = form.value.value_2

  if (v1 === null || v2 === null) return ''

  switch (form.value.operator) {
    case '+': return v1 + v2
    case '-': return v1 - v2
    case '*': return v1 * v2
    case '/': return v2 !== 0 ? v1 / v2 : 0
    default: return ''
  }
})

async function load() {
  try {
    const r = await fetch(API)
    rows.value = await r.json()
  } catch (e) {
    msg.value = 'Failed to load data'
  }
}

async function save() {
  if (form.value.value_1 === null || form.value.value_2 === null) {
    msg.value = 'Enter both values'
    return
  }

  loading.value = true
  msg.value = ''

  const payload = {
    value_1: form.value.value_1,
    value_2: form.value.value_2,
    operator: form.value.operator,
    value_3: result.value,
  }

  try {
    const r = await fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    if (!r.ok) {
      const err = await r.text()
      msg.value = 'Error: ' + err
      loading.value = false
      return
    }

    const created = await r.json()
    rows.value.unshift(created)

    form.value = { value_1: null, value_2: null, operator: '+' }
    msg.value = 'Saved successfully'
  } catch (e) {
    msg.value = 'Request failed'
  }

  loading.value = false
}

async function del(id) {
  try {
    await fetch(API + id + '/', { method: 'DELETE' })
    rows.value = rows.value.filter(r => r.id !== id)
  } catch {
    msg.value = 'Delete failed'
  }
}

onMounted(load)
</script>
<style scoped>
div {
  max-width: 700px;
  margin: 40px auto;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

input,
select {
  padding: 8px 10px;
  margin: 5px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  transition: 0.2s;
}

input:focus,
select:focus {
  border-color: #42b983;
}

input[readonly] {
  background-color: #f5f5f5;
  font-weight: bold;
}

button {
  padding: 8px 14px;
  margin: 5px;
  border: none;
  border-radius: 6px;
  background-color: #42b983;
  color: white;
  cursor: pointer;
  transition: 0.2s;
}

button:hover {
  background-color: #369870;
}

button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

p {
  margin-top: 10px;
  color: #333;
}

table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

thead {
  background-color: #42b983;
  color: white;
}

th,
td {
  padding: 10px;
  text-align: center;
}

tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

tbody tr:hover {
  background-color: #eefaf5;
}

td button {
  background-color: #ff4d4f;
}

td button:hover {
  background-color: #d9363e;
}
</style>