This folder was originally downloaded from:
https://www.waveshare.net/w/upload/9/95/STServo_Python.zip
It includes Feet ST3215 servo SDK.
The files I wrote is in folder: my_py
st_sync_read.py is used to read 6 servo at one time.
st_adjust_pos.py is used to adjust position range.
Usage: 
stservo-env\Scripts\activate.bat
python st_sync_read.py
python st_adjust_pos.py
I have adjusted all the position ranges without break point. Next step is to setup highest current, after that, we can start coding.

leader arm
Servo No.	Start	End	total position number
1	3716	1378	2338
2	1117	3496	2379
3	2288	95	2383
4	3730	5741	2011
5	6737	2926	3811
6	3188	4342	1154
<img width="321" height="169" alt="image" src="https://github.com/user-attachments/assets/77e817d8-0cd1-49e2-b381-dc51e80f7255" />

follower arm
Servo No.	Start	End	total position number
1	3314	603	2711
2	1260	3619	2359
3	4075	1874	2201
4	973	2959	1986
5	3839	36	3803
6	1809	3248	1439
<img width="321" height="169" alt="image" src="https://github.com/user-attachments/assets/0a4b4dd5-1a40-45d3-a40b-5e3a34893a93" />


