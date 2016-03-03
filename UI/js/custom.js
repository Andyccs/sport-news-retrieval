$('#crawl').click(function() {
  // Here initialize a recrawling request to backend
  // Upon finished, generate an alert window
  alert('Finish Recrawling');
});

var app = angular.module('myApp', []);

app.controller('newsCtrl', function($scope, $http) {

  $scope.comment = "Popular searches: Warriors, Curry for Three";
  $('#search').click(function() {
    var keywords = $scope.keywords;
    var url = "http://localhost:8983/solr/sport/select?json.wrf=JSON_CALLBACK&q=" + keywords + "&wt=json&indent=true";

    $http.jsonp(url).success(function(data) {

      $scope.news = data.response.docs ;

      var queryTime = data.responseHeader.QTime;
      $scope.comment = "The query takes " + queryTime + " milliseconds. ";
    });
  });
});