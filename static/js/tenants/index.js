import $ from "jquery";

$(async function () {
  const [{ default: Choices }, {formatCurrencyDynamic}] = await Promise.all([
    import("choices.js"),
    import("../libs/formatter"),
    import("./auth"),
    import("../../sass/tenants/project.scss"),
    import("bootstrap/dist/css/bootstrap.min.css"),
    import("bootstrap"),
    import("bootstrap-icons/font/bootstrap-icons.css"),
    import("@fortawesome/fontawesome-free/css/all.min.css"),
    import("./events"),
    import("./core"),
    import("choices.js/src/styles/choices"),
    import("./payments/scripts"),
  ]);

  if ($(".selectpicker").get(0)) {
    new Choices(".selectpicker", {
      searchEnabled: true,
      itemSelectText: "",
    });
  }
  const countdown = $(".countdown");
  if (countdown.get(0)) {
    startCountdown(countdown);
  }
  function startCountdown(countdown) {
    const startAtStr = countdown.data("start-at");
    const eventDate = new Date(startAtStr.replace(" ", "T"));

    function updateTimer() {
      const now = new Date();
      const diff = eventDate - now;

      if (diff <= 0) {
        $("#day, #hour, #minute, #second").text("0");
        clearInterval(interval);
        return;
      }

      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
      const minutes = Math.floor((diff / (1000 * 60)) % 60);
      const seconds = Math.floor((diff / 1000) % 60);

      $("#day").text(days);
      $("#hour").text(hours);
      $("#minute").text(minutes);
      $("#second").text(seconds);
    }
    updateTimer();
    const interval = setInterval(updateTimer, 1000);
  }

  formatCurrencyDynamic()

});
