# Tax Calculator

The aim of this project was to create a tax calculator designed specifically for IT contractors that would compare and contrast take home pay across different jurisdictions. 

IT contractors are highly paid, incredibly busy people who usually have no or little knowledge of tax law, and especially international tax law. Being a demographic who often are able to work remotely, they are often able to benefit from relocating. 

Tax law is complex and it can take a huge amount of research and knowledge for the lay person to understand it. Since tax is such a critical aspect in financial planning, this project aims to democratise tax knowledge so that the average IT contractor can see with a quick calculation how they will be affected by taxes in different jurisdictions. 

This calculator is of use to any IT contractor considering moving countries. It is also particularly useful to those in the UK, since certain tax matters are devolved which means that tax rates can be different in England, Wales, Scotland and Northern Ireland. This means that, for some residents who live near the borders, a simple house move to the next village can result in a drastically different tax bill. 

With an increasing tax burden, inflation and ever diminishing levels of service in the UK, it is likely that increasing numbers of contractors will consider a move abroad. The goal of this calculator is to allow them to see an indicative calculation of how a move would affect their take home pay, without them having to spend weeks investigating complex legal issues or spending thousands on tax advisers. In the event that they are seriously considering a move to another jurisdiction after seeing the indicative calculation, then they will be advised to seek personalised, specialist advice.

The tax calculator could be expanded in the future to be of use to a wider demographic than just IT contractors. However, because of the time limits involved I have selected IT contractors specifically to limit the scope of the project in order to allow me to create it to a high standard within the time permitted. The software architecture of this project has been designed with scalability/xxxx? In mind, to ensure that additional jurisdictions and demographics can be added easily.

## Users
The users of this site will be any IT contractor working outside IR35 and considering moving to another tax jurisdiction. The site may also be suitable for any other type of contractor working through a limited company in the same way.  

Finding accurate demographics for this group was not easy, and as this is a new application I have no existing business data to draw on. The most accurate data I found related to the IT contractor market in the USA, so it was not ideal, but it does give a clear view of the typical demographic: 
86.3% male, 13.7% female 
Average age is 42 years old
11% identified as LGBT 

Source: Information Technology Contractor Demographics and Statistics [2023]: Number Of Information Technology Contractors In The US (zippia.com)

Since IT contractors work through limited companies and have to submit various tax returns each year I would expect the users to be reasonably sophisticated users, possibly with multiple sources of income, and a reasonable understanding of tax language. I therefore did not define terms like ‘corporation tax’ as the average user of this site would more likely than not already be familiar with these terms. I do not have any data to test this assumption at this stage, as this is a totally new site that does not build on anything existing. As the site is used, data will be collected and if it appears that my assumptions are incorrect then the user experience can be tweaked to perfect it for less sophisticated users. For example the terms could be clarified in some additional notes. For the sake of a clean user experience those notes have not been included at this stage. 

Additionally, there will also be at least one admin user who will be able to log in and and new jurisdictions and update tax rates for existing jurisdictions. 

## User stories 

### As an IT contractor  I want to…..
- Be able to enter my income details in an easy-to understand way 
- See how much progress i am making while using the application 
- See a clear result that is accurate and easy to understand
- Be able to compare how much tax i would pay in multiple jurisdictions
- Be able to log in easily and securely 
- Be able to purchase………………

### As an admin user I want to….
- Be able to add a new country 
- Be able to delete a country
- Be able to update the tax rates for an existing country 
- Be able to log in easily and securely 

## Branding 
The aim of this site was to appear professional, accurate and trustworthy with good levels of contrast to satisfy optimal UX design. As a result the following colour scheme was used: 

(colours TBC!!!!)

As this is an entirely new site, I do not have any demographic data about the expected users. Once the site is in use data will be collected and demographic assumptions will be revised. The colour scheme could then be changed if it was felt necessary. 

## Complexities 
Tax ranges and limits are specified in the currency of the jurisdiction. This site is currently aimed at UK residents so will only take income in GBP for the time being. Since currencies change all the time, we will need to plug into a currency conversion site to get an up to date conversion, or manually enter the currency conversion rates but then they will go out of date quickly. We need to convert the GBP income into the currency of the jurisdiction (UAED, SD) and then convert it back to GBP using the same conversion rate after the calculation is done. So if we take a rate from a live site we will want to save that rate somewhere until the conversion back is completed, rather than using 2 different rates. 

