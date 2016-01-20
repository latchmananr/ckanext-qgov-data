(function( $ ) {
	'use strict';

	$( document ).ready(function() {
		$( '#article' ).trigger( 'x-height-change' );
	});
	$( '#article' ).on('click', '.show-more', function() {
		$( '#article' ).trigger( 'x-height-change' );
	});
	$( '#article' ).on('click', '.show-less', function() {
		$( '#article' ).trigger( 'x-height-change' );			  
	});

	if ( $( 'body' ).hasClass( "theme-index-with-asides" ) ) {
      $("#asides").insertAfter ('#ia');
    }

    $( 'body' ).addClass( window.location.hostname == "data.qld.gov.au" || window.location.hostname == "www.data.qld.gov.au" || window.location.hostname == "publications.qld.gov.au" || window.location.hostname == "www.publications.qld.gov.au" ? 'prod' : 'env-staging'  );

}( jQuery ));