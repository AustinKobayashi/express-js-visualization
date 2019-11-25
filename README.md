# Running the Project

`
$ python <SERAPH>
`

# Express.js Visualization Tool

### What is the software engineering task you are facilitating with your analysis/visualisation?

We are designing a visualization tool for web developers to easily see what routes a code base supports and the respective handlers for those routes. For example, an onboarding software engineer might not know exactly what get, post, put, and delete requests a backend supports, so our tool can mitigate this problem by providing a visual layout of the backend's routes and route handlers


### What is the visualisation you are providing? Provide a sketch.


### What are the kinds of analysis that you are using to produce the visualisation?

We will be doing static syntactic analysis on the codebase to produce the graph.


### Who is doing which part? Everyone must own either a visualisation or analysis piece.

- Andrew: Finding which files the routers are in. Including request body. Made the video
- Nick:   Identifying which routes are supported, "/profile", "/account", etc..
- Jose:   Identifying what the handler is for a route
- Austin: Identifying any other classes / functions that may be accessed by the route handler
- Seraph: Drawing the graph


### What user studies do you have planned, and for when?

**Study 1:**<br>
We tasked our user with creating a POST request to add a user to the database and creating a GET request to check if the user was properly added. The user was provided only the server codebase. Our study showed that the user spent a while reading through the code before beginning to create the requests. They had to look at each file to ensure that they knew where every method was. While writing the requests, they often switched back to the code to ensure that the requests were properly formatted.

**Study 2:**<br>
We tasked our user with creating the following HTTP requests:

- Create a post request for a sign-up form
- Create a get requests to check if the user was added
- Create a post request to send a msg to the user
- Create a delete request to remove the user from the database

The user was provided with the codebase, as well as the graph generated by our visualization tool. We found that the user was able to complete the task with just the graph, but had difficulty with request bodies since they are not explicitly show in the graph. We fine tuned the visualization tool with the results of the study to clearly show the request variables for each route
