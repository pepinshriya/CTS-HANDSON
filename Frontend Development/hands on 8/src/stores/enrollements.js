import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useEnrollmentStore = defineStore("enrollment", () => {
  // State
  const enrolledCourses = ref([]);

  // Computed
  const totalCredits = computed(() => {
    return enrolledCourses.value.reduce(
      (total, course) => total + course.credits,
      0
    );
  });

  // Action
  function enroll(course) {
    enrolledCourses.value.push(course);
  }

  // Action
  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter(
      (course) => course.id !== courseId
    );
  }

  return {
    enrolledCourses,
    totalCredits,
    enroll,
    unenroll,
  };
});