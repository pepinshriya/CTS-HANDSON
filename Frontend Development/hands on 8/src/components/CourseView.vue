<template>
  <div class="courses-view">
    <h2>Courses</h2>

    <input
      type="text"
      placeholder="Search courses..."
      v-model="searchTerm"
    />

    <div
      v-for="course in filteredCourses"
      :key="course.id"
      class="course-item"
    >
      <CourseCard
        :name="course.name"
        :code="course.code"
        :credits="course.credits"
        :grade="course.grade"
      />

      <button @click="handleEnroll(course)">
        Enroll
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import CourseCard from "../components/CourseCard.vue";
import { useEnrollmentStore } from "../stores/enrollments";

const store = useEnrollmentStore();

const courses = ref([]);
const searchTerm = ref("");

const filteredCourses = computed(() => {
  return courses.value.filter((course) =>
    course.name
      .toLowerCase()
      .includes(searchTerm.value.toLowerCase())
  );
});

function handleEnroll(course) {
  store.enroll(course);
}

onMounted(() => {
  courses.value = [
    {
      id: 1,
      name: "Data Structures",
      code: "CS101",
      credits: 4,
      grade: "A",
    },
    {
      id: 2,
      name: "Database Systems",
      code: "CS102",
      credits: 4,
      grade: "A",
    },
    {
      id: 3,
      name: "Operating Systems",
      code: "CS103",
      credits: 3,
      grade: "B+",
    },
    {
      id: 4,
      name: "Computer Networks",
      code: "CS104",
      credits: 3,
      grade: "A",
    },
    {
      id: 5,
      name: "Software Engineering",
      code: "CS105",
      credits: 4,
      grade: "A+",
    },
  ];
});
</script>

<style scoped>
.courses-view {
  padding: 20px;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
}

.course-item {
  margin-bottom: 20px;
}

button {
  margin-top: 10px;
  padding: 8px 16px;
  cursor: pointer;
}
</style>

