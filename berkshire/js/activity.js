(function() {

  var app = angular.module('activity', []);

  app.controller('LogisticsController', function() {
    this.lodging = lodging;
  });

  app.controller('OptionController', function() {
    this.inputGroups = inputGroups;
    this.hello = [1, 2, 3, 4, 5];
  });

  var inputGroups = [
    {
      'inputId': 'shortDesc',
      'label': 'Short description'
    },
    {
      'inputId': 'airbnbLink',
      'label': 'AirBnb link'
    },
    {
      'inputId': 'travelTime',
      'label': 'Travel time to Sugarbush'
    },
    {
      'inputId': 'totalCost',
      'label': 'Total cost of stay'
    },
    {
      'inputId': 'numOfBedrooms',
      'label': '# of bedrooms'
    },
    {
      'inputId': 'notes',
      'label': 'Notes'
    }
  ];

  var lodging = {
    'headers': [
      'AirBnb link',
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