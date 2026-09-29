<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import BoxUnfold from '../components/BoxUnfold.vue'

const props = defineProps({ id: String })
const run = ref(null)
const err = ref('')

onMounted(async () => {
  try {
    run.value = await getJSON(`/api/runs/${props.id}`)
  } catch (e) {
    err.value = String(e.message || e)
  }
})
</script>

<template>
  <div class="page">
    <p v-if="err" class="bad">{{ err }}</p>
    <template v-else-if="run">
      <h1>用纸档 №{{ run.id }}</h1>
      <p class="lede">
        {{ run.box_name }} · 落库快照（{{ run.created_at }}），只以本页数值为准。
      </p>
      <div class="result-board">
        <div class="figure">{{ run.result.paper_m2 }}<span>m²</span></div>
        <p class="stat-line">
          盖口折入 <strong>{{ run.result.flap_m ?? 0 }}</strong> m；
          有效表面积 {{ run.result.effective_surface }} m²
          （六面 {{ run.result.box_surface }}<template v-if="(run.result.flap_m ?? 0) > 0">
          ＋折入贴合面 {{ run.result.flap_surface }}</template>）× 折边系数 {{ run.overlap }}
        </p>
        <p class="stat-line">
          丝带约 {{ run.result.ribbon?.ribbon_m ?? '—' }} m（按未折入长宽高
          {{ run.box_length }}×{{ run.box_width }}×{{ run.box_height }} m）
        </p>
        <BoxUnfold
          :l="run.box_length"
          :w="run.box_width"
          :h="run.box_height"
          :flap-m="run.result.flap_m ?? 0"
          :effective-surface="run.result.effective_surface"
          :paper-m2="run.result.paper_m2"
        />
      </div>
      <div class="row" style="margin-top:1.25rem">
        <router-link class="btn" to="/history">返回用纸档</router-link>
        <router-link class="btn ghost" to="/bench">去算纸台复核</router-link>
      </div>
    </template>
  </div>
</template>
