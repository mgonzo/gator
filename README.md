# Gator
Tests are run with `py.test`

Gator is a Craigslist screen scraper to aggregate results from all US sites into a Sqlite database. I've got a coupld of big ticket items that I need to sell and thought it would be great if I could easily get a data from across all states. Of course, there's a couple of websites that do this already, but I liked the idea of stuffing the results into a db file and being able to interact with it in different ways.

TODO:
Currently, the only command available is 'gator fetch', which retrieves the results and stores them in db/gator.db. When I get time, I'd like to add some commands for generating reports from the db. Probably gonna need some updates to the schema as well for storing results from multiple searches easily.

