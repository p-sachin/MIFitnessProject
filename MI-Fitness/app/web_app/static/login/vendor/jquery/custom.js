jQuery(document).ready(function($){

"use strict";

var nav_offset_top = $('header').height() + 345;

// Preloader

  function Preloader() {
  setTimeout(function(){
   $('.preloader').addClass('loaded')
}, 1500);
}

Preloader();


// Navigation Scroll

function navbarOnScroll(){
    if ( $('.header-content').length){ 
        $(window).scroll(function() {
            var scroll = $(window).scrollTop();   
            if (scroll >= nav_offset_top ) {
                $(".header-content").addClass("navbar-scroll");
            } else {
                $(".header-content").removeClass("navbar-scroll");
            }
        });
    };
};
navbarOnScroll();

//Owl Carousel Testimonials

 function OwlCarousel(){
$('.owl-carousel').owlCarousel({
loop:true,
margin:10,
responsive:{
    0:{
        items:1
    },
    600:{
        items:2
    },
    1000:{
        items:3
    }
}
});
}
OwlCarousel();

  
// Portfolio Filter 

function projects_isotope(){
    if ( $('#portfolio').length ){
        // Activate isotope in container
        $(".portfolio-inner").imagesLoaded( function() {
            $(".portfolio-inner").isotope({
                layoutMode: 'fitRows',
                animationOptions: {
                    duration: 750,
                    easing: 'linear'
                }
            }); 
        });
        
        // Add isotope click function
        $(".portfolio-filter ul li").on('click',function(){
            $(".portfolio-filter ul li").removeClass("active");
            $(this).addClass("active");

            var selector = $(this).attr("data-filter");
            console.log(selector);
            $(".portfolio-inner").isotope({
                filter: selector,
                animationOptions: {
                    duration: 450,
                    easing: "linear",
                    queue: false,
                }
            });
            return false;
        });
    }
}
projects_isotope();



// Stats Counter

function Counter() {
$('.count').counterUp({
    delay: 10,
    time: 1000
});
}
Counter();



// Portfolio Images Popup

 function MagnificPop() {
$('.portfolio-inner').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    removalDelay: 500,
    mainClass: 'mfp-fade',
    gallery: {
        enabled: true,
        navigateByImgClick: true,
        preload: [0,1] // Will preload 0 - before current, and 1 after the current image
    },
    image: {
        tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
        titleSrc: function(item) {
            return item.el.attr('alt') + '<small>by Kraaaw Themes</small>';
        }
    }
});
}

MagnificPop();


// SinglePage Scroll

 function SinglePage() {

    $(document).on('click', '#navbarCollapse a[href^="#"]', function (event) {
    event.preventDefault();
    var href = $.attr(this, 'href');
    $('html, body').animate({
        scrollTop: $($.attr(this, 'href')).offset().top
    }, 500, function() {
        // window.location.hash = href;
    });
    });

};

SinglePage();


// ScrollIt

function scroll() {
 $.scrollIt({
    upKey: 38,
    downKey: 40,
    activeClass: 'active',
    easing: 'swing',
    scrollTime: 600,
    onPageChange: null
 });
}

scroll();

  // About SkillBar

  function skillbar() {
 $(".skill-bar").each(function() {
    $(this).waypoint(function() {
        var progressBar = $(".progress-bar");
        progressBar.each(function(indx){
            $(this).css("width", $(this).attr("aria-valuenow") + "%")
        })
    }, {
        triggerOnce: true,
        offset: 'bottom-in-view'
    });
});
}

skillbar();

// Contact form

function ContactForm() {
var form = $('#contactForm');
form.submit(function(event){
    event.preventDefault();
    var form_status = $('<div class="form_status"></div>');
    $.ajax({
        url: $(this).attr('action'),
        beforeSend: function(){
            form.prepend( form_status.html('<p><i class="fa fa-spinner fa-spin"></i>Please wait...</p>').fadeIn() );
        }
    }).done(function(data){
        form_status.html('<p class="text-success">Thank you for your message.</p>').delay(3000).fadeOut();
    });
});
}

ContactForm();

});



