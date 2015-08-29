How to set up the study
=======================

This Django server includes almost everything you need to run our quantitative study of online audio collaboration (in conjuction with the JavaScript web app, of course). In addition to the files stored here, I am also hosting the audio files for the stimuli as *static files* in the `richreview_htk` directory. So to make the web app work correctly and load the stimuli, you should follow these steps:

1. Copy the stimuli, in "Formal" and "Informal" directories, into a folder named "static" inside `Django/richreview_htk/richreview_htk`.

2. In the terminal, navigate to the `Django/richreview_htk` directory and type `python manage.py collectstatic`. This should produce a "static" directory inside the main `Django/richreview_htk` that also contains an "admin" directory.

3. To run the server, type `python manage.py runserver --nostatic`.

Thanks!