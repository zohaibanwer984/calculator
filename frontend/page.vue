<template>
  <div>
    <h1>History</h1>

    <input v-model="form.value_1" placeholder="value_1" />
    <input v-model="form.value_2" placeholder="value_2" />
    <input v-model="form.value_3" placeholder="value_3" />
    <button @click="save" :disabled="loading">{{ loading ? 'Saving...' : 'Save' }}</button>

    <p v-if="msg">{{ msg }}</p>

    <table v-if="rows.length">
      <thead>
        <tr>
          <th>value_1</th>
          <th>value_2</th>
          <th>value_3</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in rows" :key="r.id">
          <td>{{ r.value_1 }}</td>
          <td>{{ r.value_2 }}</td>
          <td>{{ r.value_3 }}</td>
          <td><button @click="del(r.id)">Delete</button></td>
        </tr>
      </tbody>
    </table>

    <p v-else>No records yet.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API = 'http://localhost:8000/api/history/'

const rows = ref([])
const form = ref({ value_1: '', value_2: '', value_3: '' })
const loading = ref(false)
const msg = ref('')

async function load() {
  const r = await fetch(API)
  rows.value = await r.json()
}

async function save() {
  loading.value = true
  const r = await fetch(API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value),
  })
  const created = await r.json()
  rows.value.unshift(created)
  form.value = { value_1: '', value_2: '', value_3: '' }
  msg.value = 'Saved'
  loading.value = false
}

async function del(id) {
  await fetch(API + id + '/', { method: 'DELETE' })
  rows.value = rows.value.filter((r) => r.id !== id)
}

onMounted(load)
</script>s