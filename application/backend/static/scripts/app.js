/**
 *  MAIN APPLICATION
 */
(function($) {
  $(document).ready(function() {

    /**
     * ELEMENT REFERENCES
     */
    var loadingPage = $('#loading-page'),
      body = $('body'),
      categoriesContainer = $('.categories-container'),
      languagesContainer = $('.languages-container'),
      noResults = $('#no-results'),
      results = $('#results'),
      spinner = $('#spinner'),
      seachButton = $('#search-button'),
      inputSearch = $('#search-input'),
      displayOption = $('input[name=displayOption]'),
      filtersForm = $('#filters-form');

    /**
     * CONFIG VARIABLES
     */
    var displayAdvanced = IsAdvanced();

    function Init() {
      body.addClass('loading');
      var promises = [];
      var cat = $.ajax({
        url: '/static/json/categories.json',
        dataType: 'json',
        method: 'GET'
      }).done(function(data) {
        var p = categoriesContainer.loadTemplate(
          "/static/scripts/templates/checkbox.html",
          data, {
          overwriteCache: true,
          success: function() {
            // ...
          }
        });
        promises.push(p);
      });
      promises.push(cat);

      var lang = $.ajax({
        url: '/static/json/languages.json',
        dataType: 'json',
        method: 'GET'
      }).done(function(data) {
        var p = languagesContainer.loadTemplate(
          "/static/scripts/templates/checkbox.html",
          data, {
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
        url: '/static/json/results.json?' + filtersForm.serialize(),
        data: {
          query: inputSearch.val()
        },
        dataType: 'json',
        method: 'GET'
      }).done(function(data) {
        setTimeout(function() {
          spinner.hide();
          if (data.length > 0) {
            var templ = (displayAdvanced)
              ? "/static/scripts/templates/results-complete.html"
              : "/static/scripts/templates/results-simple.html";

            results.loadTemplate(templ, data, {
              overwriteCache: true,
              success: function() {
                results.show();
                noResults.hide();
              }
            });

          } else {
            noResults.show();
          }
        }, 250);
      });
    }
    seachButton.on('click', function(e){
      e.preventDefault();
      Search();
    });

    function IsAdvanced() {
      return $('input[name=displayOption]:checked').val() === "complete";
    }
    displayOption.on('change', function() {
      displayAdvanced = IsAdvanced();
      Search();
    });

  })
})(jQuery);
