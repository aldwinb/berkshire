(function() {

  var app = angular.module('activity', []);

  app.controller('LogisticsController', function() {
    this.lodging = lodging;
  });

  var lodging = {
    'headers': [
      'Link to AirBnb',
      'Travel time to Sugarbush',
      'Cost per person',
      'Number of bedrooms',
      'Notes',
      'Ranking (by votes)'
    ],
    'candidates': [
      {
        'shortDesc': 'PERFECT 4BD/2BTH-SKI/WEDDINGS/FAMILY RETREAT',
        'airbnbLink': 'https://www.airbnb.com/rooms/750405?guests=8&adults=7&children=1&location=Warren%2C%20%2C%20VT&check_in=2018-01-12&check_out=2018-01-15&s=PuqjTh9-',
        'travelTime': '15 mins',
        'cost': 1126,
        'numOfBedrooms': 4,
        'notes': '',
        'ranking': ''
      },
      {
        'shortDesc': 'Farmhouse Minutes to Sugarbush!',
        'airbnbLink': 'https://www.airbnb.com/rooms/4571714?guests=8&adults=7&children=1&location=Warren%2C%20%2C%20VT&check_in=2018-01-12&check_out=2018-01-15&s=PuqjTh9-',
        'travelTime': '15 mins',
        'cost': 1261,
        'numOfBedrooms': 5,
        'notes': '',
        'ranking': ''
      },
    ]
  };

})();