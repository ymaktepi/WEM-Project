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
      spinner = $('#spinner');

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

  })
})(jQuery);
