## Implementation

#### Designing API

First thing we should do before making any assumptions about the API is to draw simple processes for our User interacting with the application. For this purpose we will use [BPMN Viewer and Editor](https://bpmn.io/).

![diagram](diagram.svg)

I'm not good at BPMN diagrams but this should be good enough to use as a high-level overview of the domain.

As far as I'm concerned, there are at least two ways to design an API. First one is simply mapping database entities as CRUD resources using HTTP verbs (POST, GET, PUT, DELETE). But [RESTful web services shouldn't be that way](https://hackernoon.com/process-driven-rest-api-design-75ca88917582). Here is the example how that API could look like:

```
# Users - `users`
POST /users/ { first_name: 'John', last_name: 'Smith', date_of_birth: '1989-11-27' }
GET /users/?limit=20&start=0
PUT /users/1 { first_name: 'Bob', last_name: 'Smith', date_of_birth: '1982-11-27' }
DELETE /users/1

# User addresses - `user_addresses`
POST /users/1/addresses/ { address: '681 Gainsway Street, Canandaigua, NY 14424' }
GET /users/1/addresses/?limit=20&start=0
PUT /users/1/addresses/1 { address: '363 SE. Beech Avenue, Whitestone, NY 11357' }
DELETE /users/1/addresses/1

# etc for `user_phones`, `user_emails`...
```

Second approach is a little bit more complicated since it requires you to actually think about users consuming your API. As we can see from the BPMN diagram, it seems we can design our API to be a little bit more efficient in terms of network usage. Instead of making additional requests for getting every type of user detail (phones, emails, addresses), we can create endpoint for getting initial user list:

```
GET /users/details/?limit=20&start=41
```

As an example response we'll get 20 users with all necessary details.

```json
{
    "meta": {
      "total-pages": 5
    },
    "users": [
      {
        "id": 1,
        "first_name": "John",
        "last_name": "Smith",
        "date_of_birth": "1982-11-28",
        "link": {
          "rel": "self",
          "href": "http://api.example.com/user/1"
        },
        "addresses": [
          {
            "id": 1,
            "address": "681 Gainsway Street, Canandaigua, NY 14424",
            "link": {
              "rel": "self",
              "href": "http://api.example.com/user/1/address/1"
            }
          }
        ],
        "phones": [
          {
            "id": 1,
            "phone": "+12025550160",
            "link": {
              "rel": "self",
              "href": "http://api.example.com/user/1/phones/1"
            }
          }
        ],
        "emails": [
          {
            "id": 1,
            "email": "john.smith@example.com",
            "link": {
              "rel": "self",
              "href": "http://api.example.com/user/1/emails/1"
            }
          }
        ]
      },
      ...
    ],
    "links": {
      "self": "http://api.example.com/users/details/?limit=20&start=41",
      "first": "http://api.example.com/users/details/?limit=20&start=1",
      "prev": "http://api.example.com/users/details/?limit=20&start=21",
      "next": "http://api.example.com/users/details/?limit=20&start=61",
      "last": "http://api.example.com/users/details/?limit=20&start=81"
    }
}
```


The client app could cache the query results and allow user to edit and probably search records even if network is too slow or completely offline.

The next use case is creating a new Person:

```
POST /users/ { first_name: 'John', last_name: 'Smith', date_of_birth: '1989-11-27', email: 'john.smith@example.com', phone: '+12025550160' }
```

Application requirements mention that **Person could contain one or more emails and one or more phone numbers**. That means we must create `user`, `user_phones`, and `user_emails` records in a single request. Simply mapping our database scheme to CRUD operations would not make much sense in this case. Fortunately, Resources in REST API could be anything we would like &mdash; like getting traffic directions from Seattle to San Francisco (`GET /directions/?from=Seattle&to=SanFrancisco`), generate random numbers (`GET /random/?min=1&max=100`), etc.
 
In this case, we have simply added two more required fields: `email` and `phone`. Behind the scenes, our API would create `user`, `user_phones`, and `user_emails` records. Thereby, client app developer doesn't even need to think about relations in our database. He doesn't have to write code to make 3 subsequent requests, and we have also saved bandwidth and reduced overall complexity for our API.

#### TDD approach for creating Django API

At first, we can focus on creating Postgres tables and getting basic CRUD operations in place.