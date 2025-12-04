import $ from "jquery";
import api from "../../libs/axios";

$(async function () {
  await initializePaymentCheckout();
  await downloadTicket();
});

export async function initializePaymentCheckout() {
  const [
    { setupAjaxForm },
    { default: PaystackPop },
  ] = await Promise.all([
    import("../../libs/formHandler"),
    import("@paystack/inline-js"),
  ]);

  const popup = new PaystackPop();

  const { data } = await api.get($("#paystack_key_url").data("url"));
  const paystack_key = data.key;

  setupAjaxForm("#checkout-form", {
    onSuccess: (data, formValues) => {
      console.log("Success:", data, "form-data", formValues);
      const { email, total_amount: amount, delete_path } = data;
      popup.checkout({
        key: paystack_key,
        email,
        amount: amount * 100,
        onSuccess: (transactionData) => {
          console.log(transactionData);
          processOrderItem(data.order_item_process_url, {
            ...transactionData,
            ...formValues,
          }).then((data) => {
            const {success_url} = data;
            if(!success_url) return;
            setTimeout(() => {
              window.location.href = success_url
            }, 1000);
          });
        },
        onLoad: (response) => {
          console.log("onLoad: ", response);
        },
        onCancel: () => {
          console.log("onCancel");
          deleteOrderOnPaymentCancel(delete_path).then((data) =>
            console.log(data)
          );
        },
        onError: (error) => {
          console.log("Error: ", error.message);
          deleteOrderOnPaymentCancel(delete_path).then((data) =>
            console.log(data)
          );
        },
      });
    },
    onError: (data) => {
      console.warn("Validation errors:", data);
    },
  });

  const deleteOrderOnPaymentCancel = async (deleteUrl) => {
    const { data } = await api.post(deleteUrl);
    return data;
  };

  const processOrderItem = async (url, _data) => {
    const { data } = await api.post(url, _data);
    return data;
  };
}



export async function downloadTicket() {
  $("#download-ticket").on("click", async function(event) {
    event.preventDefault();

    const url = $(this).data("href");

    try {
      const response = await api.get(url, { responseType: 'blob' });
            const blob = new Blob([response.data], { type: 'application/pdf' });
      const downloadUrl = window.URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = "";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(downloadUrl);

    } catch (error) {
      console.error('Download failed:', error);
      alert('Failed to download ticket.');
    }
  });
}
