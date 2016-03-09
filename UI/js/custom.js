
var app = angular.module('myApp', []);
var pageSize = 5;
var currPage = 1;
var news = [];

function displayedNews(page,news) {
  var lower = (page - 1) * pageSize;
  var higher = page * pageSize;

  if (higher > news.length) {
    higher = news.length;
  }
  return news.slice(lower,higher);
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
    $scope.news = displayedNews(currPage,news);
    $scope.$digest();
  });

  $('#next').click(function() {
    currPage = currPage + 1;
    $scope.currPage = currPage;
    $('#pre').removeAttr('disabled');
    if (currPage == Math.ceil(news.length / pageSize)) {
      $('#next').attr('disabled','disabled');
    }
    $scope.news = displayedNews(currPage,news);
    $scope.$digest();
  });

  $scope.comment = 'Popular searches: Warriors, Curry for Three';
  $('#search').click(function() {
    $('#next').attr('disabled','disabled');;
    $('#pre').attr('disabled','disabled');

    var keywords = $scope.keywords;

    // You may prefix this with http://localhost:8983 but please do not check that in. In real
    // deployment scenario, Solr will never live in localhost, but it will live in another server /
    // computer. We should not specify any domain name as well, such as http://example.com, because
    // you are not allow to do cross domain request.
    var url = 'solr/sport/select?json.wrf=JSON_CALLBACK&' +
        'q=' + keywords +
        '&wt=json';

    $http.jsonp(url).success(function(data) {
      news = data.response.docs ;
      currPage = 1;
      $scope.currPage = currPage ;
      $scope.pageCount = Math.ceil(news.length / pageSize) ;
      if ($scope.pageCount > 1) {
        $('#next').removeAttr('disabled');
      }

      $scope.news = displayedNews(currPage,news) ;

      var queryTime = data.responseHeader.QTime;

      $scope.comment = 'The query takes ' + queryTime + ' milliseconds. ';
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
