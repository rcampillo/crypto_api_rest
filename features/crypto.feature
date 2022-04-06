Feature: Test QA requirements

Background:
	Given I set required REST API url

Scenario: GET server time
  Given I Set GET posts api endpoint "/0/public/Time"
  When Send GET HTTP request
  Then I receive valid HTTP response code 200 for "GET"
	And Response BODY "GET" is non-empty

Scenario: GET pair value to BITCOIN/USD default behavior
  Given I Set GET posts api endpoint "/0/public/AssetPairs?pair=XXBTZUSD"
  When Send GET HTTP request
  Then I receive valid HTTP response code 200 for "GET"
	And Response BODY "GET" is non-empty

Scenario: GET pair value to BITCOIN/USD info leverage behavior
  Given I Set GET posts api endpoint "/0/public/AssetPairs?pair=XXBTZUSD&info=leverage"
  When Send GET HTTP request
  Then I receive valid HTTP response code 200 for "GET"
	And Response BODY "GET" is non-empty

Scenario: GET pair value to BITCOIN/USD info fees behavior
  Given I Set GET posts api endpoint "/0/public/AssetPairs?pair=XXBTZUSD&info=fees"
  When Send GET HTTP request
  Then I receive valid HTTP response code 200 for "GET"
	And Response BODY "GET" is non-empty

Scenario: GET pair value to BITCOIN/USD info margin behavior
  Given I Set GET posts api endpoint "/0/public/AssetPairs?pair=XXBTZUSD&info=margin"
  When Send GET HTTP request
  Then I receive valid HTTP response code 200 for "GET"
	And Response BODY "GET" is non-empty

Scenario: GET pair value to BITCOIN/USD info not valid value behavior
  Given I Set GET posts api endpoint "/0/public/AssetPairs?pair=XXBTZUSD&info=wrong"
  When Send GET HTTP request
  Then I receive valid HTTP response code 200 for "GET"
	And Response BODY "GET" is non-empty
	And Response ERROR "GET" is non-empty

Scenario: GET open positions to rcampillo user
  Given I Set GET posts api endpoint "/0/private/OpenOrders"
  When Send POST HTTP request once rcampillo auth has been set
  Then I receive valid HTTP response code 200 for "GET"
	And Response BODY "GET" is non-empty