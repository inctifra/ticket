
import 'swiper/css';
import { Autoplay } from 'swiper/modules';
import Swiper from "swiper";

// Engaging Online and Venue Events Slider
new Swiper('.engaging-slider', {
    loop: true,
    spaceBetween: 20,
    speed: 800,
    slidesPerView: 5,
    autoplay: {
        delay: 3000,
        disableOnInteraction: true,
    },
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        600: {
            slidesPerView: 1,
        },
        1000: {
            slidesPerView: 2,
        },
        1200: {
            slidesPerView: 3,
        },
        1400: {
            slidesPerView: 3,
        },
    },
});


// Testimonial Slider
new Swiper('.testimonial-slider', {
  slidesPerView: 1,
  spaceBetween: 20,
  loop: true,
  speed: 800,
  autoplay: {
    delay: 3000,
    pauseOnMouseEnter: true,
    disableOnInteraction: false
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: true
  },
  breakpoints: {
    1000: { slidesPerView: 2 },
    1200: { slidesPerView: 2 },
    1400: { slidesPerView: 2 }
  }
});

// Organisations Slider
// $('.organisations-slider').owlCarousel({
// 	items:7,
// 	loop:true,
// 	margin:20,
// 	nav:false,
// 	dots:false,
// 	smartSpeed:800,
// 	autoplay:true,
//     autoplayTimeout:3000,
//     autoplayHoverPause:true,
// 	responsive:{
// 		0:{
// 			items:2
// 		},
// 		600:{
// 			items:2
// 		},
// 		1000:{
// 			items:3
// 		},
// 		1200:{
// 			items:4
// 		},
// 		1400:{
// 			items:5
// 		}
// 	}
// })

try {
    new Swiper('.organisations-slider', {
      modules: [Autoplay],
      loop: true,
      spaceBetween: 20,
      autoplay: {
        delay: 3000,
        pauseOnMouseEnter: true,
      },
      speed: 800,
    
      breakpoints: {
        0: { slidesPerView: 2 },
        600: { slidesPerView: 2 },
        1000: { slidesPerView: 3 },
        1200: { slidesPerView: 4 },
        1400: { slidesPerView: 5 },
      }
    });
} catch (error) {
    
}


// More Events Slider
$('.moreEvents-slider').owlCarousel({
	items:7,
	loop:true,
	margin:20,
	nav:true,
	dots:false,
	navText: ["<i class='uil uil-angle-left'></i>", "<i class='uil uil-angle-right'></i>"],
	responsive:{
		0:{
			items:1
		},
		600:{
			items:2
		},
		800:{
			items:2
		},
		1000:{
			items:3
		},
		1200:{
			items:4
		},
		1400:{
			items:4
		}
	}
})

// More Events Slider
$('.moreEvents-slider').owlCarousel({
	items:7,
	loop:true,
	margin:20,
	nav:true,
	dots:false,
	navText: ["<i class='uil uil-angle-left'></i>", "<i class='uil uil-angle-right'></i>"],
	responsive:{
		0:{
			items:1
		},
		600:{
			items:2
		},
		800:{
			items:2
		},
		1000:{
			items:3
		},
		1200:{
			items:4
		},
		1400:{
			items:4
		}
	}
})

// Most Posts Slider
$('.most-posts-slider').owlCarousel({
	items:1,
	loop:true,
	margin:20,
	nav:false,
	dots:true,
	smartSpeed:800,
	autoplay:true,
    autoplayTimeout:3000,
    autoplayHoverPause:true,
	responsive:{
		0:{
			items:1
		},
		600:{
			items:1
		},
		800:{
			items:1
		},
		1000:{
			items:1
		},
		1200:{
			items:1
		},
		1400:{
			items:1
		}
	}
})

// Related Posts Slider
$('.related-posts-slider').owlCarousel({
	items:4,
	loop:true,
	margin:20,
	nav:true,
	dots:false,
	navText: ["<i class='uil uil-angle-left'></i>", "<i class='uil uil-angle-right'></i>"],
	responsive:{
		0:{
			items:1
		},
		600:{
			items:2
		},
		800:{
			items:2
		},
		1000:{
			items:3
		},
		1200:{
			items:3
		},
		1400:{
			items:4
		}
	}
})

// Role Slider
$('.role-slider').owlCarousel({
	items:4,
	loop:false,
	margin:20,
	nav:true,
	dots:false,
	navText: ["<i class='uil uil-angle-left'></i>", "<i class='uil uil-angle-right'></i>"],
	responsive:{
		0:{
			items:1
		},
		600:{
			items:2
		},
		800:{
			items:2
		},
		1000:{
			items:3
		},
		1200:{
			items:3
		},
		1400:{
			items:4
		}
	}
})
