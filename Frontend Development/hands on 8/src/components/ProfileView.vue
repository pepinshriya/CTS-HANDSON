<template>
  <div class="profile-view">
    <h2>My Enrolled Courses</h2>

    <div v-if="store.enrolledCourses.length > 0">
      <div
        v-for="course in store.enrolledCourses"
        :key="course.id"
        class="course-card"
      >
        <h3>{{ course.name }}</h3>

        <p>
          <strong>Code:</strong>
          {{ course.code }}
        </p>

        <p>
          <strong>Credits:</strong>
          {{ course.credits }}
        </p>

        <p>
          <strong>Grade:</strong>
          {{ course.grade }}
        </p>
      </div>

      <h3>
        Total Credits: {{ store.totalCredits }}
      </h3>
    </div>

    <p v-else>
      No enrolled courses.
    </p>
  </div>
</template>

<script setup>
import { useEnrollmentStore } from "../stores/enrollment";

const store = useEnrollmentStore();
</script>

<style scoped>
.profile-view {
  padding: 20px;
}

.course-card {
  border: 1px solid #ddd;
  padding: 16px;
  margin-bottom: 15px;
  border-radius: 8px;
}
</style>