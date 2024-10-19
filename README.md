# Crowdfunding Back End

Lisa Todesco

## Planning:

### Concept/Name

Champs in the Making
Empower Tomorrow's Champions: Fund Dreams for Disadvantaged Kids with Champs in the Making!
Champs in the Making is a dynamic crowdfunding platform dedicated to transforming the lives of disadvantaged children. Our mission is to bridge the gap between need and opportunity by empowering individuals and organizations to raise funds for essential projects that support these young champions.

### Intended Audience/User Stories

Non-profit Organizations: Groups dedicated to children's welfare, education, and health can use the platform to raise funds for specific projects and initiatives.
Community Groups: Local organizations looking to address immediate needs, such as food, clothing, and educational resources for children in their area.
Individuals: Concerned citizens or advocates who wish to launch personal campaigns to support children in need, whether through fundraising events or specific projects.
Donors and Supporters: Individuals and businesses looking to contribute to meaningful causes and make a tangible impact on the lives of disadvantaged children.

### Front End Pages/Functionality

- {{ A page on the front end }}
  - {{ A list of dot-points showing functionality is available on this page }}
  - {{ etc }}
  - {{ etc }}
- {{ A second page available on the front end }}
  - {{ Another list of dot-points showing functionality }}
  - {{ etc }F

### API Spec

format table with option + shift F
| URL | HTTP Method | Purpose | Request Body | Success Response Code | Authentication/Authorisation |
| -------------------------- | ----------- | ------------------------ | ------------ | --------------------- | ---------------------------- |
| http://127.0.0.1/pledges/ | GET | Returns all the pledges | N/A | 200 | N/A |
| http://127.0.0.1/projects/ | GET | Returns all the projects | N/A | 200 | N/A |
| http://127.0.0.1:8000/users/ | GET | Returns all the users | N/A | 200 | N/A |
| 


As a User you're not allowed to create a new crowdfunding project unless you're logged in
As a User you're not allowed to pledge to a project unless you're logged in
As a User you're not allowed to modify the details of a project unless you're the one who created it

### DB Schema

![]( {{ ./relative/path/to/your/schema/image.png }} )

## Project Requirements

Your crowdfunding project must:

- [ ] Be separated into two distinct projects: an API built using the Django Rest Framework and a website built using React.
- [ ] Have a cool name, bonus points if it includes a pun and/or missing vowels. See https://namelix.com/ for inspiration. <sup><sup>(Bonus Points are meaningless)</sup></sup>
- [ ] Have a clear target audience.
- [ ] Have user accounts. A user should have at least the following attributes:
  - [ ] Username
  - [ ] Email address
  - [ ] Password
- [ ] Ability to create a “project” to be crowdfunded which will include at least the following attributes:
  - [ ] Title
  - [ ] Owner (a user)
  - [ ] Description
  - [ ] Image
  - [ ] Target amount to fundraise
  - [ ] Whether it is currently open to accepting new supporters or not
  - [ ] When the project was created
- [ ] Ability to “pledge” to a project. A pledge should include at least the following attributes:
  - [ ] An amount
  - [ ] The project the pledge is for
  - [ ] The supporter/user (i.e. who created the pledge)
  - [ ] Whether the pledge is anonymous or not
  - [ ] A comment to go along with the pledge
- [ ] Implement suitable update/delete functionality, e.g. should a project owner be allowed to update a project description?
- [ ] Implement suitable permissions, e.g. who is allowed to delete a pledge?
- [ ] Return the relevant status codes for both successful and unsuccessful requests to the API.
- [ ] Handle failed requests gracefully (e.g. you should have a custom 404 page rather than the default error page).
- [ ] Use Token Authentication, including an endpoint to obtain a token along with the current user's details.
- [ ] Implement responsive design.

## Additional Notes

Check off each item when done:

- [ ] A link to the deployed project.
- [ ] A screenshot of Insomnia, demonstrating a successful GET method for any endpoint.
- [ ] A screenshot of Insomnia, demonstrating a successful POST method for any endpoint.
- [ ] A screenshot of Insomnia, demonstrating a token being returned.
- [ ] Step by step instructions for how to register a new user and create a new project (i.e. endpoints and body data).
- [ ] Your refined API specification and Database Schema.
