import "../sass/project.scss";
import "./components/theme";
import "owl.carousel";
import "./core/main";
import mixitup from "mixitup";
import $ from "jquery";
import { Modal } from "bootstrap";
import api from "./libs/axios";

function processEmailValidation($launchModalForm){
  $launchModalForm.find("#id_email").on("blur", async function () {
  const input = $(this);
  const email = input.val().trim();
  const helpText = input.closest(".col-md-6").find("small"); // finds the help text element

  if (!email) return;

  // reset UI first
  input.removeClass("is-invalid is-valid");
  helpText.removeClass("text-danger text-success").text("");

  try {
    const res = await api.post(input.data("verification-url"), { email });

    input.addClass("is-valid");
    helpText.addClass("text-success").text("✓ Email verified successfully");
    
    console.log(res.data);

  } catch (error) {
    const detail = error.response?.data?.detail || "Email validation failed";

    input.addClass("is-invalid");
    helpText.addClass("text-danger").text(detail);

    console.log("Validation Error:", detail);
  }
});

}

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
  processEmailValidation($launchModalForm);
  $launchModalForm.on("submit", async function (event) {
    event.preventDefault();

    const fm = $(this);
    const fd = new FormData(fm.get(0));

    console.log(Object.fromEntries(fd));
  });
}

function handleDashboardRedirect() {
  const $btn = $(".right-header__login__modal--btn");
  $btn.on("click", function (event) {
    const url = $(this).data("dashboard-url");
    if (!url) return;
    location.href = url;
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
  handleDashboardRedirect();
});
