import $ from "jquery";

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
});
