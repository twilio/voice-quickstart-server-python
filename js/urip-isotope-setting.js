$(window).load(function(){
	'use strict';
	/* ===============================
		ISOTOPE (jQuery Sort & FIlter)
	================================*/
	// ** ISOTOPE FOR TEAM SECTION ** //
	var $filterContainerTeam = $('.team-list');

	//	Show All the filter items first
	$filterContainerTeam.isotope({
	  filter: '*',
	  itemSelector: '.team-item',
	  layoutMode: 'fitRows'
	});

	//	Adjust active class for the active filter button
	$('.filter a').click(function(){
        $('.filter .active').removeClass('active');
        $(this).addClass('active');

        var selector = $(this).attr('data-filter');

        //	Filter item based on active selector
        $filterContainerTeam.isotope({
            filter: selector
         });
         return false;
    });

    // ** ISOTOPE FOR PORTFOLIO ** //
	var $filterContainer = $('.portfolio-list');

	//	Show All the filter items first
	$filterContainer.isotope({
	  filter: '*',
	  itemSelector: '.portfolio-item',
	  layoutMode: 'fitRows'
	});

	//	Adjust active class for the active filter button
	$('.portfolio-filter a').click(function(){
        $('.portfolio-filter .active').removeClass('active');
        $(this).addClass('active');

        var selector = $(this).attr('data-filter');

        //	Filter item based on active selector
        $filterContainer.isotope({
            filter: selector
         });
         return false;
    });

    // Mobile Select Filter
	$("#mobile-team-filter").click(function(){
		$(this).toggleClass("select-active");
		$("ul.filter").toggleClass("filter-active");
	});

	$("#mobile-portfolio-filter").click(function(){
		$(this).toggleClass("select-active");
		$("ul.portfolio-filter").toggleClass("filter-active");
	});

});