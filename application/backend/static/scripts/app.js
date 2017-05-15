/**
 *  MAIN APPLICATION
 */
(function($) {
  $(document).ready(function() {


    $.addTemplateFormatter("RoundFormatter",
      function(value, template) {
        return Math.floor(value);
      });

    /**
     * ELEMENT REFERENCES
     */
    var loadingPage = $('#loading-page'),
      body = $('body'),
      categoriesContainer = $('.categories-container'),
      languagesContainer = $('.languages-container'),
      noResults = $('#no-results'),
      noQuery = $('#no-query'),
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
        url: '/api/terms/category',
        dataType: 'json',
        method: 'GET'
      }).done(function(data) {
        var d = data.map(function(field) {
          return {name: field};
        });
        var p = categoriesContainer.loadTemplate(
          "/static/scripts/templates/checkbox.html",
          d, {});
        promises.push(p);
      });
      promises.push(cat);

      var lang = $.ajax({
        url: '/api/terms/language',
        dataType: 'json',
        method: 'GET'
      }).done(function(data) {
        var d = data.map(function(field) {
          return {name: field};
        });
        var p = languagesContainer.loadTemplate(
          "/static/scripts/templates/checkbox.html",
          d, {});
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
      noResults.hide();
    }
    Init();

    function Search() {
      if (inputSearch.val() === "") return;
      
      spinner.show();
      noResults.hide();
      results.hide();
      noQuery.hide();

      $.ajax({
        url: '/api/search?' + filtersForm.serialize(),
        data: {
          query: inputSearch.val()
        },
        dataType: 'json',
        method: 'GET'
      }).done(function(data) {
        if (data.length > 0) {
          var templ = (displayAdvanced)
            ? "/static/scripts/templates/results-complete.html"
            : "/static/scripts/templates/results-simple.html";
          results.loadTemplate(templ, data, {
            success: function() {
              setTimeout(function() {
                results.show();
                noResults.hide();
                spinner.hide();
              }, 250);
            }
          });
        } else {
          spinner.hide();
          noResults.show();
        }
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
