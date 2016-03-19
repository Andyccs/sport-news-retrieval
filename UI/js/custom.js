
var app = angular.module('myApp', []);
var pageSize = 5;
var currPage = 1;
var keywords;



app.controller('newsCtrl', function($scope, $http) {
	
  //Init the date range from 2 years ago until now
  $scope.endDate = new Date();
  $scope.startDate = new Date($scope.endDate.getTime() - 2 * 365 * 24 * 60 * 60 * 1000);
	
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
    makeRequest(false);
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
    	  
    var idx = -1;
    
    for(var i = 0;i < $scope.monthSelection.length;i++){
      if($scope.monthSelection[i].getTime() == month.getTime()){
        idx = i;
        break;
      }
    }

    if (idx > -1) {
      $scope.monthSelection.splice(idx, 1);
    }else {
      $scope.monthSelection.push(month);
    }
    makeRequest(false);
    
  };
  
  function makeMonthQuery(low,high){
    var query = "";
    query += "created_at:[";
    query += low.toISOString();
    query += " TO ";
    query += high.toISOString() + "]";
	
    return query;
  }
  
  function makeSourceQuery(source){
    var query = "";
    query += "author:(\"";
    query += encodeURIComponent(source);
    query += "\")";
	
    return query;
  }
  
  function makeRequest(tickAll) {
	  
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
    
    var dateQuery = "(";
    if($scope.enableMonthFilter){
      if($scope.monthSelection.length == 0){
        alert("Please at least check one month.");
	return;
      }
      var low = $scope.monthSelection[0];
      var high = new Date(low.getTime() + 2678400000);
      
      dateQuery += makeMonthQuery(low,high);
      
      for(var i = 1;i < $scope.monthSelection.length;i++){
	var low = $scope.monthSelection[i];
	var high = new Date(low.getTime() + 2678400000);
      
        dateQuery += " OR " + makeMonthQuery(low,high);
      }      	

    }else{
       var low = $scope.startDate;    
       if (typeof low === 'undefined'){
	  alert("Please enter the start date.");
	  return;
       }
       var high = $scope.endDate;    
       if (typeof high === 'undefined'){
	  alert("Please enter the end date.");
	  return;
       }
             
        dateQuery += makeMonthQuery(low,high);    	
    }
    dateQuery += ")";
    

//http://localhost:8983/solr/sport/select?json.wrf=JSON_CALLBACK&q=nba&start=…_at.facet.date.gap=%2B1MONTH&fq=cat:((created_at:[2014-03-20T08:07:29.154Z TO 2016-03-19T08:07:29.154Z]))

//   http://localhost:8983/solr/sport/select?json.wrf=JSON_CALLBACK&q=nba&start=…_at.facet.date.gap=%2B1MONTH&fq=cat:((created_at:[2014-03-20T08:07:29.154Z TO 2016-03-19T08:07:29.154Z]) AND ))
    
    var sourceQuery = "(";
    if($scope.sourceSelection.length != 0){
      sourceQuery += makeSourceQuery($scope.sourceSelection[0]);
      
      for(var i = 1;i < $scope.sourceSelection.length;i++){
        sourceQuery += " OR " + makeSourceQuery($scope.sourceSelection[i]);
      }   
    }
    sourceQuery += ")";
    if($scope.sourceSelection.length != 0){
      component += "&fq=cat:(";
      component += dateQuery;    
      component += " AND ";
      component += sourceQuery;
      component += ")" 
    }else{
      component += "&fq=cat:(";
      component += dateQuery;
      component += ")" 
    }

//http://localhost:8983/solr/sport/select?json.wrf=JSON_CALLBACK&q=nba&start=0&rows=5&wt=json&facet.field=author&facet.date=created_at&f.created_at.facet.date.start=NOW-12MONTH/MONTH&f.created_at.facet.date.end=NOW%2B1MONTH/MONTH&f.created_at.facet.date.gap=%2B1MONTH&fq=cat:((created_at:[2014-03-20T08:34:22.776Z TO 2016-03-19T08:34:22.776Z]) AND (author:(NBA%20Central)))

    
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
      
      if(tickAll){
        $scope.sourceSelection = [];
        for(var i = 0;i < $scope.sources.length;i++){
          $scope.sourceSelection.push($scope.sources[i].name);
        }
        $scope.monthSelection = [];
        for(var i = 0;i < $scope.monthRecords.length;i++){
          $scope.monthSelection.push($scope.monthRecords[i].month);
        }
      }
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

    makeRequest(false);
  };

  $scope.next = function() {
    currPage = currPage + 1;
    $scope.currPage = currPage;
    $scope.preDisabled = false;
    if (currPage == 1) {
      $scope.nextDisabled = true;
    }

    makeRequest(false);

  };


  $scope.search = function() {
    $scope.preDisabled = true;
    $scope.nextDisabled = true;
    currPage = 1;

    keywords = $scope.keywords;

    makeRequest(true);
 
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
