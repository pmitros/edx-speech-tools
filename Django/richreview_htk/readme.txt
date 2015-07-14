richreview_htk: Contains the master files for the Django site.

force_alignment: Contains the Django files to setup the force_alignment part of the website, which is denoted by 127.0.0.1/force_alignment. NOTE: You will need to change the P2FA directory in views.py to show the program where your P2FA files are located (more about this in the pyforcealign/htk_instructions file).

speech2text: Contains the Django files to setup the speech2text part of the website, which is denoted by 127.0.0.1/speech2text.

pyforcealign: A Python module containing the force alignment methods. You will need some command-line tools to use this module; see the htk_instructions file for more about how to get this working.

py_s2t: The files necessary to get Bluemix working. You can follow the instructions at https://github.com/watson-developer-cloud/text-to-speech-python to configure the Bluemix credentials appropriately. py_s2t requires Flask.

utilities: Right now, only contains a method format_access which will enable the front end to receive the server's responses. Modify the string constant in the access_control.py file as needed to reflect the location of the frontend app.