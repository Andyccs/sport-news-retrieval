
var app = angular.module('myApp', []);
var page_size = 5;
var curr_page = 1;
var news = [];

function displayed_news(page,news){
	var lower = (page - 1)* page_size;
	var higher = page * page_size;
	if(higher > news.length) higher = news.length;
	
        return news.slice(lower,higher);	
	
}

app.controller('newsCtrl', function($scope, $http) {
   $scope.curr_page = 0 ; 
  $scope.page_count = 0;
  
  $('#pre').click(function() {
	  curr_page = curr_page - 1;
          $scope.curr_page = curr_page ; 
	  $('#next').removeAttr("disabled");
	  if(curr_page == 1) $('#pre').attr("disabled","disabled");
          $scope.news = displayed_news(curr_page,news);
	  $scope.$digest()
	  
  });
  
  $('#next').click(function() {
	  curr_page = curr_page + 1;
          $scope.curr_page = curr_page ; 
	  $('#pre').removeAttr("disabled");
	  if(curr_page == Math.ceil(news.length / page_size)) $('#next').attr("disabled","disabled");
          $scope.news = displayed_news(curr_page,news);
	  $scope.$digest()
	  
  });
  
  
  $scope.comment = 'Popular searches: Warriors, Curry for Three';
  $('#search').click(function() {
    $('#next').attr("disabled","disabled");;
    $('#pre').attr("disabled","disabled");


    var keywords = $scope.keywords;

    // You may prefix this with http://localhost:8983 but please do not check that in. In real
    // deployment scenario, Solr will never live in localhost, but it will live in another server /
    // computer. We should not specify any domain name as well, such as http://example.com, because
    // you are not allow to do cross domain request.
    // var url = 'solr/sport/select?json.wrf=JSON_CALLBACK&' +
  //       'q=' + keywords +
  //   '&wt=json';

    var url = 'http://localhost:8983/solr/sport/select?json.wrf=JSON_CALLBACK&' +
        'q=' + keywords +
    '&wt=json';

    $http.jsonp(url).success(function(data) {

      news = data.response.docs ;
      curr_page = 1;
      $scope.curr_page = curr_page ;
      $scope.page_count = Math.ceil(news.length / page_size) ;
      if($scope.page_count > 1) $('#next').removeAttr("disabled");

      $scope.news = displayed_news(curr_page,news) ;

      var queryTime = data.responseHeader.QTime;

      $scope.comment = 'The query takes ' + queryTime + ' milliseconds. ';
    });
  });

  $('#crawl').click(function() {
    // Here initialize a recrawling request to backend
    // Upon finished, generate an alert window
    var url = 'recrawler-service/recrawl'
    $http.get(url).success(function(data) {
      alert('Recrawling in background');
    });
  });
});
