import $ from "jquery";
import { getApiWithHeaders as apiWithHeaders } from "../libs/axios";


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

  const fm = loginModal.find("form[method=POST]");

  fm.on("submit", async function (event) {
    event.preventDefault();
    const fd = new FormData($(this).get(0));
     const url = $(this).attr("action");
    console.log(Object.fromEntries(fd));
       const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;
    try {
        const { data } = await apiWithHeaders({
          "Content-Type": "multipart/form-data",
        }).post(url, fd);
        console.log(data)
      } catch (error) {
        console.log(error)
      }
      finally{

      }
  });
});
