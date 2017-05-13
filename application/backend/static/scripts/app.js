/**
 *  MAIN APPLICATION
 */
(function($) {
  $(document).ready(function() {

    var loadingPage = $('#loading-page'),
      body = $('body'),
      categoriesContainer = $('.categories-container'),
      languagesContainer = $('.languages-container'),
      noResults = $('#no-results'),
      results = $('#results'),
      spinner = $('#spinner'),
      seachButton = $('#search-button'),
      inputSearch = $('#search-input');

    function Init() {
      body.addClass('loading');
      var promises = [];
      var cat = $.ajax({url: '/static/json/categories.json', dataType: 'json', method: 'GET'}).done(function(data) {
        var p = categoriesContainer.loadTemplate("/static/scripts/templates/checkbox.html", data, {
          overwriteCache: true,
          success: function() {
            // ...
          }
        });
        promises.push(p);
      });
      promises.push(cat);

      var lang = $.ajax({url: '/static/json/languages.json', dataType: 'json', method: 'GET'}).done(function(data) {
        var p = languagesContainer.loadTemplate("/static/scripts/templates/checkbox.html", data, {
          overwriteCache: true,
          success: function() {
            // ...
          }
        });
        promises.push(p);
      });;
      promises.push(lang);

      $.when.apply($, promises).then(function(schemas) {
        setTimeout(function() {
          body.removeClass('loading');
          loadingPage.hide();
        }, 1000);
      }, function(e) {});

      spinner.hide();
      results.empty();

    }
    Init();

    function Search() {
      spinner.show();
      noResults.hide();
      $.ajax({
        url: '/static/json/results.json',
        data: {
          query: inputSearch.val()
        },
        dataType: 'json',
        method: 'GET'
      }).done(function(data) {
        setTimeout(function() {
          console.log(data);
          spinner.hide();
          if (data.lenth > 0) {
            noResults.hide();
          } else {
            noResults.show();
          }
        }, 250);
      });
    }
    seachButton.on('click', function(e){
      e.preventDefault();
      console.log('hello');
      Search();
    });

  })
})(jQuery);
