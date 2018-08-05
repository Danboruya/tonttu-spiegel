# Project Tonttu Spiegel

## Description
This project create smart mirror. Display current time, current weather and temperature.
In addition, you can ask mirror with google assistant built-in commands. 

## Requirements
This project require following environments
 
|Environment|Version|
|:---------:|:-----:|
| Python | 3.5.x or later |
| Google assistant sdk | 0.5.0 later |
| Google cloud Text-to-Speech | 0.2.0 or later |
| Google API client python | 1.7.4 |

Another required software

|Software|
|:------:|
| mpg321 |

## How to use
This application main program separate by 2 python file.
First one is used for running server. Another one is used for Google assistant program.  
First, you run the server following command.  
`python ./app.py`  
Then, you also run google assistant application with following command.  
`python ./application.py --project_id YOUR-PROJECT-ID --device_model_id YOURE-DVICE-MODEL-ID`   
After successful launch, access `localhost:8080/`. You can see some information that current time, current weather,
current weather and current temperature. 
 

## License
This software is released under the Apache License 2.0, see LICENSE.

## Author
[Danboruya](https://github.com/Danboruya)
