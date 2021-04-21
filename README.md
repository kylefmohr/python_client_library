DeathByCaptcha API Clients
==========================

Introduction
------------

DeathByCaptcha offers APIs of two types — HTTP and socket-based, with the latter being recommended for having faster responses and overall better performance. Switching between different APIs is usually as easy as changing the client class and/or package name, the interface stays the same.

When using the socket API, please make sure that outgoing TCP traffic to *api.dbcapi.me* to the ports range *8123–8130* is not blocked on your side.

How to Use DBC API Clients
--------------------------

### Thread-safety notes

*Python* client are thread-safe, means it is perfectly fine to share a client between multiple threads (although in a heavily multithreaded applications it is a better idea to keep a pool of clients).

### Common Clients' Interface

All the clients have to be instantiated with two string arguments: your DeathByCaptcha account's *username* and *password*.

All the clients provide a few methods to handle your CAPTCHAs and your DBC account. Below you will find those methods' short summary summary and signatures in pseudo-code. Check the example scripts and the clients' source code for more details.

#### Upload()

Uploads a CAPTCHA to the DBC service for solving, returns uploaded CAPTCHA details on success, `NULL` otherwise. Here are the signatures in pseudo-code:

`dict deathbycaptcha.Client.upload(file imageFile)`

`dict deathbycaptcha.Client.upload(str imageFileName)`

#### GetCaptcha()

Fetches uploaded CAPTCHA details, returns `NULL` on failures.

`dict deathbycaptcha.Client.get_captcha(dict imageFileName)`

#### Report()

Reports incorrectly solved CAPTCHA for refund, returns `true` on success, `false` otherwise.

Please make sure the CAPTCHA you're reporting was in fact incorrectly solved, do not just report them thoughtlessly, or else you'll be flagged as abuser and banned.

`bool deathbycaptcha.Client.report(int captchaId)`

#### Decode()

This method uploads a CAPTCHA, then polls for its status until it's solved or times out; returns solved CAPTCHA details on success, `NULL` otherwise.

`dict deathbycaptcha.Client.decode(file imageFile, int timeout)`

`dict deathbycaptcha.Client.decode(str imageFileName, int timeout)`

#### GetBalance()

Fetches your current DBC credit balance (in US cents).

`float deathbycaptcha.Client.get_balance()`

### CAPTCHA objects/details hashes

Use simple hashes (dictionaries, associative arrays etc.) to store CAPTCHA details, keeping numeric IDs under `"captcha"` key, CAPTCHA text under `"text"` key, and the correctness flag under `"is_correct"` key.

### Examples

Below you can find a few DBC API client' usage examples.
```python
import deathbycaptcha

# Put your DBC account username and password here.
# Use deathbycaptcha.HttpClient for HTTP API.
client = deathbycaptcha.SocketClient(username, password)
try:
    balance = client.get_balance()

    # Put your CAPTCHA file name or file-like object, and optional
    # solving timeout (in seconds) here:
    captcha = client.decode(captcha_file_name, timeout)
    if captcha:
        # The CAPTCHA was solved; captcha["captcha"] item holds its
        # numeric ID, and captcha["text"] item its text.
        print "CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"])

        if ...:  # check if the CAPTCHA was incorrectly solved
            client.report(captcha["captcha"])
except deathbycaptcha.AccessDeniedException:
    # Access to DBC API denied, check your credentials and/or balance
```


New Recaptcha API support
=========================

What's "new reCAPTCHA/noCAPTCHA"?
---------------------------------

They're new reCAPTCHA challenges that typically require the user to identify and click on certain images. They're not to be confused with traditional word/number reCAPTCHAs (those have no images).

For your convinience, we implemented support for New Recaptcha API. If your software works with it, and supports minimal configuration, you should be able to decode captchas using New Recaptcha API in no time.

We provide two different types of New Recaptcha API:

-   **Coordinates API**: Provided a screenshot, the API returns a group of coordinates to click.
-   **Image Group API**: Provided a group of (base64-encoded) images, the API returns the indexes of the images to click.

Coordinates API FAQ:
--------------------

What's the **Coordinates API URL**?  
To use the **Coordinates API** you will have to send a HTTP POST Request to http://api.dbcapi.me/api/captcha

What are the POST parameters for the **Coordinates API**?  

-   **username**: Your DBC account username
-   **password**: Your DBC account password
-   **captchafile**: a Base64 encoded or Multipart file contents with a valid New Recaptcha screenshot
-   **type=2**: Type 2 specifies this is a New Recaptcha **Coordinates API**