The project is dependent upon the calculations being accurate. Therefore research was a critical aspect of this project and my legal background was very useful. With more time, more jurisdictions could be added to the calculator but as a one-person project I limited it to 6 jurisdictions to keep the scope of the project reasonable. The admin user will need to keep the information up to date for the calculator to continue to be accurate over time. 

## Additions with more time 
For this project I had to be very careful to keep the scope as tight as possible since there was a large amount of legal research, algorithms and architecture to carry out. With the limited time available, I had to prioritise. I architected the project in an agile way, to ensure that I could come back to it at a later date and add functionality as easily as possible. With more time, I would consider adding the following functionality:

With more time, I would add more jurisdictions with a view to including every jurisdiction across the globe. This would take a significant amount of research which would need to be kept up to date each year as tax regimes change across the globe. 

I would also add a feature to allow various elements to be ‘mixed and matched’: for example for a user to enter their company as being based in one country whilst they are based in another. This adds an additional layer of complexity as it involves the interplay of international, cross-jurisdictional tax laws.

I would collect data on users to ensure that my assumptions about who the users are likely to be are correct. If the data suggests that the user's profile is different than expected, the user experience can be tweaked to make it more suitable to the majority of users. For example, if users are less knowledgeable than expected then additional explanatory notes/pages can be added to explain the basic terms. 

A nice additional feature would be something along the lines of ‘Where will I be best off’. This feature would allow a user to enter their details - their income and its sources, and then tell them the top 3 jurisdictions where they would benefit from the maximum level of take home pay. 

Another addition would be to include pension information, including pension tax relief. This has not been included at this time because it requires an in-depth knowledge of pension tax law in each jurisdiction, and there simply wasn’t time to accurately include these additional complex algorithms and calculations. 

Clearly, getting the legal information accurate is a critical part of this project. Fortunately, I have a legal background so am accustomed to researching and deciphering complex legal problems. In an ideal world, this would be double checked by a specialist international tax lawyer from each jurisdiction. That has not been done yet, so a disclaimer has been included on each page. If the site becomes very popular, then that is an additional step that could be undertaken each year for an added level of certainty. 

Allow the site to be used in multiple currencies.

Ability to edit an existing calculation to add additional jurisdictions, rather than to have to start all over again if adding a new jurisdiction.

A function that says your total tax percentage of income is…….
A function where you can enter your income and it will return the most tax efficient place to live, or order them from best to worst 
A function to do: company is based in jurisdiction x, person is based in jurisdiction y
Broaden it out beyond just IT contractors 
Add more jurisdictions 
Add tax reliefs and allowances 
Add dividend allowance - skipped for now for UK 

## Working notes
### Conceptual summary of the problem:
The fundamental problem is that you need to gather info from the user and then apply a series of calculations to work out, based on that info, how the user will be taxed. The problem is that the structure of the calculations, and the calculations themselves, and the info on which they are based, varies from country to country. 

The forms will be different for each country - different questions for each country, and the calculations are going to be different for each country. so …. How do we come up with a piece of software that can gather the right info from the user for all of the countries, and then apply the right calculation for all of the countries. 

We will focus on IT contractors and then expand with more time. 

The problem is this: how do I get info from users when the info needed is dependent on the particular country and the calcularton needed is also dependent on the particular country?

I want to architect this in a way that means other countries can be added in the future without needing to change the software itself. This will make the project more extensible and future-proof, and is in line with the principles of Uncle Bob’s ‘Clean Code’ - reducing the time and expense needed to update the project in the future. 

