<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, patchJSON } from '../api'
import BoxUnfold from '../components/BoxUnfold.vue'

const props = defineProps({ id: String })
const box = ref(null)
const flap = ref(0)
const calc = ref(null)
const err = ref('')
const note = ref('')
const busy = ref(false)

async function loadBox() {
  box.value = await getJSON(`/api/boxes/${props.id}`)
  flap.value = Number(box.value.flap_m || 0)
}

async function trial() {
  err.value = ''
  note.value = ''
  busy.value = true
  try {
    calc.value = await getJSON(`/api/estimate?box_id=${props.id}&flap_m=${encodeURIComponent(Number(flap) || 0)}`)
  } catch (e) {
    err.value = String(e.message || e)
  } finally {
    busy.value = false
  }
}

async function saveDefault() {
  err.value = ''
  note.value = ''
  busy.value = true
  try {
    box.value = await patchJSON(`/api/boxes/${props.id}`, { flap_m: Number(flap) || 0 })
    note.value = '已登记为该盒默认折入深度。'
  } catch (e) {
    err.value = String(e.message || e)
  } finally {
    busy.value = false
  }
}

onMounted(async () => {
  try {
    await loadBox()
    if (box.value.data_quality !== 'dirty') await trial()
  } catch (e) {
    err.value = String(e.message || e)
  }
})
</script>

<template>
  <div class="page">
    <p v-if="err" class="bad">{{ err }}</p>
    <template v-else-if="box">
      <h1>{{ box.name }}</h1>
      <p class="lede">
        {{ box.length }} × {{ box.width }} × {{ box.height }} m
        <span class="pill" :class="{ warn: box.data_quality === 'dirty' }">
          {{ box.data_quality === 'dirty' ? '脏数据' : '可用' }}
        </span>
      </p>
      <p v-if="box.data_quality === 'dirty'" class="bad">{{ box.note }}</p>
      <template v-if="box.data_quality !== 'dirty'">
        <div class="row">
          <label class="inline">
            盖口折入
            <input v-model.number="flap" type="number" min="0" step="0.01" /> m
          </label>
          <button :disabled="busy" @click="trial">回算</button>
          <button class="ghost" :disabled="busy" @click="saveDefault">登记为默认折入</button>
        </div>
        <p v-if="note" class="stat-line">{{ note }}</p>
        <div v-if="calc">
          <p class="stat-line">
            有效表面积 {{ calc.effective_surface }} m²（六面 {{ calc.box_surface }}
            <template v-if="calc.flap_m > 0">＋折入贴合面 {{ calc.flap_surface }}</template>）
            × {{ calc.overlap }} ＝ 用纸 <strong>{{ calc.paper_m2 }}</strong> m²；
            丝带约 {{ calc.ribbon.ribbon_m }} m（按未折入长宽高）
          </p>
          <BoxUnfold
            :l="box.length"
            :w="box.width"
            :h="box.height"
            :flap-m="calc.flap_m"
            :effective-surface="calc.effective_surface"
            :paper-m2="calc.paper_m2"
          />
        </div>
      </template>
      <BoxUnfold v-else :l="box.length" :w="box.width" :h="box.height" />
      <div class="row" style="margin-top: 1.25rem">
        <router-link class="btn" to="/bench">用此盒去算纸</router-link>
        <router-link class="btn ghost" to="/boxes">返回清单</router-link>
      </div>
    </template>
  </div>
</template>
