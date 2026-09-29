<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON, postJSON } from '../api'
import BoxUnfold from '../components/BoxUnfold.vue'

const boxes = ref([])
const bid = ref(1)
const flap = ref(0)
const out = ref(null)
const err = ref('')
const busy = ref(false)

onMounted(async () => {
  try {
    boxes.value = (await getJSON('/api/boxes')).items.filter((b) => b.data_quality === 'clean')
    if (boxes.value.length) {
      bid.value = boxes.value[0].id
      flap.value = Number(boxes.value[0].flap_m || 0)
    }
  } catch (e) {
    err.value = String(e.message || e)
  }
})

watch(bid, (v) => {
  const b = boxes.value.find((x) => x.id === v)
  if (b) flap.value = Number(b.flap_m || 0)
})

function flapParam() {
  return Number.isFinite(Number(flap.value)) ? Number(flap.value) : 0
}

async function go(save) {
  err.value = ''
  busy.value = true
  try {
    const d = flapParam()
    out.value = save
      ? await postJSON('/api/estimate', { box_id: bid.value, flap_m: d, save: true })
      : await getJSON(`/api/estimate?box_id=${bid.value}&flap_m=${encodeURIComponent(d)}`)
  } catch (e) {
    out.value = null
    err.value = String(e.message || e)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1>算纸</h1>
    <p class="lede">先试算看面积与展开，确认后再写入用纸档。盖口折入为可选项，单位米。</p>
    <div class="row">
      <select v-model.number="bid">
        <option v-for="b in boxes" :key="b.id" :value="b.id">{{ b.name }}</option>
      </select>
      <label class="inline">
        盖口折入
        <input v-model.number="flap" type="number" min="0" step="0.01" /> m
      </label>
      <button :disabled="busy" @click="go(false)">试算</button>
      <button class="ribbon" :disabled="busy" @click="go(true)">写入用纸档</button>
    </div>
    <p v-if="err" class="bad">{{ err }}</p>
    <div v-if="out" class="result-board">
      <div class="figure">{{ out.paper_m2 }}<span>m²</span></div>
      <p class="stat-line">
        有效表面积 {{ out.effective_surface }} m²（六面 {{ out.box_surface }}
        <template v-if="out.flap_m > 0">＋折入贴合面 {{ out.flap_surface }}（折入 {{ out.flap_m }} m）</template>）
        × 折边系数 {{ out.overlap }}
      </p>
      <p class="stat-line" v-if="out.ribbon">
        十字丝带约 {{ out.ribbon.ribbon_m ?? out.ribbon }} m（按未折入长宽高）
      </p>
      <div class="row" v-if="out.run_id" style="margin-top:0.85rem">
        <router-link class="btn" :to="`/runs/${out.run_id}`">查看用纸档 №{{ out.run_id }}</router-link>
      </div>
      <BoxUnfold
        :l="out.box.length"
        :w="out.box.width"
        :h="out.box.height"
        :flap-m="out.flap_m"
        :effective-surface="out.effective_surface"
        :paper-m2="out.paper_m2"
      />
    </div>
  </div>
</template>
