
var app = angular.module('myApp', []);
var pageSize = 5;
var currPage = 1;
var keywords;



app.controller('newsCtrl', function($scope, $http) {
  $scope.currPage = 0;
  $scope.pageCount = 0;
  
  $scope.showDateFilter = false;
  $scope.showSourceFilter = false;
  $scope.enableMonthFilter = false;
  
  $scope.sourceSelection = [];
  $scope.monthSelection = [];

  $scope.toggleSourceSelection = function (source) {
	  
    var idx = $scope.sourceSelection.indexOf(source);

    if (idx > -1) {
      $scope.sourceSelection.splice(idx, 1);
    }else {
      $scope.sourceSelection.push(source);
    }
    makeRequest();
  };

  $scope.checkMonth = function (month){
    for(var i = 0;i < $scope.monthSelection.length;i++){
      if($scope.monthSelection[i].getTime() == month.getTime()){
        return true;
      }
    }
    return false;
  };
  
  
  $scope.toggleMonthSelection = function (month) {
	  
    var idx = $scope.monthSelection.indexOf(month);

    if (idx > -1) {
      $scope.monthSelection.splice(idx, 1);
    }else {
      $scope.monthSelection.push(month);
    }
    makeRequest(); 
  };
  
  function makeRequest() {
    var start = (currPage - 1) * pageSize;

    //Be default, facet by author and months of previous year

    // You may prefix this with http://localhost:8983 but please do not check that in. In real
    // deployment scenario, Solr will never live in localhost, but it will live in another server /
    // computer. We should not specify any domain name as well, such as http://example.com, because
    // you are not allow to do cross domain request.
    var domain = 'http://localhost:8983/solr/sport/select?';
    var component = 'json.wrf=JSON_CALLBACK' +
        '&q=' + keywords +
        '&start=' + start +
        '&rows=' + pageSize +
        '&wt=json' + 
        '&facet.field=author'+
        '&facet.date=created_at' + 
        '&f.created_at.facet.date.start=NOW-12MONTH/MONTH' +
        '&f.created_at.facet.date.end=NOW%2B1MONTH/MONTH' +
        '&f.created_at.facet.date.gap=%2B1MONTH'
    ;
    
    var url = domain + component;
    
    $http.jsonp(url).success(function(data) {
      $scope.currPage = currPage ;
      $scope.pageCount = Math.ceil(data.response.numFound / pageSize) ;
      if ($scope.pageCount > 1) {
        $scope.nextDisabled = false;
      }

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
      $scope.comment = comment;
       
      var monthRecords = [];
      
      var month;
      var monthCount = 0;
      
      for (var key in data.facet_counts.facet_dates.created_at) {
	      
	if(monthCount == 12) break;
	monthCount = monthCount + 1;
	var date = new Date(key);
	count = data.facet_counts.facet_dates.created_at[key];
        var monthRecord = new Object();
	monthRecord.month = date;
	monthRecord.count = count;
	monthRecords.push(monthRecord);

      }
      $scope.showDateFilter = true;
      $scope.monthRecords = monthRecords ;
      
       
      var sources = [];
      
      var author;
      var count = 0;
      var source = new Object();
      for (i = 0; i < data.facet_counts.facet_fields.author.length; i++) {
	      
	if(i % 2 == 0){
	  author = data.facet_counts.facet_fields.author[i];
	  source.name = author;
	}else{
	  count = data.facet_counts.facet_fields.author[i];
	  source.count = count;
	  sources.push(source);
	  source = new Object();
	}
      }
      $scope.showSourceFilter = true;
      $scope.sources = sources ;
    });

  }
  $scope.comment = 'Popular searches: Warriors, Curry for Three';

  $scope.pre = function() {
    currPage = currPage - 1;
    $scope.currPage = currPage;
    $scope.nextDisabled = false;
    if (currPage == 1) {
      $scope.preDisabled = true;
    }

    makeRequest();
  };

  $scope.next = function() {
    currPage = currPage + 1;
    $scope.currPage = currPage;
    $scope.preDisabled = false;
    if (currPage == 1) {
      $scope.nextDisabled = true;
    }

    var url = constructURL();

    makeRequest();

  };


  $scope.search = function() {
    $scope.preDisabled = true;
    $scope.nextDisabled = true;
    currPage = 1;

    keywords = $scope.keywords;

    //Get the date interval
    //A string of yyyy-mm-dd
    //alert($scope.startDate);

    //Get a list of selected sources
    //alert($scope.selection);

    //Later, add these fields to http requests
    //Also modify the request when clicking the previous and next button

    makeRequest();
  };

  $scope.crawl = function() {
    // Here initialize a recrawling request to backend
    // Upon finished, generate an alert window
    var url = 'recrawler-service/recrawl';

    $http.get(url).success(function(data) {
      alert('Recrawling in background');
    });
  };
});