Solution A = use a big if statement, with hard coded calculations for each country, and then the algorithm selects if country A, use set of rules B etc. But software engineers have to change it all every time a new country added, and it requires a release of code every time a new country is added because all of the logic is hard coded. Uncle Bob doesn’t like if statements! 
Solution B = extension. Create a software module for each country and each will have hard coded questions and answers. So each country would be like a plug in, so that doesn’t require a redeployment of code if changes made, but you need a software engineer to create a new plugin and maintain the logic for each country. 
Solution C: configuration. Come up with a generic algorithm that is data driven and store all of the knowledge in a database and have an algorithm that uses the knowledge in the database to work out what questions to ask and what calculations to apply. Benefit of this is that an admin user can update the database with a new country, and no software engineering is needed. This makes the project much more accessible, usable and updateable. Therefore this is the option I selected. The issue with this option is that if a new country has totally different tax rules than those in the existing database, then a software engineer would need to update the system. This option can lead a developer down a rabbit hole, trying to anticipate every single tax rule set that might possibly come up. But all tax systems I have studied so far have had similar rules, so this still remains the best option. In the event that a new country was added with drastically different rules, software engineering would be required to ensure the overall logic still worked.
This project is about striking a balance between ensuring the application is useful to the end user (IT contractors) whilst also being easily updatable by an admin user as far as that is reasonably practicable. There may be outlying cases where a software engineer would be required to add a new country, but I am limiting the scope where possible to minimise this risk.  

### Technical Decisions
When implementing DELETE methods on APIs, I had to decide whether to put filters in the HTTP request body or in the query string. After some research, the following article recommended putting the filters in the query string for DELETEs as request bodies are not widely supported for DELETE:
REST/HTTP - Should you use a body for your DELETE requests? (peterdaugaardrasmussen.com)
Initially I used ordinals to order the questions and rules, but I later decided to use linked lists instead. Linked lists allowed me to ………………………………………..
When loading objects out of the database using ordinals, there is no guarantee that the objects will be retrieved in the order of the ordinal, so then I would need to create a sorting function. 
With linked lists, the objects would be accessed in the correct sorted order, as the first object in the list will be accessed first and then from the first object the pointers control the order in which the subsequent objects are accessed. 

### Data models
Data lives in 2 places: first in the database when storing it and second in the computer’s memory, which is where the class structure comes in (class structure is the in memory representation of the data). So if you design your class structure you are automatically designing your database structure as well. Django will automatically create the DB structure from the model layer. 
Data domains:
Users: Stores information about the users, their password hashes, and their profiles
Forms: Stores information about the questions and types of answer that we will ask to the user in order to gather the information required as input to the tax calculator.
Rules: Stores the tax rules for different jurisdictions that are used to calculate tax based on the information given by the user.
Calculations: Stores the output of the calculations that are requested by the users.
Payments: Stores information about payments made by users, and outstanding payments.

### Class structure 
There are 3 main components that I need to solve the problem. For each country I need to get certain info from the user. 
Some Qs are generic, some are country specific. 
The first part of the problem is displaying the right Qs to the user, depending on what you need. 
UX: ask only the relevant Qs to the user for the country they are interested in. 
There will be 4 elements to the data model: 
1. So the system needs to know which Qs to ask to the user. So I’ll call this the ‘form building domain or component’. 
UX: need to consider the order of the Qs. it may not make sense to ask all the generic Qs followed by the country-specific ones. We may need to intersperse them. 
Have question sections, so the country-specific Qs can be asked in the correct section i.e. corporation tax, income tax etc. 
Specify the type of answer that the Q allows - that will determine what input type is needed for the answer
Validation rules need to be considered
Classes needed for form builder@
1. Section 
2. Question 
3. Answer template/validation 
Field type can be:
Currency 
Validation will be: 
must be a whole number, no commas etc
Min value/max value
Number
Validation will be:
Min value/max value
Boolean 
yes/no
Multiselect
Single select 


2. Once I've got the info I have to produce the calculations via a set of rules. So the second part of the problem is the rule building part of the problem. 
3. The user facing application is the third part.
Plug in to currency converter. Get conversion rate, store as variable so use same rate both ways. 
4. The country builder - the admin user will use this in combination with form builder and rule builder to add new countries etc. 

## Deployment

