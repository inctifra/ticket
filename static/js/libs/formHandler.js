import $ from "jquery";

export function setupAjaxForm(selector, { onSuccess, onError } = {}) {
  $(document).on("submit", selector, async function (e) {
    e.preventDefault();

    const form = $(this);
    const submitBtn = form.find('[type="submit"]');
    const originalBtnHTML = submitBtn.html();

    submitBtn.prop("disabled", true).html(`
      <div class="d-flex align-items-center justify-content-center w-100 h-100 position-relative">
        <span class="spinner-border spinner-border-md text-white me-2" role="status" aria-hidden="true"></span>
      </div>
    `);

    const formData = new FormData(this);
    const formValues = Object.fromEntries(formData.entries());
    clearFieldErrors(form);

    try {
      const [{ getApiWithHeaders: apiWithHeaders }] = await Promise.all([
        import("./axios"),
      ]);

      const { data } = await apiWithHeaders({
        "Content-Type": "multipart/form-data",
      }).post(form.attr("action"), formData);

      if (data.success === false) {
        showFieldErrors(form, data.errors);
        if (onError) onError(data, formValues);
        return;
      }

      if (onSuccess) onSuccess(data, formValues);
    } catch (err) {
      console.error("AJAX error:", err);

      if (err.response?.data?.errors) {
        showFieldErrors(form, err.response.data.errors);
        if (onError) onError(err.response.data, formValues);
      }
    } finally {
      submitBtn.prop("disabled", false).html(originalBtnHTML);
    }
  });
}


function clearFieldErrors(form) {
  form.find(".error-message").remove();
  form.find(".is-invalid").removeClass("is-invalid");
}

function showFieldErrors(form, errors) {
  if (!errors) return;

  for (const [fieldName, messages] of Object.entries(errors)) {
    const field = form.find(`[name="${fieldName}"]`);

    if (field.length) {
      field.addClass("is-invalid");

      const errorDiv = $(
        `<div class="error-message text-danger" style="font-size: 0.85rem;">${messages.join(
          "<br>"
        )}</div>`
      );

      field.after(errorDiv);
    } else {
      form.prepend(
        `<div class="alert alert-danger">${messages.join("<br>")}</div>`
      );
    }
  }
}
