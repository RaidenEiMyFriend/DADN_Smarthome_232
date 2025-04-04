## Demo

[!Watch Demo on YouTube](https://www.youtube.com/watch?v=YOUR_VIDEO_ID](https://www.youtube.com/watch?app=desktop&v=XVBzWnVjq7s&feature=youtu.be)




## Installation

#### Clone this repository
#### Run redis server 
#### Client
  ```bash
  cd client-adafruit 
  npm install
  npm start
  ```
#### Server
  1. Move to folder server
  ```bash
  cd server
  ```
  2. Create a virtual enviroment and activate it
  ```bash
  python -m venv env
  source env/bin/activate
  ```
  3. Install the required package
  ```bash
  pip install -r requirements.txt
  ```
  4. Create a `.env` file
  ```bash
  GOOGLE_APPLICATION_CREDENTIALS = path_to_file_config_json
  ADAFRUIT_IO_USERNAME = your_user_io
  ADAFRUIT_IO_KEY = your_key_io
  ```
  5. Run
  ```bash
  python manage.py runserver
  ```
