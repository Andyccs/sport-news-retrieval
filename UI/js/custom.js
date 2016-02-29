$("#crawl").click(function(){
	//Here initialize a recrawling request to backend
	//Upon finished, generate an alert window
	alert("Finish Recrawling");
})

var app = angular.module('myApp', []);
app.controller('newsCtrl', function($scope, $http){
		
	$scope.keywords = "Enter keywords here";
	$("#search").click(function(){
		//Later, need to modify this http request so that it makes query to backend solr using keywords		
		var keywords = $scope.keywords;
		$http.get("fake_news.json").success(
			function(response) {
	          		     $scope.news = response.news;
	    		});
	})
		
 });