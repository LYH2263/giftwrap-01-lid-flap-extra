<script setup>
import { computed } from 'vue'

const props = defineProps({
  l: { type: Number, default: 0 },
  w: { type: Number, default: 0 },
  h: { type: Number, default: 0 },
  paperM2: { type: Number, default: null },
  flapM: { type: Number, default: 0 },
  effectiveSurface: { type: Number, default: null },
})

// 顶面（开口面）在示意中的画布范围：x 95..185（90px 对应 L），y 18..60（42px 对应 W）
const TOP = { x: 95, y: 18, pw: 90, ph: 42 }

const d = computed(() => Math.max(0, Number(props.flapM) || 0))

// 折入贴边按米→像素换算，封顶到半面避免盖满整面
const fx = computed(() => (props.l > 0 ? Math.min((d.value * TOP.pw) / props.l, TOP.pw / 2) : 0))
const fy = computed(() => (props.w > 0 ? Math.min((d.value * TOP.ph) / props.w, TOP.ph / 2) : 0))
const hasFlap = computed(() => d.value > 0)
</script>

<template>
  <div class="unfold">
    <p class="unfold-title">盒体展开示意{{ hasFlap ? '（含盖口折入贴边）' : '' }}</p>
    <svg class="unfold-svg" viewBox="0 0 280 180" aria-hidden="true">
      <rect class="panel" x="95" y="18" width="90" height="42" rx="2" />
      <!-- 盖口折入：开口面四边向内壁折入的贴合面 -->
      <template v-if="hasFlap">
        <rect class="flap" :x="TOP.x" :y="TOP.y" :width="fx" :height="TOP.ph" />
        <rect class="flap" :x="TOP.x + TOP.pw - fx" :y="TOP.y" :width="fx" :height="TOP.ph" />
        <rect class="flap" :x="TOP.x + fx" :y="TOP.y" :width="TOP.pw - 2 * fx" :height="fy" />
        <rect class="flap" :x="TOP.x + fx" :y="TOP.y + TOP.ph - fy" :width="TOP.pw - 2 * fx" :height="fy" />
      </template>
      <rect class="panel top" x="95" y="68" width="90" height="52" rx="2" />
      <rect class="panel" x="20" y="68" width="68" height="52" rx="2" />
      <rect class="panel" x="192" y="68" width="68" height="52" rx="2" />
      <rect class="panel" x="95" y="128" width="90" height="38" rx="2" />
      <text x="140" y="44" text-anchor="middle">
        顶 {{ Number(l).toFixed(2) }}×{{ Number(w).toFixed(2) }}<template v-if="hasFlap"> · 折入{{ Number(flapM).toFixed(3) }}</template>
      </text>
      <text x="140" y="98" text-anchor="middle">正面</text>
      <text x="54" y="98" text-anchor="middle">侧</text>
      <text x="226" y="98" text-anchor="middle">侧</text>
      <text x="140" y="152" text-anchor="middle">h≈{{ Number(h).toFixed(2) }}</text>
    </svg>
    <p v-if="effectiveSurface != null" class="stat-line">
      有效表面积（六面{{ hasFlap ? '＋折入贴合面' : '' }}）<strong>{{ Number(effectiveSurface).toFixed(4) }}</strong> m²
    </p>
    <p v-if="paperM2 != null" class="stat-line">
      估算用纸 <strong>{{ Number(paperM2).toFixed(4) }}</strong> m²（含折边系数）
    </p>
    <p v-else-if="effectiveSurface == null" class="stat-line">
      外形 {{ Number(l).toFixed(2) }} × {{ Number(w).toFixed(2) }} × {{ Number(h).toFixed(2) }} m
    </p>
  </div>
</template>
