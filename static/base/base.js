var Base = function () {

    function handleHoverOpen() {
        $(".dropdown").hover(
            function(){ $(this).addClass('open') },
            function(){ $(this).removeClass('open') }
        );
    }

    function handleNavbar() {

        $("#nav-top").affix({
					offset: {
						top: "0.1"
					}
				});
    }
    function scrollTop() {

        /* smooth scrolling for scroll to top */
        $('.scroll-top').click(function () {
            $('body,html').animate({scrollTop: 0}, 500);
        })

        /* scroll 渐渐消失 */
        $(document).on('scroll', function () {

            if ($(window).scrollTop() > 100) {
                $('.scroll-top').addClass('show');
            } else {
                $('.scroll-top').removeClass('show');
            }
        });

    }


    return {
        init: function () {

            handleNavbar();

            handleHoverOpen();

            scrollTop();
        }
    };
}();