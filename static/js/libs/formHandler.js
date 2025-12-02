import $ from "jquery";

export function setupAjaxForm(selector, { onSuccess, onError } = {}) {
  $(document).on("submit", selector, async function (e) {
    e.preventDefault();

    const form = $(this);
    const formData = new FormData(this);
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
        if (onError) onError(data);
        return;
      }
      if (onSuccess) onSuccess(data);

    } catch (err) {
      console.error("AJAX error:", err);
      if (err.response?.data?.errors) {
        showFieldErrors(form, err.response.data.errors);
        if (onError) onError(err.response.data);
      }
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
        `<div class="error-message text-danger" style="font-size: 0.85rem;">${messages.join("<br>")}</div>`
      );

      field.after(errorDiv);
    } else {
      form.prepend(
        `<div class="alert alert-danger">${messages.join("<br>")}</div>`
      );
    }
  }
}
