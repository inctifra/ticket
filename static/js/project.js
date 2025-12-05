import "../sass/project.scss";
import "./components/theme";
import "owl.carousel";
import "./core/main";
import "../src/vendors/core/tables";
import mixitup from "mixitup";
import $ from "jquery";
import { Modal } from "bootstrap";
import api, { getApiWithHeaders as apiWithHeaders } from "./libs/axios";
import "./components/events";

function processEmailValidation($launchModalForm) {
  let isValid = false;
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
      isValid = true;
    } catch (error) {
      const detail = error.response?.data?.detail || "Email validation failed";

      input.addClass("is-invalid");
      helpText.addClass("text-danger").text(detail);

      console.log("Validation Error:", detail);
      isValid = false;
    }
  });
  return isValid;
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
  // processEmailValidation($launchModalForm);
  $launchModalForm.on("submit", async function (event) {
    event.preventDefault();
    const $btn = $(this).find("button[type=submit]");
    $btn.prop("disabled", true);
    $btn.find(".spinner-border").removeClass("d-none");

    const fm = $(this);
    const fd = new FormData(fm.get(0));
    const res = fm.find("div#response");

    try {
      const { data } = await apiWithHeaders({
        "Content-Type": "multipart/form-data",
      }).post(fm.attr("action"), fd);

      res.html(`
        <div class="alert alert-success d-flex align-items-center" role="alert">
            <div>${data.detail}</div>
        </div>
    `);

      // Success actions:
      $launchModalForm[0].reset();
      setTimeout(() => {
        modal.hide();
      }, 3000);
    } catch (error) {
      if (
        error?.response &&
        error.response.data &&
        error.response.data.errors
      ) {
        const errors = error.response.data.errors;

        // Clear previous invalid states
        $launchModalForm.find(".is-invalid").removeClass("is-invalid");
        $launchModalForm.find(".invalid-feedback").remove();
        let html = `<div class="alert alert-danger">`;
        for (const field in errors) {
          const messages = errors[field];
          html += `<div><strong>${field}:</strong> ${messages.join(", ")}</div>`;

          // ------------------------------
          // Add invalid class to field
          // ------------------------------
          const input = $launchModalForm.find(`[name="${field}"]`);
          input.addClass("is-invalid");
          input.before(`<div class="invalid-feedback">${messages.join("<br>")}</div>`);
        }

        html += `</div>`;
        res.html(html);
        return;
      }

      // Unexpected error fallback
      res.html(
        `<div class="alert alert-danger">Unexpected server error.</div>`
      );
    } finally {
      $btn.prop("disabled", false);
      $btn.find(".spinner-border").addClass("d-none");
    }
  });
}

function handleDashboardRedirect() {
  const $btn = $(".right-header__login__modal--btn");
  $btn.on("click", function (event) {
    let url = $(this).data("dashboard-url");
    if (!url) url = "/accounts/login/";
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
