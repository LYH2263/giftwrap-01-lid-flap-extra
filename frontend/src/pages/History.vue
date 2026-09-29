<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'

const items = ref([])
const err = ref('')

onMounted(async () => {
  try {
    items.value = (await getJSON('/api/runs')).items
  } catch (e) {
    err.value = String(e.message || e)
  }
})
</script>

<template>
  <div class="page">
    <h1>用纸档</h1>
    <p class="lede">算纸页「写入用纸档」后的落库快照，按次保留盒名、折入与面积；快照不随后续默认值回刷。</p>
    <p v-if="err" class="bad">{{ err }}</p>
    <p v-else-if="!items.length" class="empty">还没有写入过。先去算纸试一单。</p>
    <ul v-else class="item-list">
      <li v-for="r in items" :key="r.id">
        <router-link :to="`/runs/${r.id}`">№{{ r.id }} {{ r.box_name }}</router-link>
        <span class="meta">
          折入 {{ r.result?.flap_m ?? 0 }} m ·
          {{ r.result?.paper_m2 ?? '—' }} m²
        </span>
      </li>
    </ul>
  </div>
</template>
