import $ from "jquery";
import { Offcanvas } from "bootstrap";

$(function () {
  const offcanvasEl = document.getElementById("eventCanvas");
  const bsOffcanvas = new Offcanvas(offcanvasEl);

  // Open button
  $("button.eventOffcanvas").on("click", function (e) {
    e.preventDefault();
    bsOffcanvas.show();
  });

});
