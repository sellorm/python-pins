# pins

A simple package to pin and retrieve pinned data from RStudio Connect.

Read more about pins on the [offical R implementation's website](https://pins.rstudio.com)

This project is **not affiliated** with RStudio.


## Available functions

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

