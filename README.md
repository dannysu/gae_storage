# About
This is a simple app that allows storing data on Google App Engine's datastore and also allows versioning of data.

# Usage
- To retrieve the latest version of the data you're storing, do a HTTP GET to `http://your_subdomain.appspot.com/whatever_you_want`

- To write data to storage and increment the version number, do a HTTP POST to the same URL as GET `http://your_subdomain.appspot.com/whatever_you_want` with the POST body being the data you want to store.