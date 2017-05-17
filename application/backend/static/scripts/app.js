/**
 *  MAIN APPLICATION
 */
(function($) {
  $(document).ready(function() {


    $.addTemplateFormatter({
      RoundFormatter: function(value, template) {
        return Math.floor(value);
      },
      MultipleCheckbox: function(value, template) {
        return value+"[]";
      },
      SimpleUrl: function(value, template) {
        var url = new URL(value);
        return url.hostname;
      }
    });

    /**
     * ELEMENT REFERENCES
     */
    var loadingPage = $('#loading-page'),
      body = $('body'),
      categoriesContainer = $('.categories-container'),
      nbCategories = $('.nb-categories'),
      languagesContainer = $('.languages-container'),
      nbLanguages = $('.nb-languages'),
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
          return {name: field, type: 'category'};
        });
        nbCategories.html(data.length);
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
          return {name: field, type: 'language'};
        });
        nbLanguages.html(data.length);
        var p = languagesContainer.loadTemplate(
          "/static/scripts/templates/checkbox.html",
          d, {});
        promises.push(p);
      });
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
        $('#alert-content').empty();
        if (data.length > 0) {
          var templ = (displayAdvanced)
            ? "/static/scripts/templates/results-complete.html"
            : "/static/scripts/templates/results-simple.html";
          d = data.map(function(item) {
            item.categories = item.category.map(function(cat) {
              return $('<span class="label label-primary">'+cat+'</span> <span></span>');
            });
            item.languages = item.language.map(function(lang) {
              return $('<span class="label label-danger">'+lang+'</span> <span></span>');
            });
            if (item.tags != 'undefined')
              item.parsedTags = $('<span class="label label-success">'+item.tags+'</span> <span></span>');
            return item;
          });
          results.loadTemplate(templ, d, {
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
      }).fail(function(jqXHR, textStatus) {
        $('#alert-content')
          .loadTemplate("/static/scripts/templates/message.html", {
            classes: 'alert alert-danger',
            title: 'Error!',
            message: 'An error occured, please retry later.'
            });
        spinner.hide();
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
