    Caller project


        #### solution to 'coding-task.txt' ####

        NOTE:I have implemented both global search by phone and name.
         
        INSTRUCTIONS to run:


        1.download all requirements listed in requirements.txt
        2.install postgres database if not installed
        3.create a database and edit the 'DATABASE' property in 'settings.base.py'
        4.python manage.py makemigrations
        5.python manage.py migrate
        6.python manage.py runserver

        7.Create dummy users and multiple contacts as mentioned above
        8.Go to 'api_usage' folder and follow instructions to use API

*******************************************************************************************************************        
      
        COMMANDS to add dummy_data

        1.Add dummy user

        python manage.py dummy_user <username> <name> <password> <email>

        ex:python manage.py dummy_user "9995477921" "sunil23" "sunil1234" "sunilpie@sunil.com"

            
        2. Add multiple dummy phone_numbers to phone directory at once

        python manage.py dummy_contacts <contacts>

        ex:python manage.py dummy_contacts "2222222222" "3333333333" "4444444444" "5555555555"

            
        3. Adds multiple phone no's to spam.If phone no exists,increase spam score

        python manage.py add_to_spam <contacts>

        python manage.py add_to_spam "4444444444" "5555555555"

    
********************************************************************************************************************