What's the response from the **Coordinates API**?  
**captcha**: id of the provided captcha, if the **text** field is null, you will have to pool the url http://api.dbcapi.me/api/captcha/**captcha\_id** until it becomes available

**is\_correct**:(0 or 1) specifying if the captcha was marked as incorrect or unreadable

**text**: a json-like nested list, with all the coordinates (x, y) to click relative to the image, for example:

                  [[23.21, 82.11]]
              

where the X coordinate is 23.21 and the Y coordinate is 82.11

****

Image Group API FAQ:
--------------------

What's the **Image Group API URL**?  
To use the **Image Group API** you will have to send a HTTP POST Request to http://api.dbcapi.me/api/captcha

What are the POST parameters for the **Image Group API**?  

-   **username**: Your DBC account username
-   **password**: Your DBC account password
-   **captchafile**: the Base64 encoded file contents with a valid New Recaptcha screenshot. You must send each image in a single "captchafile" parameter. The order you send them matters
-   **banner**: the Base64 encoded banner image (the example image that appears on the upper right)
-   **banner\_text**: the banner text (the text that appears on the upper left)
-   **type=3**: Type 3 specifies this is a New Recaptcha **Image Group API**
-   **grid**: Optional grid parameter specifies what grid individual images in captcha are aligned to (string, width+"x"+height, Ex.: "2x4", if images aligned to 4 rows with 2 images in each. If not supplied, dbc will attempt to autodetect the grid.

What's the response from the **Image Group API**?  
**captcha**: id of the provided captcha, if the **text** field is null, you will have to pool the url http://api.dbcapi.me/api/captcha/**captcha\_id** until it becomes available

**is\_correct**:(0 or 1) specifying if the captcha was marked as incorrect or unreadable

**text**: a json-like list of the index for each image that should be clicked. for example:

                  [1, 4, 6]
              

where the images that should be clicked are the first, the fourth and the six, counting from left to right and up to bottom

**Examples**

#### Recaptcha Coordinates API

```python
import deathbycaptcha

# Put your DBC account username and password here.
username = "user"  
password = "password"
captcha_file = 'test.jpg' # image

client = deathbycaptcha.SocketClient(username, password) 
# to use http client use: client = deathbycaptcha.HttpClient(username, password)


try:
  balance = client.get_balance()

  # Put your CAPTCHA file name or file-like object, and optional
  # solving timeout (in seconds) here:
  captcha = client.decode(captcha_file, type=2)
  if captcha:
      # The CAPTCHA was solved; captcha["captcha"] item holds its
      # numeric ID, and captcha["text"] item its list of "coordinates".
      print "CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"])

      if '':  # check if the CAPTCHA was incorrectly solved
          client.report(captcha["captcha"])
except deathbycaptcha.AccessDeniedException:
  # Access to DBC API denied, check your credentials and/or balance
  print "error: Access to DBC API denied, check your credentials and/or balance"
```

                  

#### Recaptcha Image Group

```python
import deathbycaptcha

# Put your DBC account username and password here.
username = "user"  
password = "password"
captcha_file = "test2.jpg"  # image
banner = "banner.jpg"  # image banner
banner_text = "select all pizza:"

#client = deathbycaptcha.SocketClient(username, password) 
client = deathbycaptcha.HttpClient(username, password)
# to use http client use: client = deathbycaptcha.HttpClient(username, password)


try:
  balance = client.get_balance()

  # Put your CAPTCHA file name or file-like object, and optional
  # solving timeout (in seconds) here:
  captcha = client.decode(
      captcha_file, type=3, banner=banner, banner_text=banner_text)
  #you can supply optional `grid` argument to decode() call, with a 
  #string like 3x3 or 2x4, defining what grid individual images were located at
  #example: 
  #captcha = client.decode(
  #    captcha_file, type=3, banner=banner, banner_text=banner_text, grid="2x4")
  #see 2x4.png example image to have an idea what that images look like
  #If you wont supply `grid` argument, dbc will attempt to autodetect the grid
  if captcha:
      # The CAPTCHA was solved; captcha["captcha"] item holds its
      # numeric ID, and captcha["text"] is a json-like list of the index for each image that should be clicked.
      print("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"])) 

      if '':  # check if the CAPTCHA was incorrectly solved
          client.report(captcha["captcha"])
except deathbycaptcha.AccessDeniedException:
  # Access to DBC API denied, check your credentials and/or balance
  print("error: Access to DBC API denied, check your credentials and/or balance")
```

