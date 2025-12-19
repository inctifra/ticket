import $ from "jquery";
import { getApiWithHeaders as apiWithHeaders } from "../libs/axios";
import { setupAjaxForm } from "../libs/handler";
import { showToast } from "../libs/toast";

$(async function () {
  const { Modal } = await import("bootstrap");
  const loginModal = $("#loginModal");
  const modal = new Modal(loginModal.get(0), {
    keyboard: false,
    backdrop: "static",
  });

  $(".right-header__login__modal--btn").on("click", function (event) {
    event.preventDefault();
    modal.show();
  });

  setupAjaxForm("#loginModal form[method=POST]", {
    onSuccess: (data, formValues, form) => {
      showToast({
        message: "Authentication successful",
      });
    },
    onError: function (data, formValues, form) {
      console.log(data);
      showToast({
        message: "Authentication failed",
        type: "error",
      });
    },
  });
});
