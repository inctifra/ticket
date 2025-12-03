import $ from "jquery";

export function updateEventTicketCheckout() {
  function updateTotals() {
    const price = parseFloat(
      $(".selectpicker option:selected").data("price") || 0
    );

    const qty = parseInt($("#ticket-qty").val()) || 1;

    const subtotal = price * qty;

    $("#summary-qty").text(qty);
    $("#summary-subtotal").text(`KES ${subtotal.toFixed(2)}`);
    $("#summary-total").text(`KES ${subtotal.toFixed(2)}`);
    $("#total-display").text(`KES ${subtotal.toFixed(2)}`);

    $("input[id='id_total_price']").val(subtotal);
  }

  $(".selectpicker").on("change", updateTotals);
  $("#ticket-qty").on("input", updateTotals);

  updateTotals();
}

$(async function () {
  const [{ setupAjaxForm }] = await Promise.all([
    import("../libs/formHandler"),
  ]);

  setupAjaxForm("#event_creation_form", {
    onSuccess: (data) => {
      console.log("Success:", data);
      alert("Event created successfully!");
    },
    onError: (data) => {
      console.warn("Validation errors:", data);
    },
  });

  updateEventTicketCheckout();
});
