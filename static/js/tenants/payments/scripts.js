import $ from "jquery";
import api from "../../libs/axios";

$(async function () {
  await initializePaymentCheckout();
});

export async function initializePaymentCheckout() {
  const [
    { setupAjaxForm },
    { default: PaystackPop },
    { getApiWithHeaders: apiWithHeaders },
  ] = await Promise.all([
    import("../../libs/formHandler"),
    import("@paystack/inline-js"),
    import("../../libs/axios"),
  ]);

  const popup = new PaystackPop();

  setupAjaxForm("#checkout-form", {
    onSuccess: (data) => {
      console.log("Success:", data);
      alert("Event created successfully!");

      const {email, total_amount:amount, delete_path} = data;

      popup.checkout({
        key: "pk_test_5998ac3dcc688383363198dc7fb0b22673996ffa",
        email,
        amount: amount * 100,
        onSuccess: async (transactionData) => {
      
          console.log(transactionData)
        },
        onLoad: (response) => {
          console.log("onLoad: ", response);
        },
        onCancel: () => {
          console.log("onCancel");
          deleteOrderOnPaymentCancel(delete_path).then(data=>console.log(data))
        },
        onError: (error) => {
          console.log("Error: ", error.message);
          deleteOrderOnPaymentCancel(delete_path).then(data=>console.log(data))
        },
      });
    },
    onError: (data) => {
      console.warn("Validation errors:", data);
    },
  });


  const deleteOrderOnPaymentCancel = async(deleteUrl)=>{
    const {data} = await api.post(deleteUrl);
    return data
  }
}
