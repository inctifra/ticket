import "../sass/project.scss";
import "./components/theme";
import "owl.carousel";
import "./core/main";
import mixitup from "mixitup";
import $ from "jquery";
import { Modal } from "bootstrap";

function handleLaunchEvent() {
  const $launchBtn = $(".launch-event-btn");
  const $launchModal = $("#event-launch-request");
  const $launchModalForm = $launchModal.find("form#launchRequestForm");

  const modal = new Modal($launchModal.get(0), {
    keyboard: false,
    backdrop: "static",
  });

  $launchBtn.on("click", function () {
    modal.show();
  });
}

$(function () {
  const containerEl = document.querySelector(
    '[data-ref~="event-filter-content"]'
  );
  if (!containerEl) {
    console.warn("MixItUp: container not found");
    return;
  }

  mixitup(containerEl, {
    selectors: { target: '[data-ref~="mixitup-target"]' },
  });

  handleLaunchEvent();
});
