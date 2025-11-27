import $ from "jquery";
import Chart from "chart.js/auto";
import { getApiWithHeaders as apiWithHeaders } from "../libs/axios";

function loadEventsStatChart() {
  let eventChart = null;

  async function loadEventStatusChart() {
    const canvasEl = document.querySelector("#eventStatusChart");
    if(!canvasEl) return;
    const endpoint = canvasEl.dataset.endpoint;
    const response = await fetch(endpoint);
    const result = await response.json();

    const ctx = canvasEl.getContext("2d");

    if (eventChart) {
      eventChart.destroy();
    }

    eventChart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: result.labels,
        datasets: [
          {
            label: "Event Requests by Status",
            data: result.data,
            backgroundColor: ["#4caf50", "#2196f3", "#f44336", "#ff9800"],
            borderColor: "#fff",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "top", display: true },
          tooltip: {
            callbacks: {
              label: function (context) {
                let label = context.label || "";
                let value = context.parsed;
                return `${label}: ${value}`;
              },
            },
          },
        },
      },
    });
  }

  loadEventStatusChart();
  setInterval(loadEventStatusChart, 3600000);
}
$(function () {
  $(document).on("show.bs.offcanvas", function (event) {
    const canvas = $(event.target);
    const canvasId = canvas.attr("id");

    const btnTrigger = $(`button[data-bs-target='#${canvasId}']`);

    const fm = canvas.find(`form.eventCanvasForm-${canvasId}`);

    fm.on("submit", async function (event) {
      event.preventDefault();
      const fd = new FormData(event.target);
      console.log(Object.fromEntries(fd));

      try {
        const { data } = await apiWithHeaders({
          "Content-Type": "multipart/form-data",
        }).post(fm.attr("action"), fd);
        console.log(data)
      } catch (error) {
        console.log(error)
      }
      finally{

      }
    });
  });

  loadEventsStatChart();
});
