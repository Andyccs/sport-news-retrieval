
var app = angular.module('myApp', []);
var pageSize = 5;
var currPage = 1;

function constructURL(keywords) {
    var start = (currPage - 1) * pageSize;

    // You may prefix this with http://localhost:8983 but please do not check that in. In real
    // deployment scenario, Solr will never live in localhost, but it will live in another server /
    // computer. We should not specify any domain name as well, such as http://example.com, because
    // you are not allow to do cross domain request.
    var url = 'solr/sport/select?json.wrf=JSON_CALLBACK&' +
        'q=' + keywords +
        '&start=' + start + 
        '&rows=' + pageSize + 
        '&wt=json';  
    return url  	
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

    var keywords = $scope.keywords;
    var url = constructURL(keywords);
    $http.jsonp(url).success(function(data) {
      $scope.currPage = currPage ;
      $scope.news = data.response.docs ;

      var queryTime = data.responseHeader.QTime;

      $scope.comment = 'The query takes ' + queryTime + ' milliseconds. ';
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

    var keywords = $scope.keywords;
    var url = constructURL(keywords);
    $http.jsonp(url).success(function(data) {
      $scope.currPage = currPage ;
      $scope.news = data.response.docs ;

      var queryTime = data.responseHeader.QTime;

      $scope.comment = 'The query takes ' + queryTime + ' milliseconds. ';
      $scope.$digest();
    
    });
  });

  $scope.comment = 'Popular searches: Warriors, Curry for Three';
  $('#search').click(function() {
    $('#next').attr('disabled','disabled');;
    $('#pre').attr('disabled','disabled');
    currPage = 1;

    var keywords = $scope.keywords;
    var url = constructURL(keywords);
    $http.jsonp(url).success(function(data) {
      $scope.currPage = currPage ;
      $scope.pageCount = Math.ceil(data.response.numFound / pageSize) ;
      if ($scope.pageCount > 1) {
        $('#next').removeAttr('disabled');
      }

      $scope.news = data.response.docs ;

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
