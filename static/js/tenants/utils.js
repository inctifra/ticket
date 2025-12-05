import $ from "jquery";
import "select2";
import { Modal } from "bootstrap";
import { setupAjaxForm } from "../libs/formHandler";
import { showToast } from "../libs/toast";

function setupModal(buttonSelector, modalSelector) {
  const modalBtn = $(buttonSelector);
  const modalDiv = $(modalSelector);

  if (!modalBtn.length || !modalDiv.length) return;

  const modal = new Modal(modalDiv.get(0), {
    keyboard: false,
    backdrop: "static",
  });
  modalBtn.on("click", function (e) {
    e.preventDefault();
    modal.show();
  });

  return modal;
}

$(async function () {
  await InviteStaffModal();
  await assignScanningPermission();
});

async function InviteStaffModal() {
  const modal = setupModal("button#inviteStaffModal", "div#inviteStaffModal");

  updateAccountDesc();
  $("#deactivate-toggle").on("change", function () {
    updateAccountDesc();
  });
}

async function assignScanningPermission() {
  const modal = setupModal(
    "button#assignScannerPermissionModal",
    "div#assignScannerPermissionModal"
  );

  setupAjaxForm("#assignScannerPermissionModal form", {
    onSuccess: (data, formValues, form) => {
      console.log("Success:", data);
      showToast({
        message: "Permission assigned successfully",
        type: "success",
      });
      form.get(0).reset();
      modal.hide();
    },
    onError: (error) => {
      showToast({
        message: "Permission assignment failed!",
        type: "error",
      });
    },
  });
}

function updateAccountDesc() {
  if ($("#deactivate-toggle").is(":checked")) {
    $("#account-desc").text(
      "The user account is deactivated. They can only log in once you grant permission."
    );
  } else {
    $("#account-desc").text(
      "The user account will be active immediately upon registration. We discourage this!"
    );
  }
}