The live deployed application can be found at [Tax Calculator](https://contractor-tax-calculator.herokuapp.com/).

### Heroku

This project uses [Heroku](https://www.heroku.com), a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

Deployment steps are as follows, after account setup:

- Select *New* in the top-right corner of your Heroku Dashboard, and select *Create new app* from the dropdown menu.
- Your app name must be unique, and then choose a region closest to you (EU or USA), and finally, select *Create App*.
- From the new app *Settings*, click *Reveal Config Vars*, and set the following key/value pairs:
  - `IP` 0.0.0.0
  - `PORT` 5000
  - `MONGO_URI` mongodb+srv://service:MpWP0OA5n4AMQbop@catidentifier.1ncucur.mongodb.net/?retryWrites=true&w=majority. To get the `MONGO_URI`, follow the steps outlined in the `MongoDB` section below.
  - `API_BASE_URL` https://cat-identifier.herokuapp.com/api
  - `CONFIG_FILE` ./config/config.production.json
  - `DATABASE_URL` postgres://ckqznidqkqgwsd:ee305d223a8b55f882c85661ee97a51edebf35f2dbbe67e69f3ee945a0dcfd17@ec2-46-51-187-237.eu-west-1.compute.amazonaws.com:5432/decv568a62lsdl. To get the `DATABASE_URL`, follow the steps outlined in the `Postgres DB` section below.
  - `DEBUG` False
  - `MONGO_DB` cat_identifier_db
  - `MONGO_PREDICTION_MODELS` prediction_models
  - `MONGO_PREDICTIONS` predictions
  - `MONGO_TRAINING_IMAGES` training_images
  - `MONGO_TRAINING_LOG` training_log_entries
  - `MONGO_USERS` users
  - `REDIS_URL` redis://:p8c4e2560b7ef8b787c0ff47764b61e7bf661c867be93323b0a1b98c36f775ace@ec2-52-19-136-205.eu-west-1.compute.amazonaws.com:10839. To get the `REDIS_URL`, follow the steps outlined in the `Redis` section below.
  - `SECRET_KEY` AYdrcRATjKGYa3LGGxvcm2nZ913DNTyC

Heroku needs two additional files in order to deploy properly.
- requirements.txt
- Procfile

You can install this project's requirements (where applicable) using: `pip3 install -r requirements.txt`. If you have your own packages that have been installed, then the requirements file needs updated using: `pip3 freeze --local > requirements.txt`

The Procfile can be created with the following command: `echo -e web: python app.py\nworker: celery -A worker.celery worker > Procfile`

For Heroku deployment, follow these steps to connect your GitHub repository to the newly created app:

Either:
- Connect Heroku and GitHub.
- Then select "Automatic Deployment" from the Heroku app.
- Click the _Deploy Branch_ button.

Or:
- In the Terminal/CLI, connect to Heroku using this command: `heroku login -i`
- Set the remote for Heroku: `heroku git:remote -a cat-identifier`
- After performing the standard Git `add`, `commit`, and `push` to GitHub, you can now type: `git push heroku main`

The frontend terminal should now be connected and deployed to Heroku.

### ElephantSQL DB

This project uses ElephantSQL DB as the relational database for the application's data warehouse.

Deployment steps to create the Postgres DB in Heroku are as follows:

- From your Heroku dashboard, select the `cat-identifier` app.
- Select the *Resources* tab at the top.
- Under the *Add-ons* section, search for `Postgres` and select *Heroku Postgres* from the drop-down box.
- Leave the *Plan name* as `Hobby Dev - Free` and click *Submit Order Form*.
- Heroku will automatically create the `DATABASE_URL` key and value in the config settings.

### Local Deployment

*Gitpod* IDE was used to write the code for this project.

To make a local copy of this repository, you can clone the project by typing the follow into your IDE terminal:
- `git clone https://github.com/Laura10101/cat-identifier.git`

You can install this project's requirements (where applicable) using: `pip3 install -r requirements.txt`.

Create an `env.py` file, and add the following environment variables:

```python
import os


```

Alternatively, if using Gitpod, you can click below to create your own workspace using this repository.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Laura10101/cat-identifier)

## Credits

### Educational Resources
- Uncle Bob’s Clean Code 
- Government tax websites/legal resources 
- Canva pallet picker (with colours amended by me)
- Book on architecture principles/guidelines
- [Django Best Practices: Projects vs Apps | LearnDjango.com](https://learndjango.com/tutorials/django-best-practices-projects-vs-apps)
- [Django Stripe Subscriptions | TestDriven.io](https://testdriven.io/blog/django-stripe-subscriptions/)
- [Strategy (refactoring.guru)](https://refactoring.guru/design-patterns/strategy)
- [Serializing Django objects | Django documentation | Django (djangoproject.com)](https://docs.djangoproject.com/en/4.1/topics/serialization/)
- [Convert Queryset To Json In Django (letscodemore.com)](https://www.letscodemore.com/blog/convert-queryset-to-json-in-django/)
- [URL dispatcher | Django documentation | Django (djangoproject.com)](https://docs.djangoproject.com/en/4.2/topics/http/urls/)
- [How to read JSON data in an HTTP POST request in Django | by Sampath Surineni | Medium](https://medium.com/@sampathkumar/how-to-read-json-data-in-an-http-post-request-in-django-d29fd6dae6b4)
- [python - How to disable Django's CSRF validation? - Stack Overflow](https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation)
- [REST/HTTP - Should you use a body for your DELETE requests? (peterdaugaardrasmussen.com)](https://peterdaugaardrasmussen.com/2020/11/14/rest-should-you-use-a-body-for-your-http-delete-requests/)
- [(2) How to delete multiple objects in django? : djangolearning (reddit.com)](https://www.reddit.com/r/djangolearning/comments/uq66mz/how_to_delete_multiple_objects_in_django/)
- [Getting query params from request in Django - https://pythoncircle.com](https://pythoncircle.com/post/710/getting-query-params-from-request-in-django/)
- [Python String split() Method (w3schools.com)](https://www.w3schools.com/python/ref_string_split.asp)
- [Making queries | Django documentation | Django (djangoproject.com)](https://docs.djangoproject.com/en/4.2/topics/db/queries/#the-pk-lookup-shortcut)
- [Model Inheritance In Python Django (buildatscale.tech)](https://buildatscale.tech/model-inheritance-in-django/)
- [Modeling Polymorphism in Django With Python – Real Python](https://realpython.com/modeling-polymorphism-django-python/#abstract-base-model)
- [Quickstart — django-polymorphic 3.1 documentation](https://django-polymorphic.readthedocs.io/en/stable/quickstart.html)
- [Getting query params from request in Django - https://pythoncircle.com](https://pythoncircle.com/post/710/getting-query-params-from-request-in-django/)
- [python 2.7 - How to return HTTP 400 response in Django? - Stack Overflow](https://stackoverflow.com/questions/23492000/how-to-return-http-400-response-in-django)
- [Http Delete request to django returns a 301(Moved permenantly)_django_Mangs-DevPress官方社区 (csdn.net)](https://devpress.csdn.net/python/6304bd0ac67703293080dc2d.html)
- [Add Months to datetime Object in Python - GeeksforGeeks](https://www.geeksforgeeks.org/add-months-to-datetime-object-in-python/)
- [python - how to get request object in django unit testing? - Stack Overflow](https://stackoverflow.com/questions/10277748/how-to-get-request-object-in-django-unit-testing)
- [Advanced testing topics | Django documentation | Django (djangoproject.com)](https://docs.djangoproject.com/en/4.2/topics/testing/advanced/)
- [How to write and report assertions in tests — pytest documentation](https://docs.pytest.org/en/7.1.x/how-to/assert.html)
- [Django helpers — pytest-django documentation](https://pytest-django.readthedocs.io/en/latest/helpers.html)
- [Python: Fastest — Convert list of integers to comma separated string | by Akshay Chavan | Medium](https://arccoder.medium.com/python-fastest-convert-list-of-integers-to-comma-separated-string-7818494ab8f6)
- [Use incoming webhooks to get real-time updates | Stripe Documentation](https://stripe.com/docs/webhooks)
- [Stripe API Reference - The event object](https://stripe.com/docs/api/events/object)
- [How intents work | Stripe Documentation](https://stripe.com/docs/payments/intents#intent-statuses)
- [Stripe API Reference - The PaymentIntent object](https://stripe.com/docs/api/payment_intents/object)
- [Stripe Documentation - Create Payment Method](https://stripe.com/docs/js/payment_methods/create_payment_method)