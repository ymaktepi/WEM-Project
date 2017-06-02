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
      tagsContainer = $('.tags-container'),
      nbTags = $('.nb-tags'),
      toolsContainer = $('.tools-container'),
      nbTools = $('.nb-tools'),
      categoriesContainer = $('.categories-container'),
      nbCategories = $('.nb-categories'),
      languagesContainer = $('.languages-container'),
      nbLanguages = $('.nb-languages'),
      noResults = $('#no-results'),
      noQuery = $('#no-query'),
      results = $('#results'),
      resultsContent = $('#results .content'),
      resultsHeader = $('#results .header'),
      loadMore = $('#load-more'),
      spinner = $('#spinner'),
      seachButton = $('#search-button'),
      resetButton = $('#reset-button'),
      inputSearch = $('#search-input'),
      displayOption = $('input[name=displayOption]'),
      scoringOptions = $('input[name=scoringOption]'),
      filtersForm = $('#filters-form');

    /**
     * CONFIG VARIABLES
     */
    var displayAdvanced = IsAdvanced();
    var currentPage = 1;
    var scoringOption = GetScoringOption();

    function Init() {
      body.addClass('loading');
      var promises = [];
      var tag = $.ajax({
        url: '/api/terms/tags',
        dataType: 'json',
        method: 'GET'
      }).done(function(data) {
        var d = data.map(function(field) {
          return {
            id: TransformToId(field, 'tag'),
            name: field,
            type: 'tags'
          };
        });
        nbTags.html(data.length);
        var p = tagsContainer.loadTemplate(
          "/static/scripts/templates/checkbox.html",
          d, {
            success: function() {
              tagsContainer.find('input').on('change', function(e) {
                currentPage = 1;
                Search();
              });
            }
          });
        promises.push(p);
      });
      promises.push(tag);

      var tool = $.ajax({
        url: '/api/terms/tool',
        dataType: 'json',
        method: 'GET'
      }).done(function(data) {
        var d = data.map(function(field) {
          return {
            id: TransformToId(field, 'tool'),
            name: field,
            type: 'tool'
          };
        });
        nbTools.html(data.length);
        var p = toolsContainer.loadTemplate(
          "/static/scripts/templates/checkbox.html",
          d, {
            success: function() {
              toolsContainer.find('input').on('change', function(e) {
                currentPage = 1;
                Search();
              });
            }
          });
        promises.push(p);
      });
      promises.push(tool);

      var cat = $.ajax({
        url: '/api/terms/category',
        dataType: 'json',
        method: 'GET'
      }).done(function(data) {
        var d = data.map(function(field) {
          return {
            id: TransformToId(field, 'cat'),
            name: field,
            type: 'category'
          };
        });
        nbCategories.html(data.length);
        var p = categoriesContainer.loadTemplate(
          "/static/scripts/templates/checkbox.html",
          d, {
            success: function() {
              categoriesContainer.find('input').on('change', function(e) {
                currentPage = 1;
                Search();
              });
            }
          });
        promises.push(p);
      });
      promises.push(cat);

      var lang = $.ajax({
        url: '/api/terms/language',
        dataType: 'json',
        method: 'GET'
      }).done(function(data) {
        var d = data.map(function(field) {
          return {
            id: TransformToId(field, 'lang'),
            name: field,
            type: 'language'
          };
        });
        nbLanguages.html(data.length);
        var p = languagesContainer.loadTemplate(
          "/static/scripts/templates/checkbox.html",
          d, {
            success: function() {
              languagesContainer.find('input').on('change', function(e) {
                currentPage = 1;
                Search();
              });
            }
          });
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
      resultsContent.empty();
      noResults.hide();
      loadMore.hide();
    }
    Init();

    function Search() {

      if (filtersForm.serialize() == "" && inputSearch.val() == "") {
        results.hide();
        loadMore.hide();
        noQuery.show();
        return;
      }

      var startTime = Date.now();

      noResults.hide();
      noQuery.hide();

      if (currentPage == 1) {
        spinner.show();
        results.hide();
        loadMore.hide();
      }

      $.ajax({
        url: `/api/search/${currentPage}?scoring=${scoringOption}&` + filtersForm.serialize(),
        data: {
          query: inputSearch.val()
        },
        dataType: 'json',
        method: 'GET'
      }).done(function(res) {
        $('#alert-content').empty();
        var data = res.data;
        if (data.length > 0) {
          var templ = (displayAdvanced)
            ? "/static/scripts/templates/results-complete.html"
            : "/static/scripts/templates/results-simple.html";
          d = data.map(function(item) {
            item.categories = item.category.map(function(cat) {
              return GenerateTag("label label-primary", cat, 'cat');
            });
            item.languages = item.language.map(function(lang) {
              return GenerateTag("label label-danger", lang, 'lang');
            });
            item.tools = item.tool.map(function(tool) {
              return GenerateTag("label label-warning", tool, 'tool');
            });
            if (item.tags != 'undefined' && item.tags != '')
              item.parsedTags = GenerateTag("label label-success", item.tags, 'tag');
            return item;
          });

          resultsContent.loadTemplate(templ, d, {
            append: currentPage > 1,
            success: function() {
              setTimeout(function() {

                results.show();
                noResults.hide();
                spinner.hide();
                loadMore.removeAttr("disabled");
                if (res.metadata.hasMore) {
                  loadMore.show();
                } else {
                  loadMore.hide();
                }

                $('#results .results-complete-tags .label').on('click', function(e) {
                  var tagId = $(this).attr('data-tag-id');
                  $('#'+tagId).prop('checked', true);
                  currentPage = 1;
                  Search();
                });

                var time = (Date.now() - startTime) / 1000;

                resultsHeader.html(`<span
                  class="nb-results">
                    ${res.metadata.found} results
                  </span> on ${res.metadata.on}, <span>
                    in ${time} sec
                  </span>`);

              }, 250);
            }
          });
        } else {
          spinner.hide();
          noResults.show();
        }
      }).fail(function(jqXHR, textStatus) {
        var data = JSON.parse(jqXHR.responseText);
        $('#alert-content')
          .loadTemplate("/static/scripts/templates/message.html", {
            classes: 'alert alert-danger',
            title: 'Error!',
            message: data.message || 'An error occured, please retry later.'
            });
        spinner.hide();
      });
    }
    seachButton.on('click', function(e){
      e.preventDefault();
      Search();
    });
    resetButton.on('click', function(e){
      currentPage = 1;
      filtersForm[0].reset();
      results.hide();
      spinner.hide();
      noResults.hide();
      noQuery.show();
      loadMore.hide();
    });

    function LoadMore() {
      loadMore.attr("disabled", "disabled");
      currentPage += 1;
      Search();
    }
    loadMore.on('click', function(e) {
      e.preventDefault();
      if (loadMore.attr("disabled") != "disabled") {
        LoadMore();
      }
    });

    function IsAdvanced() {
      return $('input[name=displayOption]:checked').val() === "complete";
    }
    displayOption.on('change', function() {
      currentPage = 1;
      displayAdvanced = IsAdvanced();
      Search();
    });

    function GetScoringOption() {
      return $('input[name=scoringOption]:checked').val();
    }
    scoringOptions.on('change', function() {
      currentPage = 1;
      scoringOption = GetScoringOption();
      Search();
    });

    function GenerateTag(classes, tagName, prefix) {
      var html = `<span
        class="${classes}"
        data-tag-id="${TransformToId(tagName, prefix)}">
          ${tagName}
        </span>`;
      return $(html);
    }

    function TransformToId(val, prefix) {
      return prefix + '-' + val.split(' ').join('-').toLowerCase();
    }

  })
})(jQuery);
