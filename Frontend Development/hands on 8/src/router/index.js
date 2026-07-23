import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../components/HomeView.vue";
import CoursesView from "../components/CoursesView.vue";
import CourseDetailView from "../components/CourseDetailView.vue";
import ProfileView from "../components/ProfileView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: HomeView,
    },
    {
      path: "/courses",
      component: CoursesView,
    },
    {
      path: "/courses/:id",
      component: CourseDetailView,
    },
    {
      path: "/profile",
      component: ProfileView,
    },
  ],
});



router.beforeEach((to, from, next) => {
  console.log(`Navigating to: ${to.path}`);
  next();
});
export default router;