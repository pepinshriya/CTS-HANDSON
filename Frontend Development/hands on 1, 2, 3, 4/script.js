// ===============================
// Import Course Data
// ===============================

import { courses } from "./data.js";

let displayedCourses = [...courses];

// ===============================
// ES6 Destructuring
// ===============================

for (const course of courses) {

    const { name, credits } = course;

    console.log(name, credits);

}

// ===============================
// map()
// ===============================

const formattedCourses = courses.map(

    ({ code, name, credits }) =>

        `${code} — ${name} (${credits} credits)`

);

console.log(formattedCourses);

// ===============================
// filter()
// ===============================

const highCreditCourses = courses.filter(

    course => course.credits >= 4

);

console.log(highCreditCourses);

console.log("Courses >= 4 credits :", highCreditCourses.length);

// ===============================
// reduce()
// ===============================

const totalCredits = courses.reduce(

    (sum, course) => sum + course.credits,

    0

);

console.log("Total Credits :", totalCredits);

// ===============================
// DOM Elements
// ===============================

const courseGrid =
    document.querySelector(".course-grid");

const totalCreditsText =
    document.querySelector("#total-credits");

const selectedCourse =
    document.querySelector("#selected-course");

const searchInput =
    document.querySelector("#search-courses");

const sortButton =
    document.querySelector("#sort-btn");

const loading =
    document.querySelector("#loading");

const spinner =
    document.querySelector("#spinner");

const notificationList =
    document.querySelector("#notification-list");

const retryButton =
    document.querySelector("#retry-btn");

// ===============================
// Render Courses
// ===============================

function renderCourses(courseArray) {

    courseGrid.innerHTML = "";

    const fragment =
        document.createDocumentFragment();

    courseArray.forEach(course => {

        const article =
            document.createElement("article");

        article.className = "course-card";

        article.dataset.id = course.id;

        article.innerHTML = `

            <h3>${course.name}</h3>

            <p><strong>Code :</strong> ${course.code}</p>

            <p><strong>Credits :</strong> ${course.credits}</p>

        `;

        fragment.appendChild(article);

    });

    courseGrid.appendChild(fragment);

    const total =
        courseArray.reduce(

            (sum, course) => sum + course.credits,

            0

        );

    totalCreditsText.textContent =
        `Total Credits : ${total}`;

}

// ===============================
// Search
// ===============================

searchInput.addEventListener("input", event => {

    const keyword =
        event.target.value.toLowerCase();

    displayedCourses = courses.filter(course =>

        course.name
            .toLowerCase()
            .includes(keyword)

    );

    renderCourses(displayedCourses);

});

// ===============================
// Sort
// ===============================

sortButton.addEventListener("click", () => {

    displayedCourses.sort(

        (a, b) => b.credits - a.credits

    );

    renderCourses(displayedCourses);

});

// ===============================
// Event Delegation
// ===============================

courseGrid.addEventListener("click", event => {

    const card =
        event.target.closest(".course-card");

    if (!card) return;

    const id =
        Number(card.dataset.id);

    const course =
        courses.find(c => c.id === id);

    selectedCourse.textContent =
        `Selected Course : ${course.name} | Grade : ${course.grade}`;

});

// ===============================
// Promise Example
// ===============================

function fetchUser(id) {

    return fetch(

        `https://jsonplaceholder.typicode.com/users/${id}`

    )

        .then(response => response.json())

        .then(user => {

            console.log(user.name);

            return user;

        });

}

// ===============================
// Async/Await Example
// ===============================

async function fetchUserAsync(id) {

    try {

        const response =
            await fetch(

                `https://jsonplaceholder.typicode.com/users/${id}`

            );

        const user =
            await response.json();

        console.log(user.name);

    }

    catch (error) {

        console.error(error);

    }

}

// Call Examples

fetchUser(1);

fetchUserAsync(2);

// ===============================
// Simulated Network Delay
// ===============================

function fetchAllCourses() {

    return new Promise(resolve => {

        setTimeout(() => {

            resolve(courses);

        }, 1000);

    });

}

// Loading Indicator

loading.style.display = "block";

fetchAllCourses()

    .then(data => {

        loading.style.display = "none";

        renderCourses(data);

    });

// ===============================
// Promise.all()
// ===============================

Promise.all([

    fetchUser(1),

    fetchUser(2)

]).then(users => {

    console.log(

        users[0].name,

        users[1].name

    );

});
// ======================================
// Step 50 - Reusable Fetch Function
// ======================================

async function apiFetch(url) {

    const response = await fetch(url);

    if (!response.ok) {

        throw new Error(`HTTP Error : ${response.status}`);

    }

    return await response.json();

}

// ======================================
// Step 51 & 52
// Load Notifications
// ======================================

async function loadNotifications() {

    spinner.style.display = "block";

    retryButton.style.display = "none";

    notificationList.innerHTML = "";

    try {

        const posts = await apiFetch(
            "https://jsonplaceholder.typicode.com/posts"
        );

        posts.slice(0, 5).forEach(post => {

            const article =
                document.createElement("article");

            article.className = "notification-card";

            article.innerHTML = `

                <h3>${post.title}</h3>

                <p>${post.body}</p>

            `;

            notificationList.appendChild(article);

        });

    }

    catch (error) {

        notificationList.innerHTML = `

            <p style="color:red;">
                Unable to load notifications.
            </p>

        `;

        retryButton.style.display = "inline-block";

    }

    finally {

        spinner.style.display = "none";

    }

}

loadNotifications();


// ======================================
// Step 53
// Simulate 404 Error
// (Uncomment only for testing)
// ======================================

// apiFetch(
// "https://jsonplaceholder.typicode.com/nonexistent"
// );


// ======================================
// Step 54
// Retry Button
// ======================================

retryButton.addEventListener("click", () => {

    loadNotifications();

});


// ======================================
// Step 55
// Axios CDN is already added in index.html
// ======================================


// ======================================
// Step 56
// Axios apiFetch()
// ======================================

async function apiFetchAxios(url) {

    const response = await axios.get(url);

    return response.data;

}


// ======================================
// Step 57
// Axios Params
// ======================================

async function loadUserPosts() {

    try {

        const response = await axios.get(

            "https://jsonplaceholder.typicode.com/posts",

            {

                params: {

                    userId: 1

                }

            }

        );

        console.log("Posts of User 1");

        console.log(response.data);

    }

    catch (error) {

        console.log(error);

    }

}

loadUserPosts();


// ======================================
// Step 58
// Axios Request Interceptor
// ======================================

axios.interceptors.request.use(config => {

    console.log(

        `API call started : ${config.url}`

    );

    return config;

});


// Test interceptor

axios.get(

    "https://jsonplaceholder.typicode.com/users"

);


// ======================================
// Step 59
// Fetch vs Axios
// ======================================

/*

FETCH

1. Built into modern browsers.

2. Need response.json()
   to convert JSON.

3. Does NOT throw for
   HTTP errors (404/500).
   We must check response.ok.


AXIOS

1. External library.

2. Automatically converts
   JSON.

3. Automatically throws
   errors for non-2xx responses.

4. Supports interceptors.

5. Supports timeout,
   request cancellation,
   automatic request transforms.

*/