<template>
  <header class="header">
    <h1>Student Portal</h1>

    <nav>
      <RouterLink to="/">
        Home
      </RouterLink>
      <RouterLink to="/courses">
        Courses
      </RouterLink>
      <RouterLink to="/profile">
        Profile
      </RouterLink>
    </nav>

    <div class="enrollment-count">
      Enrolled Courses:
      {{ store.enrolledCourses.length }}
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { useEnrollmentStore } from "../stores/enrollments";

const store = useEnrollmentStore();
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #42b883;
  color: white;
  padding: 15px 20px;
}

nav {
  display: flex;
  gap: 20px;
}

nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

nav a.router-link-active {
  text-decoration: underline;
}

.enrollment-count {
  font-weight: bold;
}
</style>