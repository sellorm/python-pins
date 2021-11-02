# pins

A simple package to pin and retrieve pinned data from RStudio Connect.

Read more about pins on the [offical R implementation's website](https://pins.rstudio.com)

This project is **not affiliated** with RStudio.

## v1.0 Pins API

This package currently only supports one operation with the official pins 1.0 API,
Reading a pinned csv from RStudio Connect.

The legacy API for this package is still available. See below for more details.

### Reading a pin on RStudio Connect

import the appropriate sub-module.

```
import pins.connect as pins
```

Then use the `pin_read()` function to read csv data pinned to Connect directly into a pandas dataframe.

```
pins.pin_read("<CONNECT_SERVER_URL>", "<CONNECT_API_KEY>", "<USER_NAME/PIN_NAME>")
```

Alternatively, you can return a dict of the pin metadata, by using the `meta_only=True` parameter.

For instance:

```
>>> pins.pin_read("https://connect.example.com.rstudio.com/rsc", 
... os.getenv("CONNECT_API_KEY"), 
... "mark.sellors/palmer_penguins",
... meta_only=True)
{'file': 'palmer_penguins.csv', 'file_size': '17299', 
'pin_hash': '809e9def88e78114', 'type': 'csv',
'title': "'palmer_penguins: a pinned 344 x 8 data frame'",
'description': '~', 'created': '20211029T120018Z', 'api_version': '1.0'}
```

Here's a complete example:

```
>>> import os
>>> import pins.connect as pins
>>> pins.pin_read("https://colorado.rstudio.com/rsc", 
... os.getenv("COLORADO_API_KEY"), "mark.sellors/palmer_penguins")
       species     island  bill_length_mm  ...  body_mass_g     sex  year
0       Adelie  Torgersen            39.1  ...       3750.0    male  2007
1       Adelie  Torgersen            39.5  ...       3800.0  female  2007
2       Adelie  Torgersen            40.3  ...       3250.0  female  2007
3       Adelie  Torgersen             NaN  ...          NaN     NaN  2007
4       Adelie  Torgersen            36.7  ...       3450.0  female  2007
..         ...        ...             ...  ...          ...     ...   ...
339  Chinstrap      Dream            55.8  ...       4000.0    male  2009
340  Chinstrap      Dream            43.5  ...       3400.0  female  2009
341  Chinstrap      Dream            49.6  ...       3775.0    male  2009
342  Chinstrap      Dream            50.8  ...       4100.0    male  2009
343  Chinstrap      Dream            50.2  ...       3775.0  female  2009

[344 rows x 8 columns]
>>> 
```

## Legacy functions

This functionality is deprecated and will be removed in a future version.
Please move to the v1.0 functionality if possible.

### Make a pin on RStudio Connect.

```
pin_rsconnect(data, pin_name, pretty_pin_name, connect_server, api_key)
```
  
Parameters:

* data: any object that has a to_json method (eg. pandas DataFrame)
* pin_name (str): name of pin, only alphanumeric and underscores
* pretty_pin_name (str): display name of pin
* connect_server (str): RStudio Connect server address e.g. https://connect.example.com/
* api_key (str): API key of a user on RStudio Connect
      
Returns:

* Url of content
  

### Get data from a python pin on RStudio Connect

```
pin_get_rsconnect(url, api_key):
```

Parameters:

* url (str) content solo URL on Connect (NOT dashboard URL)
* api_key (str): API key of a user on RStudio Connect
      
Returns:

* JSON version of pin


## Try it out

```
import panads
import pins

mydata = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=mydata)

# pin the data to connect
pin = pins.pin_rsconnect(
    data = df, 
    pin_name = "my_pin_7788", 
    pretty_pin_name = "Python Pin", 
    connect_server = connect_server, 
    api_key = api_key
)

# retrieve the pinned data
pins.pin_get_rsconnect(pin['content_url'], api_key = api_key)
```

## License

This package is released under an MIT license and was created by Alex Gold and Mark Sellors.

"RStudio" and "RStudio Connect" are trademarks of [RStudio, PBC](https://rstudio.com).

