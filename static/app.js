const $ = (selector) => document.querySelector(selector);
const bars = $("#bars");
const algorithm = $("#algorithm");
const size = $("#size");
const speed = $("#speed");
let values = [];
let running = false;
let paused = false;
let runToken = 0;
let chart;

const colors = ["#ff5a24", "#181817", "#3974d8", "#8c55d7", "#20a36a", "#e4a61b"];

function randomize() {
  runToken++;
  running = false;
  paused = false;
  values = Array.from({ length: Number(size.value) }, () => Math.floor(Math.random() * 94) + 6);
  renderBars(values, [], []);
  setMetrics(0, 0, 0, "READY", "준비");
  toggleControls(false);
}

function renderBars(data, active, sorted) {
  const activeSet = new Set(active);
  const sortedSet = new Set(sorted);
  const showValues = data.length <= 30;
  bars.innerHTML = data.map((value, index) => {
    const classes = ["bar", activeSet.has(index) ? "active" : "", sortedSet.has(index) ? "sorted" : ""].join(" ");
    return `<div class="${classes}" style="height:${value}%">${showValues ? `<span class="bar-value">${value}</span>` : ""}</div>`;
  }).join("");
}

function setMetrics(comparisons, swaps, step, state, message) {
  $("#comparisons").textContent = comparisons.toLocaleString();
  $("#swaps").textContent = swaps.toLocaleString();
  $("#steps").textContent = step.toLocaleString();
  $("#runState").textContent = state;
  $("#status").textContent = message;
}

function toggleControls(isRunning) {
  running = isRunning;
  $("#start").disabled = isRunning;
  $("#pause").disabled = !isRunning;
  $("#randomize").disabled = isRunning;
  algorithm.disabled = isRunning;
  size.disabled = isRunning;
}

const delay = () => new Promise(resolve => setTimeout(resolve, [500, 280, 140, 65, 20][Number(speed.value) - 1]));

async function startSort() {
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
    for (let index = 0; index < result.steps.length; index++) {
      if (token !== runToken) return;
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

randomize();
document.querySelector('tbody tr[data-algorithm="bubble"]').classList.add("active");
