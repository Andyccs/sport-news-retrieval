
var app = angular.module('myApp', []);
var pageSize = 5;
var currPage = 1;
var keywords;

function constructURL() {
  var start = (currPage - 1) * pageSize;

  // You may prefix this with http://localhost:8983 but please do not check that in. In real
  // deployment scenario, Solr will never live in localhost, but it will live in another server /
  // computer. We should not specify any domain name as well, such as http://example.com, because
  // you are not allow to do cross domain request.
  var url = 'http://localhost:8983/solr/sport/select?json.wrf=JSON_CALLBACK&' +
      'q=' + keywords +
      '&start=' + start +
      '&rows=' + pageSize +
      '&wt=json';

  return url;
}


app.controller('newsCtrl', function($scope, $http) {
  $scope.currPage = 0;
  $scope.pageCount = 0;

  $('#pre').click(function() {
    currPage = currPage - 1;
    $scope.currPage = currPage;
    $('#next').removeAttr('disabled');
    if (currPage == 1) {
      $('#pre').attr('disabled','disabled');
    }

    var url = constructURL();

    $http.jsonp(url).success(function(data) {
      $scope.currPage = currPage ;
      $scope.news = data.response.docs ;

      var queryTime = data.responseHeader.QTime;

      $scope.queryTime = 'The query takes ' + queryTime + ' milliseconds. ';

      $scope.$digest();
    });
  });

  $('#next').click(function() {
    currPage = currPage + 1;
    $scope.currPage = currPage;
    $('#pre').removeAttr('disabled');
    if (currPage ==  $scope.pageCount) {
      $('#next').attr('disabled','disabled');
    }

    var url = constructURL();

    $http.jsonp(url).success(function(data) {
      $scope.currPage = currPage ;
      $scope.news = data.response.docs ;

      var queryTime = data.responseHeader.QTime;

      $scope.queryTime = 'The query takes ' + queryTime + ' milliseconds. ';

      $scope.$digest();
    });
  });

  $scope.comment = 'Popular searches: Warriors, Curry for Three';
  $('#search').click(function() {
    $('#next').attr('disabled','disabled');;
    $('#pre').attr('disabled','disabled');
    currPage = 1;

    keywords = $scope.keywords;

    //Get the date interval
    //A string of yyyy-mm-dd
    var fromDate = $('#from').val();
    var toDate = $('#to').val();

    //Get a list of selected sources
    var sources = [];

    $('#filter input[type=checkbox]:checked').each(function() {
      sources.push($(this).val());
    });

    //Later, add these fields to http requests
    //Also modify the request when clicking the previous and next button

    var url = constructURL(keywords);

    $http.jsonp(url).success(function(data) {
      $scope.currPage = currPage ;
      $scope.pageCount = Math.ceil(data.response.numFound / pageSize) ;
      if ($scope.pageCount > 1) {
        $('#next').removeAttr('disabled');
      }

      var fromDateObject = $('#from').val();

      $scope.news = data.response.docs ;

      var queryTime = data.responseHeader.QTime;

      $scope.queryTime = 'The query takes ' + queryTime + ' milliseconds. ';

      //Later, get the actual spelling hints
      var spellings = ['ABC','DEG'];

      if(spellings.length == 0) {

      } else{
        var comment = 'Do you mean ' + spellings[0];

        for (var i = 1; i < spellings.length; i++) {
          comment += ', ' + spellings[i];
        }
        comment += '?';
      }
      $('#comment').html(comment);

      var sources = ['ESPN','NBACentral'];

      $scope.sources = sources ;
    });
  });

  $('#crawl').click(function() {
    // Here initialize a recrawling request to backend
    // Upon finished, generate an alert window
    var url = 'recrawler-service/recrawl';

    $http.get(url).success(function(data) {
      alert('Recrawling in background');
    });
  });
});
