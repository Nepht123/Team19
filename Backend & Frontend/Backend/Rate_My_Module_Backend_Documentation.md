# Rate My Module — Backend Integration Documentation

**For:** Backend Engineers  
**Project:** Rate My Module — UWC Student Module Review Platform  
**Prepared from:** Frontend prototype (HTML/CSS/JS)  
**Purpose:** This document explains what every page does, what data it needs, and exactly what API endpoints and data structures the backend must provide.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Page Map & Navigation Flow](#2-page-map--navigation-flow)
3. [Authentication System](#3-authentication-system)
4. [Page-by-Page Breakdown](#4-page-by-page-breakdown)
   - [home.html — Homepage](#41-homehtmlhomepage)
   - [login_create.html — Login & Registration](#42-login_createhtml--login--registration)
   - [by_program.html — Programme Listing](#43-by_programhtml--programme-listing)
   - [by_program_modules.html — Module Listing](#44-by_program_moduleshtml--module-listing)
   - [module_page.html — Module Reviews](#45-module_pagehtml--module-reviews)
5. [CSS & Styling Notes](#5-css--styling-notes)
6. [Complete Data Models](#6-complete-data-models)
7. [Required API Endpoints Summary](#7-required-api-endpoints-summary)
8. [URL Parameter Reference](#8-url-parameter-reference)
9. [Security Notes](#9-security-notes)

---

## 1. Project Overview

**Rate My Module** is a web platform for UWC (University of the Western Cape) students to read and submit reviews on their academic modules.

The current frontend is a working **static prototype** — all data is hardcoded in JavaScript. Your job as the backend team is to replace this hardcoded data with real API calls, a real database, and a real authentication system.

**Tech stack (frontend):**
- HTML5, CSS3, vanilla JavaScript
- Bootstrap 5.3 (layout & components)
- Font Awesome 6.4 (icons)
- No frontend framework (no React, Vue, etc.)

---

## 2. Page Map & Navigation Flow

```
home.html
│
├── (Categories dropdown / Faculty cards)
│       └── by_program.html?faculty={key}
│               └── by_program_modules.html?program={name}
│                       └── module_page.html?code={moduleCode}
│
└── login_create.html
        └── (After login → redirects back to home.html)
```

Every page links back to `home.html`. Navigation is done via plain HTML anchor tags and `history.back()` in JavaScript — no client-side router is used.

---

## 3. Authentication System

### Current state (prototype)
Authentication is **fully simulated** in the frontend. A red/green toggle button on each page lets developers switch between "Logged Out" and "Logged In" states without a real session.

### What the backend needs to implement

The frontend expects a **session-based or token-based authentication system**. Once implemented, the frontend will check whether the user is logged in on page load (e.g., by calling a `/api/auth/me` endpoint or reading a session cookie).

**Logged-out behaviour the frontend already handles:**
- The navbar shows a "Log In" button linking to `login_create.html`
- The "Write a Review" button is disabled and shows a lock icon
- Clicking "Write a Review" fires a `alert()` telling the user to log in

**Logged-in behaviour the frontend already handles:**
- The navbar "Log In" button changes to an "AI Guide" link
- The "Write a Review" button becomes active
- The review submission form can be submitted

### Recommended auth endpoint

```
GET /api/auth/me
Response (logged in):  { "loggedIn": true,  "studentNumber": "4123456" }
Response (logged out): { "loggedIn": false }
```

The frontend can call this on page load and replace the `userIsLoggedIn` / `isLoggedIn` boolean.

---

## 4. Page-by-Page Breakdown

---

### 4.1 `home.html` — Homepage

**What it does:** The landing page. Shows a search bar, a faculty browse grid, and the main navbar.

#### Navbar Auth Toggle

The navbar contains a dev-only toggle button (`#devAuthToggle`) that simulates login state. In production, remove this button and replace its logic with a real session check.

**Relevant DOM elements:**

| Element ID         | What it does                                         |
|--------------------|------------------------------------------------------|
| `devAuthToggle`    | Dev-only toggle. Remove in production.              |
| `authActionButton` | "Log In" button that becomes "AI Guide" when logged in |

**Current JS logic (to be replaced):**
```javascript
// This is the current simulation — replace with a real API call
let userIsLoggedIn = false;

function updateNavbarState() {
    if (userIsLoggedIn) {
        authActionButton.href = "AI_carear_page.html"; // Note: typo in filename
        authActionButton.textContent = "AI Guide";
    } else {
        authActionButton.href = "login_create.html";
        authActionButton.textContent = "Log In";
    }
}
```

**What the backend needs to support:** An endpoint to check session state (see Section 3).

---

#### Module Search Bar

The search bar currently has **no backend connection**. It is a visible UI element that is not yet wired up.

```html
<form class="input-group ...">
    <input type="text" placeholder="Search for a module (e.g., COS101, MAT105)...">
    <button type="submit">Search</button>
</form>
```

**Required API endpoint:**

```
GET /api/modules/search?q={searchTerm}

Response:
[
  {
    "code": "CSC111",
    "name": "Introduction to Computer Science",
    "faculty": "science",
    "program": "BSc Computer Science"
  },
  ...
]
```

The frontend should then navigate to `module_page.html?code={code}` for the selected result.

---

#### Faculty Browse Grid

Seven faculty cards are hardcoded in the HTML. Each links to `by_program.html?faculty={key}`.

**Faculty keys used:**

| URL Key      | Display Name                       |
|--------------|------------------------------------|
| `arts`       | Arts and Humanities                |
| `chs`        | Community & Health Sciences        |
| `dentistry`  | Dentistry                          |
| `ems`        | Economic & Management Sciences     |
| `education`  | Education                          |
| `law`        | Law                                |
| `science`    | Natural Sciences                   |

These keys are used as URL query parameters and as lookup keys in the JS data objects on `by_program.html`. **The backend should use the same keys** when providing faculty data.

---

### 4.2 `login_create.html` — Login & Registration

**What it does:** A three-state card: a gateway (choose login or register), a login form, and a registration form. JavaScript switches between them by toggling CSS `d-none` classes.

#### States

| State             | Visible element ID    | Default visibility |
|-------------------|-----------------------|--------------------|
| Gateway           | `gatewaySection`      | Visible            |
| Login form        | `loginFormSection`    | Hidden             |
| Register form     | `registerFormSection` | Hidden             |

State is controlled by two JS functions:
- `showForm('login')` or `showForm('register')` — shows the chosen form
- `resetGateway()` — returns to the gateway

No page reload occurs; these functions just toggle Bootstrap's `d-none` class.

---

#### Login Form

```html
<form action="#" method="POST">
    <input type="text" id="loginStudentNumber" pattern="\d{7}" required>
    <input type="password" id="loginPassword" required>
    <button type="submit">Log In</button>
</form>
```

**What the form sends:**

| Field               | HTML ID               | Type     | Validation             |
|---------------------|-----------------------|----------|------------------------|
| Student Number      | `loginStudentNumber`  | `text`   | Exactly 7 digits       |
| Password            | `loginPassword`       | `password` | Required             |

**Required API endpoint:**

```
POST /api/auth/login
Content-Type: application/json

Request body:
{
  "studentNumber": "4123456",
  "password": "UserPassword1!"
}

Response (success, 200):
{
  "success": true,
  "studentNumber": "4123456"
}

Response (failure, 401):
{
  "success": false,
  "error": "Invalid credentials"
}
```

After a successful login, redirect the user to `home.html`.

---

#### Registration Form

```html
<form action="#" method="POST">
    <input id="regStudentNumber" pattern="\d{7}" required>
    <input id="regEmailPrefix" pattern="\d{7}" required>    <!-- appended with @myuwc.ac.za -->
    <input id="regPassword" pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[...]).{8,}$" required>
    <input id="programmeSearchInput" list="programmesOptions"> <!-- optional -->
    <select id="regYear"> <!-- optional --> </select>
</form>
```

**What the form sends:**

| Field           | HTML ID               | Required | Notes                                                          |
|-----------------|-----------------------|----------|----------------------------------------------------------------|
| Student Number  | `regStudentNumber`    | Yes      | Exactly 7 digits                                               |
| Email prefix    | `regEmailPrefix`      | Yes      | 7 digits; backend appends `@myuwc.ac.za` to form the full address |
| Password        | `regPassword`         | Yes      | Min 8 chars, must contain uppercase, lowercase, number, symbol |
| Programme       | `programmeSearchInput`| No       | Free text with datalist suggestions                            |
| Year of Study   | `regYear`             | No       | Values: `1`, `2`, `3`, `4`, `postgrad`                        |

**Password validation regex (applied in HTML `pattern` attribute):**
```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+=\[{\]};:<>|./?,-]).{8,}$
```
Apply this same validation server-side.

**Programme datalist (currently hardcoded in JS):**
```javascript
const flatProgrammesList = [
    "BCom General", "BCom Accounting", "BCom Information Systems",
    "Bachelor of Administration", "BA General", "Bachelor of Laws (LLB)",
    "BA Psychology", "BSc General", "BSc Computer Science",
    "BSc Biotechnology", "BSc Chemical Sciences"
];
```
This list should come from the backend so it stays up to date.

**Required API endpoints:**

```
POST /api/auth/register
Content-Type: application/json

Request body:
{
  "studentNumber": "4123456",
  "email": "4123456@myuwc.ac.za",
  "password": "SecurePass1!",
  "programme": "BSc Computer Science",   // optional, may be null
  "yearOfStudy": "2"                      // optional, may be null
}

Response (success, 201):
{ "success": true }

Response (failure, 409):
{ "success": false, "error": "Student number already registered" }
```

```
GET /api/programmes
Response:
["BCom General", "BCom Accounting", "BSc Computer Science", ...]
```

---

### 4.3 `by_program.html` — Programme Listing

**What it does:** Displays a list of degree programmes for a selected faculty. Has a live search filter.

#### URL Parameter

```
by_program.html?faculty=science
```

The `faculty` query parameter is read with `new URLSearchParams(window.location.search)` and used to look up the faculty's programmes.

#### Current hardcoded data (to be replaced)

```javascript
const facultyData = {
    arts:       { title: "Arts and Humanities",            programmes: ["BA General", ...] },
    chs:        { title: "Community & Health Sciences",    programmes: [...] },
    dentistry:  { title: "Dentistry",                      programmes: [...] },
    ems:        { title: "Economic & Management Sciences", programmes: [...] },
    education:  { title: "Education",                      programmes: [...] },
    law:        { title: "Law",                            programmes: [...] },
    science:    { title: "Natural Sciences",               programmes: [...] }
};
```

#### Required API endpoint

```
GET /api/faculties/{facultyKey}/programmes
Example: GET /api/faculties/science/programmes

Response:
{
  "facultyKey": "science",
  "title": "Natural Sciences",
  "programmes": [
    "BSc Computer Science",
    "BSc Mathematics",
    "BSc Physics",
    "BSc Biotechnology",
    "BSc Environmental Water Science"
  ]
}
```

#### How the page renders cards

The JS function `renderProgrammes(array)` loops through the programmes array and builds a card for each one. The "View Modules" button on each card links to:

```
by_program_modules.html?program={encodeURIComponent(programmeName)}
```

The programme name is URL-encoded (e.g., `BSc%20Computer%20Science`). The backend must return programme names that exactly match the keys used in the modules endpoint (see Section 4.4).

#### Live search filter

The search input (`#searchInput`) filters the displayed cards in real time using JavaScript — **this is entirely client-side and requires no API call**.

---

### 4.4 `by_program_modules.html` — Module Listing

**What it does:** Shows all modules for a specific degree programme. Each module links to its review page.

#### URL Parameter

```
by_program_modules.html?program=BSc%20Computer%20Science
```

The programme name is decoded from the URL and used to look up the module list.

#### Current hardcoded data (to be replaced)

```javascript
const programModulesData = {
    "BSc Computer Science": [
        { code: "CSC111", name: "Introduction to Computer Science", year: "1st Year", credits: "15 Credits" },
        { code: "MAT111", name: "Mathematics for Computer Science", year: "1st Year", credits: "15 Credits" },
        // ...
    ],
    "BCom Accounting": [ ... ],
    // ... other programmes
};
```

If the programme name does not match any key in the object, a generic fallback list of 3 placeholder modules is shown.

#### Required API endpoint

```
GET /api/programmes/{programmeName}/modules
Example: GET /api/programmes/BSc%20Computer%20Science/modules

Response:
[
  {
    "code": "CSC111",
    "name": "Introduction to Computer Science",
    "year": "1st Year",
    "credits": "15 Credits"
  },
  {
    "code": "MAT111",
    "name": "Mathematics for Computer Science",
    "year": "1st Year",
    "credits": "15 Credits"
  }
]
```

#### How the page renders cards

The JS function `renderModules(array)` loops through the modules and builds a card for each. The "View Reviews" button links to:

```
module_page.html?code={encodeURIComponent(mod.code)}
```

#### Fallback behaviour

When the URL has no `?program=` parameter, the page currently flattens **all** programmes into one list. The backend may choose to handle this edge case with a `GET /api/modules` endpoint returning all modules, or simply require a programme name to always be present.

---

### 4.5 `module_page.html` — Module Reviews

**What it does:** The most complex page. It displays module details, aggregated rating statistics, and individual student reviews. Logged-in users can submit new reviews.

#### URL Parameter

```
module_page.html?code=CSC111
```

Defaults to `CSC111` if no code is provided.

---

#### Module Details (Sidebar)

The page reads module metadata and populates these DOM elements:

| Element ID         | What it shows              |
|--------------------|----------------------------|
| `moduleCodeBadge`  | Module code (e.g., CSC111) |
| `moduleNameTitle`  | Full module name           |
| `modCreditsYear`   | Credits and year level     |
| `modPrereqs`       | Prerequisites              |
| `modCoreqs`        | Corequisites               |

**Current hardcoded data:**
```javascript
const mockModuleDatabase = {
    "CSC111": { name: "Introduction to Computer Science", credits: "15 Credits", year: "1st Year", prereqs: "None", coreqs: "MAT111" },
    "MAT111": { name: "Mathematics for Computer Science", credits: "15 Credits", year: "1st Year", prereqs: "Grade 12 Mathematics", coreqs: "None" },
    "CSC211": { name: "Data Structures and Algorithms",   credits: "20 Credits", year: "2nd Year", prereqs: "CSC111",              coreqs: "None" }
};
```

**Required API endpoint:**

```
GET /api/modules/{moduleCode}
Example: GET /api/modules/CSC111

Response:
{
  "code": "CSC111",
  "name": "Introduction to Computer Science",
  "credits": "15 Credits",
  "year": "1st Year",
  "prereqs": "None",
  "coreqs": "MAT111"
}
```

---

#### Reviews List

**Current hardcoded data (3 sample reviews):**
```javascript
let reviewDataset = [
    {
        user:       "Anonymous Student",
        date:       "Oct 12, 2025",
        difficulty: 8,    // Score out of 10
        teaching:   7,    // Score out of 10
        content:    9,    // Score out of 10
        pros:       "The coursework is very well structured...",
        cons:       "The workload ramps up very quickly...",
        advice:     "Make sure you attend all the practical sessions..."
    },
    // ...
];
```

**Required API endpoint:**

```
GET /api/modules/{moduleCode}/reviews
Example: GET /api/modules/CSC111/reviews

Response:
[
  {
    "id": 1,
    "studentNumber": "Anonymous",
    "date": "Oct 12, 2025",
    "difficulty": 8,
    "teaching": 7,
    "content": 9,
    "pros": "The coursework is very well structured...",
    "cons": "The workload ramps up very quickly...",
    "advice": "Make sure you attend all the practical sessions..."
  }
]
```

> **Note on anonymity:** The current frontend displays `"Anonymous Student"` or `"Jane Doe"` etc. The backend should decide the anonymity policy. One option: always display `"Verified Student"` and never expose the real student number on the frontend.

---

#### Rating Calculation (done in JavaScript)

The frontend calculates all ratings from the raw scores. You do **not** need to store pre-computed averages — the frontend does this math itself. However, for performance at scale, you may want to cache these on the backend.

**How the star rating is calculated:**
```javascript
// Each review has 3 scores out of 10
const localTenPointAvg = (difficulty + teaching + content) / 3;
const localFiveStarRating = localTenPointAvg / 2;  // Convert to /5

// Overall rating = average of all reviews' 5-star ratings
```

**Sidebar statistics (also calculated in JS):**
- `avgDifficulty` = sum of all `difficulty` values / number of reviews
- `avgTeaching` = sum of all `teaching` values / number of reviews
- `avgContent` = sum of all `content` values / number of reviews
- Progress bars are set with `width: ${value * 10}%` (so a score of 7/10 = 70% width)

---

#### Review Submission Form (Modal)

A Bootstrap modal (`#reviewModal`) contains the review form. It is only accessible to logged-in users.

**Form fields:**

| Field        | Element ID        | Type     | Values                          |
|--------------|-------------------|----------|---------------------------------|
| Difficulty   | `inputDifficulty` | `select` | Integer 1–10                    |
| Teaching     | `inputTeaching`   | `select` | Integer 1–10                    |
| Content      | `inputContent`    | `select` | Integer 1–10                    |
| Pros         | `inputPros`       | `textarea`| Free text, required            |
| Cons         | `inputCons`       | `textarea`| Free text, required            |
| Advice       | `inputAdvice`     | `textarea`| Free text, required            |

**Current frontend behaviour on submit:**
1. Checks `isLoggedIn` — if false, shows an alert and stops.
2. Reads all 6 field values.
3. Creates a new review object and adds it to the top of the `reviewDataset` array with `unshift()`.
4. Re-renders all review cards and recalculates averages.
5. Resets the form and closes the modal.

> This means the new review currently only persists in memory (it disappears on page refresh). The backend must persist it.

**Required API endpoint:**

```
POST /api/modules/{moduleCode}/reviews
Authorization: Bearer {token}  (or session cookie)
Content-Type: application/json

Request body:
{
  "difficulty": 7,
  "teaching": 8,
  "content": 9,
  "pros": "Great practical sessions.",
  "cons": "Workload is heavy.",
  "advice": "Start assignments early."
}

Response (success, 201):
{
  "success": true,
  "review": {
    "id": 4,
    "studentNumber": "Anonymous",
    "date": "Jun 26, 2026",
    "difficulty": 7,
    "teaching": 8,
    "content": 9,
    "pros": "Great practical sessions.",
    "cons": "Workload is heavy.",
    "advice": "Start assignments early."
  }
}

Response (failure — not authenticated, 401):
{ "success": false, "error": "Not authenticated" }

Response (failure — already reviewed, 409):
{ "success": false, "error": "You have already reviewed this module" }
```

---

## 5. CSS & Styling Notes

All custom styles live in `home.css`. Most pages either link to this file or duplicate a small subset of the styles inline.

**Brand colours (do not change these):**

| Token         | Hex       | Usage                                |
|---------------|-----------|--------------------------------------|
| Navy          | `#002147` | Primary colour — headers, buttons, text |
| Gold          | `#FFC72C` | Accent — search button, card top borders |
| Dark navy hover | `#001630` | Navy button hover state             |
| Dark gold hover | `#E5B325` | Gold button hover state             |

**Key CSS classes:**

| Class                 | Where used      | What it does                                               |
|-----------------------|-----------------|------------------------------------------------------------|
| `.bg-navy`            | All pages       | Navy background                                            |
| `.btn-navy`           | All pages       | Navy button with white text                                |
| `.btn-gold`           | `home.html`     | Gold search button                                         |
| `.custom-faculty-card`| `home.html`     | Card with gold top border, lifts on hover                  |
| `.custom-pattern-bg`  | Home, login     | Light grey background with subtle SVG dot pattern          |
| `.login-card`         | `login_create`  | Card with gold top border                                  |
| `.programme-card`     | `by_program`    | Card with left border that turns gold on hover             |
| `.module-card`        | `by_program_modules` | Same as programme-card, also lifts slightly on hover  |
| `.review-card`        | `module_page`   | Card with left border that turns navy on hover             |
| `.micro-progress`     | `module_page`   | Small 6px progress bar for per-review score bars           |

---

## 6. Complete Data Models

### User
```json
{
  "studentNumber": "4123456",
  "email": "4123456@myuwc.ac.za",
  "password": "(hashed)",
  "programme": "BSc Computer Science",
  "yearOfStudy": "2"
}
```

### Faculty
```json
{
  "key": "science",
  "title": "Natural Sciences",
  "programmes": ["BSc Computer Science", "BSc Mathematics"]
}
```

### Programme
```json
{
  "name": "BSc Computer Science",
  "facultyKey": "science",
  "modules": ["CSC111", "MAT111", "CSC211"]
}
```

### Module
```json
{
  "code": "CSC111",
  "name": "Introduction to Computer Science",
  "credits": "15 Credits",
  "year": "1st Year",
  "prereqs": "None",
  "coreqs": "MAT111",
  "programme": "BSc Computer Science",
  "facultyKey": "science"
}
```

### Review
```json
{
  "id": 1,
  "moduleCode": "CSC111",
  "studentNumber": "4123456",
  "date": "Oct 12, 2025",
  "difficulty": 8,
  "teaching": 7,
  "content": 9,
  "pros": "The coursework is very well structured.",
  "cons": "The workload ramps up quickly.",
  "advice": "Attend all practical sessions."
}
```

---

## 7. Required API Endpoints Summary

| Method | Endpoint                                       | Auth Required | Description                              |
|--------|------------------------------------------------|---------------|------------------------------------------|
| `GET`  | `/api/auth/me`                                 | No            | Check current session / login status     |
| `POST` | `/api/auth/login`                              | No            | Log in with student number + password    |
| `POST` | `/api/auth/register`                           | No            | Register a new student account           |
| `POST` | `/api/auth/logout`                             | Yes           | End session                              |
| `GET`  | `/api/programmes`                              | No            | List all programme names (for datalist)  |
| `GET`  | `/api/faculties/{facultyKey}/programmes`       | No            | Get programmes for a faculty             |
| `GET`  | `/api/programmes/{programmeName}/modules`      | No            | Get modules for a programme              |
| `GET`  | `/api/modules/{moduleCode}`                    | No            | Get details for a single module          |
| `GET`  | `/api/modules/{moduleCode}/reviews`            | No            | Get all reviews for a module             |
| `POST` | `/api/modules/{moduleCode}/reviews`            | Yes           | Submit a new review for a module         |
| `GET`  | `/api/modules/search?q={term}`                 | No            | Search modules by name or code           |

---

## 8. URL Parameter Reference

All page-to-page data is passed through URL query parameters.

| Page                     | Parameter   | Example Value            | Where it comes from                         |
|--------------------------|-------------|--------------------------|---------------------------------------------|
| `by_program.html`        | `faculty`   | `science`                | Hardcoded in faculty card links             |
| `by_program_modules.html`| `program`   | `BSc Computer Science`   | Programme name from `by_program.html` card  |
| `module_page.html`       | `code`      | `CSC111`                 | Module code from `by_program_modules.html` card |

All parameter values are URL-encoded using `encodeURIComponent()` and decoded using `new URLSearchParams(window.location.search).get('key')`.

---

## 9. Security Notes

The following items in the frontend prototype must be handled carefully by the backend:

**1. Dev auth toggle buttons must be removed in production.**  
Both `home.html` (`#devAuthToggle`) and `module_page.html` (`#authSimulateToggle`) contain buttons that fake a logged-in state. These must be removed before the site goes live.

**2. Review submission must be validated server-side.**  
The frontend checks `isLoggedIn` before allowing form submission, but a malicious user can bypass this with a direct API call. The backend must verify the session on every `POST /api/modules/{code}/reviews` request.

**3. Student number is used as both a username and email prefix.**  
The registration form constructs the email as `{studentNumber}@myuwc.ac.za`. The backend should validate that the student number is a real, registered UWC student number if that data is available.

**4. Scores are integers 1–10.**  
The frontend sends numeric scores from `<select>` dropdowns. The backend should validate that these are integers within the 1–10 range before saving.

**5. One review per student per module.**  
The frontend does not enforce this (prototype limitation). The backend must enforce it at the database level with a unique constraint on `(studentNumber, moduleCode)`.

**6. Password requirements must be enforced server-side.**  
The HTML `pattern` attribute only validates in the browser. Apply the same password strength rules in your API:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

---

*End of documentation.*  
*Generated from frontend prototype files: `home.html`, `login_create.html`, `by_program.html`, `by_program_modules.html`, `module_page.html`, `home.css`.*
