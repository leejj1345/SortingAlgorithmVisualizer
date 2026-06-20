const $ = (selector) => document.querySelector(selector);
const bars = $("#bars");
const algorithm = $("#algorithm");
const size = $("#size");
const speed = $("#speed");

// 현재 배열과 애니메이션 실행 상태를 브라우저에서 관리합니다.
let values = [];
let running = false;
let paused = false;
let runToken = 0;
let chart;

const colors = ["#ff5a24", "#181817", "#3974d8", "#8c55d7", "#20a36a", "#e4a61b"];

function randomize() {
  // 기존 실행 토큰을 무효화하여 이전 애니메이션이 화면을 갱신하지 못하게 합니다.
  runToken++;
  running = false;
  paused = false;
  values = Array.from({ length: Number(size.value) }, () => Math.floor(Math.random() * 94) + 6);
  renderBars(values, [], []);
  setMetrics(0, 0, 0, "READY", "준비");
  toggleControls(false);
}

function renderBars(data, active, sorted) {
  // 매 단계의 배열 값을 막대 높이로, 연산 상태를 CSS 클래스로 표현합니다.
  const activeSet = new Set(active);
  const sortedSet = new Set(sorted);
  // 막대가 너무 좁아질 때 숫자가 겹치지 않도록 30개 이하에서만 값을 표시합니다.
  const showValues = data.length <= 30;
  bars.innerHTML = data.map((value, index) => {
    const classes = ["bar", activeSet.has(index) ? "active" : "", sortedSet.has(index) ? "sorted" : ""].join(" ");
    return `<div class="${classes}" style="height:${value}%">${showValues ? `<span class="bar-value">${value}</span>` : ""}</div>`;
  }).join("");
}

function setMetrics(comparisons, swaps, step, state, message) {
  // Python에서 누적한 통계와 현재 실행 상태를 한 번에 갱신합니다.
  $("#comparisons").textContent = comparisons.toLocaleString();
  $("#swaps").textContent = swaps.toLocaleString();
  $("#steps").textContent = step.toLocaleString();
  $("#runState").textContent = state;
  $("#status").textContent = message;
}

function toggleControls(isRunning) {
  // 실행 중 데이터가 변경되거나 정렬 요청이 중복 전송되는 것을 방지합니다.
  running = isRunning;
  $("#start").disabled = isRunning;
  $("#pause").disabled = !isRunning;
  $("#randomize").disabled = isRunning;
  algorithm.disabled = isRunning;
  size.disabled = isRunning;
}

// 슬라이더 단계에 따라 각 애니메이션 프레임 사이의 대기 시간을 결정합니다.
const delay = () => new Promise(resolve => setTimeout(resolve, [500, 280, 140, 65, 20][Number(speed.value) - 1]));

async function startSort() {
  // 각 실행에 고유 토큰을 부여하여 새 데이터 생성 시 오래된 실행을 안전하게 중단합니다.
  const token = ++runToken;
  toggleControls(true);
  setMetrics(0, 0, 0, "LOADING", "Python 정렬 엔진에 요청 중…");
  try {
    const response = await fetch("/api/sort", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ algorithm: algorithm.value, values })
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "정렬 요청 실패");
    document.querySelectorAll("tbody tr").forEach(row => row.classList.toggle("active", row.dataset.algorithm === algorithm.value));
    // 서버가 기록한 정렬 단계를 현재 속도 설정에 맞춰 순서대로 재생합니다.
    for (let index = 0; index < result.steps.length; index++) {
      if (token !== runToken) return;
      // 일시정지 중에는 상태를 유지하면서 짧은 간격으로 재개 여부만 확인합니다.
      while (paused) await new Promise(resolve => setTimeout(resolve, 80));
      const step = result.steps[index];
      renderBars(step.values, step.active, step.sorted);
      setMetrics(step.comparisons, step.swaps, index, "RUNNING", step.message);
      await delay();
    }
    values = result.steps.at(-1).values;
    setMetrics(result.steps.at(-1).comparisons, result.steps.at(-1).swaps, result.steps.length - 1, "DONE", "정렬 완료");
  } catch (error) {
    setMetrics(0, 0, 0, "ERROR", error.message);
  } finally {
    if (token === runToken) toggleControls(false);
  }
}

async function runBenchmark() {
  // 측정 중 버튼을 비활성화하여 중복 벤치마크 요청을 막습니다.
  const button = $("#benchmark");
  button.disabled = true;
  button.textContent = "측정 중…";
  try {
    const response = await fetch("/api/benchmark", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ algorithms: ["bubble", "selection", "insertion", "merge", "quick", "heap"] })
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "성능 측정 실패");
    // 재측정 시 기존 Chart 인스턴스를 제거해야 캔버스가 중복 사용되지 않습니다.
    if (chart) chart.destroy();
    chart = new Chart($("#performanceChart"), {
      type: "line",
      data: {
        labels: result.sizes.map(n => `${n}개`),
        datasets: result.series.map((item, index) => ({
          label: item.name,
          data: item.times,
          borderColor: colors[index],
          backgroundColor: colors[index],
          borderWidth: 2,
          pointRadius: 3,
          tension: .2
        }))
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: { legend: { position: "bottom", labels: { usePointStyle: true, boxWidth: 8, padding: 18 } } },
        scales: {
          y: { beginAtZero: true, title: { display: true, text: "실행 시간 (ms)" }, grid: { color: "#e5e1d8" } },
          x: { grid: { display: false } }
        }
      }
    });
  } catch (error) {
    alert(error.message);
  } finally {
    button.disabled = false;
    button.textContent = "다시 측정하기";
  }
}

// 컨트롤 이벤트를 화면 상태 변경 함수와 연결합니다.
size.addEventListener("input", () => { $("#sizeValue").textContent = size.value; randomize(); });
speed.addEventListener("input", () => { $("#speedValue").textContent = `${[.5, .75, 1, 1.5, 2][Number(speed.value) - 1]}×`; });
$("#randomize").addEventListener("click", randomize);
$("#start").addEventListener("click", startSort);
$("#pause").addEventListener("click", () => {
  paused = !paused;
  $("#pause").textContent = paused ? "계속하기" : "일시정지";
  $("#runState").textContent = paused ? "PAUSED" : "RUNNING";
});
$("#benchmark").addEventListener("click", runBenchmark);
algorithm.addEventListener("change", () => document.querySelectorAll("tbody tr").forEach(row => row.classList.toggle("active", row.dataset.algorithm === algorithm.value)));

// 첫 화면에 무작위 데이터와 기본 선택 행을 표시합니다.
randomize();
document.querySelector('tbody tr[data-algorithm="bubble"]').classList.add("active");
