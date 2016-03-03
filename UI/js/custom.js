$('#crawl').click(function() {
  // Here initialize a recrawling request to backend
  // Upon finished, generate an alert window
  alert('Finish Recrawling');
});

var app = angular.module('myApp', []);

app.controller('newsCtrl', function($scope, $http) {

  $scope.comment = 'Popular searches: Warriors, Curry for Three';
  $('#search').click(function() {
    var keywords = $scope.keywords;

    // You may prefix this with http://localhost:8983 but please do not check that in. In real
    // deployment scenario, Solr will never live in localhost, but it will live in another server /
    // computer. We should not specify any domain name as well, such as http://example.com, because
    // you are not allow to do cross domain request.
    var url = 'solr/sport/select?json.wrf=JSON_CALLBACK&' +
        'q=' + keywords +
        '&wt=json';

    $http.jsonp(url).success(function(data) {

      $scope.news = data.response.docs ;

      var queryTime = data.responseHeader.QTime;

      $scope.comment = 'The query takes ' + queryTime + ' milliseconds. ';
    });
  });
});
