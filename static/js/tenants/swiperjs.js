

import $ from "jquery";


$(async function() {
    const [{default:Swiper}] = await Promise.all([
        import("swiper"),
    ])
    
    new Swiper(".moreEvents-slider", {
      slidesPerView: 1,
      spaceBetween: 20,
      loop: true,
      autoplay: {
        delay: 3500,
        disableOnInteraction: false,
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        768: {
          slidesPerView: 2,
        },
        992: {
          slidesPerView: 3,
        },
        1200: {
          slidesPerView: 4,
        },
      },
    });
      const blogSlider = new Swiper('.events-slider', {
        loop: true,
        speed: 600,
        autoplay: {
            delay: 3500,
            disableOnInteraction: false,
        },
        slidesPerView: 1,
        spaceBetween: 20,

        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },

        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },

        breakpoints: {
            768: {
                slidesPerView: 1,
            },
            1024: {
                slidesPerView: 1,
            }
        },
    });
});

